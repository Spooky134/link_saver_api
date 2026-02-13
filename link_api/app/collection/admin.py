from sqladmin import ModelView

from app.collection.model import CollectionModel


class CollectionAdmin(ModelView, model=CollectionModel):
    column_list = [c.name for c in CollectionModel.__table__.c] + [CollectionModel.links]
    can_delete = False
    show_compact_lists = True
    icon = "fa-solid fa-layer-group"
