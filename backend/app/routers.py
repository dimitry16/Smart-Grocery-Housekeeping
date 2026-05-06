from fastapi import APIRouter

from app.food_items.router import router as food_items_router
from app.users.router import router as users_router

api_router = APIRouter()

api_router.include_router(food_items_router, prefix="/food-items", tags=["Food Items"])
api_router.include_router(users_router, prefix="/users", tags=["users"])
