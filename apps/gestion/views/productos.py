"""
Vistas de administración de catálogo y fichas de producto (/gestion/productos/).
Cumple con los Ajustes Obligatorios #13 (Publicación controlada), #14 (Despublicar),
#16 (Precios derivados inalterables a mano) y #17 (Distinción demanda vs venta) de Humm.
"""

from decimal import Decimal
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.db.models import Q, Count, Sum
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST

from apps.gestion.decorators import gestion_required, permiso_requerido
from apps.gestion.models import EventoUso
from apps.gestion.services_auditoria import registrar_actividad
from apps.catalogo.models import Producto, Categoria, TecnologiaCompatible, Proveedor
from apps.catalogo.services_publicacion import ProductoPublicationService
from apps.cotizaciones.models import SolicitudItem


@gestion_required
@permiso_requerido("gestion.can_manage_catalogo")
def productos_lista_view(request):
    """
    Listado general de administración de catálogo con KPIs dinámicos (Ajuste 4),
    regla genérica de cuarentena activo=False (Ajuste 3), filtros multidimensionales,
    tabs de flujo y barra de acciones en lote.
    """
    # 1. KPIs Dinámicos calculados directamente desde la base de datos (Ajuste 4)
    total_maestro = Producto.objects.count()
    total_publicados = Producto.objects.filter(publicado=True).count()
    total_candidatos = Producto.objects.filter(activo=True, estado_curaduria="CANDIDATO").count()
    total_validados_no_pub = Producto.objects.filter(activo=True, estado_curaduria="VALIDADO", publicado=False).count()
    total_sin_revisar = Producto.objects.filter(activo=True, estado_curaduria="SIN_REVISAR").count()

    ids_con_imagen = Producto.objects.filter(
        activo=True, imagenes__archivo__isnull=False
    ).exclude(imagenes__archivo="").values_list("id", flat=True)
    total_sin_imagen = Producto.objects.filter(activo=True).exclude(id__in=ids_con_imagen).count()
    total_inactivos = Producto.objects.filter(activo=False).count()

    kpis = {
        "total_maestro": total_maestro,
        "total_publicados": total_publicados,
        "total_candidatos": total_candidatos,
        "total_validados_no_pub": total_validados_no_pub,
        "total_sin_revisar": total_sin_revisar,
        "total_sin_imagen": total_sin_imagen,
        "total_inactivos": total_inactivos,
    }

    # 2. Manejo de Acciones en Lote POST desde el listado visual
    if request.method == "POST":
        accion = request.POST.get("accion")
        selected_ids = request.POST.getlist("selected_ids")
        if not selected_ids:
            messages.warning(request, "Debe seleccionar al menos un producto para ejecutar la acción.")
            return redirect(request.get_full_path())

        if accion == "marcar_candidatos":
            # Regla Ajuste 3 y 7: solo activos y en estado SIN_REVISAR
            prods = Producto.objects.filter(id__in=selected_ids, activo=True, estado_curaduria="SIN_REVISAR")
            cant = prods.update(estado_curaduria="CANDIDATO")
            omitidos = len(selected_ids) - cant
            registrar_actividad(
                request=request,
                accion="MARCAR_CANDIDATO_LOTE",
                modelo_afectado="Producto",
                objeto_id="",
                descripcion=f"Marcó {cant} productos como CANDIDATO desde el listado visual.",
                detalles={"total_seleccionados": len(selected_ids), "marcados": cant, "omitidos": omitidos}
            )
            msg = f"{cant} producto(s) marcado(s) como CANDIDATO."
            if omitidos > 0:
                msg += f" ({omitidos} omitidos por estar inactivos, ya candidatos o validados)."
            messages.success(request, msg)
            return redirect(request.get_full_path())

    # 3. Construcción del QuerySet
    qs = Producto.objects.all().select_related("categoria", "proveedor").prefetch_related("imagenes")

    # Tab / Flujo rápido
    tab = request.GET.get("tab", "").strip()
    if tab == "publicados":
        qs = qs.filter(publicado=True)
    elif tab == "candidatos":
        qs = qs.filter(activo=True, estado_curaduria="CANDIDATO")
    elif tab == "validados_no_pub":
        qs = qs.filter(activo=True, estado_curaduria="VALIDADO", publicado=False)
    elif tab == "sin_revisar":
        qs = qs.filter(activo=True, estado_curaduria="SIN_REVISAR")
    elif tab == "sin_imagen":
        qs = qs.filter(activo=True).exclude(id__in=ids_con_imagen)
    elif tab == "inactivos":
        qs = qs.filter(activo=False)

    # Buscador por texto amplio (SKU Humm, SKU proveedor, nombre comercial, original proveedor, marca, modelo)
    q = request.GET.get("q", "").strip()
    if q:
        qs = qs.filter(
            Q(sku_humm__icontains=q)
            | Q(sku_proveedor__icontains=q)
            | Q(nombre_comercial__icontains=q)
            | Q(nombre_original_proveedor__icontains=q)
            | Q(marca__icontains=q)
            | Q(modelo__icontains=q)
        )

    # Filtros multidimensionales
    categoria_id = request.GET.get("categoria")
    if categoria_id:
        qs = qs.filter(categoria_id=categoria_id)

    proveedor_id = request.GET.get("proveedor")
    if proveedor_id:
        qs = qs.filter(proveedor_id=proveedor_id)

    publicado = request.GET.get("publicado")
    if publicado in ("true", "1"):
        qs = qs.filter(publicado=True)
    elif publicado in ("false", "0"):
        qs = qs.filter(publicado=False)

    activo_filtro = request.GET.get("activo")
    if activo_filtro in ("true", "1"):
        qs = qs.filter(activo=True)
    elif activo_filtro in ("false", "0"):
        qs = qs.filter(activo=False)

    curaduria = request.GET.get("curaduria")
    if curaduria:
        qs = qs.filter(estado_curaduria=curaduria)

    validacion = request.GET.get("validacion")
    if validacion:
        qs = qs.filter(estado_especificacion_neutral=validacion)

    stock = request.GET.get("stock")
    if stock:
        qs = qs.filter(estado_stock=stock)

    dificultad = request.GET.get("dificultad")
    if dificultad:
        qs = qs.filter(nivel_dificultad=dificultad)

    destacado = request.GET.get("destacado")
    if destacado in ("true", "1"):
        qs = qs.filter(destacado=True)

    # Ordenamiento
    orden = request.GET.get("orden", "-updated_at")
    qs = qs.order_by(orden)

    total_productos = qs.count()

    # Paginación configurable (25, 50, 100)
    try:
        per_page = int(request.GET.get("per_page", 25))
        if per_page not in (25, 50, 100):
            per_page = 25
    except (ValueError, TypeError):
        per_page = 25

    paginator = Paginator(qs, per_page)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # Listas auxiliares para selectores
    categorias = Categoria.objects.all().order_by("orden", "nombre")
    proveedores = Proveedor.objects.all().order_by("nombre")

    context = {
        "page_obj": page_obj,
        "total_productos": total_productos,
        "kpis": kpis,
        "tab_activa": tab,
        "categorias": categorias,
        "proveedores": proveedores,
        "curaduria_choices": Producto.ESTADOS_CURADURIA,
        "validacion_choices": Producto.ESTADOS_ESPECIFICACION_NEUTRAL,
        "stock_choices": Producto.ESTADOS_STOCK,
        "dificultad_choices": Producto.NIVELES_DIFICULTAD,
        "q": q,
        "categoria_activa": categoria_id,
        "proveedor_activo": proveedor_id,
        "publicado_activo": publicado,
        "activo_activo": activo_filtro,
        "curaduria_activa": curaduria,
        "validacion_activa": validacion,
        "stock_activo": stock,
        "dificultad_activa": dificultad,
        "destacado_activo": destacado,
        "orden_activo": orden,
        "per_page": per_page,
    }
    return render(request, "gestion/productos/lista.html", context)



