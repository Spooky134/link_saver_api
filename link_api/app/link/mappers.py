from app.collection.entities import CollectionShortEntity
from app.core.mappers import BaseMapper
from app.link.entities import LinkEntity, LinkWithCollectionsEntity
from app.link.models import LinkModel


class LinkMapper(BaseMapper):
    @classmethod
    def to_link(cls, model: LinkModel) -> LinkEntity:
        data = cls.model_to_dict(model)
        return LinkEntity(**data)
    
    @classmethod
    def to_link_with_collections(cls, model: LinkModel) -> LinkWithCollectionsEntity:
        data = cls.model_to_dict(model)

        data["collections"] = (
            [CollectionShortEntity(id=m.id, name=m.name) for m in model.collections]
            if cls.is_loaded(model, "collections")
            else []
        )

        return LinkWithCollectionsEntity(**data)

