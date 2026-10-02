"""
Módulo de Selección Masiva de Productos por Lista de SKU (/gestion/productos/seleccion-sku/).
Implementa Bloque B del Plan de Gestión Simplificada y Ajuste Obligatorio #7 (Selección masiva segura).
"""

import re
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render, redirect
from apps.gestion.decorators import gestion_required, permiso_requerido
from apps.gestion.services_auditoria import registrar_actividad
from apps.catalogo.models import Producto


def parsear_skus(texto):
    """
    Parsea texto libre separando por saltos de línea, comas, puntos y comas, o espacios/tabs.
    Normaliza a mayúsculas, elimina espacios y deduplica preservando el orden de aparición.
    """
    if not texto:
        return []
    # Separar por salto de línea, coma, punto y coma, tabulador o espacios múltiples
    tokens_raw = re.split(r"[\r\n,;\t]+", texto)
    skus_limpios = []
    vistos = set()
    for t in tokens_raw:
        limpio = t.strip().upper()
        if limpio and limpio not in vistos:
            vistos.add(limpio)
            skus_limpios.append(limpio)
    return skus_limpios


@gestion_required
@permiso_requerido("gestion.can_manage_catalogo")
def productos_seleccion_sku_view(request):
    """
    Vista de dos fases para selección masiva por lista de SKU:
    1. Pre-análisis exhaustivo y diagnóstico sin escrituras en base de datos.
    2. Aplicación segura de marcado como candidatos (exclusivamente para activos sin revisar).
    """
    skus_input = ""
    analisis = None

    if request.method == "POST":
        accion = request.POST.get("accion")
        skus_input = request.POST.get("skus_texto", "").strip()
        tokens = parsear_skus(skus_input)

        if not tokens:
            messages.warning(request, "Debe ingresar al menos un SKU válido en el cuadro de texto.")
            return render(request, "gestion/productos/seleccion_sku.html", {"skus_input": skus_input})

        # Buscar en base de datos por sku_proveedor o por sku_humm
        qs = Producto.objects.filter(
            Q(sku_proveedor__in=tokens) | Q(sku_humm__in=tokens)
        ).select_related("categoria", "proveedor").prefetch_related("imagenes")

        productos_encontrados = list(qs)
        mapa_sku_proveedor = {p.sku_proveedor.upper(): p for p in productos_encontrados}
        mapa_sku_humm = {p.sku_humm.upper(): p for p in productos_encontrados}

        # Separar encontrados de faltantes
        tokens_encontrados = set()
        for p in productos_encontrados:
            tokens_encontrados.add(p.sku_proveedor.upper())
            tokens_encontrados.add(p.sku_humm.upper())

        faltantes = [t for t in tokens if t not in tokens_encontrados]

        # Clasificación de productos encontrados (Ajuste 3: regla genérica activo=False)
        aptos_candidato = []
        ya_publicados = []
        validados_no_pub = []
        en_curaduria = []
        ya_candidatos = []
        descartados_previos = []
        inactivos_cuarentena = []
        sin_imagen = []

        diagnostico_filas = []

        for token in tokens:
            p = mapa_sku_proveedor.get(token) or mapa_sku_humm.get(token)
            if not p:
                diagnostico_filas.append({
                    "token": token,
                    "producto": None,
                    "estado_desc": "No encontrado en maestro",
                    "apto": False,
                    "clase_badge": "badge-rojo",
                    "motivo": "El SKU no existe en la base unificada de abastecimiento.",
                })
                continue

            tiene_imagen = p.imagenes.filter(archivo__isnull=False).exclude(archivo="").exists()
            if not tiene_imagen:
                sin_imagen.append(p)

            # Clasificar
            if not p.activo:
                inactivos_cuarentena.append(p)
                diagnostico_filas.append({
                    "token": token,
                    "producto": p,
                    "estado_desc": "Inactivo / Cuarentena",
                    "apto": False,
                    "clase_badge": "badge-rojo",
                    "motivo": "Producto inactivo (activo=False). Excluido de operaciones comerciales.",
                })
            elif p.publicado:
                ya_publicados.append(p)
                diagnostico_filas.append({
                    "token": token,
                    "producto": p,
                    "estado_desc": "Ya Publicado",
                    "apto": False,
                    "clase_badge": "badge-verde",
                    "motivo": "Ya está visible en catálogo escolar.",
                })
            elif p.estado_curaduria == "VALIDADO":
                validados_no_pub.append(p)
                diagnostico_filas.append({
                    "token": token,
                    "producto": p,
                    "estado_desc": "Validado (no publicado)",
                    "apto": False,
                    "clase_badge": "badge-amarillo",
                    "motivo": "Ya tiene curaduría validada. Pasar directo a módulo de publicación.",
                })
            elif p.estado_curaduria == "CANDIDATO":
                ya_candidatos.append(p)
                diagnostico_filas.append({
                    "token": token,
                    "producto": p,
                    "estado_desc": "Ya es Candidato",
                    "apto": False,
                    "clase_badge": "badge-info",
                    "motivo": "Ya se encuentra en cola de curaduría.",
                })
            elif p.estado_curaduria == "EN_CURADURIA":
                en_curaduria.append(p)
                diagnostico_filas.append({
                    "token": token,
                    "producto": p,
                    "estado_desc": "En Curaduría",
                    "apto": False,
                    "clase_badge": "badge-info",
                    "motivo": "En proceso de revisión pedagógica.",
                })
            elif p.estado_curaduria == "DESCARTADO_CATALOGO_PUBLICO":
                descartados_previos.append(p)
                # Permitir re-marcar como candidato si Humm decide re-evaluarlo
                aptos_candidato.append(p)
                diagnostico_filas.append({
                    "token": token,
                    "producto": p,
                    "estado_desc": "Descartado previo (Re-evaluable)",
                    "apto": True,
                    "clase_badge": "badge-gris",
                    "motivo": "Fue descartado antes, pero está activo. Se puede reactivar como candidato.",
                })
            elif p.estado_curaduria == "SIN_REVISAR":
                aptos_candidato.append(p)
                diagnostico_filas.append({
                    "token": token,
                    "producto": p,
                    "estado_desc": "Sin revisar (Apto)",
                    "apto": True,
                    "clase_badge": "badge-azul",
                    "motivo": "Apto para marcar como candidato e iniciar curaduría.",
                })
            else:
                diagnostico_filas.append({
                    "token": token,
                    "producto": p,
                    "estado_desc": p.get_estado_curaduria_display(),
                    "apto": False,
                    "clase_badge": "badge-gris",
                    "motivo": "Estado actual no requiere acción.",
                })

        # ACCIÓN 2: Confirmar y marcar como candidatos
        if accion == "confirmar_marcado_candidatos":
            ids_aptos = [p.id for p in aptos_candidato]
            if not ids_aptos:
                messages.warning(request, "No hay productos aptos para marcar como candidatos en la lista enviada.")
            else:
                # Regla Ajuste 3 y 7: solo activos y elegibles
                actualizados = Producto.objects.filter(
                    id__in=ids_aptos,
                    activo=True,
                ).update(estado_curaduria="CANDIDATO")

                registrar_actividad(
                    request=request,
                    accion="MARCAR_CANDIDATOS_SKU_MASIVO",
                    modelo_afectado="Producto",
                    objeto_id="",
                    descripcion=f"Marcó masivamente {actualizados} productos como CANDIDATO mediante lista de SKU.",
                    detalles={
                        "total_tokens": len(tokens),
                        "actualizados": actualizados,
                        "faltantes": len(faltantes),
                        "ya_publicados": len(ya_publicados),
                        "inactivos": len(inactivos_cuarentena),
                    }
                )

                messages.success(
                    request,
                    f"¡Operación exitosa! {actualizados} productos marcados como CANDIDATO a catálogo público. "
                    f"Omitidos: {len(ya_publicados)} ya publicados, {len(inactivos_cuarentena)} inactivos/cuarentena, "
                    f"{len(faltantes)} no encontrados."
                )
                return redirect("gestion:productos_candidatos")

        analisis = {
            "total_tokens": len(tokens),
            "total_encontrados": len(productos_encontrados),
            "total_faltantes": len(faltantes),
            "faltantes": faltantes,
            "aptos_candidato_count": len(aptos_candidato),
            "ya_publicados_count": len(ya_publicados),
            "validados_no_pub_count": len(validados_no_pub),
            "en_curaduria_count": len(en_curaduria),
            "ya_candidatos_count": len(ya_candidatos),
            "inactivos_cuarentena_count": len(inactivos_cuarentena),
            "sin_imagen_count": len(sin_imagen),
            "diagnostico_filas": diagnostico_filas,
            "ids_aptos_csv": ",".join(str(p.id) for p in aptos_candidato),
        }

    context = {
        "skus_input": skus_input,
        "analisis": analisis,
    }
    return render(request, "gestion/productos/seleccion_sku.html", context)
