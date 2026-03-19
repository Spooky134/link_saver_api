from dataclasses import asdict
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.repositories import BaseRepository
from app.core.types import UNSET
from app.user.entities import CreateUserEntity, UpdateUserEntity, UserEntity
from app.user.mappers import UserMapper
from app.user.models import UserModel


class UserRepository(BaseRepository):
    def __init__(self, db_session: AsyncSession):
        super().__init__(model=UserModel, db_session=db_session)

    async def get_by_email(self, email: str) -> Optional[UserEntity]:
        user_orm = await self._get_by_filters(self._model.email == email)
        if not user_orm:
            return None
        return UserMapper.to_entity(user_orm)

    async def add(self, entity: CreateUserEntity) -> UserEntity:
        payload = asdict(entity)
        user_orm = self._model(**payload)

        self._db_session.add(user_orm)
        await self._db_session.flush()
        await self._db_session.refresh(user_orm)

        return UserMapper.to_entity(user_orm)

    async def get(self, user_id: int) -> Optional[UserEntity]:
        user_orm = await self._get_by_filters(self._model.id == user_id)
        if not user_orm:
            return None

        return UserMapper.to_entity(user_orm)

    async def update(self, user_id: int, entity: UpdateUserEntity) -> Optional[UserEntity]:
        user_orm = await self._get_by_filters(
            self._model.id == user_id,
        )
        if not user_orm:
            return None

        update_data = asdict(entity)
        update_data = {
            key: value for key, value in update_data.items()
            if value is not UNSET
        }

        await self._update(user_orm, update_data)

        return UserMapper.to_entity(user_orm)


