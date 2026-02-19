from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request

from app.auth.dependencies import get_current_user
from app.auth.schemas import UserLogin
from app.auth.services import AuthService
from app.config.project_config import settings
from app.core.database import get_db_session
from app.user.dependencies import get_user_repository
from app.user.entities import UserEntity


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()

        user_data = UserLogin(
            email=form.get("username"),
            password=form.get("password")
        )

        async for async_session in get_db_session():
            user_repo = await get_user_repository(async_session)
            auth_service = AuthService(user_repo)
            try:
                user_entity = UserEntity(**user_data.model_dump())
                access_token = await auth_service.login(
                    user_login=user_entity
                )
                request.session.update({"token": access_token})
                return True
            except Exception:
                return False
        return False

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")
        if not token:
            return False
        async for async_session in get_db_session():
            user_repo = await get_user_repository(async_session)
            user = await get_current_user(token, user_repo)
            if not user:
                return False
        return True


authentication_backend = AdminAuth(secret_key=settings.SECRET_KEY)