# Name: Krystal Lu (klu04)
# Citation for async integration
# Date: 04/20/2025
# Adapted from "Python FastAPI Tutorial (Part 7): Sync vs Async - Converting Your App to Asynchronous"
# Source URL: https://www.youtube.com/watch?v=2JPDt-Jp6fM&list=PL-osiE80TeTsak-c-QsVeg0YYG_0TeyXI&index=8

from uuid import UUID
from typing import Annotated
from app.database.sqlconnector import get_db
from app.database.models import FoodItems as FoodItemsModel
from fastapi import APIRouter, Depends, HTTPException, status
from ..food_items.schema import FoodItemCreate, FoodItemResponse, FoodItemUpdate
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.get("", response_model=list[FoodItemResponse])
async def get_all_food_items(db: Annotated[AsyncSession, Depends(get_db)]):
    """Read all food items (in ascending order)

    Returns:
        All existing food items.
    """
    result = await db.execute(
        select(FoodItemsModel).order_by(FoodItemsModel.name.asc())
    )
    food_items = result.scalars().all()
    return food_items


@router.post("", response_model=FoodItemResponse, status_code=status.HTTP_201_CREATED)
async def create_food_item(
    food_item: FoodItemCreate, db: Annotated[AsyncSession, Depends(get_db)]
):
    """Create a food item.

    Returns:
        The food item that was created.
    """
    new_food_item = FoodItemsModel(**food_item.model_dump())
    db.add(new_food_item)
    await db.commit()
    await db.refresh(new_food_item)
    return new_food_item


@router.get("/{food_item_id}", response_model=FoodItemResponse)
async def get_food_item(
    food_item_id: UUID, db: Annotated[AsyncSession, Depends(get_db)]
):
    """Get a food item by their ID.

    Raises:
        HTTPException: 404 if food item not found.

    Returns:
        The requested food item.
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


@router.patch("/{food_item_id}", response_model=FoodItemResponse)
async def partial_update_food_item(
    food_item_id: UUID,
    food_item_data: FoodItemUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """Partially update a food item.

    Only the fields that are provided in the request body will be updated.
    If a barcode is provided, it must not belong to another existing food item.

    Raises:
        HTTPException: 404 if item is not found.
        HTTPException: 400 if barcode is already in use.

    Returns:
        The updated food item.
    """
    result = await db.execute(
        select(FoodItemsModel).where(FoodItemsModel.id == food_item_id)
    )
    food_item = result.scalar_one_or_none()
    if not food_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Food Item not found."
        )

    # Only update fields that were passed in the request
    update_data = food_item_data.model_dump(exclude_unset=True)

    # Check if barcode is being updated and if it's unique
    if "barcode" in update_data and update_data["barcode"] is not None:
        result = await db.execute(
            select(FoodItemsModel).where(
                FoodItemsModel.barcode == update_data["barcode"]
            )
        )
        exist = result.scalar_one_or_none()

        if exist and exist.id != food_item_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Barcode already exists.",
            )

    for key, val in update_data.items():
        setattr(food_item, key, val)

    await db.commit()
    await db.refresh(food_item)
    return food_item


@router.delete("/{food_item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_food_item(
    food_item_id: UUID, db: Annotated[AsyncSession, Depends(get_db)]
):
    """Delete a food item by their ID.

    Raises:
        HTTPException: 404 if food item not found.

    Returns:
        None
    """
    result = await db.execute(
        select(FoodItemsModel).where(FoodItemsModel.id == food_item_id),
    )
    food_item = result.scalar_one_or_none()

    if not food_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Food Item not found."
        )

    await db.delete(food_item)
    await db.commit()

    return None
