"""
Utilidades para cálculo de rangos de fechas de períodos en la plataforma de gestión.
"""

from datetime import datetime, time
from django.utils import timezone


def obtener_rango_fechas(periodo="30_dias", fecha_desde_str="", fecha_hasta_str=""):
    """
    Retorna (fecha_inicio, fecha_fin, nombre_etiqueta) conscientes de zona horaria (timezone-aware).
    """
    ahora = timezone.now()
    hoy_inicio = timezone.make_aware(datetime.combine(ahora.date(), time.min))
    hoy_fin = timezone.make_aware(datetime.combine(ahora.date(), time.max))

    if periodo == "hoy":
        return hoy_inicio, hoy_fin, "Hoy"

    elif periodo == "7_dias":
        inicio = hoy_fin - timezone.timedelta(days=7)
        return inicio, hoy_fin, "Últimos 7 días"

    elif periodo == "este_mes":
        primer_dia = ahora.date().replace(day=1)
        inicio = timezone.make_aware(datetime.combine(primer_dia, time.min))
        return inicio, hoy_fin, "Este mes"

    elif periodo == "mes_anterior":
        primer_dia_este = ahora.date().replace(day=1)
        ultimo_dia_anterior = primer_dia_este - timezone.timedelta(days=1)
        primer_dia_anterior = ultimo_dia_anterior.replace(day=1)
        inicio = timezone.make_aware(datetime.combine(primer_dia_anterior, time.min))
        fin = timezone.make_aware(datetime.combine(ultimo_dia_anterior, time.max))
        return inicio, fin, "Mes anterior"

    elif periodo == "personalizado" and fecha_desde_str and fecha_hasta_str:
        try:
            d_desde = datetime.strptime(fecha_desde_str, "%Y-%m-%d").date()
            d_hasta = datetime.strptime(fecha_hasta_str, "%Y-%m-%d").date()
            inicio = timezone.make_aware(datetime.combine(d_desde, time.min))
            fin = timezone.make_aware(datetime.combine(d_hasta, time.max))
            return inicio, fin, f"Desde {fecha_desde_str} hasta {fecha_hasta_str}"
        except ValueError:
            pass

    # Predeterminado: Últimos 30 días
    inicio = hoy_fin - timezone.timedelta(days=30)
    return inicio, hoy_fin, "Últimos 30 días"
