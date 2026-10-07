from pathlib import Path
from pydantic_settings import BaseSettings

BACKEND_DIR = Path(__file__).resolve().parents[2]

# Oznaczenie wydania aplikacji zapisywane przy analizach i uwagach.
APP_VERSION = "0.01-dev"


class Settings(BaseSettings):
    database_url: str = "postgresql+asyncpg://obsil:obsil@localhost:5432/obsil"
    secret_key: str = "dev-secret-change-in-production"
    llm_provider: str = "anthropic"
    llm_api_key: str = ""
    llm_model_name: str = "claude-sonnet-4-5"
    # Lista dozwolonych modeli rozdzielona przecinkami; pusta = bez ograniczenia.
    llm_allowed_models: str = ""
    llm_endpoint_url: str = ""
    codex_executable: str = ""
    codex_reasoning_effort: str = "medium"
    llm_timeout_seconds: int = 300
    knowledge_mode: str = "off"
    knowledge_project_path: str = str(BACKEND_DIR.parent)
    local_test_mode: bool = False
    # Logowanie: "local" (komputer AJ, bez logowania) albo "cloudflare" (Cloudflare Access).
    auth_mode: str = "local"
    cf_access_team_domain: str = ""  # np. obsil.cloudflareaccess.com
    cf_access_aud: str = ""  # „Application Audience (AUD) Tag” aplikacji w Cloudflare
    operator_email_list: str = ""  # adresy operatorów rozdzielone przecinkami
    allowed_origins: list[str] = ["http://localhost:3000"]
    debug: bool = False

    @property
    def allowed_models(self) -> list[str]:
        return [m.strip() for m in self.llm_allowed_models.split(",") if m.strip()]

    @property
    def operator_emails(self) -> set[str]:
        return {e.strip().lower() for e in self.operator_email_list.split(",") if e.strip()}

    class Config:
        env_file = (str(BACKEND_DIR / ".env"), str(BACKEND_DIR / ".env.local"))
        extra = "ignore"


settings = Settings()
