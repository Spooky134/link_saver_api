from dataclasses import is_dataclass, asdict
from typing import TypeVar, Generic, Type, List, Optional

from sqlalchemy import delete, select, func, exists
from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar('T')
E = TypeVar('E')


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

    def _to_model(self, entity: E, exclude_unset: bool=False) -> T:
        if is_dataclass(entity):
            payload = asdict(entity)
        else:
            payload = entity.__dict__.copy()

        if exclude_unset:
            payload = {k: v for k, v in payload.items() if v is not None}

        return self.model(**payload)

    async def get_by_id(self, entity_id: int) -> Optional[E]:
        orm_obj = await self.async_session.get(self.model, entity_id)
        return self._to_entity(orm_obj)

    async def get_by_ids(self, entity_ids: list[int]) -> list[E]:
        query = (
            select(self.model)
            .where(self.model.id.in_(entity_ids))
        )
        res = await self.async_session.execute(query)
        res = [self._to_entity(m for m in res.scalars().all())]
        return res

    async def get_all(self, offset: int = 0, limit: int = 100) -> list[E]:
        stmt = (
            select(self.model)
            .offset(offset)
            .limit(limit)
        )
        res = await self.async_session.execute(stmt)
        res = [self._to_entity(m) for m in res.scalars().all()]
        return res

    async def add(self, entity: E, exclude_unset=True) -> E:
        instance = self._to_model(entity, exclude_unset=exclude_unset)
        self.async_session.add(instance)
        await self.async_session.flush()
        await self.async_session.refresh(instance)
        return self._to_entity(instance)

    async def delete(self, entity_id: int) -> bool:
        stmt = (
            delete(self.model)
            .filter_by(id=entity_id)
        )
        res = await self.async_session.execute(stmt)
        await self.async_session.flush()
        return res.rowcount > 0

    async def exists_by_id(self, entity_id: int) -> bool:
        query = select(exists().where(self.model.id == entity_id))
        res = await self.async_session.execute(query)
        return res.scalar() or False

    async def update(self, entity_id: int, entity: E, _exclude: Optional[set[str]] = None) -> Optional[E]:
        default_exclude = {"id", "created_at", "updated_at"}
        if _exclude:
            default_exclude.update(_exclude)
        orm_obj = await self.async_session.get(self.model, entity_id)
        if not orm_obj:
            return None

        update_data = asdict(entity)
        for key, value in update_data.items():
            if key not in _exclude and hasattr(orm_obj, key) and value is not None:
                setattr(orm_obj, key, value)

        await self.async_session.flush()
        await self.async_session.refresh(orm_obj)

        return self._to_entity(orm_obj)