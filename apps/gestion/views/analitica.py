"""
Vistas de analítica, telemetría y demanda no cubierta (/gestion/analitica/).
Cumple con los Ajustes Obligatorios #4 (Sesión no es profesor), #17 (Distinción demanda vs venta)
y #24 (Demanda No Cubierta) de Humm.
"""

from decimal import Decimal
from django.db.models import Count, Sum, Q
from django.shortcuts import render
from apps.gestion.decorators import gestion_required, permiso_requerido
from apps.gestion.models import EventoUso
from apps.gestion.utils_periodos import obtener_rango_fechas
from apps.catalogo.models import Producto
from apps.cotizaciones.models import SolicitudItem, SolicitudCotizacion


@gestion_required
@permiso_requerido("gestion.can_view_analitica")
def analitica_uso_view(request):
    """
    Telemetría de uso global, sesiones únicas y desglose de eventos por período.
    """
    periodo = request.GET.get("periodo", "30_dias")
    fecha_inicio, fecha_fin, periodo_label = obtener_rango_fechas(periodo=periodo)

    eventos = EventoUso.objects.filter(created_at__gte=fecha_inicio, created_at__lte=fecha_fin)
    total_eventos = eventos.count()
    sesiones_unicas = eventos.values("session_hash").distinct().count() if total_eventos > 0 else 0

    # Eventos por tipo
    conteo_por_tipo = eventos.values("tipo_evento").annotate(total=Count("id")).order_by("-total")

    # Fuentes de tráfico UTM más frecuentes
    fuentes_ranking = (
        eventos.exclude(fuente="")
        .values("fuente")
        .annotate(total=Count("id"))
        .order_by("-total")[:10]
    )

    campanas_ranking = (
        eventos.exclude(utm_campaign="")
        .values("utm_campaign", "utm_source")
        .annotate(total=Count("id"))
        .order_by("-total")[:10]
    )

    context = {
        "periodo": periodo,
        "periodo_label": periodo_label,
        "total_eventos": total_eventos,
        "sesiones_unicas": sesiones_unicas if total_eventos > 0 else None,
        "conteo_por_tipo": conteo_por_tipo,
        "fuentes_ranking": fuentes_ranking,
        "campanas_ranking": campanas_ranking,
    }
    return render(request, "gestion/analitica/uso.html", context)


