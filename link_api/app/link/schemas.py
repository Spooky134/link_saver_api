from pydantic import BaseModel, Field, HttpUrl, field_serializer
from datetime import datetime
from typing import Optional, List
from app.link.enums import LinkType


class CollectionInLink(BaseModel):
    id: int
    name: str

class CreateLink(BaseModel):
    url: HttpUrl = Field(examples=["https://example.com"])

class UpdateLink(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=100)
    description: Optional[str] = Field(default=None, min_length=1, max_length=400)
    image_url: Optional[HttpUrl] = Field(default=None, examples=["https://example.com/images/picture.jpg"])
    link_type: Optional[LinkType] = Field(default=None)

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

class LinkWithCollections(Link):
    collections: Optional[List[CollectionInLink]]