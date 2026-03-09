from app.core.mappers import BaseMapper
from app.user.entities import UserEntity
from app.user.models import UserModel


class UserMapper(BaseMapper):
    @classmethod
    def to_user(cls, model: UserModel) -> UserEntity:
        data = cls.model_to_dict(model)
        return UserEntity(**data)
