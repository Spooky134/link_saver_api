from app.link.models import LinkModel
from app.collection.models import CollectionModel
from app.link.entities import LinkEntity
from app.collection.entities import CollectionEntity
from app.base.mappers import BaseMapper
from sqlalchemy import inspect


class EntityMapper(BaseMapper):
    @classmethod
    def to_link_entity(cls, model: LinkModel) -> LinkEntity:
        data = cls.model_to_dict(model)
        inspected = inspect(model)

        if 'collections' not in inspected.unloaded:
            data["collections"] = [
                cls.to_collection_entity(col) for col in model.collections
            ]
        else:
            pass
        entity = LinkEntity(**data)
        return entity

    @classmethod
    def to_collection_entity(cls, model: CollectionModel) -> CollectionEntity:
        data = cls.model_to_dict(model)
        inspected = inspect(model)
        if 'links' not in inspected.unloaded:
            data["links"] = [
                cls.to_link_entity(link) for link in model.links
            ]
        else:
            pass
        entity = CollectionEntity(**data)
        return entity

class ModelMapper(BaseMapper):
    @classmethod
    def to_link_model(cls, link_entity: LinkEntity) -> LinkModel:
        pass