@gestion_required
@permiso_requerido("gestion.can_view_analitica")
def analitica_productos_view(request):
    """
    Rankings de demanda de productos y matriz de alerta Alta vista / baja solicitud.
    Ajuste #17: Usa 'Productos en solicitudes cerradas' en lugar de 'Más vendidos'.
    """
    periodo = request.GET.get("periodo", "30_dias")
    fecha_inicio, fecha_fin, periodo_label = obtener_rango_fechas(periodo=periodo)

    # 1. Más Vistos en el período
    mas_vistos = (
        EventoUso.objects.filter(tipo_evento="VER_PRODUCTO", created_at__gte=fecha_inicio, created_at__lte=fecha_fin)
        .values("producto__id", "producto__nombre_comercial", "producto__sku_humm")
        .annotate(total_vistas=Count("id"))
        .order_by("-total_vistas")[:15]
    )

    # 2. Más Agregados a Mi Cotización
    mas_agregados = (
        EventoUso.objects.filter(tipo_evento="AGREGAR_COTIZACION", created_at__gte=fecha_inicio, created_at__lte=fecha_fin)
        .values("producto__id", "producto__nombre_comercial", "producto__sku_humm")
        .annotate(total_agregados=Count("id"))
        .order_by("-total_agregados")[:15]
    )

    # 3. Más Solicitados en Solicitudes (Ítems y unidades)
    solicitudes_periodo = SolicitudCotizacion.objects.filter(
        created_at__gte=fecha_inicio,
        created_at__lte=fecha_fin,
        es_prueba=False
    )
    items_periodo = SolicitudItem.objects.filter(solicitud__in=solicitudes_periodo)

    mas_solicitados = (
        items_periodo.values("nombre_comercial_snapshot", "sku_humm_snapshot")
        .annotate(
            unidades_totales=Sum("cantidad"),
            monto_total=Sum("subtotal_referencial_snapshot"),
            conteo_solicitudes=Count("solicitud", distinct=True)
        )
        .order_by("-unidades_totales")[:15]
    )

    # 4. Productos en solicitudes cerradas (Ajuste Obligatorio #17)
    items_cerradas = items_periodo.filter(solicitud__estado="CERRADA")
    en_solicitudes_cerradas = (
        items_cerradas.values("nombre_comercial_snapshot", "sku_humm_snapshot")
        .annotate(
            unidades_cerradas=Sum("cantidad"),
            solicitudes_cerradas_conteo=Count("solicitud", distinct=True)
        )
        .order_by("-unidades_cerradas")[:15]
    )

    # 5. Matriz de Alerta: Alta vista / baja solicitud
    # Productos con más de 5 vistas en el período pero 0 solicitudes
    skus_solicitados = set(items_periodo.values_list("sku_humm_snapshot", flat=True))
    alta_vista_baja_solicitud = []
    for mv in mas_vistos:
        sku = mv.get("producto__sku_humm")
        if sku and sku not in skus_solicitados and mv["total_vistas"] >= 3:
            alta_vista_baja_solicitud.append(mv)

    context = {
        "periodo": periodo,
        "periodo_label": periodo_label,
        "mas_vistos": mas_vistos,
        "mas_agregados": mas_agregados,
        "mas_solicitados": mas_solicitados,
        "en_solicitudes_cerradas": en_solicitudes_cerradas,
        "alta_vista_baja_solicitud": alta_vista_baja_solicitud,
    }
    return render(request, "gestion/analitica/productos.html", context)


@gestion_required
@permiso_requerido("gestion.can_view_analitica")
def analitica_busquedas_view(request):
    """
    Analítica de búsquedas y bloque de Demanda No Cubierta (Ajuste Obligatorio #24).
    """
    periodo = request.GET.get("periodo", "30_dias")
    fecha_inicio, fecha_fin, periodo_label = obtener_rango_fechas(periodo=periodo)

    busquedas_qs = EventoUso.objects.filter(
        tipo_evento="BUSQUEDA",
        created_at__gte=fecha_inicio,
        created_at__lte=fecha_fin
    ).exclude(termino_busqueda_normalizado="")

    total_busquedas = busquedas_qs.count()
    terminos_unicos = busquedas_qs.values("termino_busqueda_normalizado").distinct().count()

    busquedas_con_resultado = busquedas_qs.filter(resultados_busqueda__gt=0).count()
    busquedas_sin_resultado = busquedas_qs.filter(Q(resultados_busqueda=0) | Q(resultados_busqueda__isnull=True)).count()

    # Búsquedas más frecuentes generales
    top_busquedas = (
        busquedas_qs.values("termino_busqueda_normalizado")
        .annotate(total=Count("id"))
        .order_by("-total")[:20]
    )

    # BLOQUE DESTACADO: DEMANDA NO CUBIERTA (Ajuste Obligatorio #24)
    # Ranking de búsquedas con 0 resultados devueltos
    demanda_no_cubierta = (
        busquedas_qs.filter(Q(resultados_busqueda=0) | Q(resultados_busqueda__isnull=True))
        .values("termino_busqueda_normalizado")
        .annotate(veces=Count("id"), ultima_fecha=Sum("id"))  # ordenamiento
        .order_by("-veces")[:25]
    )

    context = {
        "periodo": periodo,
        "periodo_label": periodo_label,
        "total_busquedas": total_busquedas,
        "terminos_unicos": terminos_unicos,
        "busquedas_con_resultado": busquedas_con_resultado,
        "busquedas_sin_resultado": busquedas_sin_resultado,
        "top_busquedas": top_busquedas,
        "demanda_no_cubierta": demanda_no_cubierta,
    }
    return render(request, "gestion/analitica/busquedas.html", context)
