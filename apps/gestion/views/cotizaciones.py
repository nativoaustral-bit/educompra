"""
Vistas de administración de Cotizaciones Formales (/gestion/cotizaciones/).
Cumple con el candado técnico de compra pública y especificación neutral (VALIDADO_HUMM).
"""

from django.core.paginator import Paginator
from django.db.models import Q, Sum
from django.shortcuts import render, get_object_or_404
from apps.gestion.decorators import gestion_required, permiso_requerido
from apps.cotizaciones.models import CotizacionFormal


@gestion_required
@permiso_requerido("gestion.can_manage_cotizaciones")
def cotizaciones_lista_view(request):
    """
    Listado de cotizaciones formales emitidas por Humm.
    """
    qs = CotizacionFormal.objects.all().select_related("solicitud__establecimiento_ref")

    q = request.GET.get("q", "").strip()
    if q:
        qs = qs.filter(
            Q(numero_cotizacion__icontains=q)
            | Q(solicitud__establecimiento__icontains=q)
            | Q(solicitud__codigo_seguimiento__icontains=q)
            | Q(solicitud__nombre_solicitante__icontains=q)
        )

    total_cotizaciones = qs.count()
    monto_total_cotizado = qs.aggregate(total=Sum("total"))["total"] or 0

    paginator = Paginator(qs, 20)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "total_cotizaciones": total_cotizaciones,
        "monto_total_cotizado": monto_total_cotizado,
        "q": q,
    }
    return render(request, "gestion/cotizaciones/lista.html", context)
