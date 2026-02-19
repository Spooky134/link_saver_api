from sqladmin import ModelView

from app.link.models import LinkModel

exclude = ["user_id"]

class LinkAdmin(ModelView, model=LinkModel):
    column_list = [c.name for c in LinkModel.__table__.c if c.name not in exclude] + [LinkModel.collections]
    can_delete = False
    show_compact_lists = True
    icon = "fa-solid fa-link"