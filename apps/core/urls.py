from django.urls import path
from .views import health_check, home_view

app_name = "core"

urlpatterns = [
    path("", home_view, name="home"),
    path("health/", health_check, name="health"),
]
