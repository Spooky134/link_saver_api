from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class UserEntity:
    id: Optional[int] = None
    email: Optional[str] = None
    password: Optional[str] = None

    # links: list["LinkEntity"]
    # collections: list["CollectionEntity"]
