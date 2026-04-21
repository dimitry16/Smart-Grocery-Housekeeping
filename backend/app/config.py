# Name: Krystal Lu (klu04)
# Citation for config.py
# Adapted from "full-stack-fastapi-template"
# Author: fastapi
# Date: 04/19/2025
# Source URL: https://github.com/fastapi/full-stack-fastapi-template/blob/master/backend/app/core/config.py

from pydantic import PostgresDsn, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Literal

class Settings(BaseSettings):
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )
    ENVIRONMENT: Literal["local", "production"] = "local"
    DEBUG: bool
    
    # Local PostgreSQL
    POSTGRES_SERVER: str = ""
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = ""
    POSTGRES_USER: str = ""
    POSTGRES_PASSWORD: str = ""
    
    # Production (Cloud SQL)
    INSTANCE_CONNECTION_NAME: str = ""
    DB_USER: str = ""
    DB_PASS: str = ""
    DB_NAME: str = ""

    @computed_field
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> PostgresDsn | None:
        if self.ENVIRONMENT != "local": 
            return None 
        
        # Validate that local vars are actually present before building
        if not all([self.POSTGRES_SERVER, self.POSTGRES_DB, self.POSTGRES_USER]):
            raise ValueError("Local Postgres settings are required when ENVIRONMENT is 'local'")
        
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_SERVER,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB.lstrip("/"),
        )

settings = Settings()
