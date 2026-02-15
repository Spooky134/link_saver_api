from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class UserEntity:
    id: int
    email: str
    password: str

    # links: list["LinkEntity"]
    # collections: list["CollectionEntity"]
