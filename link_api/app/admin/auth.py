from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from app.auth.exceptions import UserNotPresent, PasswordNotMatch, TokenExpired, IncorrectFormatToken
from app.auth.services import AuthService
from app.auth.utils import validate_token
from app.config.project_config import settings
from app.core.dependecies import get_uow
from app.core.unit_of_work import UnitOfWork
from app.user.repositories import UserRepository


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        email=form.get("username")
        password=form.get("password")

        if not email or not password:
            return False

        async with UnitOfWork() as uow:
            user_repo = UserRepository(uow.session)
            auth_service = AuthService(uow, user_repo)

            try:
                access_token = await auth_service.login(
                    email=str(email),
                    password=str(password)
                )

                request.session.update({"access_token": access_token})
                return True
            except (UserNotPresent, PasswordNotMatch, Exception):
                return False


    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request):
        token = request.session.get("access_token")
        if not token:
            return False
        try:
            async for uow in get_uow():
                user_repo = UserRepository(uow.session)
                user_id = validate_token(token)
                user = await user_repo.get(user_id)
                if not user:
                    return False
            return True
        except (TokenExpired, IncorrectFormatToken, Exception):
            return False


authentication_backend = AdminAuth(secret_key=settings.SECRET_KEY)