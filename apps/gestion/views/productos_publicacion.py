"""
Módulo de Publicación y Despublicación Masiva Controlada (/gestion/productos/publicacion-lote/ y despublicacion-lote/).
Implementa Bloque D del Plan de Gestión Simplificada y Ajuste Obligatorio #6 (Puerta única de publicación).
"""

from django.contrib import messages
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from apps.gestion.decorators import gestion_required, permiso_requerido
from apps.gestion.services_auditoria import registrar_actividad
from apps.catalogo.models import Producto
from apps.catalogo.services_publicacion import ProductoPublicationService


@gestion_required
@permiso_requerido("gestion.can_publish_producto")
def productos_publicacion_lote_view(request):
    """
    Evaluación y publicación por lote con previsualización obligatoria (Ajuste 6).
    Separa exhaustivamente productos LISTOS vs BLOQUEADOS usando ProductoPublicationService.
    Publica individualmente y con trazabilidad cada producto listo.
    """
    ids_param = request.GET.get("ids", "").strip()
    if not ids_param and request.method == "POST":
        ids_param = request.POST.get("ids", "").strip()

    if not ids_param:
        messages.warning(request, "No se seleccionaron productos para evaluar publicación.")
        return redirect("gestion:productos_lista")

    ids_lista = [i.strip() for i in ids_param.split(",") if i.strip().isdigit()]
    productos = list(
        Producto.objects.filter(id__in=ids_lista)
        .select_related("categoria", "proveedor")
        .prefetch_related("imagenes")
    )

    if not productos:
        messages.warning(request, "No se encontraron productos con los identificadores suministrados.")
        return redirect("gestion:productos_lista")

    # 1. Evaluar cada producto con ProductoPublicationService
    listos = []
    bloqueados = []
    ya_publicados = []

    for p in productos:
        if p.publicado:
            ya_publicados.append(p)
            continue

        motivos = ProductoPublicationService.validar_para_publicacion(p)
        if motivos:
            bloqueados.append({
                "producto": p,
                "motivos": motivos,
            })
        else:
            listos.append(p)

    # 2. Confirmación y Ejecución de Publicación
    if request.method == "POST" and request.POST.get("accion") == "confirmar_publicacion":
        publicados_ok = []
        errores_inesperados = []

        for p in listos:
            try:
                ProductoPublicationService.publicar(p, usuario=request.user, request=request)
                publicados_ok.append(p)
            except ValidationError as ve:
                errores_inesperados.append({"producto": p, "error": str(ve)})
            except Exception as e:
                errores_inesperados.append({"producto": p, "error": f"Error inesperado: {str(e)}"})

        registrar_actividad(
            request=request,
            accion="PUBLICACION_MASIVA_LOTE",
            modelo_afectado="Producto",
            objeto_id="",
            descripcion=f"Publicación masiva: {len(publicados_ok)} publicados con éxito, {len(bloqueados)} bloqueados omitidos.",
            detalles={
                "publicados_count": len(publicados_ok),
                "bloqueados_count": len(bloqueados),
                "errores_count": len(errores_inesperados),
                "skus_publicados": [p.sku_humm for p in publicados_ok],
            }
        )

        msg = f"✓ {len(publicados_ok)} producto(s) publicado(s) exitosamente en el catálogo escolar."
        if bloqueados:
            msg += f" {len(bloqueados)} producto(s) bloqueado(s) permanecieron sin cambios."
        if errores_inesperados:
            msg += f" {len(errores_inesperados)} error(es) inesperado(s)."

        messages.success(request, msg)
        return redirect("gestion:productos_lista")

    context = {
        "productos": productos,
        "ids_param": ids_param,
        "listos": listos,
        "bloqueados": bloqueados,
        "ya_publicados": ya_publicados,
        "total_evaluados": len(productos),
        "total_listos": len(listos),
        "total_bloqueados": len(bloqueados),
        "total_ya_publicados": len(ya_publicados),
    }
    return render(request, "gestion/productos/publicacion_lote.html", context)


@gestion_required
@permiso_requerido("gestion.can_publish_producto")
def productos_despublicacion_lote_view(request):
    """
    Despublicación por lote con confirmación explícita (Ajuste #14 de Humm y Bloque D).
    Retira productos de la vista pública sin alterar el catálogo maestro ni cotizaciones históricas.
    """
    ids_param = request.GET.get("ids", "").strip()
    if not ids_param and request.method == "POST":
        ids_param = request.POST.get("ids", "").strip()

    if not ids_param:
        messages.warning(request, "No se seleccionaron productos para despublicar.")
        return redirect("gestion:productos_lista")

    ids_lista = [i.strip() for i in ids_param.split(",") if i.strip().isdigit()]
    productos_publicados = list(
        Producto.objects.filter(id__in=ids_lista, publicado=True)
        .select_related("categoria", "proveedor")
    )

    if not productos_publicados:
        messages.info(request, "Ninguno de los productos seleccionados se encuentra actualmente publicado.")
        return redirect("gestion:productos_lista")

    if request.method == "POST" and request.POST.get("accion") == "confirmar_despublicacion":
        motivo = request.POST.get("motivo_despublicacion", "").strip()
        despublicados = []

        for p in productos_publicados:
            ProductoPublicationService.despublicar(p, usuario=request.user, request=request, motivo=motivo)
            despublicados.append(p)

        registrar_actividad(
            request=request,
            accion="DESPUBLICACION_MASIVA_LOTE",
            modelo_afectado="Producto",
            objeto_id="",
            descripcion=f"Despublicó en lote {len(despublicados)} productos del catálogo escolar.",
            detalles={
                "total_despublicados": len(despublicados),
                "motivo": motivo,
                "skus": [p.sku_humm for p in despublicados],
            }
        )

        messages.info(request, f"Se han retirado {len(despublicados)} producto(s) del catálogo público. Permanecen en el catálogo maestro.")
        return redirect("gestion:productos_lista")

    context = {
        "productos": productos_publicados,
        "ids_param": ids_param,
        "total_publicados": len(productos_publicados),
    }
    return render(request, "gestion/productos/despublicacion_lote.html", context)
