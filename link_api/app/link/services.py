from sqlalchemy.ext.asyncio import AsyncSession
from app.link.entities import LinkEntity
from app.link.enums import LinkType
from app.link.repositories import LinkRepository
from app.link.utils.async_link_parser import AsyncLinkInfoParser, HEADERS
from app.core.exceptions import ValidationError, NotFoundError


class LinkService:
    def __init__(self, link_repository: LinkRepository):
        self.link_repo = link_repository

    #TODO добавлять ссылку в бд сразу а парсить в фоне!!!!
    async def create_link(self, link_data: LinkEntity) -> LinkEntity:
        if await self.link_repo.exists_by_url(str(link_data.url)):
            raise ValidationError(detail="Link already exists")

        parser = AsyncLinkInfoParser(headers=HEADERS)    
        full_link_data = await parser.fetch(str(link_data.url))

        link = await self.link_repo.add(full_link_data)
        await self.link_repo.async_session.commit()
        return link
    
    async def update_link(self, link_id: int, update_link: LinkEntity) -> LinkEntity:
        updated_link = await self.link_repo.update(link_id, update_link)
        if updated_link is None:
            raise NotFoundError(detail="Link not found")

        await self.link_repo.async_session.commit()
        return updated_link
    
    async def delete_link(self, link_id: int) -> None:
        result = await self.link_repo.delete(link_id)
        if not result:
            raise NotFoundError(detail="Link not found")

        await self.link_repo.async_session.commit()

    async def get_link(self, link_id: int) -> LinkEntity:
        link = await self.link_repo.get_by_id_with_collections(link_id)

        if not link:
            raise NotFoundError(detail="Link not found")

        return link

    async def get_all_links(self, skip: int = 0, limit: int = 10) -> list[LinkEntity]:
        return await self.link_repo.get_all_with_collections(skip, limit)
    
    async def get_links_by_type(self, link_type: LinkType, skip: int = 0, limit: int = 10) -> list[LinkEntity]:
        return await self.link_repo.get_all_by_type(link_type, skip, limit)