from pathlib import Path
from typing import Literal

from pydantic import PostgresDsn, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(Path(__file__).parent.parent / ".env"),
        env_file_encoding="utf-8",
    )
    # ENVIRONMENT variable must be 'local' or 'production' (case sensitive)
    ENVIRONMENT: Literal["local", "production"] = "local"

    API_V1_URL: str = "/v1"

    # Local PostgreSQL DB
    POSTGRES_SERVER: str = ""
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = ""
    POSTGRES_USER: str = ""
    POSTGRES_PASSWORD: str = ""
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

    @computed_field
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        if self.ENVIRONMENT != "local":
            return None

        # Validate that local vars are actually present before building
        if not all([self.POSTGRES_SERVER, self.POSTGRES_DB, self.POSTGRES_USER]):
            raise ValueError(
                "Local Postgres settings are required when ENVIRONMENT is 'local'"
            )

        return str(
            PostgresDsn.build(
                scheme="postgresql+asyncpg",
                username=self.POSTGRES_USER,
                password=self.POSTGRES_PASSWORD,
                host=self.POSTGRES_SERVER,
                port=self.POSTGRES_PORT,
                path=self.POSTGRES_DB.lstrip("/"),
            )
        )


settings = Settings()
