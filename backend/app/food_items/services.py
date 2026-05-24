from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import FoodItem as FoodItemModel
from app.food_items.schema import (
    FoodItemResponse,
    FoodItemsPublic,
)


async def get_food_items_by_user(user_id: UUID, db: AsyncSession) -> FoodItemsPublic:
    """Get user's food items from the database.

    Args:
        user_id (UUID): ID of the user making the request.
        db (AsyncSession): Async database session.

    Returns:
        FoodItemsPublic: List of food items that the user owns.
    """
    result = await db.execute(
        select(FoodItemModel).where(FoodItemModel.user_id == user_id)
    )
    food_items = result.scalars().all()

    # Validates each food item against the pydantic response schema
    food_items_public = [
        FoodItemResponse.model_validate(food_item) for food_item in food_items
    ]

    return FoodItemsPublic(data=food_items_public)


async def get_food_item(food_item_id: UUID, db: AsyncSession) -> FoodItemModel | None:
    """Get food item.

    Args:
        food_item_id (UUID): ID of the requested food item.
        db (AsyncSession): Async database session.

    Returns:
        FoodItemModel: The food item matching the given ID, or None if not found.
    """
    food_item = await db.get(FoodItemModel, food_item_id)
    return food_item
    
