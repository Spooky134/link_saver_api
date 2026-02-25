from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from starlette.responses import RedirectResponse

from app.auth.dependencies import get_current_user
from app.auth.schemas import UserLogin
from app.auth.services import AuthService
from app.config.project_config import settings
from app.core.dependecies import get_uow
from app.user.dependencies import get_user_repository


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()

        user_data = UserLogin(
            email=form.get("username"),
            password=form.get("password")
        )

        async for uow in get_uow():
            user_repo = await get_user_repository(uow)
            auth_service = AuthService(uow, user_repo)
            try:
                access_token = await auth_service.login(
                    email=str(user_data.email),
                    password=user_data.password,
                )
                request.session.update({"token": access_token})
                return True
            except Exception:
                return False
        return False

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request):
        token = request.session.get("token")
        if not token:
            return RedirectResponse(request.url_for("admin:login"))
        try:
            async for uow in get_uow():
                user_repo = await get_user_repository(uow)
                user = await get_current_user(token, user_repo)
                if not user:
                    return False
        except Exception:
            # Если токен протух — просто гоним на логин, а не падаем в 500
            return RedirectResponse(request.url_for("admin:login"))


authentication_backend = AdminAuth(secret_key=settings.SECRET_KEY)