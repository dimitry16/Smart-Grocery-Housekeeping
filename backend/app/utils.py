from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import FoodItem as FoodItemModel
from app.database.models import User as UserModel


async def get_user(user_id: UUID, db: AsyncSession):
    """Helper function to get user.

    Args:
        user_id (UUID): Id of user.
        db (Annotated[AsyncSession, Depends): Session

    Raises:
        HTTPException: Raises 404 if user not found.
    """
    result = await db.execute(select(UserModel).where(UserModel.id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user


async def get_food_item(food_item_id: UUID, db: AsyncSession):
    """Helper function to get a specific food item by their ID.

    Args:
        food_item_id (UUID): Id of food item.
        db (AsyncSession): Session

    Raises:
        HTTPException: 404 response if food item does not exist.
    """
    result = await db.execute(
        select(FoodItemModel).where(FoodItemModel.id == food_item_id),
    )
    food_item = result.scalars().first()
    if food_item:
        return food_item
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Food Item not found"
    )
