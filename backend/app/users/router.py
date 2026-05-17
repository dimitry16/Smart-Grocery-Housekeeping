# Name: Krystal Lu (klu04)
# Citation for login_for_access_token and get_current_user
# Date: 05/14/2026
# Code Adapted from "FastAPI Docs - OAuth2 with Password (and hashing), Bearer with JWT tokens"
# Source URL: https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/

from datetime import timedelta
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.auth import (
    create_access_token,
    get_password_hash,
    oauth2_scheme,
    verify_access_token,
    verify_password,
)
from app.auth.schema import Token
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
        password_hash=get_password_hash(user.password),
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return new_user


@router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> Token:
    """Authenticate a user and return an access token.

    NOTE: "OAuth2PasswordRequestForm uses "username" field, but we will
    use an email instead.

    Args:
        form_data (Annotated[OAuth2PasswordRequestForm, Depends): Login form data.
        db (Annotated[AsyncSession, Depends): Database session.
    Raises:
        HTTPException: 401 if email or password is incorrect.

    Returns:
        Token: Access token and token type.
    """

    # Find user by email
    result = await db.execute(
        select(UserModel).where(
            func.lower(UserModel.email_address) == form_data.username.lower()
        ),
    )
    user = result.scalar_one_or_none()

    # Verify user and password
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create an access token with user id
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=access_token_expires,
    )
    return Token(access_token=access_token, token_type="bearer")


@router.get("/me", response_model=UserPrivate)
async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """Get current user information.

    Args:
        token (Annotated[str, Depends): Received JWT token.
        db (Annotated[AsyncSession, Depends): Database session.

    Raises:
        HTTPException: 401 Unauthorized if invalid or expired token.
        HTTPException: 401 Unauthorized if user not found.
    """
    # Verify token and get user id
    try:
        user_id = verify_access_token(token)
    except TypeError, ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Look for user id in the database
    user = await db.get(UserModel, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


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
    # Note: email addresses are case-insensitive
    if (
        user_update_data.email_address is not None
        and user_update_data.email_address.lower() != user.email_address.lower()
    ):
        result = await db.execute(
            select(UserModel).where(
                func.lower(UserModel.email_address)
                == user_update_data.email_address.lower()
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
