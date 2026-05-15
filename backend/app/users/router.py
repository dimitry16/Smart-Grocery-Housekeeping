from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.database.models import User as UserModel
from app.database.sqlconnector import get_db
from app.users.schema import UserCreate, UserPrivate, UserPublic, UserUpdate
from app.utils import get_user_util

router = APIRouter()


@router.post("", response_model=UserPrivate, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: Annotated[AsyncSession, Depends(get_db)]):
    """Creates a new user.

    Args:
        user (UserCreate): Pydantic Schema for validation check
        db (Annotated[AsyncSession, Depends): Session

    Raises:
        HTTPException: Raises 409 on duplicate email.
    """

    # Check if email has already been registered
    result = await db.execute(
        select(UserModel).where(
            func.lower(UserModel.email_address) == user.email_address.lower()
        ),
    )
    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Email already registered."
        )

    new_user = UserModel(
        name=user.name,
        email_address=user.email_address.lower(),
        password_hash=user.password,
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return new_user


@router.get("/{user_id}", response_model=UserPublic)
async def get_user(user_id: UUID, db: Annotated[AsyncSession, Depends(get_db)]):
    """Get a user by their id.

    Args:
        user_id (UUID): Id of user.
        db (Annotated[AsyncSession, Depends): Session

    Raises:
        HTTPException: Raises 404 if user not found.
    """
    return await get_user_util(user_id, db)


@router.patch("/{user_id}", response_model=UserPrivate)
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
    user = await get_user(user_id, db)

    # only update fields that were sent in the request
    user_update_data = user_data.model_dump(exclude_unset=True)

    # Check if email address already exists
    if (
        "email_address" in user_update_data
        and user_update_data["email_address"].lower() is not None
    ):
        result = await db.execute(
            select(UserModel).where(
                func.lower(UserModel.email_address)
                == user_update_data["email_address"].lower()
            )
        )
        exist = result.scalar_one_or_none()

        if exist and exist.id != user_id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Email already registered."
            )

    # Update user info
    for key, val in user_update_data.items():
        # Make email_address lowercase
        setattr(user, key, val.lower() if key == "email_address" else val)

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
    user = await get_user_util(user_id, db)

    await db.delete(user)
    await db.commit()

    return None
