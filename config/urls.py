"""
URL configuration for EduCompra Humm project.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from apps.catalogo.views import sitemap_view, robots_view
from apps.cotizaciones.views import (
    mi_cotizacion_view,
    agregar_item_view,
    actualizar_cantidad_view,
    eliminar_item_view,
    vaciar_canasta_view,
    solicitar_cotizacion_view,
    solicitud_recibida_view,
)

# Personalización del panel administrativo Django con branding Humm
admin.site.site_header = "EduCompra Humm — Administración Operativa"
admin.site.site_title = "EduCompra Humm"
admin.site.index_title = "Control de Catálogo, Precios y Cotizaciones"

urlpatterns = [
    # Panel de administración interno Humm
    path("admin/", admin.site.urls),

    # SEO canónico
    path("sitemap.xml", sitemap_view, name="sitemap"),
    path("robots.txt", robots_view, name="robots"),

    # Rutas comerciales amigables de cotización en primer nivel
    path("mi-cotizacion/", mi_cotizacion_view, name="mi_cotizacion"),
    path("mi-cotizacion/agregar/", agregar_item_view, name="canasta_agregar"),
    path("mi-cotizacion/actualizar/", actualizar_cantidad_view, name="canasta_actualizar"),
    path("mi-cotizacion/eliminar/", eliminar_item_view, name="canasta_eliminar"),
    path("mi-cotizacion/vaciar/", vaciar_canasta_view, name="canasta_vaciar"),
    path("solicitar-cotizacion/", solicitar_cotizacion_view, name="solicitar_cotizacion"),
    path("solicitud-recibida/<uuid:token>/", solicitud_recibida_view, name="solicitud_recibida"),

    # Apps de dominio
    path("", include("apps.core.urls")),
    path("catalogo/", include("apps.catalogo.urls")),
    path("cotizaciones/", include("apps.cotizaciones.urls")),
]

# Servir archivos multimedia en modo DEBUG
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
