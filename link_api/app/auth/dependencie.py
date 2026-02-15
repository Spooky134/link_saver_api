from datetime import datetime, timezone

from fastapi import Depends, HTTPException, Request, status
from jose import jwt, JWTError

from app.config.project_config import settings
from fastapi import Request
from app.auth.exception import MissingToken, TokenExpired, IncorrectFormatToken, UserNotPresent
from app.dependencies import service_factory
from app.user.repository import UserRepository
from app.core.database import get_db_session, async_session_maker


def get_access_token(request: Request):
    token = request.cookies.get("link_saver_access_token")
    if not token:
        raise MissingToken
    return token


async def get_current_user(token: str = Depends(get_access_token)):
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=settings.SERVICE_ALGORITHM
        )
    except JWTError:
        raise IncorrectFormatToken
    expire = payload.get("exp")
    if (not expire) or (int(expire) < datetime.now(timezone.utc).timestamp()):
        raise TokenExpired
    user_id = int(payload.get("sub"))
    if not user_id:
        raise UserNotPresent
    async with async_session_maker() as session:
        user_repo = UserRepository(session)
        user = await user_repo.get_by_id(user_id)
        if not user:
            raise UserNotPresent
        return user