from app.link.repositories import LinkRepository
from app.collection.repositories import CollectionRepository
from app.link.models import LinkModel
from app.collection.schemas import CollectionLinkRequest
from app.collection.entities import CollectionEntity
from app.core.exceptions import ValidationError, NotFoundError


class CollectionService:
    def __init__(self, collection_repository: CollectionRepository, link_repository: LinkRepository):
        self.collection_repo = collection_repository
        self.link_repo = link_repository

    # TODO состояние гонки при проверке???
    async def create_collection(self, collection_entity: CollectionEntity) -> CollectionEntity:
        if await self.collection_repo.exists_by_name(name=str(collection_entity.name)):
            raise ValidationError(detail="Collection with this name already exists")

        created_collection = await self.collection_repo.add(collection_entity)

        await self.collection_repo.async_session.commit()
        return created_collection

    # TODO состояние гонки при проверке???
    async def update_collection(self, collection_id: int, update_collection: CollectionEntity) -> CollectionEntity:
        if await self.collection_repo.exists_by_name(update_collection.name):
            raise NotFoundError(detail="Collection with this name already exists")

        updated_collection = await self.collection_repo.update(collection_id, update_collection)
        if updated_collection is None:
            raise NotFoundError(detail="Collection not found")

        await self.collection_repo.async_session.commit()
        return updated_collection
    
    
    async def get_collection(self, collection_id: int) -> CollectionEntity:
        collection = await self.collection_repo.get_by_id_with_links(collection_id)
        if not collection:
            raise NotFoundError(detail="Collection not found")

        return collection


    async def get_all_collections(self, skip: int = 0, limit: int = 10) -> list[CollectionEntity]:
        return await self.collection_repo.get_all_with_links(skip, limit)
    

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

        answer = await self.collection_repo.remove_link_from_collection(collection_id, link_id)

        if not answer:
            raise NotFoundError(detail="Link not found in this collection")

        await self.collection_repo.async_session.commit()
        
    # TODO нормальный ответ придумать
    async def links_count(self, collection_id: int) -> dict:
        if not await self.collection_repo.exists_by_id(collection_id):
            raise NotFoundError(detail="Collection not found")

        result = await self.collection_repo.get_count_links(collection_id=collection_id)

        return {"count_links" : result}
    

    async def search_by_name(self, query_string: str, skip: int = 0, limit: int = 10) -> list[CollectionEntity]:
        return await self.collection_repo.search_by_name(query_string, skip, limit)