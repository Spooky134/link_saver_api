from pydantic import BaseModel, Field, HttpUrl
from datetime import datetime
from typing import Optional
from enum import Enum
from app.schemas.collections import Collection

class LinkType(str, Enum):
      WEBSITE = 'website'
      BOOK = 'book'
      ARTICLE ='article'
      MUSIC = 'music'
      VIDEO = 'video'

class LinkCreate(BaseModel):
      url:HttpUrl = Field(..., example="https://example.com")

class LinkUpdate(BaseModel):
    # url:HttpUrl = Field(..., example="https://example.com")
    title: Optional[str] = Field(default=None, max_length=100)
    description: Optional[str] = Field(default=None, max_length=400)
    image: Optional[HttpUrl] = Field(default=None)
    link_type: Optional[LinkType] = Field(default=None, example=LinkType.ARTICLE)
    
    # collections: list[Collection]


class LinkResponse(BaseModel):
    ## user = models.ForeignKey(User, on_delete=models.CASCADE)
    id:int
    title: str
    description: str
    url:HttpUrl
    image: HttpUrl
    link_type: LinkType
    time_create: datetime
    time_update: datetime
    # collections: list[Collection]


# class LinkBase(BaseModel):
    ## user = models.ForeignKey(User, on_delete=models.CASCADE)
    #   title: str = Field(max_length=100)
    #   description: str = Field(max_length=400)
    #   url:HttpUrl = Field(..., example="https://example.com")
    #   image: HttpUrl
    #   link_type: LinkType = Field(..., example=LinkType.ARTICLE)
    #   time_create: datetime = Field(default_factory=datetime.now)
    #   time_update: datetime = Field(default_factory=datetime.now)
    #   collections: list[Collection]