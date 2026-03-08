from typing import Optional, List, Set

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select
from sqlalchemy.orm import selectinload

from app.link.models import LinkModel
from app.collection.models import CollectionModel
from app.core.repositories import OwnedEntityRepository
from app.collection.entities import CollectionEntity
from app.collection.mappers import CollectionMapper


class CollectionRepository(OwnedEntityRepository[CollectionModel, CollectionEntity]):
    def __init__(self, async_session: AsyncSession):
        super().__init__(
            model=CollectionModel,
            async_session=async_session
        )

    def _to_entity(self, orm_obj: CollectionModel) -> CollectionEntity:
        return CollectionMapper.to_collection(orm_obj)

    async def search_by_name(self, user_id: int, name_query: str, offset: int = 0, limit: int = 100) -> List[CollectionEntity]:
        orm_objects = await self._list_by_filters(
            self.model.name.ilike(f"%{name_query}%"),
            self.model.user_id == user_id,
            offset=offset,
            limit=limit
        )

        return self._to_entities(orm_objects)

    async def exists_by_name(self, user_id: int,  name: str) -> bool:
        return await self._exists_by_filters(
            self.model.name == name,
            self.model.user_id == user_id
        )

    async def exists(self, user_id: int, collection_id: int) -> bool:
        return await self._exists_by_filters(
            self.model.user_id == user_id,
            self.model.id == collection_id
        )


    async def add_links(self, user_id: int, collection_id: int, link_ids: Set[int]) -> None:
        if not link_ids:
            return

        query = (
            select(self.model)
            .options(selectinload(self.model.links))
            .where(self.model.id == collection_id, self.model.user_id == user_id)
        )
        res = await self._async_session.execute(query)
        collection = res.scalar_one_or_none()

        if collection is None:
            return

        link_query = (
            select(LinkModel)
            .where(
                LinkModel.id.in_(link_ids),
                LinkModel.user_id == user_id
            )
        )
        links_res = await self._async_session.execute(link_query)
        links_to_add = links_res.scalars().all()

        existing_ids = {link.id for link in collection.links}

        for link in links_to_add:
            if link.id not in existing_ids:
                collection.links.append(link)

        await self._async_session.flush()

    async def remove_links(self, user_id: int, collection_id: int, link_ids: Set[int]) -> None:
        if not link_ids:
            return

        query = (
            select(self.model)
            .options(selectinload(self.model.links))
            .where(self.model.id == collection_id, self.model.user_id == user_id)
        )
        res = await self._async_session.execute(query)
        collection = res.scalar_one_or_none()

        if collection is None:
            return

        collection.links = [
            link for link in collection.links if link.id not in link_ids
        ]

        await self._async_session.flush()

    async def count_links(self, user_id: int, collection_id: int) -> Optional[int]:
        query = (
            select(func.count(LinkModel.id))
            .select_from(self.model)
            .outerjoin(self.model.links)
            .where(self.model.id == collection_id, self.model.user_id == user_id)
            .group_by(self.model.id)
        )
        result = await self._async_session.execute(query)
        return result.scalar_one_or_none()