from datetime import datetime
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.schemas.enums import LinkType
from app.db.repositories.link import LinkRepository
from app.db.repositories.collection import CollectionRepository
from app.db.models.link_model import Link
from app.api.schemas.link import LinkCreate, LinkUpdate
# from ..exceptions import NotFoundError, ValidationError
from app.utils.async_link_parser import AsyncLinkInfoParser, HEADERS
from pydantic import BaseModel, Field, HttpUrl, field_validator
from app.exceptions.exceptions import ValidationError, NotFoundError
from asyncio import to_thread

#TODO оптимизиировать количество методов
class LinkService:
    def __init__(self, db: AsyncSession):
        self.link_repo = LinkRepository(db)
        self.collection_repo = CollectionRepository(db)

    async def create_link(self, link_data: LinkCreate) -> Link:

        if await self.link_repo.exists_by_url(str(link_data.url)):
            raise ValidationError(detail="Link already exists")

        parser = AsyncLinkInfoParser(headers=HEADERS)    
        data = await parser.fetch(str(link_data.url))

        dt = datetime.now()
        new_link = {
            "title": data["title"],
            "description": data["description"],
            "url": str(link_data.url),
            "image": data["image"],
            "link_type": data["link_type"],
            "time_create": dt,
            "time_update": dt
        }

        return await self.link_repo.create(link_data=new_link)
    
    async def update_link(self, link_id: int, data: LinkUpdate) -> Link:
        if not await self.link_repo.exists_by_id(link_id):
            raise NotFoundError(detail="Link not found")
        
        new_collections = None
        if data.collection_ids is not None:
            new_collections = await self.collection_repo.get_by_ids(collection_ids=data.collection_ids)
            
            if len(new_collections) != len(data.collection_ids):
                raise NotFoundError(
                    detail="One or more collections not found"
                )

        update_data = data.model_dump(exclude_unset=True, exclude={"collection_ids"})
        

        link = await self.link_repo.update(link_id=link_id,
                                           data=update_data, 
                                           collections=new_collections if new_collections else None)

        return link
    
    async def delete_link(self, link_id: int):
        if not await self.link_repo.exists_by_id(link_id=link_id):
            raise NotFoundError(status_code=404, detail="Link not found")

        await self.link_repo.delete(link_id=link_id)

    async def get_link(self, link_id: int) -> Link:
        link = await self.link_repo.get(link_id=link_id)

        if not link:
            raise NotFoundError(detail="Link not found")

        return link

    async def get_links(self):
        links = await self.link_repo.get_all()

        return links
    
    async def get_filtered_links(self, type_str: Optional[str] = None) -> list[Link]:
        if type_str:
            try:
                link_type_enum = LinkType(type_str)
            except:
                raise ValidationError(status_code=400,
                                        detail=f"Invalid link_type. Available values: {[e.value for e in LinkType]}")
        else:
            link_type_enum = None


        return await self.link_repo.get_by_type(link_type_enum)