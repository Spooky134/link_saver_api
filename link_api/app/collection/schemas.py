from pydantic import BaseModel, Field, field_validator, HttpUrl
from datetime import datetime
from app.link.enums import LinkType
from pydantic import field_validator
from typing import Any, List, Optional


class CollectionModifyBase(BaseModel):
    name: str = Field(min_length=1, max_length=100, description="Name cannot be empty")
    description: Optional[str] = Field(default=None, min_length=1, max_length=200)

    @field_validator("name")
    @classmethod
    def name_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("Name cannot be empty or contain only spaces")
        return v

class CollectionCreate(CollectionModifyBase):
    pass

class CollectionUpdateFull(CollectionModifyBase):
    name: str = Field(min_length=1, max_length=100, description="Name cannot be empty")
    description: Optional[str] = Field(min_length=1, max_length=200)

class CollectionUpdate(CollectionModifyBase):
    name: Optional[str] = Field(default=None, min_length=1, max_length=100, description="Name cannot be empty")
    description: Optional[str] = Field(default=None, min_length=1, max_length=200)

class Collection(BaseModel):
    id: int
    name: str
    description: Optional[str]
    created_at: datetime
    updated_at: datetime

class CollectionWithLinks(BaseModel):
    links: list["LinkInCollection"]

class LinkInCollection(BaseModel):
    id: int
    title: str
    url: HttpUrl
    link_type: LinkType

class CountLinkInCollection(BaseModel):
    count: int

class AddLinksToCollection(BaseModel):
    link_ids: list[int]

class RemoveLinksFromCollection(BaseModel):
    link_ids: list[int]



#
# def validate_ids_field(field_name: str):
#     """Декоратор для конвертации строковых ID в int в указанном поле"""
#
    # def decorator(cls):
    #     @field_validator(field_name, mode='before')
    #     @classmethod
    #     def convert_ids(cls, v: Any) -> Optional[List[int]]:
    #         if v is None:
    #             return None
    #         if isinstance(v, list):
    #             return [
    #                 int(item) if isinstance(item, str) and item.isdigit()
    #                 else item
    #                 for item in v
    #             ]
    #         return v
    #
    #     # Динамически добавляем валидатор к классу
    #     setattr(cls, f"_validate_{field_name}", convert_ids)
    #     return cls
    #
    # return decorator