from __future__ import annotations

from sentence_transformers import SentenceTransformer

MODEL = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")


def embed_texts(texts: list[str]) -> list[list[float]]:
    return MODEL.encode(texts, convert_to_numpy=True, normalize_embeddings=False).tolist()


def embed_text(text: str) -> list[float]:
    return MODEL.encode(text, convert_to_numpy=True, normalize_embeddings=False).tolist()
