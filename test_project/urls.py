"""URL configuration for test_project project."""

from django.contrib import admin
from django.urls import path, include
from ninja import NinjaAPI
from amis_python.ninja import AmisNinja
from amis_python.builder.app import AppBuilder
from amis_python.builder.page import PageBuilder

# Create django-ninja API instance
api = NinjaAPI()

# Create amis app instance
amis_app = AppBuilder(brand_name="My System")

# Create sample pages
home_page = PageBuilder(title="Home Page", body=[{"type": "button", "label": "Click Me"}])
user_list_page = PageBuilder(title="User List", body=[{"type": "table", "api": "/api/users"}])

# Register pages
amis_app.register_page("/home", home_page, label="Home")
amis_app.register_page("/users/list", user_list_page, label="User List")

# Integrate amis app with django-ninja
amis_ninja = AmisNinja(api)
amis_ninja.register_amis_app(amis_app, prefix="/amis")

# API routes
@api.get("/users")
def get_users(request):
    return [{"id": 1, "name": "John Doe"}, {"id": 2, "name": "Jane Smith"}]

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api.urls),
    path("amis/", include("amis_python.urls")),
]
