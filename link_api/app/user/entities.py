from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Union

from app.core.types import UnsetType, UNSET


@dataclass(frozen=True)
class UserEntity:
    id: int
    email: str
    password: str
    created_at: datetime
    updated_at: datetime

@dataclass(frozen=True)
class CreateUserEntity:
    email: str
    password: str

@dataclass(frozen=True)
class UpdateUserEntity:
    password: Union[str, None, UnsetType] = UNSET