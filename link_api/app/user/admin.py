from sqladmin import ModelView

from app.user.model import UserModel


class UserAdmin(ModelView, model=UserModel):
    column_list = [c.name for c in UserModel.__table__.c]
    can_delete = False
    show_compact_lists = True
    icon = "fa-regular fa-user"