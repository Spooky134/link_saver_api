from dataclasses import asdict
from typing import List, Optional, Set

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.collection.entities import CollectionEntity, CreateCollectionEntity, UpdateCollectionEntity
from app.collection.mappers import CollectionMapper
from app.collection.models import CollectionModel
from app.core.repositories import BaseRepository
from app.core.types import UNSET
from app.link.models import LinkModel


class CollectionRepository(BaseRepository):
    def __init__(self, db_session: AsyncSession):
        super().__init__(model=CollectionModel, db_session=db_session)


    async def add(self, user_id: int, entity: CreateCollectionEntity) -> CollectionEntity:
        payload = asdict(entity)
        orm_obj = self._model(**payload)

        orm_obj.user_id = user_id

        self._db_session.add(orm_obj)
        await self._db_session.flush()
        await self._db_session.refresh(orm_obj)

        return CollectionMapper.to_entity(orm_obj)


    async def delete(self, user_id: int, collection_id: int) -> bool:
        return await self._delete_by_filters(
            self._model.id == collection_id, self._model.user_id == user_id
        )


    async def list(self, user_id: int, offset: int = 0, limit: int = 100) -> List[CollectionEntity]:
        orm_objects = await self._list_by_filters(
            self._model.user_id == user_id, offset=offset, limit=limit
        )

        return CollectionMapper.to_entities(orm_objects)


    async def update(self, user_id: int, collection_id: int, entity: UpdateCollectionEntity) -> Optional[CollectionEntity]:
        orm_obj = await self._get_by_filters(
            self._model.user_id == user_id,
            self._model.id == collection_id,
        )
        if not orm_obj:
            return None
        
        update_data = asdict(entity)
        update_data = {
            key: value for key, value in update_data.items()
            if value is not UNSET
        }

        await self._update(orm_obj, update_data)
        return CollectionMapper.to_entity(orm_obj)


    async def get(self, user_id: int, collection_id: int) -> Optional[CollectionEntity]:
        orm_object = await self._get_by_filters(
            self._model.id == collection_id, self._model.user_id == user_id
        )
        if orm_object is None:
            return None
        return CollectionMapper.to_entity(orm_object)


    async def search_by_name(self, user_id: int, name_query: str, offset: int = 0, limit: int = 100) -> List[CollectionEntity]:
        orm_objects = await self._list_by_filters(
            self._model.name.ilike(f"%{name_query}%"),
            self._model.user_id == user_id,
            offset=offset,
            limit=limit,
        )

        return CollectionMapper.to_entities(orm_objects)


    async def exists_by_name(self, user_id: int, name: str) -> bool:
        return await self._exists_by_filters(
            self._model.name == name, self._model.user_id == user_id
        )


    async def exists(self, user_id: int, collection_id: int) -> bool:
        return await self._exists_by_filters(
            self._model.user_id == user_id, self._model.id == collection_id
        )


    async def attach_links(self, user_id: int, collection_id: int, link_ids: List[int]) -> None:
        if not link_ids:
            return

        query = (
            select(self._model)
            .options(selectinload(self._model.links))
            .where(self._model.id == collection_id, self._model.user_id == user_id)
        )
        res = await self._db_session.execute(query)
        collection = res.scalar_one_or_none()

        if collection is None:
            return

        link_query = select(LinkModel).where(
            LinkModel.id.in_(link_ids), LinkModel.user_id == user_id
        )
        links_res = await self._db_session.execute(link_query)
        links_to_add = links_res.scalars().all()

        existing_ids = {link.id for link in collection.links}

        new_links = [link for link in links_to_add if link.id not in existing_ids]
        collection.links.extend(new_links)

        await self._db_session.flush()


    async def remove_links(self, user_id: int, collection_id: int, link_ids: List[int]) -> None:
        if not link_ids:
            return

        query = (
            select(self._model)
            .options(selectinload(self._model.links))
            .where(self._model.id == collection_id, self._model.user_id == user_id)
        )
        res = await self._db_session.execute(query)
        collection = res.scalar_one_or_none()

        if collection is None:
            return

        collection.links = [
            link for link in collection.links if link.id not in link_ids
        ]

        await self._db_session.flush()


    async def count_links(self, user_id: int, collection_id: int) -> Optional[int]:
        query = (
            select(func.count(LinkModel.id))
            .select_from(self._model)
            .outerjoin(self._model.links)
            .where(self._model.id == collection_id, self._model.user_id == user_id)
            .group_by(self._model.id)
        )
        result = await self._db_session.execute(query)
        return result.scalar_one_or_none()
