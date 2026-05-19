# Name: Krystal Lu (klu04)
# Citation for login_for_access_token and get_current_user
# Date: 05/14/2026
# Code Adapted from "FastAPI Docs - OAuth2 with Password (and hashing), Bearer with JWT tokens"
# Source URL: https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.services import CurrentUser, get_password_hash
from app.database.models import User as UserModel
from app.database.sqlconnector import get_db
from app.users.schema import UserCreate, UserPrivate, UserUpdate

from . import services

router = APIRouter()


@router.post("", response_model=UserPrivate, status_code=status.HTTP_201_CREATED)
async def register_user(
    user: UserCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """
    Creates a new user.

    **Args**:
    - **user (UserCreate)**: Pydantic Schema for validation check
    - **db (Annotated[AsyncSession, Depends)**: Session

    **Raises**:
    - **HTTPException**: Raises 409 on duplicate email.
    """

    # Check if email has already been registered
    user = services.get_user(user.email_address, session=db)

    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Email already registered."
        )

    new_user = UserModel(
        name=user.name,
        email_address=user.email_address.lower(),
        password_hash=get_password_hash(user.password),
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return new_user


@router.get("/me", response_model=UserPrivate)
async def read_user_info_me(current_user: CurrentUser):
    """
    Return information of current user.

    **Args**:
    - **current_user (CurrentUser)**: The authenticated user making the request.
    """
    return current_user


@router.patch("/{user_id}", response_model=UserPrivate)
async def partial_update_user(
    user_id: UUID,
    current_user: CurrentUser,
    user_data: UserUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """
    Update or partially update a user.

    **Args**:
    - **user_id (UUID)**: Id of user.
    - **current_user (CurrentUser)**: The authenticated user making the request.
    - **user_data (UserUpdate)**: original user data
    - **db (Annotated[AsyncSession, Depends)**: session

    **Raises**:
    - **HTTPException**: 403 if user not authorized to update user.
    - **HTTPException**: Raises 404 if user not found.
    - **HTTPException**: Raises 409 if email address is a duplicate.
    """
    if user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this user.",
        )

    user = await db.get(UserModel, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found."
        )

    # only update fields that were sent in the request
    user_update_data = user_data.model_dump(exclude_unset=True)

    # Check if email address already exists
    # Note: email addresses are case-insensitive

    email = user_update_data["email_address"]
    if email is not None and email.lower() != user.email_address.lower():
        result = await db.execute(
            select(UserModel).where(
                func.lower(UserModel.email_address) == email.lower()
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
async def delete_user(
    user_id: UUID,
    current_user: CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """
    Delete a user.

    **Args**:
    - **user_id (UUID)**: Id of user
    - **current_user (CurrentUser)**: The authenticated user making the request.
    - **db (Annotated[AsyncSession, Depends)**: Session

    **Raises**:
    - **HTTPException**: 403 if user not authorized to delete user.
    - **HTTPException**: 404 if user not found.
    """

    if user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this user.",
        )

    user = await db.get(UserModel, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found."
        )

    await db.delete(user)
    await db.commit()

    return None
