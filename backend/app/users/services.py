from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import User as UserModel


async def get_user_by_email(email: str, db: AsyncSession) -> UserModel | None:
    """Get user by their email address.

    Args:
        email (str): The email of the user that owns the inventory.
        db (Annotated[AsyncSession, Depends): Async database session.

    Returns:
        UserModel | None: The user connected to the given email, or None if not found.
    """
    result = await db.execute(
        select(UserModel).where(func.lower(UserModel.email_address) == email.lower()),
    )
    user = result.scalar_one_or_none()
    return user