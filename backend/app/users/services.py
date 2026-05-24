from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import User as UserModel


async def get_user_by_email(email: str, db: AsyncSession) -> UserModel | None:
    result = await db.execute(
        select(UserModel).where(func.lower(UserModel.email_address) == email.lower())
    )
    return result.scalar_one_or_none()
