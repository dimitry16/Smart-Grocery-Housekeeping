# Name: Krystal Lu (klu04)
# Citation for auth.py
# Date: 05/14/2026
# Code Adapted from "FastAPI Docs - OAuth2 with Password (and hashing), Bearer with JWT tokens"
# Source URL: https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/

from datetime import datetime, timedelta, timezone

import jwt
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash
from pydantic import ValidationError

from app.config import settings

# NOTE: Default hasher = Argon2
password_hash = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_URL}/users/token")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies if the password matches the given hash and updates the hash if necessary.

    Args:
        plain_password (str): The password to be checked.
        hashed_password (str): The hashed password to be verified.

    Returns:
        bool: True if the password matches the hash, False otherwise.

    Reference: https://frankie567.github.io/pwdlib/reference/pwdlib/#pwdlib.PasswordHash.verify_and_update
    """
    return password_hash.verify_and_update(plain_password, hashed_password)


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


def verify_access_token(token: str) -> str | None:
    """Helper function to decode and verify a JWT access token.

    Args:
        token (str): Token to be verified.

    Returns:
        str | None: The subject claim if token is valid, otherwise None.

    References: https://pyjwt.readthedocs.io/en/stable/api.html
                https://pyjwt.readthedocs.io/en/stable/usage.html

    """
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY.get_secret_value(),
            algorithms=[settings.ALGORITHM],
            options={"require": ["exp", "sub"]},
        )
    except (InvalidTokenError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials.",
        )
    else:
        # Returns a subject claim
        # Ref: https://auth0.com/docs/secure/tokens/json-web-tokens/json-web-token-claims
        return payload.get("sub")
