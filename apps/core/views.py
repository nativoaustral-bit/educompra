"""
Vistas principales de EduCompra Humm: Portada y comprobación de salud.
"""

from django.http import JsonResponse
from django.shortcuts import render
from django.db import connection
from apps.catalogo.models import Producto, Categoria

def health_check(request):
    """
    Endpoint de comprobación de salud mínimo para monitoreo y CI/CD.
    No expone versiones, rutas, servidores, variables ni configuración interna.
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
        db_status = "ok"
        status_code = 200
    except Exception:
        db_status = "error"
        status_code = 503

    payload = {
        "status": "ok" if db_status == "ok" else "error",
        "db": db_status,
    }
    return JsonResponse(payload, status=status_code)


def home_view(request):
    """
    Portada de EduCompra Humm con buscador principal, categorías destacadas y productos curados.
    """
    from apps.gestion.services_telemetria import TelemetriaService, capturar_utms_en_sesion
    capturar_utms_en_sesion(request)
    TelemetriaService.registrar_evento(request, "VISITA")

    publicables_qs = Producto.objects.publicables(user=request.user)
    
    # Productos destacados
    productos_destacados = publicables_qs.filter(destacado=True)[:8]
    if not productos_destacados.exists():
        productos_destacados = publicables_qs[:8]

    # Categorías activas que tienen productos
    publicables_ids = publicables_qs.values_list("id", flat=True)
    categorias = Categoria.objects.filter(
        productos__id__in=publicables_ids,
        activa=True
    ).distinct().order_by("orden", "nombre")

    es_preview_staff = request.user.is_authenticated and request.user.is_staff

    context = {
        "productos_destacados": productos_destacados,
        "categorias": categorias,
        "total_catalogo": publicables_qs.count(),
        "es_preview_staff": es_preview_staff,
        "disclaimer_precios": "Precios referenciales en pesos chilenos con IVA incluido para fines de presupuesto y postulación a fondos. La cotización formal final será emitida por Humm confirmando disponibilidad y costos logísticos."
    }
    return render(request, "core/home.html", context)
