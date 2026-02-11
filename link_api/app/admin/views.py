from sqladmin import ModelView

from app.link.model import Link
from app.collection.model import Collection


class LinkAdmin(ModelView, model=Link):
    column_list = [c.name for c in Link.__table__.c] + [Link.collections]
    can_delete = False
    show_compact_lists = True
    icon = "fa-solid fa-link"

class CollectionAdmin(ModelView, model=Collection):
    column_list = [c.name for c in Collection.__table__.c] + [Collection.links]
    can_delete = False
    show_compact_lists = True
    icon = "fa-solid fa-layer-group"
