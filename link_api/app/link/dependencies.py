from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db_session
from app.link.repositories import LinkRepository
from app.link.services import LinkService
from app.link.utils.async_link_parser import AsyncLinkInfoParser, HEADERS


async def get_link_repository(async_session: AsyncSession = Depends(get_db_session)) -> LinkRepository:
    return LinkRepository(async_session=async_session)

async def get_link_parser():
    return AsyncLinkInfoParser(headers=HEADERS)

async def get_link_service(
        link_repository: LinkRepository = Depends(get_link_repository),
        link_parser: AsyncLinkInfoParser = Depends(get_link_parser)
) -> LinkService:
    return LinkService(
        link_repository=link_repository,
        link_parser=link_parser,
    )

LinkServiceDep: type[LinkService] = Annotated[LinkService, Depends(get_link_service)]