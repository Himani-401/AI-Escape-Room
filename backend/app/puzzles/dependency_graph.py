from __future__ import annotations

from typing import Dict, List, Set

from llama_index.core import PropertyGraphIndex, SimpleDirectoryReader
from llama_index.core.indices.property_graph import PropertyGraphIndex


class PuzzleDependencyGraph:
    def __init__(self) -> None:
        self.graph = {}  # type: ignore[var-annotated]

    def build(self, puzzles: List[Dict[str, object]]) -> Dict[str, List[str]]:
        adjacency: Dict[str, List[str]] = {p["id"]: list(p.get("unlocks", [])) for p in puzzles}
        self.graph = adjacency
        return adjacency

    def unlocked_from(self, solved: Set[str]) -> List[str]:
        unlocked: List[str] = []
        for node, neighbors in self.graph.items():
            if node in solved:
                continue
            deps = [n for n in self.graph if node in self.graph[n]]
            if all(dep in solved for dep in deps):
                unlocked.append(node)
        return unlocked
