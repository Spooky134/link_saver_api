from app.link.models import LinkModel
from app.collection.models import CollectionModel
from app.link.entities import LinkEntity, LinkWithCollectionsEntity
from app.collection.entities import CollectionEntity, CollectionWithLinksEntity
from app.core.mappers import BaseMapper
from sqlalchemy import inspect



class EntityMapper(BaseMapper):
    @classmethod
    def to_link_with_collections(cls, model: LinkModel) -> LinkWithCollectionsEntity:
        data = cls.model_to_dict(model)

        data["collections"] = [
            CollectionEntity(**cls.model_to_dict(m)) for m in model.collections
        ] if cls.is_loaded(model, 'collections') else []

        return LinkWithCollectionsEntity(**data)

    @classmethod
    def to_collection_with_links(cls, model: CollectionModel) -> CollectionWithLinksEntity:
        data = cls.model_to_dict(model)


        data["links"] = [
            LinkEntity(**cls.model_to_dict(m)) for m in model.links
        ] if cls.is_loaded(model, 'links') else []

        return CollectionWithLinksEntity(**data)