from pydantic import BaseModel, Field
from datetime import datetime
from pydantic import field_validator
from typing import List, Optional


class CollectionModifyBase(BaseModel):
    @field_validator("name")
    @classmethod
    def name_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("Name cannot be empty or contain only spaces")
        return v

class CollectionCreate(CollectionModifyBase):
    name: str = Field(min_length=1, max_length=100, description="Name cannot be empty")
    description: Optional[str] = Field(default=None, min_length=1, max_length=200)

class CollectionUpdate(CollectionModifyBase):
    name: str = Field(min_length=1, max_length=100, description="Name cannot be empty")
    description: Optional[str] = Field(min_length=1, max_length=200)

class CollectionPatch(CollectionModifyBase):
    name: Optional[str] = Field(default=None, min_length=1, max_length=100, description="Name cannot be empty")
    description: Optional[str] = Field(default=None, min_length=1, max_length=200)

class Collection(BaseModel):
    id: int
    name: str
    description: Optional[str]
    created_at: datetime
    updated_at: datetime
    user_id: int

class CountLinkInCollection(BaseModel):
    count: int

class AddLinksToCollection(BaseModel):
    link_ids: List[int]

class RemoveLinksFromCollection(BaseModel):
    link_ids: List[int]
