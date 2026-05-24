from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.services import CurrentUser
from app.database.models import FoodItem as FoodItemModel
from app.database.sqlconnector import get_db
from app.food_items.schema import (
    FoodItemCreate,
    FoodItemResponse,
    FoodItemsPublic,
    FoodItemUpdate,
)

from . import services

router = APIRouter()


@router.post("", response_model=FoodItemResponse, status_code=status.HTTP_201_CREATED)
async def create_food_item(
    current_user: CurrentUser,
    food_item_data: FoodItemCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """Add food item to inventory.

    **Args**:
    - **current_user (CurrentUser)**: The authenticated user making the request.
    - **food_item_data (FoodItemCreate)**: JSON data containing food inventory details.
    - **db (Annotated[AsyncSession, Depends)**: Async database session

    **Raises**:
    - **HTTPException**: Raise 401 if user is not authorized.
    - **HTTPException**: Raise 404 if specified user not found.
    - **HTTPException**: Raise 409 if item with barcode already exists.
    """

    # Check if barcode is in the request, check if it exists in the pantry.
    if food_item_data.barcode:
        food_barcode = await db.execute(
            select(FoodItemModel).where(
                FoodItemModel.user_id == current_user.id,
                FoodItemModel.barcode == food_item_data.barcode,
            )
        )
        if food_barcode.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="An item with this barcode already exists.",
            )

    new_food_item = FoodItemModel(
        **food_item_data.model_dump(), user_id=current_user.id
    )
    db.add(new_food_item)
    await db.commit()
    await db.refresh(new_food_item)
    return new_food_item


@router.get("", response_model=FoodItemsPublic)
async def read_food_items(
    current_user: CurrentUser, db: Annotated[AsyncSession, Depends(get_db)]
):
    """Read user's items in their pantry.

    **Args**:
    - **current_user (CurrentUser):** The authenticated user making the request.
    - **db (Annotated[AsyncSession, Depends)**: Async database session

    """
    result = await services.get_food_items_by_user(user_id=current_user.id, db=db)
    return result


@router.get("/{food_item_id}", response_model=FoodItemResponse)
async def read_food_item(
    current_user: CurrentUser,
    food_item_id: UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """Get a specific food item by their ID.

    **Args**:
    - **current_user (CurrentUser)**: The authenticated user making the request.
    - **food_item_id (UUID)**: The UUID of the food item in the inventory.
    - **db (Annotated[AsyncSession, Depends)**: Async database session

    **Raises**:
    - **HTTPException**: 404 response if user does not exist.
    - **HTTPException**: 404 response if food item does not exist or user is not authorized to view the item..
    """
    food_item = await services.get_food_item(food_item_id=food_item_id, db=db)
    if not food_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Food item not found."
        )
    if food_item.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="User not authorized."
        )
    return food_item


@router.patch("/{food_item_id}", response_model=FoodItemResponse)
async def partial_update_food_item(
    current_user: CurrentUser,
    food_item_id: UUID,
    food_item_data: FoodItemUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """Partially updates a food item by its ID.

    - Only include fields that you want to update in the request body.

    - Omit any fields that remain unchanged.

    **Args**:
    - **current_user (CurrentUser)**: The authenticated user making the request.
    - **food_item_id (UUID)**: The UUID of the food item in the inventory.
    - **update_data (FoodItemUpdate)**: JSON data containing food inventory details to update.
    - **db (Annotated[AsyncSession, Depends)**: Async database session

    **Raises**:
    - **HTTPException**: 401 response if user is not authorized to update food item.
    - **HTTPException**: 404 response if food item does not exist.
    - **HTTPException**: 409 response if barcode already exists.
    """

    food_item = await services.get_food_item(food_item_id=food_item_id, db=db)
    if not food_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Food item not found."
        )
    if food_item.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="User not authorized."
        )

    # Only update fields that were sent in the request
    update_data = food_item_data.model_dump(exclude_unset=True)

    # If barcode is being updated, then check if barcode is unique
    if "barcode" in update_data and update_data["barcode"] is not None:
        result = await db.execute(
            select(FoodItemModel).where(
                FoodItemModel.user_id == current_user.id,
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
    current_user: CurrentUser,
    food_item_id: UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """Delete food item by ID.

    **Args**:
    - **current_user (CurrentUser)**: The authenticated user making the request.
    - **food_item_id (UUID)**: The UUID of the food item in the inventory.
    - **db (Annotated[AsyncSession, Depends)**: Async database session

    **Raises**:
    - **HTTPException**: 404 response if user does not exist.
    - **HTTPException**: 404 response if food item does not exist.
    """
    food_item = await services.get_food_item(food_item_id=food_item_id, db=db)
    if not food_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Food item not found."
        )
    if food_item.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="User not authorized."
        )

    await db.delete(food_item)
    await db.commit()

    return None
