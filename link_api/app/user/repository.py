from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from app.user.model import UserModel
from app.user.entity import UserEntity
from app.base.repository import BaseRepository


class UserRepository(BaseRepository[UserModel, UserEntity]):
    def __init__(self, async_session: AsyncSession):
        super().__init__(
            model=UserModel,
            entity=UserEntity,
            async_session=async_session
        )

    async def get_by_email(self, email: str) -> Optional[UserEntity]:
        query = (
            select(self.model)
            .where(self.model.email == email)
        )

        res = await self.async_session.execute(query)
        user = res.scalar_one_or_none()
        return self._to_entity(user)

    async def update(self) -> Optional[UserModel]:
        pass
