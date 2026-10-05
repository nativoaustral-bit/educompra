"""
Enrutamiento URL de la plataforma de Administración EduCompra Humm (/gestion/).
"""

from django.urls import path
from apps.gestion.views import (
    auth,
    dashboard,
    productos,
    productos_seleccion,
    productos_curaduria,
    productos_publicacion,
    precios,
    importaciones,
    solicitudes,
    establecimientos,
    contactos,
    cotizaciones,
    analitica,
    configuracion,
    exportaciones,
)

app_name = "gestion"

urlpatterns = [
    # Autenticación
    path("login/", auth.login_view, name="login"),
    path("logout/", auth.logout_view, name="logout"),

    # Dashboard Principal
    path("", dashboard.dashboard_view, name="dashboard"),

    # Catálogo & Productos (Gestión Simplificada Fase 5A)
    path("productos/", productos.productos_lista_view, name="productos_lista"),
    path("productos/nuevo/", productos.producto_crear_view, name="producto_crear"),
    path("productos/seleccion-sku/", productos_seleccion.productos_seleccion_sku_view, name="productos_seleccion_sku"),
    path("productos/candidatos/", productos_curaduria.productos_candidatos_view, name="productos_candidatos"),
    path("productos/curaduria-lote/", productos_curaduria.productos_curaduria_lote_view, name="productos_curaduria_lote"),
    path("productos/curaduria-masiva-campos/", productos_curaduria.productos_curaduria_masiva_campos_view, name="productos_curaduria_masiva_campos"),
    path("productos/publicacion-lote/", productos_publicacion.productos_publicacion_lote_view, name="productos_publicacion_lote"),
    path("productos/despublicacion-lote/", productos_publicacion.productos_despublicacion_lote_view, name="productos_despublicacion_lote"),
    path("productos/<int:id>/", productos.producto_detalle_view, name="producto_detalle"),
    path("productos/<int:id>/editar/", productos.producto_editar_view, name="producto_editar"),
    path("productos/<int:id>/toggle-publicado/", productos.producto_toggle_publicado_view, name="producto_toggle_publicado"),

    # Pricing y Simulador
    path("precios/", precios.precios_dashboard_view, name="precios_dashboard"),

    # Importaciones Web Asistidas (DRY-RUN en 6 pasos)
    path("importaciones/", importaciones.importaciones_lista_view, name="importaciones"),
    path("importaciones/subir/", importaciones.importaciones_subir_view, name="importaciones_subir"),
    path("importaciones/<int:id>/", importaciones.importacion_detalle_view, name="importacion_detalle"),
    path("importaciones/<int:id>/aprobar/", importaciones.importacion_aprobar_view, name="importacion_aprobar"),

    # Solicitudes Comerciales
    path("solicitudes/", solicitudes.solicitudes_lista_view, name="solicitudes_lista"),
    path("solicitudes/kanban/", solicitudes.solicitudes_kanban_view, name="solicitudes_kanban"),
    path("solicitudes/eliminar-masivo/", solicitudes.solicitudes_eliminar_masivo_view, name="solicitudes_eliminar_masivo"),
    path("solicitudes/<int:id>/", solicitudes.solicitud_detalle_view, name="solicitud_detalle"),
    path("solicitudes/<int:id>/eliminar/", solicitudes.solicitud_eliminar_view, name="solicitud_eliminar"),
    path("solicitudes/<int:id>/estado/", solicitudes.solicitud_cambiar_estado_view, name="solicitud_cambiar_estado"),

    # Establecimientos y Contactos
    path("establecimientos/", establecimientos.establecimientos_lista_view, name="establecimientos_lista"),
    path("establecimientos/<int:id>/", establecimientos.establecimiento_detalle_view, name="establecimiento_detalle"),
    path("contactos/", contactos.contactos_lista_view, name="contactos_lista"),
    path("contactos/<int:id>/editar/", contactos.contacto_editar_view, name="contacto_editar"),

    # Cotizaciones Formales
    path("cotizaciones/", cotizaciones.cotizaciones_lista_view, name="cotizaciones_lista"),

    # Analítica y Telemetría
    path("analitica/", analitica.analitica_uso_view, name="analitica_uso"),
    path("analitica/productos/", analitica.analitica_productos_view, name="analitica_productos"),
    path("analitica/busquedas/", analitica.analitica_busquedas_view, name="analitica_busquedas"),

    # Configuración de Pricing
    path("configuracion/", configuracion.configuracion_pricing_view, name="configuracion"),

    # Exportaciones CSV
    path("exportar/<str:recurso>/", exportaciones.exportar_csv_view, name="exportar_csv"),
]
