from pydantic import BaseModel, Field, field_validator, HttpUrl
from datetime import datetime
from typing import Optional

from app.link.enum import LinkType
from app.core.decorators import validate_ids_field


class LinkInCollection(BaseModel):
    id: int
    title: str
    url: HttpUrl
    link_type: LinkType

    class Config:
        from_attributes = True


@validate_ids_field("link_ids")
class CollectionCreate(BaseModel):
    name: str = Field(max_length=50)
    description: Optional[str] = Field(default='', max_length=200)
    # link_ids: Optional[list[int]] = None


class CollectionUpdateBase(BaseModel):
    class Config:
        extra = "forbid"


@validate_ids_field("link_ids")
class CollectionLinkRequest(CollectionUpdateBase):
    link_ids: list[int]


@validate_ids_field("link_ids")
class CollectionUpdateFull(CollectionUpdateBase):
    name: str = Field(max_length=50)
    description: str = Field(max_length=200)
    link_ids: list[int]

    @field_validator('name')
    def name_cannot_be_empty(cls, value):
        if value is not None and value.strip() == "":
            raise ValueError("Название не может быть пустым")
        return value


@validate_ids_field("link_ids")
class CollectionUpdate(CollectionUpdateFull):
    name: Optional[str] = Field(default=None, max_length=50)
    description: Optional[str] = Field(default=None, max_length=200)
    link_ids: Optional[list[int]] = None


class CollectionResponse(BaseModel):
    ## user = models.ForeignKey(User, on_delete=models.CASCADE)
    id: int
    name: str
    description: str
    created_at: datetime
    updated_at: datetime
    links: list[LinkInCollection] = Field(default_factory=list)

    class Config:
        from_attributes = True

