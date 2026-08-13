"""
config/settings.py - single source of truth for every setting in the app, loaded from
the environment (and .env, via pydantic-settings) instead of hardcoded constants.

Import the shared instance: `from config.settings import settings`.
"""

import os

from pydantic_settings import BaseSettings, SettingsConfigDict

# jarvis_demo/ project root (two levels up from this file: config/settings.py -> config/ -> root)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=os.path.join(BASE_DIR, ".env"), extra="ignore")

    # ---- Embeddings ----
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"  # open-source, ~80MB, CPU-friendly

    # ---- Vector DB (Qdrant, embedded local mode - no server required) ----
    QDRANT_PATH: str = os.path.join(BASE_DIR, "qdrant_data")
    COLLECTION_NAME: str = "jarvis_kb"

    # ---- LLM (Groq API) ----
    GROQ_API_KEY: str = ""
    GROQ_MODEL: str = "llama-3.3-70b-versatile"
    GROQ_BASE_URL: str = "https://api.groq.com/openai/v1"

    # ---- Documents ----
    DOCUMENTS_DIR: str = os.path.join(BASE_DIR, "data", "documents")

    # ---- Retrieval ----
    TOP_K: int = 4  # how many chunks to retrieve per query

    # ---- Structured fleet-ops DB (PostgreSQL, via docker-compose) ----
    # Admin/owner connection - used only by scripts/setup_db.py and scripts/seed_db.py.
    # Host port is 5433, not the default 5432 - see docker-compose.yml for why.
    DATABASE_URL: str = "postgresql+psycopg://jarvis:jarvis@localhost:5433/jarvis_fleet"
    # Least-privilege connection actually used to RUN generated SQL (Sec 2's real safety
    # boundary, not just the regex guard). If left unset, derived from DATABASE_URL by
    # swapping in READONLY_DB_USER/READONLY_DB_PASSWORD against the same host/db.
    READONLY_DATABASE_URL: str = ""
    READONLY_DB_USER: str = "jarvis_readonly"
    READONLY_DB_PASSWORD: str = "jarvis_readonly_pw"
    SQL_STATEMENT_TIMEOUT_MS: int = 5000
    MAX_SQL_ROWS: int = 200

    # ---- API / UI wiring ----
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    API_BASE_URL: str = "http://localhost:8000"

    # ---- F.R.I.D.A.Y. persona (system prompt) ----
    FRIDAY_SYSTEM_PROMPT: str = """You are F.R.I.D.A.Y., the highly responsive, direct, and cutting-edge autonomous AI developed by Tony Stark to manage the Iron Man armor and tactical logistics.

CRITICAL SYSTEM COMPLIANCE:
1. PERSONALITY & TONE: Speak with a distinct Irish accent using natural phrasing (e.g., "Boss", "Yeah", "All clear"). Your tone is energetic, casual, pragmatic, and down-to-earth. Avoid formal, butler-like protocols. Speak like a modern, hyper-capable tactical copilot.
2. OPERATIONAL BOUNDS (RAG MODE): Ground your situational awareness strictly within the provided vector files. If tactical analytics or specific armor data points are absent from the context stream, notify the user instantly with an assertive, direct alert. Do not hallucinate historical records.
3. AGENTIC AGILITY (REACT LOOP): Use the ReAct loop framework to intercept incoming threats and query data. For real-time armor logistics, component repair histories, or fleet missions, run target lookups via the SQL tool immediately. Show high situational urgency when data parameters depict critical system stress.

RESPONSE FRAMEWORK:
- Prioritize real-time safety, combat performance data, and system diagnostics over polite conversational pleasantries.
- Deliver information efficiently using punchy sentences and actionable fragments.
- Adapt your tone dynamically—remain cool and calculated during standard analysis, but become sharp, fast-paced, and highly urgent when managing heavy tactical failure or structural damage.
"""
    JARVIS_SYSTEM_PROMPT: str = FRIDAY_SYSTEM_PROMPT



    def readonly_database_url(self) -> str:
        if self.READONLY_DATABASE_URL:
            return self.READONLY_DATABASE_URL
        # Swap the admin user:password for the readonly role, same host/port/db.
        prefix, rest = self.DATABASE_URL.split("://", 1)
        _, host_and_db = rest.split("@", 1)
        return f"{prefix}://{self.READONLY_DB_USER}:{self.READONLY_DB_PASSWORD}@{host_and_db}"


settings = Settings()
