from django.urls import path
from .views import resumen_solicitud

app_name = "cotizaciones"

urlpatterns = [
    path("solicitud/<str:codigo>/", resumen_solicitud, name="resumen_solicitud"),
]
