from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict


class LLMProvider(ABC):
    @abstractmethod
    def generate(self, prompt: str, **kwargs: Any) -> str:
        raise NotImplementedError

    @abstractmethod
    def structured(self, prompt: str, schema: type, **kwargs: Any) -> Dict[str, Any]:
        raise NotImplementedError
