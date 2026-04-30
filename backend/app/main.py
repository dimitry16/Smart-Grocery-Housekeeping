from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import app.database.models
from app.database.sqlconnector import close_db
from app.food_items import router


# FastAPI Docs - Lifespan: https://fastapi.tiangolo.com/advanced/events/#lifespan-events
@asynccontextmanager
async def lifespan(app: FastAPI):

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
async def read_msg():
    return {"message": "Navigate to /food-items"}
