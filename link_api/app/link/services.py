from app.core.exceptions import NotFoundError, ObjectAlreadyExists
from app.core.unit_of_work import UnitOfWork
from app.link.entities import (
    CreateLinkEntity,
    LinkEntity,
    LinkWithCollectionsEntity,
    UpdateLinkEntity,
)
from app.link.enums import LinkType
from app.link.repositories import LinkRepository


class LinkService:
    def __init__(self, uow: UnitOfWork, link_repository: LinkRepository):
        self.uow = uow
        self.link_repo = link_repository

    async def create_link(self, user_id: int, link_url: str) -> LinkEntity:
        if await self.link_repo.exists_by_url(user_id, link_url):
            raise ObjectAlreadyExists("Link with this url already exists")

        create_link_entity = CreateLinkEntity(link_url)
        created_link = await self.link_repo.add(user_id, create_link_entity)

        await self.uow.commit()
        return created_link

    async def update_link(
        self, user_id: int, link_id: int, update_link: UpdateLinkEntity
    ) -> LinkEntity:
        updated_link = await self.link_repo.update(user_id, link_id, update_link)
        if updated_link is None:
            raise NotFoundError(detail="Link not found")
        await self.uow.commit()
        return updated_link

    async def delete_link(self, user_id: int, link_id: int) -> None:
        deleted = await self.link_repo.delete(user_id, link_id)
        if not deleted:
            raise NotFoundError(detail="Link not found")
        await self.uow.commit()

    async def get_link(self, user_id: int, link_id: int) -> LinkWithCollectionsEntity:
        link = await self.link_repo.get_with_collections(user_id, link_id)

        if not link:
            raise NotFoundError(detail="Link not found")

        return link

    async def list_links(
        self, user_id: int, skip: int = 0, limit: int = 10
    ) -> list[LinkEntity]:
        return await self.link_repo.list(user_id, skip, limit)

    async def list_by_type(
        self, user_id: int, link_type: LinkType, skip: int = 0, limit: int = 10
    ) -> list[LinkEntity]:
        return await self.link_repo.list_by_type(user_id, link_type, skip, limit)
