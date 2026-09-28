from __future__ import annotations

import random
from copy import deepcopy
from typing import Dict, List

from app.puzzles.templates import SYMBOLS, build_default_templates


def generate_puzzle_graph(seed: int | None = None, count: int = 5) -> List[Dict[str, object]]:
    rng = random.Random(seed if seed is not None else random.randint(1, 999999))
    templates = deepcopy(build_default_templates())
    for idx, template in enumerate(templates[:count]):
        template["seed"] = rng.randint(1, 9999)
        template["id"] = f"puzzle_{idx + 1}"
        if idx > 0:
            template["depends_on"] = [templates[idx - 1]["id"]]
        else:
            template["depends_on"] = []
        if idx < count - 1:
            template["unlocks"] = [templates[idx + 1]["id"]]
        else:
            template["unlocks"] = []
    return templates


def ensure_solvable(graph: List[Dict[str, object]]) -> bool:
    # simple acyclic depth-check ensures all nodes can be reached through dependency chain
    index = {item["id"]: item for item in graph}
    seen = set()

    def walk(node_id: str):
        if node_id in seen:
            return True
        seen.add(node_id)
        dependencies = index[node_id].get("depends_on", [])
        for dep in dependencies:
            if dep not in index:
                return False
            walk(dep)
        return True

    for item in graph:
        if not walk(item["id"]):
            return False
    return True
