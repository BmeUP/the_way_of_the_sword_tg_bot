from sqladmin import ModelView

from users.models.orm.user import User
from admin_panel.utils import hash_password


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.first_name]

    async def on_model_change(self, data, model, is_created, request):
        if data.get("password"):
            data["password"] = hash_password(data["password"])
