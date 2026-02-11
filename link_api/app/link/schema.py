from pydantic import BaseModel, Field, HttpUrl, field_validator, field_serializer
from datetime import datetime
from typing import Optional


from app.link.enum import LinkType
from app.core.decorators import validate_ids_field

class CollectionInLink(BaseModel):
    ## user = models.ForeignKey(User, on_delete=models.CASCADE)
    id: int
    name: str

    class Config:
        from_attributes = True


class LinkCreate(BaseModel):
    url: HttpUrl = Field(..., example="https://example.com")


@validate_ids_field("collections_ids")
class LinkUpdate(BaseModel):
    # url:HttpUrl = Field(..., example="https://example.com")
    title: Optional[str] = Field(default=None, max_length=100)
    description: Optional[str] = Field(default=None, max_length=400)
    image: Optional[HttpUrl] = None
    link_type: Optional[LinkType] = Field(default=None, example=LinkType.ARTICLE)
    collection_ids: Optional[list[int]] = None

    @field_serializer("image")
    def serialize_image(self, v):
        return str(v) if v else None


class LinkResponse(BaseModel):
    ## user = models.ForeignKey(User, on_delete=models.CASCADE)
    id: int
    title: str
    description: str
    url: HttpUrl
    image: Optional[HttpUrl]
    link_type: LinkType
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    collections: list[CollectionInLink]

    class Config:
        from_attributes = True


