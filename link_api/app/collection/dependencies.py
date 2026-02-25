from typing import Annotated
from fastapi import Depends
from app.collection.repositories import CollectionRepository
from app.collection.services import CollectionService
from app.core.unit_of_work import UnitOfWork
from app.link.dependencies import get_link_repository
from app.link.repositories import LinkRepository
from app.core.dependecies import get_uow


async def get_collection_repository(uow: UnitOfWork=Depends(get_uow)
) -> CollectionRepository:
    return CollectionRepository(uow.session)

async def get_collection_service(
        uow: UnitOfWork=Depends(get_uow),
        collection_repository: CollectionRepository = Depends(get_collection_repository),
        link_repository: LinkRepository = Depends(get_link_repository)
) -> CollectionService:
    return CollectionService(
        uow=uow,
        collection_repository=collection_repository,
        link_repository=link_repository
    )

CollectionServiceDep: type[CollectionService] = Annotated[CollectionService, Depends(get_collection_service)]