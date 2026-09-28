import os
import sys
from pathlib import Path

import cv2
import numpy as np
import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.graph.workflow import build_workflow
from app.puzzles.generator import ensure_solvable, generate_puzzle_graph
from app.rag.index import FAISSKnowledgeIndex
from app.main import app
from app.vision.preprocess import resize_and_normalize
from app.vision.symbols import segment_symbols


def test_puzzle_generator_solvability():
    graph = generate_puzzle_graph(seed=123, count=5)
    assert len(graph) == 5
    assert ensure_solvable(graph) is True
    assert graph[0]["depends_on"] == []


def test_opencv_detection():
    image = np.zeros((200, 200, 3), dtype=np.uint8)
    cv2.rectangle(image, (20, 20), (120, 120), (255, 255, 255), -1)
    findings = segment_symbols(image)
    assert len(findings) >= 1
    processed = resize_and_normalize(image)
    assert processed.shape == (224, 224)


def test_faiss_retrieval_relevance():
    index = FAISSKnowledgeIndex(dimension=384, index_path=Path(__file__).resolve().parents[1] / "data" / "test_faiss.index", meta_path=Path(__file__).resolve().parents[1] / "data" / "test_faiss.json")
    for path in [index.index_path, index.meta_path]:
        if path.exists():
            path.unlink()
    docs = [
        {"id": "fire-1", "text": "The fire symbol stands for warmth and courage.", "category": "symbol"},
        {"id": "moon-1", "text": "The moon is a quiet watcher of the night sky.", "category": "symbol"},
    ]
    index.add_documents(docs)
    results = index.search("flame in the dark", top_k=1)
    assert results and results[0]["id"] == "fire-1"


def test_langgraph_transitions():
    workflow = build_workflow()
    graph = workflow.compile()
    output = graph.invoke({"session_id": "s1", "current_answer": "fire", "is_correct": True})
    assert output["is_correct"] is True
    assert output["narrative"]


def test_hint_ladder_logic():
    from app.logic.hints import build_hint_ladder

    ladder = build_hint_ladder(0, 0)
    assert len(ladder) == 3
    assert "nudge" in ladder[0].lower() or "hint" in ladder[0].lower()


def test_semantic_matching():
    from app.rag.embeddings import embed_text
    from app.rag.matching import semantic_match

    score = semantic_match("a burning flame", "fire")
    assert score >= 0.6
    assert semantic_match("sun", "moon") < 0.8


def test_api_session_offline_llm():
    client = TestClient(app)
    response = client.post("/api/sessions")
    assert response.status_code == 200
    payload = response.json()
    assert payload["session_id"]
    assert payload["id"] == payload["session_id"]
    assert payload["first_unlocked_puzzle"]
