from dataclasses import asdict
from datetime import datetime
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import exists, func, select, update, delete
from sqlalchemy.orm import selectinload

# from app.link.entity import LinkEntity
from app.link.models import LinkModel
from app.link.enums import LinkType
from app.collection.models import CollectionModel
from app.common.model import link_collection
from app.base.repositories import BaseRepository, T, E
from app.collection.entities import CollectionEntity
from app.common.mappers import EntityMapper


class CollectionRepository(BaseRepository[CollectionModel, CollectionEntity]):
    def __init__(self, async_session: AsyncSession):
        super().__init__(
            model=CollectionModel,
            entity=CollectionEntity,
            async_session=async_session
        )

    def _to_entity(self, collection_model: CollectionModel) -> E:
        return EntityMapper.to_collection_entity(collection_model)

    async def get_by_id_with_links(self, collection_id: int) -> Optional[CollectionEntity]:
        query = (
            select(self.model)
            .options(selectinload(self.model.links))
            .where(self.model.id == collection_id)
        )
        res = await self.async_session.execute(query)
        res = res.scalar_one_or_none()
        return self._to_entity(res) if res else None

    async def get_all_with_links(self, skip: int = 0, limit: int = 10) -> list[CollectionEntity]:
        query = (
            select(CollectionModel)
            .options(selectinload(CollectionModel.links))
            .offset(skip)
            .limit(limit)
        )
        res = await self.async_session.execute(query)
        res = [self._to_entity(m) for m in res.scalars().all()]
        return res

    async def get_count_links(self, collection_id: int) -> int:
        query = (
            select(func.count())
            .select_from(self.model)
            .where(self.model.c.collection_id == collection_id)
        )
        count = await self.async_session.execute(query)
        return count or 0

    async def exists_by_name(self, name: str) -> bool:
        query = (
            select(exists().where(self.model.name == name))
        )
        res = await self.async_session.execute(query)
        return res.scalar() or False

    # TODO юзер не нужен
    async def update(self, collection_id: int, collection_entity: CollectionEntity, _exclude: Optional[set[str]] = None) -> Optional[CollectionEntity]:
        excluded_fields = {"links", "user_id"}
        if _exclude:
            excluded_fields.update(_exclude)
        collection_update = await super().update(collection_id, collection_entity, _exclude=excluded_fields)
        return collection_update


    # async def set_links_to_collection(self, collection_id: int, link_entities: list["LinkEntity"]) -> None:
    #     query = (
    #         select(self.model)
    #         .options(selectinload(self.model.links))
    #         .where(self.model.id == collection_id)
    #     )
    #     res = await self.async_session.execute(query)
    #     collection = res.scalar_one_or_none()
    #     collection.links = [self._to_model(e) for e in link_entities]
    #     await self.async_session.flush()
    #     await self.async_session.refresh(collection)

    async def add_links_to_collection(self, collection_id, link_entities: list["LinkEntity"]) -> None:
        query = (
            select(self.model)
            .options(selectinload(self.model.links))
            .where(self.model.id == collection_id)
        )
        res = await self.async_session.execute(query)
        collection = res.scalar_one_or_none()

        existing_urls = {link.url for link in collection.links}

        collection.links.extend(
            [self._to_model(e) for e in link_entities if e.url not in existing_urls]
        )

        await self.async_session.flush()

    async def remove_link_from_collection(self, collection_id: int, link_id: int) -> bool:
        stmt = (
            delete(link_collection)
            .where((link_collection.c.collection_id == collection_id)
                   & (link_collection.c.link_id == link_id))
        )
        res = await self.async_session.execute(stmt)
        await self.async_session.flush()
        return res.rowcount > 0

    async def search_by_name(self, name_query: str, skip: int = 0, limit: int = 10) -> list[CollectionEntity]:
        query = (
            select(self.model)
            .options(selectinload(self.model.links))
            .where(self.model.name.ilike(f"%{name_query}%"))
            .offset(skip)
            .limit(limit)
        )
        res = await self.async_session.execute(query)
        res = [self._to_entity(m) for m in res.scalars().all()]
        return res