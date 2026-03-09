from dataclasses import asdict
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.user.mappers import UserMapper
from app.user.models import UserModel
from app.user.entities import UserEntity, CreateUserEntity, UpdateUserEntity
from app.core.repositories import EntityRepository


class UserRepository(EntityRepository[UserModel, UserEntity]):
    def __init__(self, async_session: AsyncSession):
        super().__init__(
            model=UserModel,
            async_session=async_session
        )

    def _to_entity(self, orm_obj: UserModel) -> UserEntity:
        return UserMapper.to_user(orm_obj)

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

        self._async_session.add(orm_obj)
        await self._async_session.flush()
        await self._async_session.refresh(orm_obj)

        return self._to_entity(orm_obj)

    async def get(self, entity_id: int) -> Optional[UserEntity]:
        user_model = await self._get_by_filters(
            self.model.id == entity_id
        )
        if not user_model:
            return None

        return self._to_entity(user_model)

    async def update(self, user_id: int, entity: UpdateUserEntity) -> Optional[UserEntity]:
        orm_obj = await self._get_by_filters(
            self.model.id == user_id,
        )
        if not orm_obj:
            return None

        await self._update_model(
            orm_obj = orm_obj,
            entity = entity
        )

        return self._to_entity(orm_obj)