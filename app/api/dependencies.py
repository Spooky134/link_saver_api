from typing import Type, TypeVar
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.config.database import get_db

T = TypeVar('T')

def service_factory(service_class: Type[T]) -> T:
    def _factory(db: AsyncSession = Depends(get_db)) -> T:
        return service_class(db)
    return _factory

# from app.services.link_service import LinkService

# def service_factory(service_class: type[LinkService]) -> LinkService:
#     async def _factory(db: AsyncSession = Depends(get_db)) -> LinkService:
#         return service_class(db)
#     return _factory