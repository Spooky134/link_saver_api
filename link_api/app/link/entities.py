from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Union

from app.collection.entities import CollectionEntity
from app.link.enums import LinkType
from app.core.constants import UNSET


@dataclass(frozen=True)
class CreateLinkEntity:
    url: str = None
    title: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    link_type: LinkType = None


@dataclass(frozen=True)
class UpdateLinkEntity:
    title: Union[str, None, object] = UNSET
    description: Union[str, None, object] = UNSET
    image_url: Union[str, None, object] = UNSET
    link_type: Union[LinkType, object] = UNSET

# TODO не все поля None
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
    user_id: Optional[int] = None


@dataclass(frozen=True)
class LinkWithCollectionsEntity(LinkEntity):
    url: Optional[str] = None
    id: Optional[int] = None
    title: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    link_type: Optional[LinkType] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    user_id: Optional[int] = None
    collections: list["CollectionEntity"] = field(default_factory=list)