from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from app.user.entity import UserEntity


@dataclass(frozen=True)
class CollectionEntity:
    id: Optional[int]
    name: str
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    links: Optional[list["LinkEntity"]]

    # user: UserEntity
