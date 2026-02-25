from typing import List

from app.core.unit_of_work import UnitOfWork
from app.link.entities import LinkEntity
from app.collection.repositories import CollectionRepository
from app.collection.entities import CollectionEntity, CreateCollectionEntity, UpdateCollectionEntity
from app.core.exceptions import ValidationError, NotFoundError
from app.link.repositories import LinkRepository


class CollectionService:
    def __init__(self, uow: UnitOfWork, collection_repository: CollectionRepository, link_repository: LinkRepository):
        self.uow = uow
        self.collection_repo = collection_repository
        self.link_repo = link_repository

    async def create_collection(self, user_id: int, collection_entity: CreateCollectionEntity) -> CollectionEntity:
        if await self.collection_repo.exists_by_name(user_id, collection_entity.name):
            raise ValidationError(detail="Collection with this name already exists")

        created_collection = await self.collection_repo.add(user_id, collection_entity)
        await self.uow.commit()
        return created_collection


    async def update_collection(self, user_id: int, collection_id: int, update_collection: UpdateCollectionEntity) -> CollectionEntity:
        if await self.collection_repo.exists_by_name(user_id, update_collection.name):
            raise NotFoundError(detail="Collection with this name already exists")

        updated_collection = await self.collection_repo.update(user_id, collection_id, update_collection)
        if updated_collection is None:
            raise NotFoundError(detail="Collection not found")
        await self.uow.commit()
        return updated_collection


    async def get_collection(self, user_id: int, collection_id: int) -> CollectionEntity:
        collection = await self.collection_repo.get(user_id, collection_id)
        if not collection:
            raise NotFoundError(detail="Collection not found")

        return collection


    async def list_collections(self, user_id: int, skip: int = 0, limit: int = 10) -> List[CollectionEntity]:
        return await self.collection_repo.list(user_id, skip, limit)
    

    async def delete_collection(self, user_id: int, collection_id: int) -> None:
        deleted = await self.collection_repo.delete(user_id, collection_id)
        if not deleted:
            raise NotFoundError(detail="Collection not found")
        await self.uow.commit()



    async def list_links(self, user_id: int, collection_id: int, skip: int = 0, limit: int = 10) -> List[LinkEntity]:
        exists = await self.collection_repo.exists(user_id, collection_id)

        if not exists:
            raise NotFoundError(detail="Collection not found")

        links = await self.link_repo.list_by_collection(user_id, collection_id, skip, limit)

        return links


    async def attach_links(self, user_id: int, collection_id: int, link_ids: List[int]) -> None:
        exists = await self.collection_repo.exists(user_id, collection_id)

        if not exists:
            raise NotFoundError(detail="Collection not found")

        await self.collection_repo.add_links(user_id, collection_id, link_ids)
        await self.uow.commit()


    async def remove_links(self, user_id: int, collection_id: int, link_ids: List[int]) -> None:
        exists = await self.collection_repo.exists(user_id, collection_id)

        if not exists:
            raise NotFoundError(detail="Collection not found")

        await self.collection_repo.remove_links(user_id, collection_id, link_ids)
        await self.uow.commit()


    async def links_count(self, user_id: int, collection_id: int) -> int:
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
    ) -> List[CollectionEntity]:
        return await self.collection_repo.search_by_name(user_id, query_string, skip, limit)