from app.link.models import LinkModel
from app.link.entities import LinkEntity
from app.core.mappers import BaseMapper


class LinkMapper(BaseMapper):
    @classmethod
    def to_link(cls, model: LinkModel) -> LinkEntity:
        data = cls.model_to_dict(model)
        return LinkEntity(**data)
