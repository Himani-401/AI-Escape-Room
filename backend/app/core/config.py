import os
from functools import lru_cache
from pathlib import Path

from pydantic import ConfigDict
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent.parent
PROJECT_ROOT = BASE_DIR.parent
DB_PATH = PROJECT_ROOT / "backend" / "data" / "escape_room.db"
DB_PATH.parent.mkdir(parents=True, exist_ok=True)


class Settings(BaseSettings):
    model_config = ConfigDict(env_file=PROJECT_ROOT / ".env", env_file_encoding="utf-8")

    app_name: str = "AI Escape Room"
    environment: str = "development"
    app_port: int = 8000
    debug: bool = False
    database_url: str = f"sqlite:///{DB_PATH.as_posix()}"
    openai_api_key: str = ""
    anthropic_api_key: str = ""
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    semantic_threshold: float = 0.72
    log_level: str = "INFO"


@lru_cache

def get_settings() -> Settings:
    return Settings()
