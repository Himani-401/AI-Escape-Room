import json
from typing import Any, Dict

from app.llm.base import LLMProvider


class OfflineLLM(LLMProvider):
    def generate(self, prompt: str, **kwargs: Any) -> str:
        lowered = prompt.lower()
        if "riddle" in lowered or "answer" in lowered:
            if "fire" in lowered:
                return "fire"
            if "water" in lowered:
                return "water"
            if "moon" in lowered:
                return "moon"
            if "sun" in lowered:
                return "sun"
            if "key" in lowered:
                return "key"
            if "leaf" in lowered:
                return "leaf"
            if "star" in lowered:
                return "star"
        if "symbol" in lowered and "sequence" in lowered:
            return "fire -> water -> moon"
        return "fire"

    def structured(self, prompt: str, schema: type, **kwargs: Any) -> Dict[str, Any]:
        content = self.generate(prompt, **kwargs)
        result = {"answer": content, "confidence": 0.91, "reason": "Offline fallback reasoning using retrieval context and template logic."}
        if hasattr(schema, "model_fields"):
            try:
                return schema.model_validate(result).model_dump()
            except Exception:
                pass
        return result
