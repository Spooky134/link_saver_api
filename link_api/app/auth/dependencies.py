
from fastapi import Depends

from typing import Annotated
from app.auth.services import AuthService
from fastapi import Request
from app.auth.exceptions import MissingToken, UserNotPresent
from app.auth.utils import validate_token
from app.core.unit_of_work import UnitOfWork
from app.user.dependencies import get_user_repository
from app.user.entities import UserEntity
from app.user.repositories import UserRepository
from app.core.dependecies import get_uow


def get_access_token(request: Request) -> str:
    token = request.cookies.get("access_token")
    if not token:
        raise MissingToken()
    return token


async def get_current_user(
        token: str = Depends(get_access_token),
        user_repository: UserRepository = Depends(get_user_repository)
) -> UserEntity:

    user_id = validate_token(token)

    user = await user_repository.get(user_id)
    if not user:
        raise UserNotPresent()
    return user


async def get_auth_service(
        uow: UnitOfWork = Depends(get_uow),
        user_repository: UserRepository = Depends(get_user_repository)
) -> AuthService:
    return AuthService(
        uow=uow,
        user_repository=user_repository
    )


AuthServiceDep: type[AuthService] = Annotated[AuthService, Depends(get_auth_service)]

CurrentUserDep: type[UserEntity] = Annotated[UserEntity, Depends(get_current_user)]