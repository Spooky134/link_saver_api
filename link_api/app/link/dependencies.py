from typing import Annotated

from fastapi import Depends

from app.core.dependecies import get_uow
from app.core.unit_of_work import UnitOfWork
from app.link.repositories import LinkRepository
from app.link.services import LinkService


async def get_link_service(uow: UnitOfWork = Depends(get_uow)) -> LinkService:
    link_repo = LinkRepository(uow.session)
    return LinkService(link_repo)

LinkServiceDep = Annotated[LinkService, Depends(get_link_service)]