@gestion_required
@permiso_requerido("gestion.can_manage_catalogo")
def producto_detalle_view(request, id):
    """
    Ficha administrativa modular de producto organizada en 6 bloques temáticos.
    """
    producto = get_object_or_404(
        Producto.objects.select_related("categoria", "proveedor")
        .prefetch_related("tecnologias_compatibles", "tecnologias_verificadas", "imagenes"),
        id=id
    )

    # Bloque Rendimiento (Ajuste #17: Distinguir demanda de venta)
    vistas_count = EventoUso.objects.filter(producto=producto, tipo_evento="VER_PRODUCTO").count()
    agregados_count = EventoUso.objects.filter(producto=producto, tipo_evento="AGREGAR_COTIZACION").count()
    
    solicitudes_items = SolicitudItem.objects.filter(producto=producto).select_related("solicitud")
    solicitudes_count = solicitudes_items.values("solicitud").distinct().count()
    unidades_solicitadas = solicitudes_items.aggregate(total=Sum("cantidad"))["total"] or 0
    monto_solicitado = solicitudes_items.aggregate(total=Sum("subtotal_referencial_snapshot"))["total"] or Decimal("0")

    # Solicitudes cerradas (indicador provisional antes de 5C)
    solicitudes_cerradas_count = solicitudes_items.filter(solicitud__estado="CERRADA").values("solicitud").distinct().count()

    # Ratios de conversión
    tasa_vista_agregado = round((agregados_count / vistas_count) * 100, 1) if vistas_count > 0 else 0
    tasa_vista_solicitud = round((solicitudes_count / vistas_count) * 100, 1) if vistas_count > 0 else 0

    # Motivos de rechazo de publicación si no está publicado
    motivos_publicacion = ProductoPublicationService.validar_para_publicacion(producto) if not producto.publicado else []

    context = {
        "producto": producto,
        "vistas_count": vistas_count,
        "agregados_count": agregados_count,
        "solicitudes_count": solicitudes_count,
        "unidades_solicitadas": unidades_solicitadas,
        "monto_solicitado": monto_solicitado,
        "solicitudes_cerradas_count": solicitudes_cerradas_count,
        "tasa_vista_agregado": tasa_vista_agregado,
        "tasa_vista_solicitud": tasa_vista_solicitud,
        "motivos_publicacion": motivos_publicacion,
    }
    return render(request, "gestion/productos/detalle.html", context)


