from datetime import datetime
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.link.enum import LinkType
from app.link.repository import LinkRepository
from app.collection.repository import CollectionRepository
from app.link.model import LinkModel
from app.collection.model import CollectionModel
from app.collection.schema import CollectionCreate, CollectionUpdate, CollectionUpdateBase, CollectionLinkRequest
# from ..exceptions import NotFoundError, ValidationError
from app.exceptions import ValidationError, NotFoundError
from app.collection.entity import CollectionEntity


#TODO оптимизиировать количество методов
class CollectionService:
    def __init__(self, db: AsyncSession):
        self.link_repo = LinkRepository(db)
        self.collection_repo = CollectionRepository(db)

    async def create_collection(self, collection_entity: CollectionEntity,  data: CollectionCreate=None) -> CollectionModel:
        if await self.collection_repo.exists_by_name(name=str(collection_entity.name)):
            raise ValidationError(detail="Collection with this name already exists")

        created_collection = await self.collection_repo.add(collection_entity)

        await self.collection_repo.async_session.commit()
        return created_collection
    

    async def update_collection(self, collection_id: int, data: CollectionUpdateBase, replace=False) -> CollectionModel:
        if not await self.collection_repo.exists_by_id(collection_id):
            raise NotFoundError(detail="Collection not found")

        new_links = []
        if hasattr(data, 'link_ids') and data.link_ids is not None:
            new_links = self.link_repo.get_by_ids(data.link_ids)
            
            if len(new_links) != len(data.link_ids):
                raise NotFoundError(detail="One or more links not found")

        update_data = data.model_dump(exclude_unset=True, exclude={"link_ids"})

        
        collection = await self.collection_repo.update(collection_id=collection_id, data=update_data)

        
        if replace:
            await self.collection_repo.set_links_to_collection(new_links)
        else:
            if new_links: 
                await self.collection_repo.add_links_to_collection(new_links)
        await self.collection_repo.async_session.commit()
        return collection
    
    
    async def get_collection(self, collection_id: int) -> CollectionModel:
        collection = await self.collection_repo.get_by_id_with_links(collection_id)

        if not collection:
            raise NotFoundError(detail="Collection not found")

        return collection
    

    async def get_collections(self) -> list[CollectionModel]:
        collections = await self.collection_repo.get_all_with_links()
        return collections
    

    async def delete_collection(self, collection_id: int) -> None:
        result = await self.collection_repo.delete(collection_id)
        if not result:
            raise NotFoundError(detail="Collection not found")

        await self.collection_repo.async_session.commit()


    async def add_links(self, collection_id: int, data: CollectionLinkRequest) -> list[LinkModel]:
        if not await self.collection_repo.exists_by_id(collection_id):
            raise NotFoundError(detail="Collection not found")

        new_links = await self.link_repo.get_by_ids(data.link_ids)

        if len(new_links) != len(data.link_ids):
            raise NotFoundError(detail="One or more links not found")

        await self.collection_repo.add_links_to_collection(collection_id=collection_id, links=new_links)

        collection = await self.collection_repo.get_by_id_with_links(collection_id=collection_id)

        await self.collection_repo.async_session.commit()
        return collection.links


    async def get_links(self, collection_id: int) -> list[LinkModel]:
        collection = await self.collection_repo.get_by_id_with_links(collection_id)

        if collection is None:
            raise NotFoundError(detail="Collection not found")

        return collection.links
    

    async def remove_link(self, collection_id: int, link_id: int) -> None:
        if not await self.collection_repo.exists_by_id(collection_id):
            raise NotFoundError(detail="Collection not found")

        answer = await self.collection_repo.remove_link_from_collection(collection_id=collection_id, link_id=link_id)

        if not answer:
            raise NotFoundError(detail="Link not found in this collection")

        await self.collection_repo.async_session.commit()
        

    async def links_count(self, collection_id: int) -> dict:
        if not await self.collection_repo.exists_by_id(collection_id):
            raise NotFoundError(detail="Collection not found")

        result = await self.collection_repo.get_count_links(collection_id=collection_id)

        return {"count_links" : result}
    

    async def search_by_name(self, query_string: str):

        return await self.collection_repo.search_by_name(name_query=query_string, limit=30)