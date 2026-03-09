from dataclasses import replace


from app.auth.exceptions import (
    InvalidCurrentPassword,
    PasswordNotMatch,
    SamePasswordError,
    UserExistsError,
    UserNotPresent,
)
from app.auth.tasks import send_reset_password_email
from app.auth.utils import (
    create_access_token,
    create_password_reset_token,
    get_password_hash,
    validate_reset_password_token,
    verify_password,
)
from app.core.config import settings
from app.core.logging import get_logger
from app.core.unit_of_work import UnitOfWork
from app.user.entities import CreateUserEntity, UpdateUserEntity
from app.user.repositories import UserRepository

logger = get_logger(__name__)


class AuthService:
    def __init__(self, uow: UnitOfWork, user_repository: UserRepository):
        self.uow = uow
        self.user_repo = user_repository

    async def register(self, user_register: CreateUserEntity) -> None:
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
            raise UserNotPresent()
        password_is_valid = verify_password(password, user.password)
        if not password_is_valid:
            raise PasswordNotMatch()
        access_token = create_access_token({"sub": str(user.id)})
        return access_token

    async def change_password(
        self, user_id: int, old_password: str, new_password: str
    ) -> None:
        user = await self.user_repo.get(user_id)
        if not user:
            raise UserNotPresent()
        if not verify_password(old_password, user.password):
            raise InvalidCurrentPassword()
        if verify_password(new_password, user.password):
            raise SamePasswordError()

        updated_user = UpdateUserEntity(password=get_password_hash(new_password))

        await self.user_repo.update(user_id, updated_user)
        await self.uow.commit()

    async def request_password_reset(self, email: str) -> None:
        user = await self.user_repo.get_by_email(email)
        if not user:
            return

        token = create_password_reset_token(user.id)

        reset_link = f"{settings.FRONTEND_URL}?token={token}"

        await send_reset_password_email.kiq(
            email=user.email,
            reset_link=reset_link,
        )

    async def reset_password(self, reset_token: str, new_password: str) -> None:
        user_id = validate_reset_password_token(reset_token)

        user = await self.user_repo.get(user_id)
        if not user:
            raise UserNotPresent()

        updated_user = UpdateUserEntity(password=get_password_hash(new_password))

        await self.user_repo.update(user_id, updated_user)
        await self.uow.commit()
