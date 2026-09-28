from __future__ import annotations

import os
from typing import Any, Dict

from anthropic import Anthropic

from app.llm.base import LLMProvider


class AnthropicClient(LLMProvider):
    def __init__(self) -> None:
        self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY", ""))

    def generate(self, prompt: str, **kwargs: Any) -> str:
        if not os.getenv("ANTHROPIC_API_KEY"):
            raise ValueError("ANTHROPIC_API_KEY is not set")
        message = self.client.messages.create(
            model=kwargs.get("model", "claude-3-haiku-20240307"),
            max_tokens=256,
            messages=[{"role": "user", "content": prompt}],
        )
        return message.content[0].text

    def structured(self, prompt: str, schema: type, **kwargs: Any) -> Dict[str, Any]:
        if not os.getenv("ANTHROPIC_API_KEY"):
            raise ValueError("ANTHROPIC_API_KEY is not set")
        text = self.generate(prompt, **kwargs)
        try:
            return schema.model_validate_json(text).model_dump()
        except Exception:
            return {"answer": text, "confidence": 0.8, "reason": "Anthropic response parsed into a minimal structured payload."}
