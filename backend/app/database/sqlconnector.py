# Name: Krystal Lu (klu04)
# Citation for "Production (Cloud SQL)"
# Date: 04/29/2025
# Adapted from "Cloud SQL Python Connector - Async Driver Usage (SQLAlchemy async engine)"
# Source URL: https://github.com/GoogleCloudPlatform/cloud-sql-python-connector#sqlalchemy-async-engine

# Name: Krystal Lu (klu04)
# Citation for DB Connection async integration
# Date: 04/29/2025
# Adapted from "Python FastAPI Tutorial (Part 7): Sync vs Async - Converting Your App to Asynchronous"
# Source URL: https://www.youtube.com/watch?v=2JPDt-Jp6fM&list=PL-osiE80TeTsak-c-QsVeg0YYG_0TeyXI&index=8


from google.cloud.sql.connector import create_async_connector
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from ..config import settings


class Base(DeclarativeBase):
    pass


connector = None
engine = None
AsyncSessionLocal = None


async def init_db():
    """Switch database engines depending on development environment."""
    global engine, AsyncSessionLocal, connector

    # Local Development (Local PostgreSQL Database)
    # Change ENVIRONMENT to "production" in your env file to connect to cloud sql
    if settings.ENVIRONMENT == "local":
        engine = create_async_engine(settings.DATABASE_URL)

    # Production (Cloud SQL)
    else:
        connector = await create_async_connector()

        async def get_connection():
            return await connector.connect_async(
                settings.instance_connection_name,
                "asyncpg",
                user=settings.db_user,
                password=settings.db_pass,
                db=settings.db_name,
            )

        engine = create_async_engine(
            "postgresql+asyncpg://", async_creator=get_connection
        )

    AsyncSessionLocal = async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    return engine


async def close_db():  #
    """Shutdown database engine"""
    if connector:
        await connector.close_async()
    if engine:
        await engine.dispose()


async def get_db():
    """Session Dependency"""
    async with AsyncSessionLocal() as session:
        yield session
