# Name: Krystal Lu (klu04)
# Citation for "Production (Cloud SQL)"
# Date: 04/29/2026
# Adapted from "Cloud SQL Python Connector - Async Driver Usage (SQLAlchemy async engine)"
# Source URL: https://github.com/GoogleCloudPlatform/cloud-sql-python-connector#sqlalchemy-async-engine

# Name: Krystal Lu (klu04)
# Citation for DB Connection async integration
# Date: 04/29/2026
# Adapted from "Python FastAPI Tutorial (Part 7): Sync vs Async - Converting Your App to Asynchronous"
# Source URL: https://www.youtube.com/watch?v=2JPDt-Jp6fM&list=PL-osiE80TeTsak-c-QsVeg0YYG_0TeyXI&index=8


from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from ..config import settings


class Base(DeclarativeBase):
    pass


engine = None
AsyncSessionLocal = None


async def init_db():
    global engine, AsyncSessionLocal
    try:
        engine = create_async_engine(settings.SQLALCHEMY_DATABASE_URI)

        AsyncSessionLocal = async_sessionmaker(
            engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )

        return engine
    except Exception:
        # Close any partially created resources.
        await close_db()
        raise RuntimeError("Database failed to initialize. Check the config.")


async def close_db():
    """Shutdown database engine"""

    if engine:
        await engine.dispose()


async def get_db():
    """Session Dependency"""

    if AsyncSessionLocal is None:
        raise Exception("Database is not initialized")

    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            # Rollback session on exception to maintain data integrity.
            await session.rollback()
            raise
