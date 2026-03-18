from typing import Annotated

from fastapi import Depends

from app.collection.repositories import CollectionRepository
from app.collection.services import CollectionService
from app.core.dependecies import get_uow
from app.core.unit_of_work import UnitOfWork
from app.link.repositories import LinkRepository


async def get_collection_service(uow: UnitOfWork = Depends(get_uow)) -> CollectionService:
    collection_repo = CollectionRepository(uow.session)
    link_repo = LinkRepository(uow.session)
    return CollectionService(
        collection_repository=collection_repo,
        link_repository=link_repo
    )


CollectionServiceDep = Annotated[CollectionService, Depends(get_collection_service)]
