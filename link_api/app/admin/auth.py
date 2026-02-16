from fastapi import Depends
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request

from app.auth.dependencies import get_current_user
from app.auth.schemas import UserLogin
from app.auth.services import AuthService
from app.config.project_config import settings
from app.core.database import async_session_maker


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        email, password = form["username"], form["password"]


        async with async_session_maker() as session:
            auth_service = AuthService(session)
            try:
                access_token = await auth_service.login(
                    user_login=UserLogin(email=email, password=password)
                )
                request.session.update({"token": access_token})
                return True
            except Exception:
                return False


    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")
        if not token:
            return False

        user = await get_current_user(token=token)
        if not user:
            return False
        # Check the token in depth
        return True


authentication_backend = AdminAuth(secret_key=settings.SECRET_KEY)