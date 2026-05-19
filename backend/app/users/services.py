from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import User as UserModel


async def get_user_by_email(email: str, session: AsyncSession) -> UserModel:
    """Get user by their email address.

    Args:
        email (str): The email of the user that owns the inventory.
        db (Annotated[AsyncSession, Depends): Async database session.

    Raises:
        HTTPException: Raises 404 if user does not exist.
    """
    result = await session.execute(
        select(UserModel).where(func.lower(UserModel.email_address) == email.lower()),
    )
    user = result.scalar_one_or_none()
    return user