@gestion_required
@permiso_requerido("gestion.can_manage_catalogo")
def producto_crear_view(request):
    """
    Alta manual de nuevo producto.
    Regla estricta: publicado=False, estado_curaduria='SIN_REVISAR', activo=True.
    """
    categorias = Categoria.objects.filter(activa=True).order_by("orden", "nombre")
    proveedores = Proveedor.objects.filter(activo=True).order_by("nombre")

    if request.method == "POST":
        sku_humm = request.POST.get("sku_humm", "").strip().upper()
        sku_proveedor = request.POST.get("sku_proveedor", "").strip().upper()
        nombre_comercial = request.POST.get("nombre_comercial", "").strip()
        categoria_id = request.POST.get("categoria")
        proveedor_id = request.POST.get("proveedor")
        marca = request.POST.get("marca", "Keyestudio").strip()
        modelo = request.POST.get("modelo", "").strip()
        unidad_compra = request.POST.get("unidad_compra", "unidad").strip()
        costo_usd_str = request.POST.get("costo_proveedor_usd", "0.00").strip()

        if not sku_humm or not nombre_comercial or not proveedor_id:
            messages.error(request, "Faltan campos obligatorios (SKU Humm, Nombre comercial, Proveedor).")
        elif Producto.objects.filter(sku_humm=sku_humm).exists():
            messages.error(request, f"El SKU Humm '{sku_humm}' ya existe en el catálogo maestro.")
        else:
            try:
                costo_usd = Decimal(costo_usd_str)
            except Exception:
                costo_usd = Decimal("0.00")

            prov = get_object_or_404(Proveedor, id=proveedor_id)
            cat = Categoria.objects.filter(id=categoria_id).first() if categoria_id else None

            prod = Producto(
                sku_humm=sku_humm,
                sku_proveedor=sku_proveedor or sku_humm,
                proveedor=prov,
                categoria=cat,
                marca=marca,
                modelo=modelo,
                nombre_comercial=nombre_comercial,
                unidad_compra=unidad_compra,
                costo_proveedor_usd=costo_usd,
                # REGLAS OBLIGATORIAS HUMM:
                publicado=False,
                activo=True,
                estado_curaduria="SIN_REVISAR",
                estado_especificacion_neutral="NO_REVISADO",
            )
            prod.save()  # calcula precios sugeridos automáticamente si costo > 0

            registrar_actividad(
                request=request,
                accion="CREAR_PRODUCTO",
                modelo_afectado="Producto",
                objeto_id=prod.id,
                descripcion=f"Creó producto manual '{prod.nombre_comercial}' [{prod.sku_humm}]. Queda en borrador (publicado=False).",
                detalles={"sku_humm": prod.sku_humm, "costo_usd": str(costo_usd)}
            )

            messages.success(request, f"Producto '{prod.nombre_comercial}' creado en borrador. Continúe con la curaduría.")
            return redirect("gestion:producto_detalle", id=prod.id)

    context = {
        "categorias": categorias,
        "proveedores": proveedores,
    }
    return render(request, "gestion/productos/crear.html", context)


@gestion_required
@permiso_requerido("gestion.can_publish_producto")
@require_POST
def producto_toggle_publicado_view(request, id):
    """
    Switch de publicación/despublicación controlado por ProductoPublicationService (Ajustes #13 y #14).
    """
    producto = get_object_or_404(Producto, id=id)
    is_ajax = request.headers.get("x-requested-with") == "XMLHttpRequest"

    if producto.publicado:
        # Despublicar
        ProductoPublicationService.despublicar(producto, usuario=request.user, request=request)
        if is_ajax:
            return JsonResponse({"status": "ok", "publicado": False, "mensaje": "Producto despublicado con éxito."})
        messages.info(request, f"El producto '{producto.sku_humm}' ha sido retirado del catálogo público.")
    else:
        # Intentar publicar validando requisitos de calidad
        try:
            ProductoPublicationService.publicar(producto, usuario=request.user, request=request)
            if is_ajax:
                return JsonResponse({"status": "ok", "publicado": True, "mensaje": "Producto publicado con éxito."})
            messages.success(request, f"El producto '{producto.sku_humm}' está ahora publicado en EduCompra.")
        except ValidationError as e:
            if is_ajax:
                return JsonResponse({"status": "error", "mensaje": str(e.message)}, status=400)
            messages.error(request, str(e.message))

    return redirect("gestion:producto_detalle", id=producto.id)


