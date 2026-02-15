from app.link.model import LinkModel
from app.collection.model import CollectionModel
from app.link.entity import LinkEntity
from app.collection.entity import CollectionEntity
from app.base.mapper import BaseMapper
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