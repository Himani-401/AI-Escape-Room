from __future__ import annotations

from typing import List


def build_hint_ladder(attempts: int, elapsed_minutes: int) -> List[str]:
    if attempts >= 3 or elapsed_minutes >= 10:
        return [
            "Nudge: think of the room's natural cycle and what it protects.",
            "Clue: the answer is an element of the sky, not a tool.",
            "Near-solution: the symbol is the moon."
        ]
    return [
        "Nudge: start with the broadest category before choosing a symbol.",
        "Clue: it glows softly in the dark and reflects light.",
        "Near-solution: the answer is the moon."
    ]
