"""
URL configuration for EduCompra Humm project.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Personalización del panel administrativo Django con branding Humm
admin.site.site_header = "EduCompra Humm — Administración Operativa"
admin.site.site_title = "EduCompra Humm"
admin.site.index_title = "Control de Catálogo, Precios y Cotizaciones"

urlpatterns = [
    # Panel de administración interno Humm
    path("admin/", admin.site.urls),

    # Apps de dominio
    path("", include("apps.core.urls")),
    path("catalogo/", include("apps.catalogo.urls")),
    path("cotizaciones/", include("apps.cotizaciones.urls")),
]

# Servir archivos multimedia en modo DEBUG
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
