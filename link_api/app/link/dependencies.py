from typing import Annotated

from fastapi import Depends

from app.core.dependecies import get_uow
from app.core.unit_of_work import UnitOfWork
from app.link.repositories import LinkRepository
from app.link.services import LinkService


async def get_link_repository(uow: UnitOfWork = Depends(get_uow)) -> LinkRepository:
    return LinkRepository(uow.session)


async def get_link_service(
    uow: UnitOfWork = Depends(get_uow),
    link_repository: LinkRepository = Depends(get_link_repository),
) -> LinkService:
    return LinkService(
        uow=uow,
        link_repository=link_repository,
    )


LinkServiceDep: type[LinkService] = Annotated[LinkService, Depends(get_link_service)]
