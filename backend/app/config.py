"""Application settings, overridable via environment variables (prefix KI_)."""

from pathlib import Path
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict

BACKEND_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="KI_")

    database_url: str = f"sqlite:///{BACKEND_DIR / 'knowledge_islands.db'}"
    # Vite dev server (frontend) runs on port 5173 by default.
    cors_origins: List[str] = ["http://localhost:5173", "http://127.0.0.1:5173"]


settings = Settings()
