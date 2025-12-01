from django.http import JsonResponse
from amis_python.builder.app import AppBuilder
from amis_python.builder.page import PageBuilder

# Create amis app instance
amis_app = AppBuilder(brand_name="My System")

# Create sample page
home_page = PageBuilder(title="Home Page", body=[{"type": "button", "label": "Click Me"}])

# Register page
amis_app.register_page("/home", home_page, label="Home")

def home(request):
    """Home view"""
    return JsonResponse(home_page.to_schema())

def app_config(request):
    """App config view"""
    return JsonResponse(amis_app.to_schema())
