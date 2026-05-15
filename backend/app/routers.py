from fastapi import APIRouter

from app.food_items.router import router as food_items_router
from app.users.router import router as users_router
from app.external_api_services.vision_router import router as vision_router

api_router = APIRouter()

api_router.include_router(
    food_items_router,
    prefix="/users/{user_id}/food-items",
    tags=["Food Items"],
)
api_router.include_router(users_router, prefix="/users", tags=["users"])
api_router.include_router(vision_router, prefix="/vision", tags=["Vision"])
