# Name: Yasser Hernandez (hernayas)
# Citation for logic of getting food item inventory by users.
# Date: 05/15/2026
# Adapted from food_items/router.py by Krystal Lu

from datetime import date, timedelta

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from typing import Annotated
from uuid import UUID

from app.database.sqlconnector import get_db
from app.utils import get_user_util

from app.database.models import FoodItem as FoodItemModel

from app.external_api_services.recipe_api import get_recipes_from_ingredients
from app.recipes.schema import RecipeListResponse

router = APIRouter()


def calculate_expiration(user_items):
    """calculates expiration status of food items. Retuns a list of food items that are expiring within 3 days."""
    today = date.today()
    food_items = []
    for item in user_items:
        if item.expiration_date and item.expiration_date <= today + timedelta(days=3):
            food_items.append(item.name)

    # for tesing recipe suggestions
    # food_items = ["milk", "strawberry", "yogurt", "vanilla", "whipped cream"]
    print("Food items expiring soon:", food_items)
    return food_items


@router.get("/get-recipe-suggestions", response_model=RecipeListResponse)
async def get_recipe_suggestions(
    user_id: UUID, db: Annotated[AsyncSession, Depends(get_db)]
):
    """Get food items for the user's current inventory that are expiring within 3 days for a user."""

    # Check if user exists
    await get_user_util(user_id, db)

    result = await db.execute(
        select(FoodItemModel).where(FoodItemModel.user_id == user_id)
    )

    user_items = result.scalars().all()
    items_expiring_soon = calculate_expiration(user_items)
    recipes = await get_recipes_from_ingredients(items_expiring_soon)

    return {"recipes": recipes}
