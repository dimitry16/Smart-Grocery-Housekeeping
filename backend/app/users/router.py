from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import User as UserModel
from app.database.sqlconnector import get_db
from app.users.schema import UserCreate, UserResponse, UserUpdate

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


@router.patch("/{user_id}", response_model=UserResponse)
async def partial_update_user(
    user_id: UUID, user_data: UserUpdate, db: Annotated[AsyncSession, Depends(get_db)]
):
    """Update or partially update a user.

    Args:
        user_id (UUID): Id of user.
        user_data (UserUpdate): original user data
        db (Annotated[AsyncSession, Depends): session

    Raises:
        HTTPException: Raises 404 if user not found.
        HTTPException: Raises 409 if email address is a duplicate.
    """

    # Check of user exists
    result = await db.execute(select(UserModel).where(UserModel.id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found."
        )

    # only update fields that were sent in the request
    user_update_data = user_data.model_dump(exclude_unset=True)

    # Check if email address already exists
    if (
        "email_address" in user_update_data
        and user_update_data["email_address"] is not None
    ):
        result = await db.execute(
            select(UserModel).where(
                UserModel.email_address == user_update_data["email_address"]
            )
        )
        exist = result.scalar_one_or_none()

        if exist and exist.id != user_id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Email already registered."
            )

    # Update user info
    for key, val in user_update_data.items():
        setattr(user, key, val)

    await db.commit()
    await db.refresh(user)
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: UUID, db: Annotated[AsyncSession, Depends(get_db)]):
    """Delete a user.

    Args:
        user_id (UUID): Id of user
        db (Annotated[AsyncSession, Depends): Session

    Raises:
        HTTPException: Raises 404 if user not found.
    """
    result = await db.execute(select(UserModel).where(UserModel.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found."
        )

    await db.delete(user)
    await db.commit()

    return None
