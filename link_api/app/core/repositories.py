from dataclasses import is_dataclass, asdict
from typing import TypeVar, Generic, Type, List, Optional, Any

from sqlalchemy import delete, select, func, exists
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.constants import UNSET


T = TypeVar('T')
E = TypeVar('E')
C = TypeVar("C")
U = TypeVar("U")


class BaseRepository(Generic[T, E]):
    def __init__(self, model: Type[T], entity: Type[E], async_session: AsyncSession):
        self.model: Type[T] = model
        self.entity: Type[E] = entity
        self.async_session = async_session

    def _to_entity(self, orm_obj: T) -> E:
        if orm_obj is None:
            return None

        fields = {c.key: getattr(orm_obj, c.key) for c in orm_obj.__table__.columns}
        return self.entity(**fields)

    def _to_model(self, entity: Any) -> T:
        if is_dataclass(entity):
            payload = asdict(entity)
        else:
            payload = entity.__dict__.copy()

        payload = {k: v for k, v in payload.items() if v is not UNSET}

        return self.model(**payload)

    # async def get(self, entity_id: int) -> Optional[E]:
    #     query = (
    #         select(self.model)
    #         .where(self.model.id == entity_id)
    #     )
    #     result = await self.async_session.execute(query)
    #     orm_obj = result.scalar_one_or_none()
    #     if orm_obj is None:
    #         return None
    #     return self._to_entity(orm_obj)
    #
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
    #

class OwnedRepository(BaseRepository[T, E]):
    async def get(self, user_id: int, entity_id: int) -> Optional[E]:
        query = (
            select(self.model)
            .where(self.model.id == entity_id, self.model.user_id == user_id)
        )
        result = await self.async_session.execute(query)
        orm_obj = result.scalar_one_or_none()
        if orm_obj is None:
            return None
        return self._to_entity(orm_obj)

    async def list_by_ids(self, user_id: int, entity_ids: list[int]) -> list[E]:
        query = (
            select(self.model)
            .where(self.model.id.in_(entity_ids), self.model.user_id == user_id)
        )
        res = await self.async_session.execute(query)
        entities = [self._to_entity(m) for m in res.scalars().all()]
        return entities

    async def list(self, user_id: int, offset: int = 0, limit: int = 100) -> list[E]:
        query = (
            select(self.model)
            .where(self.model.user_id == user_id)
            .offset(offset)
            .limit(limit)
        )
        res = await self.async_session.execute(query)
        entities = [self._to_entity(m) for m in res.scalars().all()]
        return entities

    async def add(self, user_id: int, entity: E) -> E:
        instance = self._to_model(entity)

        instance.user_id = user_id

        self.async_session.add(instance)
        await self.async_session.flush()
        await self.async_session.refresh(instance)

        return self._to_entity(instance)

    async def delete(self, user_id: int, entity_id: int) -> bool:
        stmt = (
            delete(self.model)
            .where(self.model.id == entity_id, self.model.user_id == user_id)
        )
        res = await self.async_session.execute(stmt)
        await self.async_session.flush()
        return res.rowcount > 0

    async def exists_by_id(self, user_id: int, entity_id: int) -> bool:
        query = (
            select(exists().where(self.model.id == entity_id, self.model.user_id == user_id))
        )
        res = await self.async_session.execute(query)
        return res.scalar() or False

    async def update(self, user_id: int, entity_id: int, entity: E) -> Optional[E]:
        query = (
            select(self.model)
            .where(self.model.id == entity_id, self.model.user_id == user_id)
        )
        res = await self.async_session.execute(query)
        orm_obj = res.scalar_one_or_none()
        if not orm_obj:
            return None

        update_data = asdict(entity)
        for key, value in update_data.items():
            if value is not UNSET and hasattr(orm_obj, key):
                setattr(orm_obj, key, value)

        await self.async_session.flush()
        await self.async_session.refresh(orm_obj)

        return self._to_entity(orm_obj)
