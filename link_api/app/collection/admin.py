from sqladmin import ModelView

from app.collection.models import CollectionModel

exclude = ["user_id"]

class CollectionAdmin(ModelView, model=CollectionModel):
    column_list = [c.name for c in CollectionModel.__table__.c if c.name not in exclude] + [CollectionModel.links]
    can_delete = False
    show_compact_lists = True
    icon = "fa-solid fa-layer-group"
