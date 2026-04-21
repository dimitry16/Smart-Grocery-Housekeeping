# Name: Krystal Lu (klu04)
# Citation for async integration
# Date: 04/19/2025
# Adapted from "Python FastAPI Tutorial (Part 7): Sync vs Async - Converting Your App to Asynchronous"
# Source URL: https://www.youtube.com/watch?v=2JPDt-Jp6fM&list=PL-osiE80TeTsak-c-QsVeg0YYG_0TeyXI&index=8

from contextlib import asynccontextmanager
from typing import Annotated

from app.database.sqlconnector import Base, close_db, get_db, init_db
from app.food_items import router
from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
import app.database.models


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Start up database engine
    db_engine = await init_db()

    # Create database tables
    async with db_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    # Shutdown database engine
    await close_db()


app = FastAPI(lifespan=lifespan)

app.include_router(router.router, prefix="/v1/food-items", tags=["Food Items"])


@app.get("/")
async def home(db: Annotated[AsyncSession, Depends(get_db)]):
    return {"message": "Connected to database."}
