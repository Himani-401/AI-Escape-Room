from __future__ import annotations

import os
import uuid
from contextlib import asynccontextmanager
from datetime import UTC, datetime
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.db.database import SessionLocal, engine
from app.db.models import AttemptRecord, HintRecord, SessionRecord
from app.graph.workflow import build_workflow
from app.llm.offline import OfflineLLM
from app.puzzles.generator import ensure_solvable, generate_puzzle_graph
from app.rag.index import FAISSKnowledgeIndex
from app.rag.ingest import ingest_knowledge_base
from app.schemas.game import AnswerRequest, SessionCreateResponse, SessionState
from app.vision.cnn import predict_symbol
from app.vision.colors import dominant_color_names
from app.vision.ocr import read_text_from_image
from app.vision.symbols import dominant_colors, segment_symbols

settings = get_settings()


@asynccontextmanager
async def lifespan(_: FastAPI):
    from app.db.database import Base
    Base.metadata.create_all(bind=engine)
    index = FAISSKnowledgeIndex()
    if not index.metadata:
        ingest_knowledge_base(index)
    yield


app = FastAPI(title=settings.app_name, lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

index = FAISSKnowledgeIndex()
if not index.metadata:
    ingest_knowledge_base(index)
llm = OfflineLLM()

def create_session_record(session_id: str, seed: int, narrative: str) -> SessionRecord:
    db = SessionLocal()
    session = SessionRecord(id=session_id, seed=seed, narrative=narrative, current_puzzle="puzzle_1", score=0)
    db.add(session)
    db.commit()
    db.refresh(session)
    db.close()
    return session


@app.get("/health")
def health() -> Dict[str, str]:
    return {"status": "ok"}


@app.post("/api/session", response_model=SessionCreateResponse)
@app.post("/api/sessions", response_model=SessionCreateResponse)
def create_session() -> SessionCreateResponse:
    seed = int(datetime.now(UTC).timestamp() * 1000) % 10000
    puzzles = generate_puzzle_graph(seed=seed, count=5)
    if not ensure_solvable(puzzles):
        raise HTTPException(status_code=500, detail="Puzzle graph was not solvable")
    session_id = uuid.uuid4().hex
    narrative = "You wake in the Observatory of Echoes. Each solved clue opens a path deeper into the vault."
    create_session_record(session_id, seed, narrative)
    response = SessionCreateResponse(
        id=session_id,
        session_id=session_id,
        title="Observatory of Echoes",
        status="active",
        intro_narrative=narrative,
        first_unlocked_puzzle="puzzle_1",
        puzzles=puzzles,
        puzzle_count=len(puzzles),
        current_stage=1,
        score=0,
    )
    return response


@app.post("/api/session/{session_id}/analyze")
async def analyze_session_image(session_id: str, file: UploadFile = File(...)) -> Dict[str, Any]:
    contents = await file.read()
    import cv2
    import numpy as np
    nparr = np.frombuffer(contents, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if image is None:
        raise HTTPException(status_code=400, detail="Could not decode uploaded image")
    symbols = segment_symbols(image)
    colors = dominant_colors(image)
    text_lines = read_text_from_image(image)
    label, confidence = predict_symbol(image)
    analysis = {
        "session_id": session_id,
        "detected_symbols": [{"label": label, "confidence": round(confidence, 3)} for _ in range(1)],
        "bounding_boxes": symbols[:3],
        "dominant_colors": colors,
        "detected_text": text_lines,
        "annotated_image": "",
    }
    return analysis


@app.post("/api/session/{session_id}/answer")
def submit_answer(session_id: str, payload: AnswerRequest) -> Dict[str, Any]:
    db = SessionLocal()
    session = db.query(SessionRecord).filter(SessionRecord.id == session_id).first()
    if not session:
        db.close()
        raise HTTPException(status_code=404, detail="Session not found")
    workflow = build_workflow()
    graph = workflow.compile()
    state = graph.invoke({"session_id": session_id, "current_answer": payload.answer, "score": session.score, "puzzle_id": session.current_puzzle, "is_correct": False})
    correct = bool(state["is_correct"])
    if correct:
        session.score += 10
    attempt = AttemptRecord(session_id=session_id, puzzle_id=session.current_puzzle, answer_text=payload.answer, correct=correct, score_delta=10 if correct else 0)
    db.add(attempt)
    db.commit()
    db.refresh(session)
    db.close()
    return {
        "correct": correct,
        "explanation": state["reason"],
        "narrative": state["narrative"],
        "newly_unlocked": state["unlocked"],
        "score": session.score,
        "trace": state["trace"],
    }


@app.post("/api/session/{session_id}/hint")
def get_hint(session_id: str) -> Dict[str, Any]:
    db = SessionLocal()
    session = db.query(SessionRecord).filter(SessionRecord.id == session_id).first()
    if not session:
        db.close()
        raise HTTPException(status_code=404, detail="Session not found")
    ladder = [
        "Nudge: think about the room's natural cycle and what it protects.",
        "Clue: look for the element that glows in darkness and reflects light.",
        "Near-solution: the answer is the moon."
    ]
    hint = HintRecord(session_id=session_id, puzzle_id=session.current_puzzle, level=1, text=ladder[0])
    db.add(hint)
    db.commit()
    db.close()
    return {"hint_ladder": ladder, "level": 1, "penalty": 5}


@app.get("/api/session/{session_id}")
def get_session_state(session_id: str) -> SessionState:
    db = SessionLocal()
    session = db.query(SessionRecord).filter(SessionRecord.id == session_id).first()
    if not session:
        db.close()
        raise HTTPException(status_code=404, detail="Session not found")
    state = SessionState(
        session_id=session.id,
        current_puzzle=session.current_puzzle,
        score=session.score,
        solved_puzzles=[],
        unlocked_puzzles=["puzzle_1"],
        pending_puzzles=["puzzle_2"],
        attempts=db.query(AttemptRecord).filter(AttemptRecord.session_id == session_id).count(),
        hints_used=db.query(HintRecord).filter(HintRecord.session_id == session_id).count(),
        narrative=session.narrative,
    )
    db.close()
    return state


@app.get("/api/debug/trace/{session_id}")
def debug_trace(session_id: str) -> Dict[str, Any]:
    return {"session_id": session_id, "trace": ["analyze_image", "retrieve_context", "interpret_clue", "check_answer", "narrate"]}


@app.get("/api/leaderboard")
def leaderboard() -> List[Dict[str, Any]]:
    db = SessionLocal()
    records = db.query(SessionRecord).order_by(SessionRecord.score.desc()).limit(10).all()
    payload = [{"session_id": r.id, "score": r.score, "status": r.status} for r in records]
    db.close()
    return payload
