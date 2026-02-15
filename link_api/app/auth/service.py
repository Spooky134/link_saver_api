from fastapi import Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.user.repository import UserRepository
from app.user.schema import UserLogin
from app.user.exception import UserExistsError, UserNotExistsError
from app.auth.schema import UserRegister
from app.auth.auth import get_password_hash, verify_password, create_access_token
from app.core.logger import get_logger
from app.auth.exception import PasswordNotMatch

logger = get_logger(__name__)

class AuthService:
    def __init__(self, db: AsyncSession):
        self.user_repo = UserRepository(db)

    async def register(self, user_register: UserRegister):
        existing_user = await self.user_repo.get_by_email(str(user_register.email))
        if existing_user:
            raise UserExistsError
        hashed_password = get_password_hash(user_register.password)
        data = {
            "email": user_register.email,
            "password": hashed_password
        }
        await self.user_repo.add(
            data
        )
        await self.user_repo.async_session.commit()


    async def login(self, user_login: UserLogin):
        user = await self.user_repo.get_by_email(str(user_login.email))
        if not user:
            raise UserNotExistsError
        password_is_valid = verify_password(user_login.password, user.password)
        if not password_is_valid:
            raise PasswordNotMatch
        access_token = create_access_token(
            {"sub": str(user.id)},
        )
        return access_token

    async def logout(self, response: Response):
        response.delete_cookie("access_token")