@gestion_required
@permiso_requerido("gestion.can_manage_catalogo")
def producto_editar_view(request, id):
    """
    Edición de datos pedagógicos, comerciales y técnicos del producto.
    Precios derivados no son editables directamente a mano (Ajuste #16).
    """
    producto = get_object_or_404(Producto, id=id)
    categorias = Categoria.objects.all().order_by("orden", "nombre")
    tecnologias = TecnologiaCompatible.objects.all().order_by("orden", "nombre")

    if request.method == "POST":
        producto.nombre_comercial = request.POST.get("nombre_comercial", "").strip()
        producto.descripcion_corta = request.POST.get("descripcion_corta", "").strip()
        producto.descripcion_educativa = request.POST.get("descripcion_educativa", "").strip()
        producto.uso_educativo = request.POST.get("uso_educativo", "").strip()
        producto.advertencia_uso = request.POST.get("advertencia_uso", "").strip()
        producto.unidad_compra = request.POST.get("unidad_compra", "unidad").strip()
        producto.nivel_dificultad = request.POST.get("nivel_dificultad", "NO_DEFINIDO")
        producto.estado_curaduria = request.POST.get("estado_curaduria", producto.estado_curaduria)
        producto.estado_stock = request.POST.get("estado_stock", "disponible")
        producto.destacado = request.POST.get("destacado") == "on"
        producto.apto_para_kit = request.POST.get("apto_para_kit") == "on"

        # Categoría
        cat_id = request.POST.get("categoria")
        producto.categoria = Categoria.objects.filter(id=cat_id).first() if cat_id else None

        # Bloque Técnico para Compra Pública
        producto.titulo_especificacion_neutral = request.POST.get("titulo_especificacion_neutral", "").strip()
        producto.especificacion_tecnica_neutral = request.POST.get("especificacion_tecnica_neutral", "").strip()
        producto.criterios_equivalencia = request.POST.get("criterios_equivalencia", "").strip()
        producto.estado_especificacion_neutral = request.POST.get("estado_especificacion_neutral", "NO_REVISADO")
        producto.fuente_tecnica = request.POST.get("fuente_tecnica", "").strip()
        producto.referencia_tecnica_url = request.POST.get("referencia_tecnica_url", "").strip()
        producto.responsable_revision_tecnica = request.POST.get("responsable_revision_tecnica", "").strip()

        # Costo USD (Ajuste #16: precios CLP se derivan automáticamente al guardar)
        costo_usd_raw = request.POST.get("costo_proveedor_usd", "").strip()
        if costo_usd_raw:
            try:
                producto.costo_proveedor_usd = Decimal(costo_usd_raw)
            except Exception:
                pass

        # Recargo específico opcional
        recargo_raw = request.POST.get("porcentaje_recargo", "").strip()
        if recargo_raw:
            try:
                producto.porcentaje_recargo = Decimal(recargo_raw)
            except Exception:
                producto.porcentaje_recargo = None
        else:
            producto.porcentaje_recargo = None

        # Guardar y recalcular derivados
        producto.save()

        # Tecnologías compatibles
        tech_ids = request.POST.getlist("tecnologias_compatibles")
        producto.tecnologias_compatibles.set(tech_ids)

        registrar_actividad(
            request=request,
            accion="EDITAR_PRODUCTO",
            modelo_afectado="Producto",
            objeto_id=producto.id,
            descripcion=f"Actualizó ficha de '{producto.nombre_comercial}' [{producto.sku_humm}].",
            detalles={"sku_humm": producto.sku_humm, "curaduria": producto.estado_curaduria}
        )

        messages.success(request, f"Ficha de '{producto.nombre_comercial}' actualizada con éxito.")
        return redirect("gestion:producto_detalle", id=producto.id)

    context = {
        "producto": producto,
        "categorias": categorias,
        "tecnologias": tecnologias,
        "curaduria_choices": Producto.ESTADOS_CURADURIA,
        "validacion_choices": Producto.ESTADOS_ESPECIFICACION_NEUTRAL,
        "stock_choices": Producto.ESTADOS_STOCK,
        "dificultad_choices": Producto.NIVELES_DIFICULTAD,
    }
    return render(request, "gestion/productos/editar.html", context)
