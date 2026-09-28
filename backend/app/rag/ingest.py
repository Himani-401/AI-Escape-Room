from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

from app.core.config import PROJECT_ROOT

KNOWLEDGE_DIR = PROJECT_ROOT / "data" / "knowledge_base"


def load_knowledge_base() -> List[Dict[str, Any]]:
    items: List[Dict[str, Any]] = []
    for file in sorted(KNOWLEDGE_DIR.glob("*.json")):
        with open(file, "r", encoding="utf-8") as fh:
            payload = json.load(fh)
        if isinstance(payload, list):
            items.extend(payload)
        elif isinstance(payload, dict):
            items.extend(payload.get("items", []))
    for file in sorted(KNOWLEDGE_DIR.glob("*.md")):
        text = file.read_text(encoding="utf-8")
        items.append({"id": file.stem, "text": text, "source": str(file), "category": "lore"})
    return items


def ingest_knowledge_base(index) -> None:
    docs = load_knowledge_base()
    if docs:
        index.add_documents(docs)
