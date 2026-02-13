from typing import Type, TypeVar
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db_session

T = TypeVar('T')

def service_factory(service_class: Type[T]) -> T:
    def _factory(db: AsyncSession = Depends(get_db_session)) -> T:
        return service_class(db)
    return _factory
