from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db_session
from app.user.repositories import UserRepository


async def get_user_repository(async_session: AsyncSession = Depends(get_db_session)) -> UserRepository:
    return UserRepository(async_session)