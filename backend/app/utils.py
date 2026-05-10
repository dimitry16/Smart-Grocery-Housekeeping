from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import User as UserModel


async def get_user_util(user_id: UUID, db: AsyncSession):
    """Helper function to get user.

    Args:
        user_id (UUID): The UUID of user that owns the inventory.
        db (Annotated[AsyncSession, Depends): Async database session.

    Raises:
        HTTPException: Raises 404 if user does not exist.
    """
    result = await db.execute(select(UserModel).where(UserModel.id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found."
        )
    return user
