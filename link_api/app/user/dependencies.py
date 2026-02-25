from fastapi import Depends
from app.core.dependecies import get_uow
from app.core.unit_of_work import UnitOfWork
from app.user.repositories import UserRepository


async def get_user_repository(uow: UnitOfWork = Depends(get_uow)) -> UserRepository:
    return UserRepository(uow.session)