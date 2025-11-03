from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    APP_ENV: str = "dev"
    DATABASE_URL: str | None = None
    JWT_SECRET: str = "change_me"
    JWT_REFRESH_SECRET: str = "change_me_too"

    NOTION_TOKEN: str | None = None
    NOTION_TASKS_DB_ID: str | None = None
    NOTION_ATT_DB_ID: str | None = None

    TIMEZONE: str = "Asia/Kolkata"
    APP_BASE_URL: str = "http://127.0.0.1:8000"
    ALLOWED_ORIGINS: str = "http://localhost:5173"

    @property
    def effective_db_url(self) -> str:
        return self.DATABASE_URL or "sqlite:///./dev.db"

@lru_cache
def get_settings() -> Settings:
    return Settings()
