from typing import List

from app.collection.entities import CollectionShortEntity
from app.core.mappers import BaseMapper
from app.link.entities import LinkEntity, LinkWithCollectionsEntity
from app.link.models import LinkModel


class LinkMapper(BaseMapper):
    @classmethod
    def to_entity(cls, model: LinkModel) -> LinkEntity:
        data = cls.model_to_dict(model)
        return LinkEntity(**data)
    
    @classmethod
    def to_entities(cls, models: List[LinkModel]) -> List[LinkEntity]:
        return [cls.to_entity(model) for model in models]

    @classmethod
    def to_entity_with_coll(cls, model: LinkModel) -> LinkWithCollectionsEntity:
        data = cls.model_to_dict(model)

        data["collections"] = (
            [CollectionShortEntity(id=m.id, name=m.name) for m in model.collections]
            if cls.is_loaded(model, "collections")
            else []
        )

        return LinkWithCollectionsEntity(**data)

