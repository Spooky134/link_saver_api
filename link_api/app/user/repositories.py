from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from app.user.models import UserModel
from app.user.entities import UserEntity
from app.core.repositories import BaseRepository


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
        return self._to_entity(user) if user else None


    async def add(self, entity: UserEntity, exclude_unset=True) -> UserEntity:
        instance = self._to_model(entity, exclude_unset=exclude_unset)

        self.async_session.add(instance)
        await self.async_session.flush()
        await self.async_session.refresh(instance)

        return self._to_entity(instance)


    async def get(self, entity_id: int) -> Optional[UserEntity]:
        query = (
            select(self.model)
            .where(self.model.id == entity_id)
        )
        result = await self.async_session.execute(query)
        orm_obj = result.scalar_one_or_none()
        if orm_obj is None:
            return None
        return self._to_entity(orm_obj)


    # async def list_by_ids(self, entity_ids: list[int]) -> list[E]:
    #     query = (
    #         select(self.model)
    #         .where(self.model.id.in_(entity_ids))
    #     )
    #     res = await self.async_session.execute(query)
    #     entities = [self._to_entity(m) for m in res.scalars().all()]
    #     return entities
    #
    # async def list(self, offset: int = 0, limit: int = 100) -> list[E]:
    #     query = (
    #         select(self.model)
    #         .offset(offset)
    #         .limit(limit)
    #     )
    #     res = await self.async_session.execute(query)
    #     entities = [self._to_entity(m) for m in res.scalars().all()]
    #     return entities
    #
    # async def add(self, entity: E, exclude_unset=True) -> E:
    #     instance = self._to_model(entity, exclude_unset=exclude_unset)
    #
    #     self.async_session.add(instance)
    #     await self.async_session.flush()
    #     await self.async_session.refresh(instance)
    #
    #     return self._to_entity(instance)
    #
    # async def delete(self, entity_id: int) -> bool:
    #     stmt = (
    #         delete(self.model)
    #         .where(self.model.id == entity_id)
    #     )
    #     res = await self.async_session.execute(stmt)
    #     await self.async_session.flush()
    #     return res.rowcount > 0
    #
    # async def exists_by_id(self, entity_id: int) -> bool:
    #     query = (
    #         select(exists().where(self.model.id == entity_id))
    #     )
    #     res = await self.async_session.execute(query)
    #     return res.scalar() or False
    #
    # async def update(self, entity_id: int, entity: E, _exclude: Optional[set[str]] = None) -> Optional[E]:
    #     default_exclude = {"id", "created_at", "updated_at"}
    #     if _exclude:
    #         default_exclude.update(_exclude)
    #
    #     query = (
    #         select(self.model)
    #         .where(self.model.id == entity_id)
    #     )
    #     res = await self.async_session.execute(query)
    #     orm_obj = res.scalar_one_or_none()
    #     if not orm_obj:
    #         return None
    #
    #     update_data = asdict(entity)
    #     for key, value in update_data.items():
    #         if key not in _exclude and hasattr(orm_obj, key) and value is not None:
    #             setattr(orm_obj, key, value)
    #
    #     await self.async_session.flush()
    #     await self.async_session.refresh(orm_obj)
    #
    #     return self._to_entity(orm_obj)