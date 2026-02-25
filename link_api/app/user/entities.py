from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class UserEntity:
    id: int
    email: str
    password: str

@dataclass(frozen=True)
class CreateUserEntity:
    email: str
    password: str