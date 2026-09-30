"""
Vistas de administración de configuración y parámetros de pricing (/gestion/configuracion/).
Cumple con el Ajuste Obligatorio #15 de Humm:
- Previsualización obligatoria del impacto antes de recalcular.
- Confirmación explícita con alcance seleccionable (catálogo completo, activos, públicos).
- Registro estricto en auditoría.
- Cero exposición de secretos o variables de entorno.
"""

from decimal import Decimal
from django.contrib import messages
from django.shortcuts import render, redirect
from apps.gestion.decorators import gestion_required, permiso_requerido
from apps.gestion.services_auditoria import registrar_actividad
from apps.core.models import ConfiguracionPricing
from apps.catalogo.models import Producto


@gestion_required
@permiso_requerido("gestion.can_manage_configuracion")
def configuracion_pricing_view(request):
    """
    Gestión de parámetros financieros y flujo de recálculo con previsualización de impacto.
    """
    config = ConfiguracionPricing.get_solo()

    simulacion = None
    modo = request.GET.get("modo", "ver")

    if request.method == "POST":
        accion = request.POST.get("accion")

        # 1. Guardar parámetros sin recalcular productos
        if accion == "guardar_parametros":
            tc_raw = request.POST.get("tipo_cambio_usd_clp")
            recargo_raw = request.POST.get("recargo_general_porcentaje")
            internacion_raw = request.POST.get("factor_internacion_flete_porcentaje")
            iva_raw = request.POST.get("iva_porcentaje")
            email_notif = request.POST.get("email_notificaciones_humm", "").strip()

            try:
                tc_ant = config.tipo_cambio_usd_clp
                rec_ant = config.recargo_general_porcentaje
                int_ant = config.factor_internacion_flete_porcentaje

                config.tipo_cambio_usd_clp = Decimal(tc_raw)
                config.recargo_general_porcentaje = Decimal(recargo_raw)
                config.factor_internacion_flete_porcentaje = Decimal(internacion_raw)
                config.iva_porcentaje = Decimal(iva_raw)
                if email_notif:
                    config.email_notificaciones_humm = email_notif
                config.save()

                registrar_actividad(
                    request=request,
                    accion="MODIFICAR_PRICING",
                    modelo_afectado="ConfiguracionPricing",
                    objeto_id="1",
                    descripcion=f"Modificó parámetros: TC ${tc_ant} → ${config.tipo_cambio_usd_clp}, Recargo {rec_ant}% → {config.recargo_general_porcentaje}%",
                    detalles={
                        "tipo_cambio_usd_clp": str(config.tipo_cambio_usd_clp),
                        "recargo_general_porcentaje": str(config.recargo_general_porcentaje),
                        "factor_internacion_flete_porcentaje": str(config.factor_internacion_flete_porcentaje),
                    }
                )
                messages.success(request, "Parámetros de pricing guardados. Los productos NO se han recalculado automáticamente.")
                return redirect("gestion:configuracion")
            except Exception as e:
                messages.error(request, f"Error validando parámetros: {e}")

        # 2. Previsualizar Impacto (Ajuste #15)
        elif accion == "previsualizar_impacto":
            alcance = request.POST.get("alcance", "publicos")
            if alcance == "todos":
                qs = Producto.objects.filter(costo_proveedor_usd__gt=0)
            elif alcance == "activos":
                qs = Producto.objects.filter(activo=True, costo_proveedor_usd__gt=0)
            else:  # publicos
                qs = Producto.objects.filter(publicado=True, activo=True, costo_proveedor_usd__gt=0)

            total_afectados = qs.count()
            
            # Muestra de 5 productos para comparar
            muestra = []
            for p in qs[:5]:
                precio_actual = p.precio_sugerido_total_clp
                p_sim = Producto(costo_proveedor_usd=p.costo_proveedor_usd, porcentaje_recargo=p.porcentaje_recargo)
                p_sim.calcular_precios_sugeridos(config=config)
                precio_nuevo = p_sim.precio_sugerido_total_clp
                dif = precio_nuevo - precio_actual
                pct_dif = ((dif / precio_actual) * 100) if precio_actual > 0 else 0
                muestra.append({
                    "sku": p.sku_humm,
                    "nombre": p.nombre_comercial,
                    "precio_actual": precio_actual,
                    "precio_nuevo": precio_nuevo,
                    "diferencia": dif,
                    "porcentaje": round(pct_dif, 1),
                })

            simulacion = {
                "alcance": alcance,
                "total_afectados": total_afectados,
                "muestra": muestra,
            }

        # 3. Confirmar y Recalcular (Ajuste #15)
        elif accion == "confirmar_recalculo":
            alcance = request.POST.get("alcance", "publicos")
            if alcance == "todos":
                qs = Producto.objects.filter(costo_proveedor_usd__gt=0)
            elif alcance == "activos":
                qs = Producto.objects.filter(activo=True, costo_proveedor_usd__gt=0)
            else:  # publicos
                qs = Producto.objects.filter(publicado=True, activo=True, costo_proveedor_usd__gt=0)

            total_recalculados = 0
            for prod in qs:
                prod.calcular_precios_sugeridos(config=config)
                prod.save(update_fields=["costo_puesto_chile_clp", "precio_sugerido_neto_clp", "precio_sugerido_total_clp", "updated_at"])
                total_recalculados += 1

            registrar_actividad(
                request=request,
                accion="RECALCULAR_PRECIOS_MASIVO",
                modelo_afectado="Producto",
                objeto_id="",
                descripcion=f"Recálculo masivo de precios ejecutado para {total_recalculados} productos (Alcance: {alcance}).",
                detalles={"alcance": alcance, "total_recalculados": total_recalculados}
            )

            messages.success(request, f"¡Recálculo exitoso! Se actualizaron los precios referenciales de {total_recalculados} productos.")
            return redirect("gestion:configuracion")

    context = {
        "config": config,
        "simulacion": simulacion,
    }
    return render(request, "gestion/configuracion/pricing.html", context)
