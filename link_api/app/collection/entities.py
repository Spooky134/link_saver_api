from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Union

from app.core.types import UNSET, UnsetType


@dataclass(frozen=True)
class CollectionEntity:
    name: str
    user_id: int

    id: Optional[int] = None
    description: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


@dataclass(frozen=True)
class CreateCollectionEntity:
    name: str
    description: Optional[str] = None


@dataclass(frozen=True)
class UpdateCollectionEntity:
    name: Union[str, None, UnsetType] = UNSET
    description: Union[str, None, UnsetType] = UNSET


@dataclass(frozen=True)
class CollectionShortEntity:
    id: int
    name: str
