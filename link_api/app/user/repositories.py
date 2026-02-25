from dataclasses import asdict
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.common.mappers import EntityMapper
from app.user.models import UserModel
from app.user.entities import UserEntity, CreateUserEntity
from app.core.repositories import EntityRepository


class UserRepository(EntityRepository[UserModel, UserEntity]):
    def __init__(self, async_session: AsyncSession):
        super().__init__(
            model=UserModel,
            async_session=async_session
        )

    def _to_entity(self, orm_obj: UserModel) -> UserEntity:
        return EntityMapper.to_user(orm_obj)

    async def get_by_email(self, email: str) -> Optional[UserEntity]:
        user = await self._get_by_filters(
            self.model.email == email
        )
        if not user:
            return None
        return self._to_entity(user)

    async def add(self, entity: CreateUserEntity) -> UserEntity:
        payload = asdict(entity)
        orm_obj = self.model(**payload)

        self.async_session.add(orm_obj)
        await self.async_session.flush()
        await self.async_session.refresh(orm_obj)

        return self._to_entity(orm_obj)

    async def get(self, entity_id: int) -> Optional[UserEntity]:
        user_model = await self._get_by_filters(
            self.model.id == entity_id
        )
        if not user_model:
            return None

        return self._to_entity(user_model)
