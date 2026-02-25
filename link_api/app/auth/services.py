from dataclasses import replace

from app.core.unit_of_work import UnitOfWork
from app.user.repositories import UserRepository
from app.user.exceptions import UserExistsError, UserNotExistsError
from app.auth.utils import get_password_hash, verify_password, create_access_token
from app.core.logger import get_logger
from app.auth.exceptions import PasswordNotMatch
from app.user.entities import UserEntity, CreateUserEntity

logger = get_logger(__name__)

class AuthService:
    def __init__(self, uow: UnitOfWork, user_repository: UserRepository):
        self.uow = uow
        self.user_repo = user_repository

    async def register(self, user_register: CreateUserEntity):
        existing_user = await self.user_repo.get_by_email(str(user_register.email))
        if existing_user:
            raise UserExistsError()

        hashed_password = get_password_hash(user_register.password)
        new_user = replace(user_register, password=hashed_password)

        await self.user_repo.add(new_user)
        await self.uow.commit()


    async def login(self, email: str, password: str) -> str:
        user = await self.user_repo.get_by_email(email)
        if not user:
            raise UserNotExistsError()
        password_is_valid = verify_password(password, user.password)
        if not password_is_valid:
            raise PasswordNotMatch()
        access_token = create_access_token(
            {"sub": str(user.id)}
        )
        return access_token

