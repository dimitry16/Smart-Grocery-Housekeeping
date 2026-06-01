from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import app.database.models
from app.config import settings
from app.database.sqlconnector import close_db, init_db
from app.routers import api_router


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

origins = [
    "http://127.0.0.1:5173",
    "http://localhost",
    "http://localhost:5173",
    "https://localhost",
    "https://localhost:5173",
]

# CORS Middleware edited by Zilin Xu
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_URL)
