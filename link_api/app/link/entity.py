from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from app.collection.entity import CollectionEntity
from app.link.enum import LinkType
from app.user.entity import UserEntity


@dataclass(frozen=True)
class LinkEntity:
    url: Optional[str] = None
    id: Optional[int] = None
    title: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    link_type: Optional[LinkType] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    collections: Optional[list["CollectionEntity"]] = None
    user_id: int = 1
    # user: UserEntity

