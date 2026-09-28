from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

import faiss
import numpy as np

from app.core.config import PROJECT_ROOT
from app.rag.embeddings import embed_texts

INDEX_PATH = PROJECT_ROOT / "backend" / "data" / "faiss_index.index"
META_PATH = PROJECT_ROOT / "backend" / "data" / "faiss_metadata.json"


class FAISSKnowledgeIndex:
    def __init__(self, dimension: int = 384, index_path: Path | None = None, meta_path: Path | None = None):
        self.dimension = dimension
        self.index_path = index_path or INDEX_PATH
        self.meta_path = meta_path or META_PATH
        self.index = self._load_or_create_index()
        self.metadata: List[Dict[str, Any]] = self._load_metadata()

    def _load_or_create_index(self):
        path = self.index_path
        path.parent.mkdir(parents=True, exist_ok=True)
        if path.exists():
            return faiss.read_index(str(path))
        return faiss.IndexFlatL2(self.dimension)

    def _load_metadata(self):
        if self.meta_path.exists():
            with open(self.meta_path, "r", encoding="utf-8") as fh:
                return json.load(fh)
        return []

    def add_documents(self, docs: List[Dict[str, Any]]) -> None:
        if not docs:
            return
        embeddings = np.asarray(embed_texts([doc["text"] for doc in docs]), dtype="float32")
        self.index.add(embeddings)
        self.metadata.extend(docs)
        self._persist()

    def search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        query_vector = np.asarray(embed_texts([query]), dtype="float32")
        distances, indices = self.index.search(query_vector, min(top_k, len(self.metadata)))
        results = []
        for idx, dist in zip(indices[0], distances[0]):
            if idx < 0 or idx >= len(self.metadata):
                continue
            item = dict(self.metadata[int(idx)])
            item["score"] = float(dist)
            results.append(item)
        return results

    def _persist(self) -> None:
        faiss.write_index(self.index, str(self.index_path))
        with open(self.meta_path, "w", encoding="utf-8") as fh:
            json.dump(self.metadata, fh, ensure_ascii=False, indent=2)
