from pydantic import BaseModel, HttpUrl
from app.schemas.link import LinkType



class LinkInCollection(BaseModel):
     id: int
     title: str
     url: HttpUrl
     link_type: LinkType

     class Config:
        from_attributes = True


class CollectionInLink(BaseModel):
    ## user = models.ForeignKey(User, on_delete=models.CASCADE)
    id:int
    name: str

    class Config:
        from_attributes = True