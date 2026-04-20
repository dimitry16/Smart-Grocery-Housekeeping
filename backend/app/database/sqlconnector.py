# Name: Krystal Lu (klu04)
# Citation for "Production - Cloud SQL" starting line 34
# Date: 04/19/2025
# Adapted from "Cloud SQL Python Connector"
# Source URL: https://github.com/GoogleCloudPlatform/cloud-sql-python-connector#async-driver-usage

# Name: Krystal Lu (klu04)
# Citation for async integration
# Date: 04/19/2025
# Adapted from "Python FastAPI Tutorial (Part 7): Sync vs Async - Converting Your App to Asynchronous"
# Source URL: https://www.youtube.com/watch?v=2JPDt-Jp6fM&list=PL-osiE80TeTsak-c-QsVeg0YYG_0TeyXI&index=8

from ..config import settings
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, create_async_engine
from google.cloud.sql.connector import create_async_connector
from sqlalchemy.orm import DeclarativeBase


# Base class for models
class Base(DeclarativeBase):
    pass


connector = None
engine = None
AsyncSessionLocal = None


async def init_db():
    """Switch database engines depending on environment"""
    global engine, AsyncSessionLocal, connector

    # Local Development - (Local PSQL Database)
    if settings.ENVIRONMENT == "local":
        engine = create_async_engine(
            str(settings.SQLALCHEMY_DATABASE_URI), echo=settings.DEBUG
        )
    # Production - Cloud SQL
    else:
        connector = await create_async_connector()

        async def get_conn():
            return await connector.connect_async(
                settings.INSTANCE_CONNECTION_NAME,
                "asyncpg",
                user=settings.DB_USER,
                password=settings.DB_PASS,
                db=settings.DB_NAME,
            )

        engine = create_async_engine(
            "postgresql+asyncpg://",
            async_creator=get_conn,
            echo=settings.DEBUG,
        )

    AsyncSessionLocal = async_sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    return engine


# Shutdown the database engine
async def close_db():
    if connector:
        await connector.close_async()
    if engine:
        await engine.dispose()


# Session dependency
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
