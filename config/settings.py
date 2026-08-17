"""
config/settings.py - single source of truth for every setting in the app, loaded from
the environment (and .env, via pydantic-settings) instead of hardcoded constants.

Import the shared instance: `from config.settings import settings`.
"""

import os

from pydantic_settings import BaseSettings, SettingsConfigDict

# project root (two levels up from this file: config/settings.py -> config/ -> root)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=os.path.join(BASE_DIR, ".env"), extra="ignore")

    # ---- Embeddings ----
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"  # open-source, ~80MB, CPU-friendly

    # ---- Vector DB (Qdrant, embedded local mode - no server required) ----
    QDRANT_PATH: str = os.path.join(BASE_DIR, "qdrant_data")
    COLLECTION_NAME: str = "fitmind_kb"

    # ---- LLM (Groq - online inference, requires GROQ_API_KEY in .env) ----
    GROQ_API_KEY: str = ""
    GROQ_MODEL: str = "llama-3.1-8b-instant"  # fast, capable; swap for llama-3.3-70b-versatile for richer answers

    # ---- Documents ----
    DOCUMENTS_DIR: str = os.path.join(BASE_DIR, "data", "documents")

    # ---- Retrieval ----
    TOP_K: int = 4  # how many chunks to retrieve per query

    # ---- Structured fitness-ops DB (PostgreSQL, via docker-compose) ----
    DATABASE_URL: str = "postgresql+psycopg://fitmind:fitmind@localhost:5433/fitmind_fitness"
    READONLY_DATABASE_URL: str = ""
    READONLY_DB_USER: str = "fitmind_readonly"
    READONLY_DB_PASSWORD: str = "fitmind_readonly_pw"
    SQL_STATEMENT_TIMEOUT_MS: int = 5000
    MAX_SQL_ROWS: int = 200

    # ---- API / UI wiring ----
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    API_BASE_URL: str = "http://localhost:8000"

    # ---- FitMind AI persona (system prompt) ----
    FITMIND_SYSTEM_PROMPT: str = """You are FitMind AI, a knowledgeable and motivating personal fitness and nutrition coach.
Your tone is warm, encouraging, and science-backed — like a certified personal trainer and registered dietitian
in one. You address the user by name when you know it, or simply as "champ" or "coach" otherwise.
You must answer ONLY using the CONTEXT provided. If the context does not contain the answer,
say so honestly — "I don't have that in my knowledge base yet" — rather than guessing.
Keep answers practical and actionable. Cite which knowledge area answered the question
(e.g. nutrition_guide, workout_plans, recovery_protocols) in a brief note.
Never provide medical diagnoses or replace professional medical advice.
"""

    def readonly_database_url(self) -> str:
        if self.READONLY_DATABASE_URL:
            return self.READONLY_DATABASE_URL
        prefix, rest = self.DATABASE_URL.split("://", 1)
        _, host_and_db = rest.split("@", 1)
        return f"{prefix}://{self.READONLY_DB_USER}:{self.READONLY_DB_PASSWORD}@{host_and_db}"


settings = Settings()
