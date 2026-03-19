from dataclasses import asdict
from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core import logging
from app.core.repositories import BaseRepository
from app.core.types import UNSET
from app.link.entities import CreateLinkEntity, LinkEntity, LinkWithCollectionsEntity, UpdateLinkEntity
from app.link.enums import LinkType
from app.link.mappers import LinkMapper
from app.link.models import LinkModel, link_collection

logger = logging.get_logger(__name__)

class LinkRepository(BaseRepository):
    def __init__(self, db_session: AsyncSession):
        super().__init__(model=LinkModel, db_session=db_session)

    async def add(self, user_id: int, entity: CreateLinkEntity) -> LinkEntity:
        payload = asdict(entity)
        orm_obj = self._model(**payload)

        orm_obj.user_id = user_id

        self._db_session.add(orm_obj)
        await self._db_session.flush()
        await self._db_session.refresh(orm_obj)

        return LinkMapper.to_entity(orm_obj)
    
    async def delete(self, user_id: int, link_id: int) -> bool:
        return await self._delete_by_filters(
            self._model.id == link_id, self._model.user_id == user_id
        )

    async def list(self, user_id: int, offset: int = 0, limit: int = 100) -> List[LinkEntity]:
        orm_objects = await self._list_by_filters(
            self._model.user_id == user_id, offset=offset, limit=limit
        )

        return LinkMapper.to_entities(orm_objects)

    async def update(self, user_id: int, link_id: int, entity: UpdateLinkEntity) -> Optional[LinkEntity]:
        orm_obj = await self._get_by_filters(
            self._model.user_id == user_id,
            self._model.id == link_id,
        )
        if not orm_obj:
            return None
        
        update_data = asdict(entity)
        update_data = {
            key: value for key, value in update_data.items()
            if value is not UNSET
        }

        await self._update(orm_obj, update_data)

        return LinkMapper.to_entity(orm_obj)

    async def get(self, user_id: int, link_id: int) -> Optional[LinkEntity]:
        orm_object = await self._get_by_filters(
            self._model.id == link_id, self._model.user_id == user_id
        )
        if orm_object is None:
            return None
        return LinkMapper.to_entity(orm_object)
    

    async def exists_by_url(self, user_id: int, url: str) -> bool:
        logger.debug(f"Checking existence: url='{url}' for user_id={user_id}")
        return await self._exists_by_filters(
            self._model.url == url, self._model.user_id == user_id
        )
    
    async def get_with_collections(self, user_id: int, link_id: int) -> Optional[LinkWithCollectionsEntity]:
        logger.debug(f"Fetching link with collections: id={link_id}, user_id={user_id}")
        query = (
            select(self._model)
            .where(self._model.id == link_id, self._model.user_id == user_id)
            .options(selectinload(self._model.collections))
        )
        res = await self._db_session.execute(query)
        link = res.scalar_one_or_none()
        if link is None:
            logger.debug(f"Link id={link_id} not found in DB")
            return None
        return LinkMapper.to_entity_with_coll(link)

    async def list_by_collection(self, user_id: int, collection_id: int, offset: int = 0, limit: int = 10) -> List[LinkEntity]:
        logger.debug(
            f"Listing links for collection={collection_id}, user={user_id} "
            f"(offset={offset}, limit={limit})"
        )
        links_query = (
            select(LinkModel)
            .join(link_collection, link_collection.c.link_id == LinkModel.id)
            .where(
                link_collection.c.collection_id == collection_id,
                self._model.user_id == user_id,
            )
            .offset(offset)
            .limit(limit)
        )
        links_res = await self._db_session.execute(links_query)
        orm_links = links_res.scalars().all()
        return [LinkMapper.to_entity(orm) for orm in orm_links]

    async def list_by_type(
        self,
        user_id: int,
        link_type: LinkType = LinkType.WEBSITE,
        offset: int = 0,
        limit: int = 100,
    ) -> List[LinkEntity]:
        logger.debug(f"Listing links by type={link_type.value} for user={user_id}")
        orm_objects = await self._list_by_filters(
            self._model.link_type == link_type.value,
            self._model.user_id == user_id,
            offset=offset,
            limit=limit,
        )

        return LinkMapper.to_entities(orm_objects)
