from app.core import logging
from app.core.exceptions import NotFoundError, ObjectAlreadyExists
from app.link.entities import (
    CreateLinkEntity,
    LinkEntity,
    LinkWithCollectionsEntity,
    UpdateLinkEntity,
)
from app.link.enums import LinkType
from app.link.repositories import LinkRepository


logger = logging.get_logger(__name__)

class LinkService:
    def __init__(self, link_repository: LinkRepository):
        self.link_repo = link_repository

    async def create_link(self, user_id: int, link_url: str) -> LinkEntity:
        if await self.link_repo.exists_by_url(user_id, link_url):
            logger.info(f"Link creation failed: URL already exists for user_id={user_id}, url={link_url}")
            raise ObjectAlreadyExists("Link with this url already exists")

        create_link_entity = CreateLinkEntity(link_url)
        created_link = await self.link_repo.add(user_id, create_link_entity)

        logger.info(f"Link created: id={created_link.id}, user_id={user_id}")
        return created_link

    async def update_link(
        self, user_id: int, link_id: int, update_link: UpdateLinkEntity
    ) -> LinkEntity:
        updated_link = await self.link_repo.update(user_id, link_id, update_link)
        if updated_link is None:
            logger.warning(f"Update failed: Link not found. id={link_id}, user_id={user_id}")
            raise NotFoundError(detail="Link not found")
        logger.info(f"Link updated: id={link_id}, user_id={user_id}")
        return updated_link

    async def delete_link(self, user_id: int, link_id: int) -> None:
        deleted = await self.link_repo.delete(user_id, link_id)
        if not deleted:
            logger.warning(f"Delete failed: Link not found. id={link_id}, user_id={user_id}")
            raise NotFoundError(detail="Link not found")
        logger.info(f"Link deleted: id={link_id}, user_id={user_id}")

    async def get_link(self, user_id: int, link_id: int) -> LinkWithCollectionsEntity:
        link = await self.link_repo.get_with_collections(user_id, link_id)

        if not link:
            logger.info(f"Link fetch failed: id={link_id} not found for user_id={user_id}")
            raise NotFoundError(detail="Link not found")

        return link

    async def list_links(
        self, user_id: int, skip: int = 0, limit: int = 10
    ) -> list[LinkEntity]:
        logger.debug(f"Listing links for user_id={user_id}, skip={skip}, limit={limit}")
        return await self.link_repo.list(user_id, skip, limit)

    async def list_by_type(
        self, user_id: int, link_type: LinkType, skip: int = 0, limit: int = 10
    ) -> list[LinkEntity]:
        logger.debug(f"Listing links for user_id={user_id}, type={link_type}, skip={skip}, limit={limit}")
        return await self.link_repo.list_by_type(user_id, link_type, skip, limit)
