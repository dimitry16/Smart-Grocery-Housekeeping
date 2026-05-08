from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

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
    """_summary_

    Args:
        user_id (UUID): Id of user who owns the pantry.
        food_item_data (UserFoodItemCreate): Food item from global catalog to be added to pantry.
        db (Annotated[AsyncSession, Depends): Session

    Raises:
        HTTPException: Raises 409 if item already exists in the pantry
    """
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


@router.get("", response_model=list[UserFoodItemResponse])
async def get_pantry(user_id: UUID, db: Annotated[AsyncSession, Depends(get_db)]):
    """Get items from pantry.

    Args:
        user_id (UUID): Id of user who owns the pantry.
        db (Annotated[AsyncSession, Depends): Session

    References:
        Loader Strategies for attributes mapped using relationship():
            https://docs.sqlalchemy.org/en/20/tutorial/orm_related_objects.html#loader-strategies
            https://docs.sqlalchemy.org/en/20/tutorial/orm_related_objects.html#selectin-load
    """
    # Check if user exists
    await get_user(user_id, db)

    # Get user's pantry items
    result = await db.execute(
        select(UserFoodItemModel)
        .where(UserFoodItemModel.user_id == user_id)
        .options(selectinload(UserFoodItemModel.food_item))
    )
    pantry_items = result.scalars().all()
    return pantry_items


@router.patch("", response_model=UserFoodItemResponse)
async def partial_update_pantry(
    user_id: UUID,
    item_id: UUID,
    update_data: UserFoodItemUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """

    Args:
        user_id (UUID): Id of user who owns pantry.
        item_id (UUID): Id of user's pantry item to be updated.
        update_data (UserFoodItemUpdate): Update data from the request.
        db (Annotated[AsyncSession, Depends): Session

    Raises:
        HTTPException: Raises 404 if pantry item not found.
        HTTPException: Raises 403 if an unauthorized user tries to update an item.

    References:
        Loader Strategies for attributes mapped using relationship():
            https://docs.sqlalchemy.org/en/20/tutorial/orm_related_objects.html#loader-strategies
            https://docs.sqlalchemy.org/en/20/tutorial/orm_related_objects.html#selectin-load
    """
    result = await db.execute(
        select(UserFoodItemModel)
        .where(UserFoodItemModel.id == item_id)
        .options(selectinload(UserFoodItemModel.food_item))
    )

    pantry_item = result.scalar_one_or_none()

    if not pantry_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Pantry item not found."
        )
    if pantry_item.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User not authorized to update this item.",
        )

    update_item = update_data.model_dump(exclude_unset=True)
    for key, val in update_item.items():
        setattr(pantry_item, key, val)

    await db.commit()
    await db.refresh(pantry_item, attribute_names=["food_item"])
    return pantry_item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_pantry_item(
    user_id: UUID, item_id: UUID, db: Annotated[AsyncSession, Depends(get_db)]
):
    """Delete an item from the pantry.

    Args:
        user_id (UUID): Id of user
        item_id (UUID): Id of user's pantry item to be deleted.
        db (Annotated[AsyncSession, Depends): Session

    Raises:
        HTTPException: Raises 404 if pantry item not found.
        HTTPException: Raises 403 if an unauthorized user tries to delete an item
    References:
    Loader Strategies for attributes mapped using relationship():
        https://docs.sqlalchemy.org/en/20/tutorial/orm_related_objects.html#loader-strategies
        https://docs.sqlalchemy.org/en/20/tutorial/orm_related_objects.html#selectin-load
    """

    result = await db.execute(
        select(UserFoodItemModel).where(
            UserFoodItemModel.id == item_id,
        )
    )

    user_item = result.scalar_one_or_none()

    if not user_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pantry item not found.",
        )
    if user_item.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User not authorized to delete this item.",
        )

    await db.delete(user_item)
    await db.commit()
