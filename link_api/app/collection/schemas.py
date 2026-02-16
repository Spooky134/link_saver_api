from pydantic import BaseModel, Field, field_validator, HttpUrl
from datetime import datetime
from typing import Optional

from app.link.enums import LinkType
from app.core.decorators import validate_ids_field


class LinkInCollection(BaseModel):
    id: int
    title: str
    url: HttpUrl
    link_type: LinkType


class CollectionCreate(BaseModel):
    name: str = Field(max_length=50)
    description: Optional[str] = Field(default='', max_length=255)


class CollectionUpdateBase(BaseModel):
    name: str = Field(min_length=1, max_length=100, description="Name cannot be empty")
    description: str = Field(min_length=1, max_length=200)

    @field_validator("name")
    @classmethod
    def name_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("Name cannot be empty or contain only spaces")
        return v


@validate_ids_field("link_ids")
class CollectionLinkRequest(CollectionUpdateBase):
    link_ids: list[int]



class CollectionUpdatePUT(CollectionUpdateBase):
    pass

class CollectionUpdatePATCH(CollectionUpdateBase):
    name: Optional[str] = Field(default=None, min_length=1, max_length=100, description="Name cannot be empty")
    description: Optional[str] = Field(default=None, min_length=1, max_length=200)



class CollectionResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    created_at: datetime
    updated_at: datetime
    links: Optional[list[LinkInCollection]]

