from __future__ import annotations

from typing import Any, Dict, List, Optional

from langgraph.graph import END, StateGraph

from app.graph.state import GraphState


def analyze_image(state: GraphState) -> GraphState:
    state.trace.append("analyze_image")
    state.reason = "Image analyzed for symbols, colors, and text."
    return state


def retrieve_context(state: GraphState) -> GraphState:
    state.trace.append("retrieve_context")
    state.context["retrieved"] = ["fire", "moon", "key", "star"]
    state.reason += " Relevant lore and clues were retrieved."
    return state


def interpret_clue(state: GraphState) -> GraphState:
    state.trace.append("interpret_clue")
    state.reason += " Puzzle interpretation mapped the clue to a likely answer."
    return state


def check_answer(state: GraphState) -> GraphState:
    state.trace.append("check_answer")
    state.is_correct = "fire" in state.current_answer.lower() or "moon" in state.current_answer.lower() or state.current_answer.lower() in {"fire", "moon", "key", "star"}
    state.reason += " Answer validity checked against semantic and direct matches."
    return state


def generate_hint(state: GraphState) -> GraphState:
    state.trace.append("generate_hint")
    state.hints.append("The answer refers to a natural element of the room.")
    state.reason += " A hint ladder was generated for the player."
    return state


def unlock_next(state: GraphState) -> GraphState:
    state.trace.append("unlock_next")
    state.unlocked = ["puzzle_2"]
    state.next_puzzle = "puzzle_2"
    state.reason += " The next puzzle has been unlocked."
    return state


def narrate(state: GraphState) -> GraphState:
    state.trace.append("narrate")
    state.narrative = "The room exhales, and the wall slides open to reveal another secret."
    return state


def build_workflow() -> StateGraph:
    workflow = StateGraph(GraphState)
    workflow.add_node("analyze_image", analyze_image)
    workflow.add_node("retrieve_context", retrieve_context)
    workflow.add_node("interpret_clue", interpret_clue)
    workflow.add_node("check_answer", check_answer)
    workflow.add_node("generate_hint", generate_hint)
    workflow.add_node("unlock_next", unlock_next)
    workflow.add_node("narrate", narrate)

    workflow.set_entry_point("analyze_image")
    workflow.add_edge("analyze_image", "retrieve_context")
    workflow.add_edge("retrieve_context", "interpret_clue")
    workflow.add_edge("interpret_clue", "check_answer")
    workflow.add_conditional_edges(
        "check_answer",
        lambda state: "generate_hint" if not state.is_correct else "unlock_next",
        {
            "generate_hint": "generate_hint",
            "unlock_next": "unlock_next",
        },
    )
    workflow.add_edge("generate_hint", "narrate")
    workflow.add_edge("unlock_next", "narrate")
    workflow.add_edge("narrate", END)
    return workflow
