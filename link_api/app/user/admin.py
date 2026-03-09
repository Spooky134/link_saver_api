from sqladmin import ModelView

from app.collection.models import CollectionModel
from app.link.models import LinkModel
from app.user.models import UserModel


class UserAdmin(ModelView, model=UserModel):
    column_list = (
        [c.name for c in UserModel.__table__.c]
        + [UserModel.links]
        + [UserModel.collections]
    )
    can_delete = False
    show_compact_lists = True
    icon = "fa-regular fa-user"
