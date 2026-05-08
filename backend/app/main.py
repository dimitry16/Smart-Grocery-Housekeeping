from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession

import app.database.models
from app.database.sqlconnector import close_db, get_db, init_db
from app.food_items import router


# FastAPI Docs - Lifespan: https://fastapi.tiangolo.com/advanced/events/#lifespan-events
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handles startup and shutdown of resources at app startup and shutdown."""

    # Start up database engine
    await init_db()

    yield
    # Shutdown database engine
    await close_db()


app = FastAPI(lifespan=lifespan)

app.include_router(router.router, prefix="/v1/food-items", tags=["Food Items"])

# CORS Middleware edited by Zilin Xu
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite's default port
    allow_methods=["*"],
    allow_headers=["*"],
)


# Routers
@app.get("/")
async def root(db: Annotated[AsyncSession, Depends(get_db)]):
    return {"message": "Navigate to /food-items"}
