from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class GraphState(BaseModel):
    session_id: str
    puzzle_id: str = ""
    current_answer: str = ""
    context: Dict[str, Any] = Field(default_factory=dict)
    known_symbols: List[str] = Field(default_factory=list)
    detected_text: List[str] = Field(default_factory=list)
    is_correct: bool = False
    reason: str = ""
    narrative: str = ""
    hints: List[str] = Field(default_factory=list)
    unlocked: List[str] = Field(default_factory=list)
    next_puzzle: Optional[str] = None
    score: int = 0
    attempts: int = 0
    trace: List[str] = Field(default_factory=list)
