from dataclasses import asdict, is_dataclass
from typing import Optional, List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import exists, func, select, delete
from sqlalchemy.orm import selectinload

from app.core.constants import UNSET
from app.link.models import LinkModel, link_collection
from app.collection.models import CollectionModel
from app.core.repositories import BaseRepository
from app.collection.entities import CollectionEntity, CreateCollectionEntity, UpdateCollectionEntity
from app.common.mappers import EntityMapper


class CollectionRepository(BaseRepository[CollectionModel, CollectionEntity]):
    def __init__(self, async_session: AsyncSession):
        super().__init__(
            model=CollectionModel,
            entity=CollectionEntity,
            async_session=async_session
        )

    def _to_entity(self, collection_model: CollectionModel) -> CollectionEntity:
        return EntityMapper.to_collection_with_links(collection_model)

    def _to_model(self, collection_entity: CollectionEntity) -> CollectionModel:
        if is_dataclass(collection_entity):
            payload = asdict(collection_entity)
        else:
            payload = collection_entity.__dict__.copy()

        payload = {k: v for k, v in payload.items() if v is not UNSET}

        return self.model(**payload)

    async def get(self, user_id: int, collection_id: int) -> Optional[CollectionEntity]:
        query = (
            select(self.model)
            .where(self.model.id == collection_id, self.model.user_id == user_id)
        )
        result = await self.async_session.execute(query)
        orm_obj = result.scalar_one_or_none()
        if orm_obj is None:
            return None
        return self._to_entity(orm_obj)

    async def get_with_links(
            self,
            user_id: int,
            collection_id: int,
            skip: int = 0,
            limit: int = 10
    ) -> Optional[CollectionEntity]:

        query = (
            select(self.model)
            .where(self.model.id == collection_id, self.model.user_id == user_id)
        )
        res = await self.async_session.execute(query)
        collection = res.scalar_one_or_none()

        if collection is None:
            return None

        links_query = (
            select(LinkModel)
            .join(link_collection, link_collection.c.link_id == LinkModel.id)
            .where(link_collection.c.collection_id == collection_id, self.model.user_id == user_id)
            .offset(skip)
            .limit(limit)
        )
        links_res = await self.async_session.execute(links_query)
        links = links_res.scalars().all()

        collection.links = links

        return self._to_entity(collection)

    async def add(self, user_id: int, collection_entity: CreateCollectionEntity) -> CollectionEntity:
        instance = self._to_model(collection_entity)

        instance.user_id = user_id

        self.async_session.add(instance)
        await self.async_session.flush()
        await self.async_session.refresh(instance)

        return self._to_entity(instance)

    async def count_links(self, user_id: int, collection_id: int) -> Optional[int]:
        query = (
            select(func.count(LinkModel.id))
            .select_from(self.model)
            .outerjoin(self.model.links)
            .where(self.model.id == collection_id, self.model.user_id == user_id)
            .group_by(self.model.id)
        )
        result = await self.async_session.execute(query)
        return result.scalar_one_or_none()

    async def exists_by_name(self, user_id: int,  name: str) -> bool:
        query = (
            select(exists().where(self.model.name == name, self.model.user_id == user_id))
        )
        res = await self.async_session.execute(query)
        return res.scalar() or False

    async def update(self, user_id: int, collection_id: int, collection_entity: UpdateCollectionEntity) -> Optional[CollectionEntity]:
        query = (
            select(self.model)
            .where(self.model.id == collection_id, self.model.user_id == user_id)
        )
        res = await self.async_session.execute(query)
        orm_obj = res.scalar_one_or_none()
        if not orm_obj:
            return None

        update_data = asdict(collection_entity)
        for key, value in update_data.items():
            if value is not UNSET and hasattr(orm_obj, key):
                setattr(orm_obj, key, value)

        await self.async_session.flush()
        await self.async_session.refresh(orm_obj)

        return self._to_entity(orm_obj)

    async def add_links(self, user_id: int, collection_id, link_ids: list[int]) -> None:
        if not link_ids:
            return

        query = (
            select(self.model)
            .options(selectinload(self.model.links))
            .where(self.model.id == collection_id, self.model.user_id == user_id)
        )
        res = await self.async_session.execute(query)
        collection = res.scalar_one_or_none()

        if collection is None:
            return

        link_query = (
            select(LinkModel)
            .where(LinkModel.id.in_(link_ids), self.model.user_id == user_id)
        )
        links_res = await self.async_session.execute(link_query)
        links_to_add = links_res.scalars().all()

        existing_ids = {link.id for link in collection.links}

        for link in links_to_add:
            if link.id not in existing_ids:
                collection.links.append(link)

        await self.async_session.flush()

    async def list(self, user_id: int, offset: int = 0, limit: int = 100) -> List[CollectionEntity]:
        query = (
            select(self.model)
            .where(self.model.user_id == user_id)
            .offset(offset)
            .limit(limit)
        )
        res = await self.async_session.execute(query)
        entities = [self._to_entity(m) for m in res.scalars().all()]
        return entities

    async def delete(self, user_id: int, collection_id: int) -> bool:
        stmt = (
            delete(self.model)
            .where(self.model.id == collection_id, self.model.user_id == user_id)
        )
        res = await self.async_session.execute(stmt)
        await self.async_session.flush()
        return res.rowcount > 0

    async def remove_links(self, user_id: int, collection_id: int, link_ids: List[int]) -> None:
        if not link_ids:
            return

        query = (
            select(self.model)
            .options(selectinload(self.model.links))
            .where(self.model.id == collection_id, self.model.user_id == user_id)
        )
        res = await self.async_session.execute(query)
        collection = res.scalar_one_or_none()

        if collection is None:
            return

        links_to_remove_ids = set(link_ids)

        collection.links = [
            link for link in collection.links if link.id not in links_to_remove_ids
        ]

        await self.async_session.flush()

    async def search_by_name(self, user_id: int, name_query: str, skip: int = 0, limit: int = 10) -> List[CollectionEntity]:
        query = (
            select(self.model)
            # .options(selectinload(self.model.links))
            .where(self.model.name.ilike(f"%{name_query}%"), self.model.user_id == user_id)
            .offset(skip)
            .limit(limit)
        )
        res = await self.async_session.execute(query)
        entities = [self._to_entity(m) for m in res.scalars().all()]
        return entities