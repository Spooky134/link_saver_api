from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional
from app.schemas.relations import LinkInCollection
from app.schemas.enums import LinkType
from app.schemas.decorators import validate_ids_field


@validate_ids_field("link_ids")
class CollectionCreate(BaseModel):
    name: str = Field(max_length=50)
    description: Optional[str] = Field(default='', max_length=200)
    link_ids: Optional[list[int]] = None

@validate_ids_field("link_ids")
class CollectionUpdate(BaseModel):
    name: Optional[str] = Field(default=None, max_length=50)
    description: Optional[str] = Field(default=None, max_length=200)
    link_ids: Optional[list[int]] = None

    @field_validator('name')
    def name_cannot_be_empty(cls, value):
        if value is not None and value.strip() == "":
            raise ValueError("Название не может быть пустым")
        return value


class CollectionResponse(BaseModel):
    ## user = models.ForeignKey(User, on_delete=models.CASCADE)
    id:int
    name: str
    description: str
    time_create: datetime
    time_update: datetime
    links: list[LinkInCollection] = []

    class Config:
        from_attributes = True

class CollectionInLink(BaseModel):
    ## user = models.ForeignKey(User, on_delete=models.CASCADE)
    id:int
    name: str

    class Config:
        from_attributes = True