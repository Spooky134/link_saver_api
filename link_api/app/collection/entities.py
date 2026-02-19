from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Union

from app.core.constants import UNSET


@dataclass(frozen=True)
class CreateCollectionEntity:
    name: str
    description: Optional[str] = None


@dataclass(frozen=True)
class UpdateCollectionEntity:
    name: Union[str, None, object] = UNSET
    description: Union[str, None, object] = UNSET


@dataclass(frozen=True)
class CollectionEntity:
    id: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    user_id: int = None
    links: Optional[list["LinkEntity"]] = None

@dataclass(frozen=True)
class CollectionWithLinksEntity(CollectionEntity):
    links: list["LinkEntity"] = field(default_factory=list)
