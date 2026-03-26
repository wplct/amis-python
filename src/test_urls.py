from django.urls import include, path


urlpatterns = [
    path("amis/", include("amis_python.urls")),
]
