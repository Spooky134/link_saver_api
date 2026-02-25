from dataclasses import dataclass
from datetime import datetime
from typing import Optional


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
