"""
Rutas de la aplicación cotizaciones en EduCompra Humm.
"""

from django.urls import path
from .views import (
    mi_cotizacion_view,
    agregar_item_view,
    actualizar_cantidad_view,
    eliminar_item_view,
    vaciar_canasta_view,
    solicitar_cotizacion_view,
    solicitud_recibida_view,
)

app_name = "cotizaciones"

urlpatterns = [
    path("", mi_cotizacion_view, name="mi_cotizacion"),
    path("agregar/", agregar_item_view, name="agregar_item"),
    path("actualizar/", actualizar_cantidad_view, name="actualizar_cantidad"),
    path("eliminar/", eliminar_item_view, name="eliminar_item"),
    path("vaciar/", vaciar_canasta_view, name="vaciar_canasta"),
    path("solicitar/", solicitar_cotizacion_view, name="solicitar_cotizacion"),
    path("recibida/<uuid:token>/", solicitud_recibida_view, name="solicitud_recibida"),
]
