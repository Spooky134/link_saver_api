from datetime import datetime, timezone
from fastapi import Depends
from jose import jwt, JWTError
from typing import Annotated
from app.auth.services import AuthService
from app.config.project_config import settings
from fastapi import Request
from app.auth.exceptions import MissingToken, TokenExpired, IncorrectFormatToken, UserNotPresent
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
        user_repository: UserRepository = Depends(get_user_repository)
) -> UserEntity:
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=settings.SERVICE_ALGORITHM
        )
    except JWTError:
        raise IncorrectFormatToken()
    expire = payload.get("exp")
    if (not expire) or (int(expire) < datetime.now(timezone.utc).timestamp()):
        raise TokenExpired()
    user_id = int(payload.get("sub"))
    if not user_id:
        raise UserNotPresent()
    user = await user_repository.get(user_id)
    if not user:
        raise UserNotPresent()
    return user


async def get_auth_service(
        user_repository: UserRepository = Depends(get_user_repository)
) -> AuthService:
    return AuthService(user_repository)


AuthServiceDep: type[AuthService] = Annotated[AuthService, Depends(get_auth_service)]

CurrentUserDep: type[UserEntity] = Annotated[UserEntity, Depends(get_current_user)]