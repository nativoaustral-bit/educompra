from django.http import JsonResponse
from django.shortcuts import render
from django.db import connection

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
    Portada inicial limpia de EduCompra Humm para la Fase 1.
    """
    context = {
        "titulo": "EduCompra Humm — Tecnología Educativa",
        "fase": "Fase 1 — Base Funcional e Infraestructura",
    }
    return render(request, "core/home.html", context)
