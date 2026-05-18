# Name: Krystal Lu (klu04)
# Citation for auth.py
# Date: 05/14/2026
# Code Adapted from "FastAPI Docs - OAuth2 with Password (and hashing), Bearer with JWT tokens"
# Source URL: https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/

from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi.security import OAuth2PasswordBearer
from pwdlib import PasswordHash

from app.config import settings
from app.database.models import User as UserModel
from app.database.sqlconnector import get_db

# NOTE: Default hasher = Argon2
password_hash = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_URL}/tokens")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies if the password matches the given hash.

    Args:
        plain_password (str): The password to be checked.
        hashed_password (str): The hashed password to be verified.

    Returns:
        bool: True if the password matches the hash, False otherwise

    Reference: https://frankie567.github.io/pwdlib/reference/pwdlib/#pwdlib.PasswordHash.verify
    """
    return password_hash.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hashes the password.

    Args:
        password (str): The password to be hashed.

    Returns:
        str: The hashed password.
    """
    return password_hash.hash(password)


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Create a JWT access token using a user's id.

    Args:
        data (dict): user id to create the JWT access token.
        expires_delta (timedelta | None, optional): Max time before JWT expires. Defaults to None.

    Returns:
        str: A JSON Web Token

    References: https://pyjwt.readthedocs.io/en/stable/api.html
                https://pyjwt.readthedocs.io/en/stable/usage.html
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY.get_secret_value(),
        algorithm=settings.ALGORITHM,
    )
    return encoded_jwt
