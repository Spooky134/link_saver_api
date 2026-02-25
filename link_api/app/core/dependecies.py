from typing import AsyncIterator
from app.core.unit_of_work import UnitOfWork


async def get_uow() -> AsyncIterator[UnitOfWork]:
    async with UnitOfWork() as uow:
        yield uow