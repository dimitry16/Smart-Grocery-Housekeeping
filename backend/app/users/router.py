from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import User as UserModel
from app.database.sqlconnector import get_db
from app.user_food_items.schema import UserFoodItemResponse
from app.users.schema import UserCreate, UserInventoryResponse, UserResponse, UserUpdate

router = APIRouter()


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: Annotated[AsyncSession, Depends(get_db)]):
    """Creates a user.

    NOTE: Password has not been hashed yet as authentication had not been implemented.
    This is just the basic implementation for testing.

    Args:
        user (UserCreate): Pydantic Schema for validation check
        db (Annotated[AsyncSession, Depends): Session

    Raises:
        HTTPException: Raises 409 on duplicate email.
    """

    # Check if email has already been registered
    result = await db.execute(
        select(UserModel).where(UserModel.email_address == user.email_address),
    )
    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Email already registered."
        )

    result = await db.execute(
        select(UserModel).where(UserModel.email_address == user.email_address)
    )

    new_user = UserModel(
        name=user.name, email_address=user.email_address, password_hash=user.password
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return new_user


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: UUID, db: Annotated[AsyncSession, Depends(get_db)]):
    """Get a user by their id.

    Args:
        user_id (UUID): Id of user.
        db (Annotated[AsyncSession, Depends): Session

    Raises:
        HTTPException: Raises 404 if user not found.
    """
    result = await db.execute(select(UserModel).where(UserModel.id == user_id))
    user = result.scalar_one_or_none()
    if user:
        return user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
