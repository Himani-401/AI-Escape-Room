from __future__ import annotations

from app.rag.index import FAISSKnowledgeIndex
from app.rag.ingest import ingest_knowledge_base


if __name__ == "__main__":
    index = FAISSKnowledgeIndex()
    ingest_knowledge_base(index)
    print(f"Indexed {len(index.metadata)} documents.")
