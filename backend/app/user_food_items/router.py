from decimal import Decimal
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import UserFoodItem as UserFoodItemModel
from app.database.sqlconnector import get_db
from app.user_food_items.schema import (
    UserFoodItemCreate,
    UserFoodItemResponse,
    UserFoodItemUpdate,
)
from app.utils import get_food_item, get_user

router = APIRouter()


@router.post(
    "", response_model=UserFoodItemResponse, status_code=status.HTTP_201_CREATED
)
async def add_item_to_pantry(
    user_id: UUID,
    food_item_data: UserFoodItemCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    # Check if user and food item exists
    await get_user(user_id, db)
    await get_food_item(food_item_data.food_item_id, db)

    # Check if item already exists in user's pantry
    result = await db.execute(
        select(UserFoodItemModel).where(
            UserFoodItemModel.user_id == user_id,
            UserFoodItemModel.food_item_id == food_item_data.food_item_id,
        )
    )
    dupe_item = result.scalar_one_or_none()
    if dupe_item:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Item already exists in the pantry.",
        )

    # Add item to pantry
    new_item = UserFoodItemModel(**food_item_data.model_dump(), user_id=user_id)
    db.add(new_item)
    await db.commit()
    await db.refresh(new_item, attribute_names=["food_item"])
    return new_item
