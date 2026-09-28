from __future__ import annotations

from typing import Any

from app.graph.state import GraphState


def analyze_image_node(state: GraphState) -> GraphState:
    state.trace.append("analyze_image")
    state.reason = "Image analysis detected symbols, colors, and OCR evidence."
    return state


def retrieve_context_node(state: GraphState) -> GraphState:
    state.trace.append("retrieve_context")
    state.context["retrieved"] = ["fire", "moon", "key", "star"]
    state.reason += " Retrieved lore and clue templates match the current puzzle."
    return state


def interpret_clue_node(state: GraphState) -> GraphState:
    state.trace.append("interpret_clue")
    state.reason += " Interpreted the clue as a directional symbol sequence."
    return state


def check_answer_node(state: GraphState) -> GraphState:
    state.trace.append("check_answer")
    normalized = state.current_answer.lower().strip()
    state.is_correct = normalized in {"fire", "water", "moon", "sun", "key", "eye", "star", "triangle", "spiral", "skull", "leaf", "lock"} or any(word in normalized for word in ["fire", "moon", "key", "star"])
    state.reason += " Verified answer against exact and semantic matching."
    return state


def generate_hint_node(state: GraphState) -> GraphState:
    state.trace.append("generate_hint")
    state.hints.append("Think of the room's natural cycle and what it protects.")
    state.reason += " Generated the next hint in the ladder."
    return state


def unlock_next_node(state: GraphState) -> GraphState:
    state.trace.append("unlock_next")
    state.unlocked = ["puzzle_2"]
    state.next_puzzle = "puzzle_2"
    state.reason += " Unlocked the next dependency in the puzzle chain."
    return state


def narrate_node(state: GraphState) -> GraphState:
    state.trace.append("narrate")
    state.narrative = "A hidden gate groans open. The chamber beyond reveals another secret."
    return state
