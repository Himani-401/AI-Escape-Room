from __future__ import annotations

from typing import Any, Dict, List

from app.rag.index import FAISSKnowledgeIndex


class RAGRetriever:
    def __init__(self, index: FAISSKnowledgeIndex | None = None) -> None:
        self.index = index or FAISSKnowledgeIndex()

    def retrieve(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        return self.index.search(query, top_k=top_k)
