from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class DetectionResult(BaseModel):
    label: str
    confidence: float
    bbox: List[int] = Field(default_factory=list)
    dominant_colors: List[str] = Field(default_factory=list)
    text: str = ""
    annotation_image: str = ""
    object_summary: Optional[str] = None


class Puzzle(BaseModel):
    id: str
    title: str
    type: str
    prompt: str
    answer: str
    hint_templates: List[str] = Field(default_factory=list)
    depends_on: List[str] = Field(default_factory=list)
    unlocks: List[str] = Field(default_factory=list)
    seed: int = 0


class SessionCreateResponse(BaseModel):
    id: str
    session_id: str
    title: str = "Observatory of Echoes"
    status: str = "active"
    intro_narrative: str
    first_unlocked_puzzle: Optional[str]
    puzzles: List[Puzzle]
    puzzle_count: int = 0
    current_stage: int = 1
    score: int = 0


class AnswerRequest(BaseModel):
    answer: str
    image_base64: Optional[str] = None


class HintRequest(BaseModel):
    puzzle_id: Optional[str] = None


class SessionState(BaseModel):
    session_id: str
    current_puzzle: str
    score: int
    solved_puzzles: List[str]
    unlocked_puzzles: List[str]
    pending_puzzles: List[str]
    attempts: int
    hints_used: int
    narrative: str
