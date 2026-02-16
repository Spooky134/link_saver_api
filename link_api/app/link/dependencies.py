from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db_session
from app.link.repositories import LinkRepository
from app.link.services import LinkService


async def get_link_repository(async_session: AsyncSession = Depends(get_db_session)) -> LinkRepository:
    return LinkRepository(async_session=async_session)


async def get_link_service(link_repository: LinkRepository = Depends(get_link_repository)) -> LinkService:
    return LinkService(link_repository=link_repository)

LinkServiceDep: type[LinkService] = Annotated[LinkService, Depends(get_link_service)]