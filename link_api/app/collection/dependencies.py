from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db_session
from app.collection.repositories import CollectionRepository
from app.collection.services import CollectionService


async def get_collection_repository(
        async_session: AsyncSession = Depends(get_db_session)
) -> CollectionRepository:
    return CollectionRepository(async_session)

async def get_collection_service(
        collection_repository: CollectionRepository = Depends(get_collection_repository),
) -> CollectionService:
    return CollectionService(
        collection_repository=collection_repository
    )

CollectionServiceDep: type[CollectionService] = Annotated[CollectionService, Depends(get_collection_service)]