from app.link.entities import LinkEntity, UpdateLinkEntity, LinkWithCollectionsEntity
from app.link.enums import LinkType
from app.link.repositories import LinkRepository
from app.link.utils.async_link_parser import AsyncLinkInfoParser
from app.core.exceptions import ValidationError, NotFoundError


class LinkService:
    def __init__(self, link_repository: LinkRepository, link_parser: AsyncLinkInfoParser):
        self.link_repo = link_repository
        self.link_parser = link_parser

    #TODO добавлять ссылку в бд сразу а парсить в фоне!!!!
    async def create_link(self, user_id: int, link_url: str) -> LinkEntity:
        if await self.link_repo.exists_by_url(user_id, link_url):
            raise ValidationError(detail="Link already exists")

        create_link_entity = await self.link_parser.fetch(link_url)

        created_link = await self.link_repo.add(user_id, create_link_entity)
        await self.link_repo.async_session.commit()
        return created_link
    
    async def update_link(self, user_id: int, link_id: int, update_link: UpdateLinkEntity) -> LinkEntity:
        updated_link = await self.link_repo.update(user_id, link_id, update_link)
        if updated_link is None:
            raise NotFoundError(detail="Link not found")

        await self.link_repo.async_session.commit()
        return updated_link
    
    async def delete_link(self, user_id: int, link_id: int) -> None:
        deleted = await self.link_repo.delete(user_id, link_id)
        if not deleted:
            raise NotFoundError(detail="Link not found")

        await self.link_repo.async_session.commit()

    async def get_link(self, user_id: int, link_id: int) -> LinkWithCollectionsEntity:
        link = await self.link_repo.get_with_collections(user_id, link_id)

        if not link:
            raise NotFoundError(detail="Link not found")

        return link

    async def list_links(self, user_id: int, skip: int = 0, limit: int = 10) -> list[LinkEntity]:
        return await self.link_repo.list(user_id, skip, limit)
    
    async def list_by_type(self, user_id: int, link_type: LinkType, skip: int = 0, limit: int = 10) -> list[LinkEntity]:
        return await self.link_repo.list_by_type(user_id, link_type, skip, limit)