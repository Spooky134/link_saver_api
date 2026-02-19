from sqladmin import ModelView

from app.link.models import LinkModel
from app.user.models import UserModel
from app.collection.models import CollectionModel


class UserAdmin(ModelView, model=UserModel):
    column_list = [c.name for c in UserModel.__table__.c] + [UserModel.links] + [UserModel.collections]
    can_delete = False
    show_compact_lists = True
    icon = "fa-regular fa-user"