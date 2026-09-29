"""
Rutas de la aplicación catálogo de EduCompra Humm.
"""

from django.urls import path
from .views import catalogo_lista_view, producto_detalle_view

app_name = "catalogo"

urlpatterns = [
    path("", catalogo_lista_view, name="lista"),
    path("<slug:slug>/", producto_detalle_view, name="detalle"),
]
