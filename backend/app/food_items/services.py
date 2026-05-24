from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import FoodItem as FoodItemModel
from app.food_items.schema import FoodItemResponse, FoodItemsPublic


async def get_food_items_by_user(user_id: UUID, db: AsyncSession) -> FoodItemsPublic:
    result = await db.execute(
        select(FoodItemModel).where(FoodItemModel.user_id == user_id)
    )
    items = result.scalars().all()
    return FoodItemsPublic(
        food_items=[FoodItemResponse.model_validate(item) for item in items]
    )


async def get_food_item(food_item_id: UUID, db: AsyncSession) -> FoodItemModel | None:
    result = await db.execute(
        select(FoodItemModel).where(FoodItemModel.id == food_item_id)
    )
    return result.scalar_one_or_none()
