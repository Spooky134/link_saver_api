from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from app.user.model import UserModel
from app.base.repository import BaseRepository


class UserRepository(BaseRepository):
    model = UserModel

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, id: int) -> Optional[UserModel]:
        query = (
            select(UserModel)
            .where(UserModel.id == id)
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> Optional[UserModel]:
        query = (
            select(UserModel)
            .where(UserModel.email == email))

        result = await self.session.execute(query)
        return result.scalar_one_or_none()


    async def create(self, link_data: dict) -> UserModel:
        new_obj = UserModel(**link_data)
        self.session.add(new_obj)
        await self.session.commit()

        return await self.get(new_obj.id)

    async def get_all(self, skip: int = 0, limit: int = 100) -> list[UserModel]:
        query = (
            select(UserModel)
            .offset(skip)
            .limit(limit)
        )
        result = await self.session.execute(query)
        result = result.scalars().all()
        return result

    async def update(self) -> Optional[UserModel]:
        pass

    async def delete(self, id: int) -> None:
        await self.session.execute(delete(UserModel).where(UserModel.id == id))
        await self.session.commit()
