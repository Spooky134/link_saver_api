from dataclasses import asdict
from datetime import datetime
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import exists, func, select, update, delete
from sqlalchemy.orm import selectinload

# from app.link.entity import LinkEntity
from app.link.model import LinkModel
from app.link.enum import LinkType
from app.collection.model import CollectionModel
from app.common.model import link_collection
from app.base.repository import BaseRepository
from app.collection.entity import CollectionEntity


class CollectionRepository(BaseRepository[CollectionModel, CollectionEntity]):
    def __init__(self, async_session: AsyncSession):
        super().__init__(
            model=CollectionModel,
            entity=CollectionEntity,
            async_session=async_session
        )

    async def get_by_id_with_links(self, collection_id: int) -> Optional[CollectionEntity]:
        query = (
            select(self.model)
            .options(selectinload(self.model.links))
            .where(self.model.id == collection_id)
        )
        res = await self.async_session.execute(query)
        return self._to_entity(res.scalar_one_or_none())

    async def get_all_with_links(self, skip: int = 0, limit: int = 100) -> list[CollectionEntity]:
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
        query = select(exists().where(self.model.name == name))
        result = await self.async_session.execute(query)
        return result.scalar() or False

    # TODO подумать еще
    async def update(self, collection_id: int, collection_entity: CollectionEntity) -> Optional[CollectionEntity]:
        excluded_fields = {"id", "created_at", "updated_at", "user_id", "links"}
        collection = self.async_session.get(self.model, collection_id)
        if collection:
            update_data = asdict(collection_entity)
            for key, value in update_data.items():
                if key not in excluded_fields and hasattr(collection, key) and value is not None:
                    setattr(collection, key, value)

        await self.async_session.flush()
        return self._to_entity(collection)

    # TODO to_model принимает не тот тип
    async def set_links_to_collection(self, collection_id: int, link_entities: list["LinkEntity"]) -> None:
        query = (
            select(self.model)
            .options(selectinload(self.model.links))
            .where(self.model.id == collection_id)
        )
        res = await self.async_session.execute(query)
        collection = res.scalar_one_or_none()
        collection.links = [self._to_model(e) for e in link_entities]
        await self.async_session.flush()

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

    async def search_by_name(self, name_query: str, limit: int = 20) -> list[CollectionEntity]:
        query = (
            select(self.model)
            .options(selectinload(self.model.links))
            .where(self.model.name.ilike(f"%{name_query}%"))
            .limit(limit)
        )
        res = await self.async_session.execute(query)
        res = [self._to_entity(m) for m in res.scalars().all()]
        return res