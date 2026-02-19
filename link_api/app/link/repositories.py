from dataclasses import asdict, is_dataclass
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import exists, select, delete
from sqlalchemy.orm import selectinload

from app.core.constants import UNSET
from app.link.models import LinkModel
from app.link.enums import LinkType
from app.core.repositories import BaseRepository
from app.link.entities import LinkEntity, CreateLinkEntity, UpdateLinkEntity, LinkWithCollectionsEntity
from app.common.mappers import EntityMapper


class LinkRepository(BaseRepository[LinkModel, LinkEntity]):
    def __init__(self, async_session: AsyncSession):
        super().__init__(
            model=LinkModel,
            entity=LinkEntity,
            async_session=async_session
        )

    def _to_entity(self, link_model: LinkModel) -> LinkWithCollectionsEntity:
        return EntityMapper.to_link_with_collections(link_model)

    def _to_model(self, link_entity: LinkEntity) -> LinkModel:
        if is_dataclass(link_entity):
            payload = asdict(link_entity)
        else:
            payload = link_entity.__dict__.copy()

        payload = {k: v for k, v in payload.items() if v is not UNSET}

        return self.model(**payload)

    async def get_with_collections(self, user_id: int, link_id: int) -> Optional[LinkWithCollectionsEntity]:
        query = (
            select(self.model)
            .where(self.model.id==link_id, self.model.user_id == user_id)
            .options(selectinload(self.model.collections))
        )
        res = await self.async_session.execute(query)
        link = res.scalar_one_or_none()
        return self._to_entity(link) if link else None

    async def list_with_collections(self, user_id: int, offset: int = 0, limit: int = 10) -> List[LinkWithCollectionsEntity]:
        query = (
            select(self.model)
            .where(self.model.user_id==user_id)
            .options(selectinload(self.model.collections))
            .offset(offset)
            .limit(limit)
        )
        res = await self.async_session.execute(query)
        entities = [self._to_entity(m) for m in res.scalars().all()]
        return entities

    async def list_by_type(self, user_id: int, link_type: LinkType = None, skip: int = 0, limit: int = 10) -> list[LinkEntity]:
        query = (
            select(self.model)
            .where(self.model.link_type == link_type.value, self.model.user_id == user_id)
            .options(selectinload(self.model.collections))
            .offset(skip)
            .limit(limit)
        )
        res = await self.async_session.execute(query)
        entities = [self._to_entity(m) for m in res.scalars().all()]
        return entities

    async def exists_by_url(self, user_id: int, url: str) -> bool:
        query = (
            select(exists().where(self.model.url == url, self.model.user_id==user_id))
        )
        result = await self.async_session.execute(query)
        return result.scalar() or False

    async def update(self, user_id: int, link_id: int, entity: UpdateLinkEntity) -> Optional[LinkEntity]:
        query = (
            select(self.model)
            .where(self.model.id == link_id, self.model.user_id == user_id)
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

    async def add(self, user_id: int, link_entity: CreateLinkEntity) -> LinkEntity:
        instance = self._to_model(link_entity)

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

    async def list(self, user_id: int, offset: int = 0, limit: int = 100) -> list[LinkEntity]:
        query = (
            select(self.model)
            .where(self.model.user_id == user_id)
            .offset(offset)
            .limit(limit)
        )
        res = await self.async_session.execute(query)
        entities = [self._to_entity(m) for m in res.scalars().all()]
        return entities