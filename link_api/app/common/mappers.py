from app.link.models import LinkModel
from app.collection.models import CollectionModel
from app.link.entities import LinkEntity, LinkWithCollectionsEntity
from app.collection.entities import CollectionEntity
from app.core.mappers import BaseMapper
from app.user.entities import UserEntity
from app.user.models import UserModel


class EntityMapper(BaseMapper):
    @classmethod
    def to_link(cls, model: LinkModel) -> LinkEntity:
        data = cls.model_to_dict(model)
        return LinkEntity(**data)

    @classmethod
    def to_link_with_collections(cls, model: LinkModel) -> LinkWithCollectionsEntity:
        data = cls.model_to_dict(model)

        data["collections"] = [
            CollectionEntity(**cls.model_to_dict(m)) for m in model.collections
        ] if cls.is_loaded(model, 'collections') else []

        return LinkWithCollectionsEntity(**data)

    @classmethod
    def to_collection(cls, model: CollectionModel) -> CollectionEntity:
        data = cls.model_to_dict(model)
        return CollectionEntity(**data)

    @classmethod
    def to_user(cls, model: UserModel) -> UserEntity:
        data = cls.model_to_dict(model)
        return UserEntity(**data)