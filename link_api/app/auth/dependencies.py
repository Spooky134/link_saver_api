from typing import Annotated

from fastapi import Depends, Request

from app.auth.exceptions import MissingToken, UserNotPresent
from app.auth.services import AuthService
from app.auth.utils import validate_token
from app.core.dependecies import get_uow
from app.core.unit_of_work import UnitOfWork
from app.user.dependencies import get_user_repository
from app.user.entities import UserEntity
from app.user.repositories import UserRepository


def get_access_token(request: Request) -> str:
    token = request.cookies.get("access_token")
    if not token:
        raise MissingToken()
    return token


async def get_current_user(
    token: str = Depends(get_access_token),
    user_repository: UserRepository = Depends(get_user_repository),
) -> UserEntity:

    user_id = validate_token(token)

    user = await user_repository.get(user_id)
    if not user:
        raise UserNotPresent()
    return user


async def get_auth_service(
    uow: UnitOfWork = Depends(get_uow),
) -> AuthService:
    user_repo = UserRepository(uow.session)
    return AuthService(user_repository=user_repo)


AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]

CurrentUserDep = Annotated[UserEntity, Depends(get_current_user)]
