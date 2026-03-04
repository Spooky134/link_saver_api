from typing import AsyncIterator, Annotated

from fastapi.params import Depends, Query
from pydantic.v1 import BaseModel

from app.core.unit_of_work import UnitOfWork


async def get_uow() -> AsyncIterator[UnitOfWork]:
    async with UnitOfWork() as uow:
        yield uow


class Pagination(BaseModel):
    skip: int
    limit: int

async def get_pagination_params(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
) -> Pagination:
    return Pagination(skip=skip, limit=limit)


PaginationDep: type[Pagination] = Annotated[Pagination, Depends(get_pagination_params)]