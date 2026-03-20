from datetime import datetime
from typing import Annotated, List, Optional
from annotated_types import MinLen, MaxLen

from pydantic import BaseModel, ConfigDict, HttpUrl, field_serializer

from app.link.enums import LinkType


class CollectionInLink(BaseModel):
    id: int
    name: str


class CreateLink(BaseModel):
    url: Annotated[HttpUrl, "https://example.com"]


class PatchLink(BaseModel):
    title: Annotated[Optional[str], MinLen(1), MaxLen(100)] = None
    description: Annotated[Optional[str], MinLen(1), MaxLen(400)] = None
    link_type: Optional[LinkType] = None
    image_url: Annotated[Optional[HttpUrl], "https://example.com/images/picture.jpg"] = None

    @field_serializer("image_url")
    def serialize_image(self, v):
        return str(v) if v else None


class Link(BaseModel):
    id: int
    title: Optional[str]
    description: Optional[str]
    url: HttpUrl
    image_url: Optional[HttpUrl]
    link_type: LinkType
    created_at: datetime
    updated_at: datetime


class CreateLinkResponse(BaseModel):
    id: int
    url: HttpUrl
    link_type: LinkType
    created_at: datetime
    updated_at: datetime
    user_id: int


class LinkWithCollections(Link):
    collections: Optional[List[CollectionInLink]]
