from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import FoodItems as FoodItemsModel
from app.database.sqlconnector import get_db

from ..food_items.food_data import food_items_data
from ..food_items.schema import (
    FoodItemCreate,
    FoodItemResponse,
    FoodItemUpdate,
)

router = APIRouter()


@router.get("", response_model=list[FoodItemResponse])
async def get_all_food_items(db: Annotated[AsyncSession, Depends(get_db)]):
    """Read all food items."""
    result = await db.execute(
        select(FoodItemsModel).order_by(FoodItemsModel.name.asc())
    )
    food_items = result.scalars().all()
    return food_items


@router.get("/{food_item_id}", response_model=FoodItemResponse)
async def get_single_food_item(
    food_item_id: UUID, db: Annotated[AsyncSession, Depends(get_db)]
):
    """Get a specific food item by their ID.

    Raises:
        HTTPException: 404 response if food item does not exist.
    """
    result = await db.execute(
        select(FoodItemsModel).where(FoodItemsModel.id == food_item_id),
    )
    food_item = result.scalars().first()
    if food_item:
        return food_item
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Food Item not found."
    )


@router.post("", response_model=FoodItemResponse, status_code=status.HTTP_201_CREATED)
async def create_food_item(
    food_item: FoodItemCreate, db: Annotated[AsyncSession, Depends(get_db)]
):
    """Create a food item."""

    new_food_item = FoodItemsModel(**food_item.model_dump())
    db.add(new_food_item)
    await db.commit()
    await db.refresh(new_food_item)
    return new_food_item


@router.patch("/{food_item_id}")
async def partial_update_food_item(
    food_item_id: str, food_item_data: FoodItemUpdate
) -> dict:
    """Partially updates a food item by its ID.

    - Only include fields that you want to update in the request body.

    - Omit any fields that remain unchanged.

    Raises:
        HTTPException: 404 response if food item does not exist.
    """
    for food_item in food_items_data:
        if food_item["id"] == food_item_id:
            # Only update fields that were sent in request
            food_item.update(food_item_data.model_dump(exclude_unset=True))
            return food_item
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Food item not found."
    )


@router.delete("/{food_item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_food_item(food_item_id: str):
    """Delete food item by ID.

    Raises:
        HTTPException: 404 response if food item does not exist.
    """
    for food_item in food_items_data:
        if food_item.get("id") == food_item_id:
            food_items_data.remove(food_item)
            return {}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Food item not found."
    )
