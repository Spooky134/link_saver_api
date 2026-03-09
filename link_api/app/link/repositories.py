from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core import logging
from app.core.repositories import OwnedEntityRepository
from app.link.entities import LinkEntity, LinkWithCollectionsEntity
from app.link.enums import LinkType
from app.link.mappers import EntityMapper, LinkMapper
from app.link.models import LinkModel, link_collection

logger = logging.get_logger(__name__)

class LinkRepository(OwnedEntityRepository[LinkModel, LinkEntity]):
    def __init__(self, async_session: AsyncSession):
        super().__init__(model=LinkModel, async_session=async_session)

    def _to_entity(self, orm_obj: LinkModel) -> LinkEntity:
        return LinkMapper.to_link(orm_obj)

    async def exists_by_url(self, user_id: int, url: str) -> bool:
        logger.debug(f"Checking existence: url='{url}' for user_id={user_id}")
        return await self._exists_by_filters(
            self.model.url == url, self.model.user_id == user_id
        )

    async def get_with_collections(
        self, user_id: int, link_id: int
    ) -> Optional[LinkWithCollectionsEntity]:
        logger.debug(f"Fetching link with collections: id={link_id}, user_id={user_id}")
        query = (
            select(self.model)
            .where(self.model.id == link_id, self.model.user_id == user_id)
            .options(selectinload(self.model.collections))
        )
        res = await self._async_session.execute(query)
        link = res.scalar_one_or_none()
        if link is None:
            logger.debug(f"Link id={link_id} not found in DB")
            return None
        return EntityMapper.to_link_with_collections(link)

    async def list_by_collection(
        self, user_id: int, collection_id: int, offset: int = 0, limit: int = 10
    ) -> List[LinkEntity]:
        logger.debug(
            f"Listing links for collection={collection_id}, user={user_id} "
            f"(offset={offset}, limit={limit})"
        )
        links_query = (
            select(LinkModel)
            .join(link_collection, link_collection.c.link_id == LinkModel.id)
            .where(
                link_collection.c.collection_id == collection_id,
                self.model.user_id == user_id,
            )
            .offset(offset)
            .limit(limit)
        )
        links_res = await self._async_session.execute(links_query)

        return self._to_entities(links_res.scalars().all())

    async def list_by_type(
        self,
        user_id: int,
        link_type: LinkType = LinkType.WEBSITE,
        offset: int = 0,
        limit: int = 100,
    ) -> List[LinkEntity]:
        logger.debug(f"Listing links by type={link_type.value} for user={user_id}")
        orm_objects = await self._list_by_filters(
            self.model.link_type == link_type.value,
            self.model.user_id == user_id,
            offset=offset,
            limit=limit,
        )

        return self._to_entities(orm_objects)
