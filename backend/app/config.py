from pathlib import Path
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(Path(__file__).parent.parent / ".env"),
        env_file_encoding="utf-8",
    )
    ENVIRONMENT: Literal["local", "production"] = "local"

    API_V1_URL: str = "/v1"

    # Local PostgreSQL DB
    DATABASE_URL: str

    # Test PostgreSQL DB
    TEST_DATABASE_URL: str

    # Production (Cloud SQL)
    INSTANCE_CONNECTION_NAME: str = ""
    DB_USER: str = ""
    DB_PASS: str = ""
    DB_NAME: str = ""

    # Frontend
    FRONTEND_URL: str = "http://localhost:5173"


settings = Settings()
