from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import FoodItem as FoodItemModel
from app.database.sqlconnector import get_db
from app.food_items.schema import (
    FoodItemCreate,
    FoodItemResponse,
    FoodItemUpdate,
)
from app.utils import get_user_util

router = APIRouter()


@router.post("", response_model=FoodItemResponse, status_code=status.HTTP_201_CREATED)
async def create_food_item(
    user_id: UUID,
    food_item_data: FoodItemCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """Add food item to inventory.

    Args:
        user_id (UUID): The UUID of user that owns the inventory.
        food_item_data (FoodItemCreate): JSON data containing food inventory details.
        db (Annotated[AsyncSession, Depends): Async database session

    Raises:
        HTTPException: Raise 404 if specified user does not exist.
        HTTPException: Raise 409 if item with barcode already exists.
    """

    # Check if user exists
    await get_user_util(user_id, db)

    # Check if barcode is in the request, check if it exists in the pantry.
    if food_item_data.barcode:
        food_barcode = await db.execute(
            select(FoodItemModel).where(
                FoodItemModel.user_id == user_id,
                FoodItemModel.barcode == food_item_data.barcode,
            )
        )
        if food_barcode.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="An item with this barcode already exists.",
            )

    new_food_item = FoodItemModel(**food_item_data.model_dump(), user_id=user_id)
    db.add(new_food_item)
    await db.commit()
    await db.refresh(new_food_item)
    return new_food_item


@router.get("", response_model=list[FoodItemResponse])
async def get_user_food_items(
    user_id: UUID, db: Annotated[AsyncSession, Depends(get_db)]
):
    """Read user's items in their pantry.

    Args:
        user_id (UUID): The UUID of user that owns the inventory.
        db (Annotated[AsyncSession, Depends): Async database session

    Raises:
        HTTPException: Raise 404 if specified user does not exist.
    """

    # Check if user exists
    await get_user_util(user_id, db)

    result = await db.execute(
        select(FoodItemModel).where(FoodItemModel.user_id == user_id)
    )

    user_items = result.scalars().all()
    return user_items


@router.get("/{food_item_id}", response_model=FoodItemResponse)
async def get_single_food_item(
    user_id: UUID, food_item_id: UUID, db: Annotated[AsyncSession, Depends(get_db)]
):
    """Get a specific food item by their ID.

    Args:
        user_id (UUID): The UUID of user that owns the inventory.
        food_item_id (UUID): The UUID of the food item in the inventory.
        db (Annotated[AsyncSession, Depends): Async database session

    Raises:
        HTTPException: 404 response if user does not exist.
        HTTPException: 404 response if food item does not exist or user is not authorized to view the item..
    """

    # Check if user exists
    await get_user_util(user_id, db)

    result = await db.execute(
        select(FoodItemModel).where(
            FoodItemModel.user_id == user_id, FoodItemModel.id == food_item_id
        ),
    )
    food_item = result.scalar_one_or_none()

    # NOTE: The user check for this section will be removed
    # once authentication/authorization has been implemented
    if not food_item or food_item.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Food item not found or user is not authorized to view item",
        )

    return food_item


@router.patch("/{food_item_id}", response_model=FoodItemResponse)
async def partial_update_food_item(
    user_id: UUID,
    food_item_id: UUID,
    food_item_data: FoodItemUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """Partially updates a food item by its ID.

    - Only include fields that you want to update in the request body.

    - Omit any fields that remain unchanged.

    Args:
        user_id (UUID): The UUID of user that owns the inventory.
        food_item_id (UUID): The UUID of the food item in the inventory.
        update_data (FoodItemUpdate): JSON data containing food inventory details to update.
        db (Annotated[AsyncSession, Depends): Async database session

    Raises:
        HTTPException: 404 response if food item does not exist or user is not authorized to update item.
        HTTPException: 409 response if barcode already exists.
    """

    await get_user_util(user_id, db)

    # Get requested food item that will be updated
    result = await db.execute(
        select(FoodItemModel).where(FoodItemModel.id == food_item_id)
    )
    food_item = result.scalar_one_or_none()

    # NOTE: The user check for this section will be removed
    # once authentication/authorization has been implemented
    if not food_item or food_item.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Food item not found or user not authorized to update item..",
        )

    # Only update fields that were sent in the request
    update_data = food_item_data.model_dump(exclude_unset=True)

    # If barcode is being updated, then check if barcode is unique
    if "barcode" in update_data and update_data["barcode"] is not None:
        result = await db.execute(
            select(FoodItemModel).where(
                FoodItemModel.user_id == user_id,
                FoodItemModel.barcode == update_data["barcode"],
            )
        )
        exist = result.scalar_one_or_none()

        if exist and exist.id != food_item_id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="An item with this barcode already exists.",
            )

    # Update food item
    for key, val in update_data.items():
        setattr(food_item, key, val)

    await db.commit()
    await db.refresh(food_item)
    return food_item


@router.delete("/{food_item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_food_item(
    user_id: UUID, food_item_id: UUID, db: Annotated[AsyncSession, Depends(get_db)]
):
    """Delete food item by ID.

    Args:
        user_id (UUID): The UUID of user that owns the inventory.
        food_item_id (UUID): The UUID of the food item in the inventory.
        db (Annotated[AsyncSession, Depends): Async database session

    Raises:
        HTTPException: 404 response if user does not exist.
        HTTPException: 404 response if food item does not exist.
    """
    # Check if user exists
    await get_user_util(user_id, db)

    result = await db.execute(
        select(FoodItemModel).where(FoodItemModel.id == food_item_id),
    )
    food_item = result.scalar_one_or_none()
    if not food_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Food item not found."
        )

    await db.delete(food_item)
    await db.commit()

    return None
