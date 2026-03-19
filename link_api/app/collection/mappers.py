from typing import List

from app.collection.entities import CollectionEntity
from app.collection.models import CollectionModel
from app.core.mappers import BaseMapper


class CollectionMapper(BaseMapper):
    @classmethod
    def to_entity(cls, model: CollectionModel) -> CollectionEntity:
        data = cls.model_to_dict(model)
        return CollectionEntity(**data)
    
    @classmethod
    def to_entities(cls, models: List[CollectionModel]) -> List[CollectionEntity]:
        return [cls.to_entity(model) for model in models]
