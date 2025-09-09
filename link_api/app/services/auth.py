from datetime import datetime
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from exceptions.exceptions import ValidationError
from app.db.models.user import User
from app.db.repositories.user import UserRepository
from link_api.app.api.schemas.user import UserCreate, UserResponse


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    def __init__(self, db: AsyncSession):
        self.user_repo = UserRepository(db)
        # self.email_service = EmailService()  # Сервис отправки email

    async def register_user(self, user_data: UserCreate) -> UserResponse:
        if await self.user_repo.exists_by_email(user_data.email):
            raise ValidationError(detail="Email already registered")

        hashed_password = pwd_context.hash(user_data.password)
        
        new_user = {
            "email": user_data.email,
            "password_hash": hashed_password,
            "username": user_data.username,
            "is_active": False,
            "created_at": datetime.now()
        }

        user = await self.user_repo.create(user_data=new_user)


        return UserResponse(
            id=user.id,
            email=user.email,
            is_active=user.is_active
        )

    # def _generate_verification_token(self, user_id: int) -> str:
    #     """Генерация JWT токена для подтверждения email"""
    #     # Здесь должна быть реализация генерации токена
    #     return f"verify-{user_id}-{datetime.now().timestamp()}"