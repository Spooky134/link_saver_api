from sqladmin import ModelView

from app.link.model import LinkModel


class LinkAdmin(ModelView, model=LinkModel):
    column_list = [c.name for c in LinkModel.__table__.c] + [LinkModel.collections]
    can_delete = False
    show_compact_lists = True
    icon = "fa-solid fa-link"