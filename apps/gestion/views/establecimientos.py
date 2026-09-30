"""
Vistas de administración de Establecimientos Educacionales (/gestion/establecimientos/).
"""

from decimal import Decimal
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Sum, Count
from django.shortcuts import render, get_object_or_404, redirect
from apps.gestion.decorators import gestion_required, permiso_requerido
from apps.cotizaciones.models import Establecimiento, SolicitudCotizacion
from apps.core.regiones_chile import REGIONES_CHILE


@gestion_required
@permiso_requerido("gestion.can_manage_establecimientos")
def establecimientos_lista_view(request):
    """
    Directorio de colegios e instituciones educacionales.
    """
    qs = Establecimiento.objects.annotate(
        total_solicitudes=Count("solicitudes", filter=Q(solicitudes__es_prueba=False)),
        monto_historico=Sum("solicitudes__total_referencial_estimado", filter=Q(solicitudes__es_prueba=False))
    )

    q = request.GET.get("q", "").strip()
    if q:
        qs = qs.filter(
            Q(nombre__icontains=q)
            | Q(comuna__icontains=q)
            | Q(rut__icontains=q)
            | Q(rbd__icontains=q)
        )

    region = request.GET.get("region")
    if region:
        qs = qs.filter(region__icontains=region)

    tipo = request.GET.get("tipo")
    if tipo:
        qs = qs.filter(tipo_institucion=tipo)

    conciliacion = request.GET.get("conciliacion")
    if conciliacion:
        qs = qs.filter(estado_conciliacion=conciliacion)

    orden = request.GET.get("orden", "-ultima_interaccion")
    qs = qs.order_by(orden)

    total_establecimientos = qs.count()

    paginator = Paginator(qs, 20)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "total_establecimientos": total_establecimientos,
        "regiones": REGIONES_CHILE,
        "tipos_institucion": Establecimiento.TIPOS_INSTITUCION,
        "estados_conciliacion": Establecimiento.ESTADOS_CONCILIACION,
        "q": q,
        "region_activa": region,
        "tipo_activo": tipo,
        "conciliacion_activa": conciliacion,
        "orden_activo": orden,
    }
    return render(request, "gestion/establecimientos/lista.html", context)


@gestion_required
@permiso_requerido("gestion.can_manage_establecimientos")
def establecimiento_detalle_view(request, id):
    """
    Ficha 360° del establecimiento educacional: contactos, solicitudes históricas y métricas.
    """
    establecimiento = get_object_or_404(
        Establecimiento.objects.prefetch_related("contactos", "solicitudes__items__producto"),
        id=id
    )

    solicitudes = establecimiento.solicitudes.filter(es_prueba=False).order_by("-created_at")
    total_solicitudes = solicitudes.count()
    monto_total_solicitado = solicitudes.aggregate(total=Sum("total_referencial_estimado"))["total"] or Decimal("0")
    monto_total_vendido = solicitudes.filter(estado="CERRADA").aggregate(total=Sum("monto_final_vendido"))["total"] or Decimal("0")
    ticket_promedio = (monto_total_solicitado / total_solicitudes) if total_solicitudes > 0 else Decimal("0")

    # Productos más solicitados por este establecimiento
    from apps.cotizaciones.models import SolicitudItem
    productos_ranking = (
        SolicitudItem.objects.filter(solicitud__establecimiento_ref=establecimiento, solicitud__es_prueba=False)
        .values("nombre_comercial_snapshot", "sku_humm_snapshot")
        .annotate(total_unidades=Sum("cantidad"), total_monto=Sum("subtotal_referencial_snapshot"))
        .order_by("-total_unidades")[:10]
    )

    contactos = establecimiento.contactos.all().order_by("-ultima_interaccion")

    context = {
        "establecimiento": establecimiento,
        "solicitudes": solicitudes,
        "total_solicitudes": total_solicitudes,
        "monto_total_solicitado": monto_total_solicitado,
        "monto_total_vendido": monto_total_vendido,
        "ticket_promedio": ticket_promedio,
        "productos_ranking": productos_ranking,
        "contactos": contactos,
    }
    return render(request, "gestion/establecimientos/detalle.html", context)
