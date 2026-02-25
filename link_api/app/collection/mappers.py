from app.collection.models import CollectionModel
from app.collection.entities import CollectionEntity
from app.core.mappers import BaseMapper


class CollectionMapper(BaseMapper):
    @classmethod
    def to_collection(cls, model: CollectionModel) -> CollectionEntity:
        data = cls.model_to_dict(model)
        return CollectionEntity(**data)
