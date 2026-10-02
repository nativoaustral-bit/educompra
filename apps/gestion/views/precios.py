"""
Módulo de Gestión de Pricing, Simulador Reactivo y Recálculo Seguro (/gestion/precios/).
Implementa Bloque E del Plan de Gestión Simplificada y Ajustes Obligatorios:
- Ajuste 1: Recálculo global preservando recargos específicos individuales.
- Ajuste 2: Simulación en memoria sin escrituras y aplicación atómica en servidor con rollback total.
"""

from decimal import Decimal, ROUND_HALF_UP
from django.contrib import messages
from django.db import transaction
from django.db.models import Q
from django.shortcuts import render, redirect
from apps.gestion.decorators import gestion_required, permiso_requerido
from apps.gestion.services_auditoria import registrar_actividad
from apps.core.models import ConfiguracionPricing
from apps.catalogo.models import Producto, Categoria
from apps.gestion.views.productos_seleccion import parsear_skus


def simular_precios_en_memoria(productos, tc, flete_pct, recargo_general_pct, iva_pct):
    """
    Calcula en memoria (sin escribir en base de datos) el impacto del cambio de pricing (Ajuste 2).
    Ajuste 1: Si un producto tiene porcentaje_recargo != None, conserva su recargo específico.
    """
    factor_flete = Decimal("1.00") + (flete_pct / Decimal("100.00"))
    factor_iva = Decimal("1.00") + (iva_pct / Decimal("100.00"))

    suma_actual = Decimal("0")
    suma_simulada = Decimal("0")
    total_con_recargo_especifico = 0
    total_con_recargo_general = 0

    muestra = []

    for idx, p in enumerate(productos):
        # Determinar recargo a aplicar (Ajuste 1)
        tiene_especifico = p.porcentaje_recargo is not None
        if tiene_especifico:
            recargo_usado = p.porcentaje_recargo
            total_con_recargo_especifico += 1
        else:
            recargo_usado = recargo_general_pct
            total_con_recargo_general += 1

        factor_recargo = Decimal("1.00") + (recargo_usado / Decimal("100.00"))

        # Cálculo de costo puesto Chile simulado
        costo_chile_sim = (p.costo_proveedor_usd * tc * factor_flete).quantize(
            Decimal("1"), rounding=ROUND_HALF_UP
        ).quantize(Decimal("1.00"))

        # Precio neto simulado
        neto_sim = (costo_chile_sim * factor_recargo).quantize(
            Decimal("1"), rounding=ROUND_HALF_UP
        ).quantize(Decimal("1.00"))

        # Precio total simulado
        total_sim = (neto_sim * factor_iva).quantize(
            Decimal("1"), rounding=ROUND_HALF_UP
        ).quantize(Decimal("1.00"))

        precio_actual = p.precio_sugerido_total_clp
        dif = total_sim - precio_actual
        pct_dif = ((dif / precio_actual) * 100) if precio_actual > 0 else Decimal("0")

        suma_actual += precio_actual
        suma_simulada += total_sim

        # Tomar los primeros 10 productos como muestra de contraste
        if idx < 10:
            muestra.append({
                "sku_humm": p.sku_humm,
                "sku_proveedor": p.sku_proveedor,
                "nombre": p.nombre_comercial,
                "costo_usd": p.costo_proveedor_usd,
                "recargo_usado": recargo_usado,
                "es_especifico": tiene_especifico,
                "precio_actual": precio_actual,
                "precio_simulado": total_sim,
                "diferencia": dif,
                "pct_diferencia": round(pct_dif, 1),
            })

    cant = len(productos)
    prom_actual = (suma_actual / cant) if cant > 0 else Decimal("0")
    prom_simulado = (suma_simulada / cant) if cant > 0 else Decimal("0")
    dif_prom = prom_simulado - prom_actual
    pct_dif_prom = ((dif_prom / prom_actual) * 100) if prom_actual > 0 else Decimal("0")

    return {
        "total_afectados": cant,
        "total_con_recargo_especifico": total_con_recargo_especifico,
        "total_con_recargo_general": total_con_recargo_general,
        "promedio_actual": round(prom_actual, 0),
        "promedio_simulado": round(prom_simulado, 0),
        "diferencia_promedio": round(dif_prom, 0),
        "pct_diferencia_promedio": round(pct_dif_prom, 1),
        "muestra": muestra,
    }


