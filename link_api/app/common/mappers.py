from app.collection.entities import CollectionShortEntity
from app.core.mappers import BaseMapper
from app.link.entities import LinkWithCollectionsEntity
from app.link.models import LinkModel


class EntityMapper(BaseMapper):
    @classmethod
    def to_link_with_collections(cls, model: LinkModel) -> LinkWithCollectionsEntity:
        data = cls.model_to_dict(model)

        data["collections"] = (
            [CollectionShortEntity(id=m.id, name=m.name) for m in model.collections]
            if cls.is_loaded(model, "collections")
            else []
        )

        return LinkWithCollectionsEntity(**data)
