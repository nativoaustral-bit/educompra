from django.urls import path
from .views import lista_catalogo

app_name = "catalogo"

urlpatterns = [
    path("", lista_catalogo, name="lista"),
]
