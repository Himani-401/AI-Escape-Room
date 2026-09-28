from __future__ import annotations

import numpy as np

from app.rag.embeddings import embed_text


def cosine_similarity(a: list[float], b: list[float]) -> float:
    a_arr = np.asarray(a, dtype=np.float32)
    b_arr = np.asarray(b, dtype=np.float32)
    denom = np.linalg.norm(a_arr) * np.linalg.norm(b_arr)
    if denom == 0:
        return 0.0
    return float(np.dot(a_arr, b_arr) / denom)


def semantic_match(query: str, target: str) -> float:
    q = embed_text(query)
    t = embed_text(target)
    return cosine_similarity(q, t)