@gestion_required
@permiso_requerido("gestion.can_manage_configuracion")
def precios_dashboard_view(request):
    """
    Dashboard del módulo de pricing:
    1. Visualización de parámetros actuales (TC, flete, recargo comercial general, IVA).
    2. Simulador en memoria con contraste de impacto (Ajuste 2).
    3. Aplicación server-side atómica con recálculo global preservando recargos específicos (Ajustes 1 y 2).
    4. Ajuste comercial explícito de recargos específicos por categoría o lista de SKU.
    """
    config = ConfiguracionPricing.get_solo()
    categorias = Categoria.objects.filter(activa=True).order_by("orden", "nombre")

    simulacion = None
    parametros_sim = {
        "tipo_cambio": str(config.tipo_cambio_usd_clp),
        "factor_internacion": str(config.factor_internacion_flete_porcentaje),
        "recargo_general": str(config.recargo_general_porcentaje),
        "iva": str(config.iva_porcentaje),
        "alcance": "activos",
    }

    if request.method == "POST":
        accion = request.POST.get("accion")

        # -------------------------------------------------------------
        # ACCIÓN 1: SIMULAR EN MEMORIA (Ajuste 2)
        # -------------------------------------------------------------
        if accion == "simular_impacto":
            try:
                tc = Decimal(request.POST.get("tipo_cambio", config.tipo_cambio_usd_clp))
                flete = Decimal(request.POST.get("factor_internacion", config.factor_internacion_flete_porcentaje))
                recargo = Decimal(request.POST.get("recargo_general", config.recargo_general_porcentaje))
                iva = Decimal(request.POST.get("iva", config.iva_porcentaje))
                alcance = request.POST.get("alcance", "activos")

                parametros_sim = {
                    "tipo_cambio": str(tc),
                    "factor_internacion": str(flete),
                    "recargo_general": str(recargo),
                    "iva": str(iva),
                    "alcance": alcance,
                }

                # Determinar alcance
                if alcance == "publicados":
                    qs = Producto.objects.filter(activo=True, publicado=True, costo_proveedor_usd__gt=0)
                else:  # activos
                    qs = Producto.objects.filter(activo=True, costo_proveedor_usd__gt=0)

                productos_sim = list(qs.select_related("categoria"))
                simulacion = simular_precios_en_memoria(productos_sim, tc, flete, recargo, iva)
                simulacion["alcance"] = alcance
                messages.info(request, f"Simulación calculada en memoria para {simulacion['total_afectados']} productos. Ningún precio fue modificado.")

            except Exception as e:
                messages.error(request, f"Error en los parámetros de simulación: {e}")

        # -------------------------------------------------------------
        # ACCIÓN 2: APLICAR CAMBIO GLOBAL EN SERVIDOR (Ajustes 1 y 2)
        # -------------------------------------------------------------
        elif accion == "aplicar_precios_servidor":
            try:
                # El servidor NO confía en precios del browser. Re-obtiene parámetros y re-calcula (Ajuste 2).
                nuevo_tc = Decimal(request.POST.get("tipo_cambio"))
                nuevo_flete = Decimal(request.POST.get("factor_internacion"))
                nuevo_recargo = Decimal(request.POST.get("recargo_general"))
                nuevo_iva = Decimal(request.POST.get("iva"))
                alcance = request.POST.get("alcance", "activos")

                with transaction.atomic():
                    # 1. Guardar nueva configuración en BD
                    config_actual = ConfiguracionPricing.get_solo()
                    tc_anterior = config_actual.tipo_cambio_usd_clp
                    rec_anterior = config_actual.recargo_general_porcentaje

                    config_actual.tipo_cambio_usd_clp = nuevo_tc
                    config_actual.factor_internacion_flete_porcentaje = nuevo_flete
                    config_actual.recargo_general_porcentaje = nuevo_recargo
                    config_actual.iva_porcentaje = nuevo_iva
                    config_actual.save()

                    # 2. Determinar productos afectados (Ajuste 3: regla genérica activo=True)
                    if alcance == "publicados":
                        qs = Producto.objects.filter(activo=True, publicado=True, costo_proveedor_usd__gt=0)
                    else:  # activos
                        qs = Producto.objects.filter(activo=True, costo_proveedor_usd__gt=0)

                    productos = list(qs)
                    total_recalculados = 0
                    con_recargo_especifico = 0

                    for p in productos:
                        if p.porcentaje_recargo is not None:
                            con_recargo_especifico += 1
                        # calcular_precios_sugeridos respeta p.porcentaje_recargo si no es None (Ajuste 1)
                        p.calcular_precios_sugeridos(config=config_actual)
                        p.save(update_fields=[
                            "costo_puesto_chile_clp",
                            "precio_sugerido_neto_clp",
                            "precio_sugerido_total_clp",
                            "updated_at"
                        ])
                        total_recalculados += 1

                    # 3. Registrar auditoría SOLO tras éxito completo (Ajuste 2)
                    registrar_actividad(
                        request=request,
                        accion="APLICAR_CAMBIO_PRICING_GLOBAL",
                        modelo_afectado="ConfiguracionPricing",
                        objeto_id="1",
                        descripcion=(
                            f"Cambio global de pricing aplicado a {total_recalculados} productos. "
                            f"TC: ${tc_anterior} → ${nuevo_tc}, Recargo General: {rec_anterior}% → {nuevo_recargo}%. "
                            f"{con_recargo_especifico} productos conservaron su recargo específico."
                        ),
                        detalles={
                            "tipo_cambio": str(nuevo_tc),
                            "factor_internacion": str(nuevo_flete),
                            "recargo_general": str(nuevo_recargo),
                            "iva": str(nuevo_iva),
                            "alcance": alcance,
                            "total_recalculados": total_recalculados,
                            "con_recargo_especifico": con_recargo_especifico,
                        }
                    )

                messages.success(
                    request,
                    f"✓ Precios aplicados exitosamente a {total_recalculados} productos. "
                    f"({con_recargo_especifico} productos con recargo específico recalcularon manteniendo su recargo propio)."
                )
                return redirect("gestion:precios_dashboard")

            except Exception as e:
                # Ajuste 2: Rollback total si ocurre cualquier error
                messages.error(request, f"Error durante la aplicación de precios. Toda la operación fue revertida: {str(e)}")

        # -------------------------------------------------------------
        # ACCIÓN 3: ASIGNAR RECARGO ESPECÍFICO POR CATEGORÍA O SKU (Ajuste 1)
        # -------------------------------------------------------------
        elif accion == "asignar_recargo_especifico":
            tipo_seleccion = request.POST.get("tipo_seleccion")
            nuevo_recargo_str = request.POST.get("porcentaje_recargo_especifico", "").strip()
            limpiar = request.POST.get("limpiar_recargo") == "1"

            try:
                nuevo_recargo_val = None if limpiar else Decimal(nuevo_recargo_str)

                if tipo_seleccion == "categoria":
                    cat_id = request.POST.get("categoria_id")
                    if not cat_id:
                        messages.warning(request, "Debe seleccionar una categoría.")
                        return redirect("gestion:precios_dashboard")
                    qs = Producto.objects.filter(categoria_id=cat_id, activo=True)
                    desc_target = f"categoría ID {cat_id}"
                else:  # sku_lista
                    skus_raw = request.POST.get("skus_lista", "")
                    tokens = parsear_skus(skus_raw)
                    if not tokens:
                        messages.warning(request, "Debe ingresar al menos un SKU válido.")
                        return redirect("gestion:precios_dashboard")
                    qs = Producto.objects.filter(
                        Q(sku_proveedor__in=tokens) | Q(sku_humm__in=tokens),
                        activo=True
                    )
                    desc_target = f"{len(tokens)} SKU(s)"

                productos_afectados = list(qs)
                if not productos_afectados:
                    messages.warning(request, f"No se encontraron productos activos para {desc_target}.")
                    return redirect("gestion:precios_dashboard")

                with transaction.atomic():
                    config_actual = ConfiguracionPricing.get_solo()
                    for p in productos_afectados:
                        p.porcentaje_recargo = nuevo_recargo_val
                        p.calcular_precios_sugeridos(config=config_actual)
                        p.save(update_fields=[
                            "porcentaje_recargo",
                            "costo_puesto_chile_clp",
                            "precio_sugerido_neto_clp",
                            "precio_sugerido_total_clp",
                            "updated_at"
                        ])

                    accion_desc = "Eliminó recargo específico (vuelve a general)" if limpiar else f"Asignó recargo específico de {nuevo_recargo_val}%"
                    registrar_actividad(
                        request=request,
                        accion="ASIGNAR_RECARGO_ESPECIFICO",
                        modelo_afectado="Producto",
                        objeto_id="",
                        descripcion=f"{accion_desc} a {len(productos_afectados)} productos ({desc_target}).",
                        detalles={
                            "target": desc_target,
                            "nuevo_recargo": str(nuevo_recargo_val),
                            "total_afectados": len(productos_afectados),
                        }
                    )

                msg = f"✓ Recargo específico actualizado para {len(productos_afectados)} productos."
                messages.success(request, msg)
                return redirect("gestion:precios_dashboard")

            except Exception as e:
                messages.error(request, f"Error asignando recargo específico: {e}")

    # Conteos para el dashboard
    total_activos_con_costo = Producto.objects.filter(activo=True, costo_proveedor_usd__gt=0).count()
    total_publicados_con_costo = Producto.objects.filter(activo=True, publicado=True, costo_proveedor_usd__gt=0).count()
    total_con_recargo_personalizado = Producto.objects.filter(activo=True, porcentaje_recargo__isnull=False).count()

    context = {
        "config": config,
        "categorias": categorias,
        "simulacion": simulacion,
        "parametros_sim": parametros_sim,
        "total_activos_con_costo": total_activos_con_costo,
        "total_publicados_con_costo": total_publicados_con_costo,
        "total_con_recargo_personalizado": total_con_recargo_personalizado,
    }
    return render(request, "gestion/precios/dashboard.html", context)
