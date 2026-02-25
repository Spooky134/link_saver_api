from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Union, List

from app.collection.entities import CollectionShortEntity
from app.link.enums import LinkType
from app.core.types import UnsetType, UNSET


@dataclass(frozen=True)
class CreateLinkEntity:
    url: str
    link_type: LinkType
    title: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None

@dataclass(frozen=True)
class UpdateLinkEntity:
    title: Union[str, None, UnsetType] = UNSET
    description: Union[str, None, UnsetType] = UNSET
    image_url: Union[str, None, UnsetType] = UNSET
    link_type: Union[LinkType, UnsetType] = UNSET

@dataclass(frozen=True)
class LinkEntity:
    url: str
    user_id: int
    link_type: LinkType

    id: Optional[int] = None
    title: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

@dataclass(frozen=True)
class LinkWithCollectionsEntity(LinkEntity):
    collections: List["CollectionShortEntity"] = field(default_factory=list)