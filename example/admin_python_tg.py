from starlette.applications import Starlette
from starlette_admin.contrib.sqla import Admin, ModelView

from alchemy import engine, User, Address


# -------------------------
# Admin Views
# -------------------------

class UserAdmin(ModelView):
    label = "Foydalanuvchilar"
    name_plural = "Foydalanuvchilar"
    icon = "fa fa-user"
    category = "Accounts"

    column_list = ["id", "username", "email", "is_active"]
    column_searchable_list = ["username", "email"]
    column_sortable_list = ["id", "username"]

    column_labels = {
        "id": "ID",
        "username": "Login",
        "email": "Email",
        "is_active": "Faol"
    }


class AddressAdmin(ModelView):
    label = "Manzillar"
    name_plural = "Manzillar"
    icon = "fa fa-map-marker"
    category = "Accounts"

    column_list = ["id", "city", "street"]
    column_searchable_list = ["city", "street"]

    column_labels = {
        "city": "Shahar",
        "street": "Ko‘cha"
    }


# -------------------------
# Admin setup
# -------------------------

def setup_admin(app: Starlette) -> None:
    admin = Admin(
        engine=engine,
        title="🚀 Admin Panel",
        base_url="/admin",
    )

    admin.add_view(UserAdmin(User))
    admin.add_view(AddressAdmin(Address))

    admin.mount_to(app)

# -------------------------
# Application factory
# -------------------------

def create_app() -> Starlette:
    app = Starlette(debug=True)

    setup_admin(app)

    return app


app = create_app()
