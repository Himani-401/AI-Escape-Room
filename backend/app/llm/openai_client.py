import os
from typing import Any, Dict

from openai import OpenAI

from app.llm.base import LLMProvider


class OpenAIClient(LLMProvider):
    def __init__(self) -> None:
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", ""))

    def generate(self, prompt: str, **kwargs: Any) -> str:
        if not os.getenv("OPENAI_API_KEY"):
            raise ValueError("OPENAI_API_KEY is not set")
        response = self.client.responses.create(
            model=kwargs.get("model", "gpt-4o-mini"),
            input=prompt,
        )
        return response.output_text

    def structured(self, prompt: str, schema: type, **kwargs: Any) -> Dict[str, Any]:
        if not os.getenv("OPENAI_API_KEY"):
            raise ValueError("OPENAI_API_KEY is not set")
        data = self.generate(prompt, **kwargs)
        try:
            return schema.model_validate_json(data).model_dump()
        except Exception:
            return {"answer": data, "confidence": 0.8, "reason": "OpenAI structured output fallback."}
