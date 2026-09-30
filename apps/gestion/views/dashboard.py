"""
Vista del Dashboard Principal de Gestión Comercial y Operacional (/gestion/).
Cumple con los Ajustes Obligatorios #4, #18, #22, #23 y #29 de Humm.
"""

from decimal import Decimal
from django.db.models import Sum, Count, Q
from django.shortcuts import render
from apps.gestion.decorators import gestion_required
from apps.gestion.models import EventoUso
from apps.gestion.utils_periodos import obtener_rango_fechas
from apps.cotizaciones.models import SolicitudCotizacion, CotizacionFormal, Establecimiento, Contacto


@gestion_required
def dashboard_view(request):
    periodo = request.GET.get("periodo", "30_dias")
    fecha_desde_str = request.GET.get("fecha_desde", "")
    fecha_hasta_str = request.GET.get("fecha_hasta", "")

    fecha_inicio, fecha_fin, periodo_label = obtener_rango_fechas(
        periodo=periodo,
        fecha_desde_str=fecha_desde_str,
        fecha_hasta_str=fecha_hasta_str
    )

    # 1. Base Querysets comerciales (Excluyendo pruebas internas, Ajuste #29)
    solicitudes_qs = SolicitudCotizacion.objects.filter(
        created_at__gte=fecha_inicio,
        created_at__lte=fecha_fin,
        es_prueba=False
    )
    cotizaciones_qs = CotizacionFormal.objects.filter(
        fecha_emision__gte=fecha_inicio.date(),
        fecha_emision__lte=fecha_fin.date()
    )

    # 2. Telemetría de sesiones únicas en el período (Ajuste #4: Sesión no es profesor)
    eventos_qs = EventoUso.objects.filter(created_at__gte=fecha_inicio, created_at__lte=fecha_fin)
    total_eventos = eventos_qs.count()
    sesiones_unicas_count = eventos_qs.values("session_hash").distinct().count() if total_eventos > 0 else 0

    # 3. Métricas Comerciales Estrictamente Separadas (Ajuste #18)
    solicitudes_count = solicitudes_qs.count()
    
    # Establecimientos y contactos únicos con solicitudes en el período
    establecimientos_con_solicitud = solicitudes_qs.values("establecimiento").distinct().count()
    contactos_con_solicitud = solicitudes_qs.values("email").distinct().count()

    # A. Monto Referencial Solicitado
    monto_solicitado = solicitudes_qs.aggregate(total=Sum("total_referencial_estimado"))["total"] or Decimal("0")

    # B. Cotizaciones Formales y Monto Cotizado
    cotizaciones_count = cotizaciones_qs.count()
    monto_cotizado = cotizaciones_qs.aggregate(total=Sum("total"))["total"] or Decimal("0")

    # C. Cierres y Monto Vendido
    solicitudes_cerradas = solicitudes_qs.filter(estado="CERRADA")
    cierres_count = solicitudes_cerradas.count()
    monto_vendido = solicitudes_cerradas.aggregate(total=Sum("monto_final_vendido"))["total"] or Decimal("0")

    # D. Ticket promedio solicitado
    ticket_promedio = (monto_solicitado / solicitudes_count) if solicitudes_count > 0 else None

    # E. Tasa de conversión sesión -> solicitud (%)
    if sesiones_unicas_count > 0 and solicitudes_count > 0:
        tasa_conversion = round((solicitudes_count / sesiones_unicas_count) * 100, 1)
    elif sesiones_unicas_count > 0:
        tasa_conversion = 0.0
    else:
        tasa_conversion = None  # "Sin datos todavía"

    # 4. Alertas Operativas
    solicitudes_nuevas_count = SolicitudCotizacion.objects.filter(estado="NUEVA", es_prueba=False).count()
    solicitudes_sin_responsable_count = SolicitudCotizacion.objects.filter(responsable__isnull=True, es_prueba=False).exclude(estado__in=["CERRADA", "PERDIDA", "CANCELADA"]).count()
    
    # Alerta de validación técnica de compra pública
    solicitudes_pendientes = SolicitudCotizacion.objects.filter(
        estado__in=["NUEVA", "EN_REVISION", "REQUIERE_ANTECEDENTES", "LISTA_PARA_COTIZAR"],
        es_prueba=False
    ).prefetch_related("items__producto")
    solicitudes_requieren_validacion = [s for s in solicitudes_pendientes if s.requiere_validacion_tecnica]

    # 5. Embudo Comercial Visual (Funnel por sesiones únicas, Ajuste #23)
    embudo = []
    if total_eventos > 0 or solicitudes_count > 0:
        sesiones_visita = eventos_qs.filter(tipo_evento="VISITA").values("session_hash").distinct().count()
        sesiones_ver_prod = eventos_qs.filter(tipo_evento="VER_PRODUCTO").values("session_hash").distinct().count()
        sesiones_agregar = eventos_qs.filter(tipo_evento="AGREGAR_COTIZACION").values("session_hash").distinct().count()
        sesiones_iniciar_sol = eventos_qs.filter(tipo_evento="INICIAR_SOLICITUD").values("session_hash").distinct().count()

        # Si no hubo visitas explícitas registradas aún pero sí otras acciones, tomar el máximo
        base_sesiones = max(sesiones_unicas_count, sesiones_visita, 1)

        pasos_raw = [
            ("1. Visita a EduCompra", sesiones_visita or sesiones_unicas_count, "sesiones"),
            ("2. Producto visto", sesiones_ver_prod, "sesiones"),
            ("3. Agregado a Mi Cotización", sesiones_agregar, "sesiones"),
            ("4. Formulario iniciado", sesiones_iniciar_sol, "sesiones"),
            ("5. Solicitud enviada", solicitudes_count, "solicitudes"),
            ("6. Cotización enviada", cotizaciones_count, "cotizaciones"),
            ("7. Venta / Cierre", cierres_count, "ventas"),
        ]

        for idx, (etapa, cant, unidad) in enumerate(pasos_raw):
            pct_base = round((cant / base_sesiones) * 100, 1) if base_sesiones > 0 else 0
            embudo.append({
                "etapa": etapa,
                "cantidad": cant,
                "unidad": unidad,
                "porcentaje": min(pct_base, 100),
            })

    # 6. Últimas 5 solicitudes recibidas para atención rápida
    ultimas_solicitudes = SolicitudCotizacion.objects.filter(es_prueba=False).select_related("establecimiento_ref", "responsable")[:5]

    context = {
        "periodo": periodo,
        "periodo_label": periodo_label,
        "fecha_desde": fecha_desde_str,
        "fecha_hasta": fecha_hasta_str,
        # KPIs principales
        "sesiones_unicas": sesiones_unicas_count if total_eventos > 0 else None,
        "solicitudes_recibidas": solicitudes_count,
        "contactos_con_solicitud": contactos_con_solicitud,
        "establecimientos_con_solicitud": establecimientos_con_solicitud,
        "monto_solicitado": monto_solicitado,
        "cotizaciones_enviadas": cotizaciones_count,
        "monto_cotizado": monto_cotizado,
        "cierres_exitosos": cierres_count,
        "monto_vendido": monto_vendido,
        "ticket_promedio": ticket_promedio,
        "tasa_conversion": tasa_conversion,
        # Alertas operacionales
        "solicitudes_nuevas_count": solicitudes_nuevas_count,
        "solicitudes_sin_responsable_count": solicitudes_sin_responsable_count,
        "requieren_validacion_tecnica_count": len(solicitudes_requieren_validacion),
        # Embudo y listas
        "embudo": embudo,
        "ultimas_solicitudes": ultimas_solicitudes,
    }
    return render(request, "gestion/dashboard.html", context)
