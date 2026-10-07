from pathlib import Path
from pydantic_settings import BaseSettings

BACKEND_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    database_url: str = "postgresql+asyncpg://obsil:obsil@localhost:5432/obsil"
    secret_key: str = "dev-secret-change-in-production"
    llm_provider: str = "anthropic"
    llm_api_key: str = ""
    llm_model_name: str = "claude-sonnet-4-5"
    llm_endpoint_url: str = ""
    codex_executable: str = ""
    codex_reasoning_effort: str = "medium"
    llm_timeout_seconds: int = 300
    knowledge_mode: str = "off"
    knowledge_project_path: str = str(BACKEND_DIR.parent.parent)
    local_test_mode: bool = False
    allowed_origins: list[str] = ["http://localhost:3000"]
    debug: bool = False

    class Config:
        env_file = (str(BACKEND_DIR / ".env"), str(BACKEND_DIR / ".env.local"))
        extra = "ignore"


settings = Settings()
