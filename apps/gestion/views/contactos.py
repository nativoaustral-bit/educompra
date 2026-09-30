"""
Vistas de administración de Contactos Docentes e Institucionales (/gestion/contactos/).
"""

from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from apps.gestion.decorators import gestion_required, permiso_requerido
from apps.cotizaciones.models import Contacto


@gestion_required
@permiso_requerido("gestion.can_manage_establecimientos")
def contactos_lista_view(request):
    """
    Directorio de docentes y encargados de compras con filtros y alertas de duplicados.
    """
    qs = Contacto.objects.all().select_related("establecimiento_principal")

    q = request.GET.get("q", "").strip()
    if q:
        qs = qs.filter(
            Q(nombre__icontains=q)
            | Q(email__icontains=q)
            | Q(cargo__icontains=q)
            | Q(telefono__icontains=q)
            | Q(establecimiento_principal__nombre__icontains=q)
        )

    posible_duplicado = request.GET.get("posible_duplicado")
    if posible_duplicado in ("true", "1"):
        qs = qs.filter(posible_duplicado=True)

    orden = request.GET.get("orden", "-ultima_interaccion")
    qs = qs.order_by(orden)

    total_contactos = qs.count()

    paginator = Paginator(qs, 25)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "total_contactos": total_contactos,
        "q": q,
        "duplicados_activos": posible_duplicado,
        "orden_activo": orden,
    }
    return render(request, "gestion/contactos/lista.html", context)
