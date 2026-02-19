from app.link.entities import LinkEntity
from app.collection.repositories import CollectionRepository
from app.link.models import LinkModel
from app.collection.entities import CollectionEntity
from app.core.exceptions import ValidationError, NotFoundError


class CollectionService:
    def __init__(self, collection_repository: CollectionRepository):
        self.collection_repo = collection_repository

    # TODO состояние гонки при проверке???
    async def create_collection(self, user_id: int, collection_entity: CollectionEntity) -> CollectionEntity:
        if await self.collection_repo.exists_by_name(user_id, collection_entity.name):
            raise ValidationError(detail="Collection with this name already exists")

        created_collection = await self.collection_repo.add(user_id, collection_entity)

        await self.collection_repo.async_session.commit()
        return created_collection

    # TODO состояние гонки при проверке???
    async def update_collection(self, user_id: int, collection_id: int, update_collection: CollectionEntity) -> CollectionEntity:
        if await self.collection_repo.exists_by_name(user_id, update_collection.name):
            raise NotFoundError(detail="Collection with this name already exists")

        updated_collection = await self.collection_repo.update(user_id, collection_id, update_collection)
        if updated_collection is None:
            raise NotFoundError(detail="Collection not found")

        await self.collection_repo.async_session.commit()
        return updated_collection
    
    
    async def get_collection(self, user_id: int, collection_id: int, skip: int=0, limit: int = 10) -> CollectionEntity:
        collection = await self.collection_repo.get_with_links(user_id, collection_id, skip, limit)
        if not collection:
            raise NotFoundError(detail="Collection not found")

        return collection


    async def get_all_collections(self, user_id: int, skip: int = 0, limit: int = 10) -> list[CollectionEntity]:
        return await self.collection_repo.list(user_id, skip, limit)
    

    async def delete_collection(self, user_id: int, collection_id: int) -> None:
        deleted = await self.collection_repo.delete(user_id, collection_id)
        if not deleted:
            raise NotFoundError(detail="Collection not found")

        await self.collection_repo.async_session.commit()


    async def get_links(self, user_id: int, collection_id: int, skip: int = 0, limit: int = 10) -> list[LinkModel]:
        collection = await self.collection_repo.get_with_links(user_id, collection_id, skip, limit)

        if collection is None:
            raise NotFoundError(detail="Collection not found")

        return collection.links


    async def add_links(self, user_id: int, collection_id: int, link_ids: list[int], skip: int = 0, limit: int = 10) -> list[LinkEntity]:
        await self.collection_repo.add_links(user_id, collection_id, link_ids)

        collection = await self.collection_repo.get_with_links(user_id, collection_id, skip, limit)

        if collection is None:
            raise NotFoundError(detail="Collection not found")

        await self.collection_repo.async_session.commit()

        return collection.links
    

    async def remove_links(self, user_id: int, collection_id: int, link_ids: list[int]) -> None:
        collection = await self.collection_repo.get(user_id, collection_id)

        if collection is None:
            raise NotFoundError(detail="Collection not found")

        await self.collection_repo.remove_links(user_id, collection_id, link_ids)

        await self.collection_repo.async_session.commit()


    async def get_links_count(self, user_id: int, collection_id: int) -> int:
        count = await self.collection_repo.count_links(user_id, collection_id)
        if count is None:
            raise NotFoundError(detail="Collection not found")

        return count


    async def search_by_name(
            self,
            user_id: int,
            query_string: str,
            skip: int = 0, limit:
            int = 10
    ) -> list[CollectionEntity]:
        return await self.collection_repo.search_by_name(user_id, query_string, skip, limit)