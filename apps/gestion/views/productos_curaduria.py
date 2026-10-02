"""
Módulo de Curaduría Pedagógica y por Lote (/gestion/productos/candidatos/ y curaduría).
Implementa Bloque C del Plan de Gestión Simplificada y Ajuste Obligatorio #5 (Curaduría asistida simple).
"""

import re
from decimal import Decimal
from django.contrib import messages
from django.db import transaction
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from apps.gestion.decorators import gestion_required, permiso_requerido
from apps.gestion.services_auditoria import registrar_actividad
from apps.catalogo.models import Producto, Categoria, TecnologiaCompatible, PrecioProveedorTramo


def generar_propuesta_deterministica(producto, categorias):
    """
    Genera sugerencias determinísticas simples basadas en evidencia del proveedor (Ajuste 5).
    Etiquetadas explícitamente como 'PROPUESTA — REQUIERE REVISIÓN HUMANA'.
    No inventa especificaciones ni valida automáticamente.
    """
    nombre_base = producto.nombre_original_proveedor or producto.nombre_comercial
    # Limpiar prefijos redundantes como 'keyestudio' repetido
    nombre_limpio = re.sub(r'^(keyestudio\s+)+', '', nombre_base, flags=re.IGNORECASE).strip()
    if not nombre_limpio:
        nombre_limpio = producto.nombre_comercial

    # Sugerencia de categoría por palabras clave determinísticas
    texto_evaluar = f"{nombre_base} {producto.features_proveedor}".lower()
    cat_sugerida = None
    for cat in categorias:
        c_nom = cat.nombre.lower()
        if "sensor" in c_nom and any(k in texto_evaluar for k in ["sensor", "detector", "probe"]):
            cat_sugerida = cat
            break
        elif "placa" in c_nom and any(k in texto_evaluar for k in ["board", "placa", "uno", "mega", "nano", "esp32", "micro:bit", "pico"]):
            cat_sugerida = cat
            break
        elif "kit" in c_nom and "kit" in texto_evaluar:
            cat_sugerida = cat
            break
        elif "robot" in c_nom and any(k in texto_evaluar for k in ["robot", "car", "tank", "arm"]):
            cat_sugerida = cat
            break
        elif "display" in c_nom or "pantalla" in c_nom and any(k in texto_evaluar for k in ["display", "lcd", "oled", "screen"]):
            cat_sugerida = cat
            break
        elif "motor" in c_nom and any(k in texto_evaluar for k in ["motor", "servo", "stepper"]):
            cat_sugerida = cat
            break

    # Propuesta de descripción educativa inicial estándar
    desc_sugerida = f"Componente {nombre_limpio} orientado a la experimentación práctica y aprendizaje de programación y electrónica en contexto escolar."
    uso_sugerido = "Proyectos prácticos de aula, laboratorios STEAM y prototipado escolar guiado."

    return {
        "nombre_comercial": nombre_limpio,
        "categoria_id": cat_sugerida.id if cat_sugerida else (producto.categoria_id if producto.categoria else ""),
        "descripcion_educativa": desc_sugerida,
        "uso_educativo": uso_sugerido,
    }


@gestion_required
@permiso_requerido("gestion.can_manage_catalogo")
def productos_candidatos_view(request):
    """
    Bandeja de trabajo para productos candidatos y en curaduría (estado CANDIDATO o EN_CURADURIA).
    Permite filtrar, seleccionar y derivar a curaduría individual o en lote.
    """
    qs = Producto.objects.filter(
        activo=True,
        estado_curaduria__in=["CANDIDATO", "EN_CURADURIA"]
    ).select_related("categoria", "proveedor").prefetch_related("imagenes")

    q = request.GET.get("q", "").strip()
    if q:
        qs = qs.filter(
            Q(sku_humm__icontains=q)
            | Q(sku_proveedor__icontains=q)
            | Q(nombre_comercial__icontains=q)
            | Q(nombre_original_proveedor__icontains=q)
        )

    estado = request.GET.get("estado", "")
    if estado in ("CANDIDATO", "EN_CURADURIA"):
        qs = qs.filter(estado_curaduria=estado)

    total_candidatos = qs.count()
    productos = list(qs.order_by("-updated_at"))

    categorias = Categoria.objects.filter(activa=True).order_by("orden", "nombre")

    context = {
        "productos": productos,
        "total_candidatos": total_candidatos,
        "q": q,
        "estado_activo": estado,
        "categorias": categorias,
    }
    return render(request, "gestion/productos/candidatos.html", context)


@gestion_required
@permiso_requerido("gestion.can_manage_catalogo")
def productos_curaduria_lote_view(request):
    """
    Interfaz ágil de curaduría por lote en tarjetas consecutivas (Ajuste 5).
    Presenta la evidencia del proveedor (solo lectura) y los campos pedagógicos Humm.
    Permite guardar borradores, validar individualmente o en lote, o descartar.
    """
    ids_param = request.GET.get("ids", "").strip()
    if not ids_param and request.method == "POST":
        ids_param = request.POST.get("ids", "").strip()

    if not ids_param:
        messages.warning(request, "No se especificaron productos para curar. Seleccione candidatos primero.")
        return redirect("gestion:productos_candidatos")

    ids_lista = [i.strip() for i in ids_param.split(",") if i.strip().isdigit()]
    productos = list(
        Producto.objects.filter(id__in=ids_lista, activo=True)
        .select_related("categoria", "proveedor")
        .prefetch_related("tecnologias_compatibles", "imagenes", "precios_tramos")
    )

    if not productos:
        messages.warning(request, "No se encontraron productos activos con los identificadores indicados.")
        return redirect("gestion:productos_candidatos")

    categorias = Categoria.objects.filter(activa=True).order_by("orden", "nombre")
    tecnologias = TecnologiaCompatible.objects.filter(activa=True).order_by("orden", "nombre")

    if request.method == "POST":
        accion = request.POST.get("accion")
        prod_id = request.POST.get("producto_id")

        # Acción individual sobre un producto del lote
        if accion in ("guardar_borrador_item", "validar_item", "descartar_item") and prod_id:
            producto = get_object_or_404(Producto, id=prod_id, activo=True)

            nombre_com = request.POST.get(f"nombre_comercial_{prod_id}", "").strip()
            desc_edu = request.POST.get(f"descripcion_educativa_{prod_id}", "").strip()
            uso_edu = request.POST.get(f"uso_educativo_{prod_id}", "").strip()
            cat_id = request.POST.get(f"categoria_{prod_id}")
            dif = request.POST.get(f"dificultad_{prod_id}", "NO_DEFINIDO")
            adv = request.POST.get(f"advertencia_uso_{prod_id}", "").strip()
            tech_ids = request.POST.getlist(f"tecnologias_{prod_id}")

            if accion == "descartar_item":
                producto.estado_curaduria = "DESCARTADO_CATALOGO_PUBLICO"
                producto.save(update_fields=["estado_curaduria", "updated_at"])
                registrar_actividad(
                    request=request,
                    accion="DESCARTAR_PRODUCTO_CURADURIA",
                    modelo_afectado="Producto",
                    objeto_id=producto.id,
                    descripcion=f"Descartó '{producto.sku_humm}' para el catálogo público (permanece en maestro).",
                )
                messages.info(request, f"Producto '{producto.sku_humm}' descartado para catálogo público (conservado en maestro).")
                return redirect(f"{request.path}?ids={ids_param}")

            # Validar campos antes de guardar
            if nombre_com:
                producto.nombre_comercial = nombre_com
            producto.descripcion_educativa = desc_edu
            producto.uso_educativo = uso_edu
            producto.advertencia_uso = adv
            producto.nivel_dificultad = dif

            if cat_id:
                producto.categoria = Categoria.objects.filter(id=cat_id).first()

            if accion == "validar_item":
                # Verificación de requisitos mínimos para curaduría VALIDADO (Ajuste 5)
                errores = []
                if not producto.nombre_comercial:
                    errores.append("Nombre comercial no puede estar vacío.")
                if not producto.categoria or not producto.categoria.activa or producto.categoria.nombre.lower() in ("sin clasificar", "general"):
                    errores.append("Debe asignar una categoría válida y activa.")
                if len(producto.descripcion_educativa.strip()) < 15:
                    errores.append("La descripción pedagógica debe contener al menos 15 caracteres.")

                if errores:
                    messages.error(request, f"No se puede validar '{producto.sku_humm}': " + " | ".join(errores))
                    return redirect(f"{request.path}?ids={ids_param}")

                producto.estado_curaduria = "VALIDADO"
                msg_accion = "Curaduría validada exitosamente"
                act_accion = "VALIDAR_CURADURIA_PRODUCTO"
            else:
                producto.estado_curaduria = "EN_CURADURIA"
                msg_accion = "Borrador de curaduría guardado"
                act_accion = "GUARDAR_BORRADOR_CURADURIA"

            producto.save()
            producto.tecnologias_compatibles.set(tech_ids)

            registrar_actividad(
                request=request,
                accion=act_accion,
                modelo_afectado="Producto",
                objeto_id=producto.id,
                descripcion=f"{msg_accion} para '{producto.nombre_comercial}' [{producto.sku_humm}].",
            )
            messages.success(request, f"{msg_accion}: '{producto.nombre_comercial}'.")
            return redirect(f"{request.path}?ids={ids_param}")

    # Preparar tarjetas con evidencia y propuestas
    tarjetas = []
    for p in productos:
        tramos = p.precios_tramos.all().order_by("cantidad_minima")
        propuesta = generar_propuesta_deterministica(p, categorias)
        tarjetas.append({
            "producto": p,
            "tramos": tramos,
            "propuesta": propuesta,
            "tecnologias_seleccionadas": list(p.tecnologias_compatibles.values_list("id", flat=True)),
        })

    context = {
        "tarjetas": tarjetas,
        "ids_param": ids_param,
        "total_lote": len(productos),
        "categorias": categorias,
        "tecnologias": tecnologias,
        "dificultad_choices": Producto.NIVELES_DIFICULTAD,
    }
    return render(request, "gestion/productos/curaduria_lote.html", context)


@gestion_required
@permiso_requerido("gestion.can_manage_catalogo")
def productos_curaduria_masiva_campos_view(request):
    """
    Asignación masiva de campos comunes (Ajuste 5 y Plan C):
    Permite fijar categoría, nivel, tecnologías, unidad de compra, stock o días de entrega
    a un conjunto de productos seleccionados, SIN tocar textos descriptivos diferenciales.
    """
    ids_param = request.GET.get("ids", "").strip()
    if not ids_param and request.method == "POST":
        ids_param = request.POST.get("ids", "").strip()

    if not ids_param:
        messages.warning(request, "No se seleccionaron productos.")
        return redirect("gestion:productos_candidatos")

    ids_lista = [i.strip() for i in ids_param.split(",") if i.strip().isdigit()]
    productos = list(Producto.objects.filter(id__in=ids_lista, activo=True))

    if not productos:
        messages.warning(request, "No se encontraron productos activos con los identificadores indicados.")
        return redirect("gestion:productos_candidatos")

    categorias = Categoria.objects.filter(activa=True).order_by("orden", "nombre")
    tecnologias = TecnologiaCompatible.objects.filter(activa=True).order_by("orden", "nombre")

    if request.method == "POST" and request.POST.get("accion") == "aplicar_campos_comunes":
        aplicar_cat = request.POST.get("aplicar_categoria") == "1"
        cat_id = request.POST.get("categoria")

        aplicar_dif = request.POST.get("aplicar_dificultad") == "1"
        dif = request.POST.get("nivel_dificultad")

        aplicar_stock = request.POST.get("aplicar_stock") == "1"
        stock = request.POST.get("estado_stock")

        aplicar_dias = request.POST.get("aplicar_dias") == "1"
        dias = request.POST.get("dias_entrega_estimados")

        aplicar_unidad = request.POST.get("aplicar_unidad") == "1"
        unidad = request.POST.get("unidad_compra", "").strip()

        aplicar_tech = request.POST.get("aplicar_tecnologias") == "1"
        tech_ids = request.POST.getlist("tecnologias_compatibles")

        cambios_realizados = []

        with transaction.atomic():
            for p in productos:
                update_fields = ["updated_at"]

                if aplicar_cat and cat_id:
                    cat_obj = Categoria.objects.filter(id=cat_id).first()
                    p.categoria = cat_obj
                    update_fields.append("categoria")

                if aplicar_dif and dif:
                    p.nivel_dificultad = dif
                    update_fields.append("nivel_dificultad")

                if aplicar_stock and stock:
                    p.estado_stock = stock
                    update_fields.append("estado_stock")

                if aplicar_dias and dias:
                    try:
                        p.dias_entrega_estimados = int(dias)
                        update_fields.append("dias_entrega_estimados")
                    except ValueError:
                        pass

                if aplicar_unidad and unidad:
                    p.unidad_compra = unidad
                    update_fields.append("unidad_compra")

                p.save(update_fields=update_fields)

                if aplicar_tech:
                    p.tecnologias_compatibles.set(tech_ids)

            registrar_actividad(
                request=request,
                accion="CURADURIA_MASIVA_CAMPOS_COMUNES",
                modelo_afectado="Producto",
                objeto_id="",
                descripcion=f"Aplicó campos comunes en masa a {len(productos)} productos seleccionados.",
                detalles={
                    "total_productos": len(productos),
                    "aplicar_categoria": aplicar_cat,
                    "aplicar_dificultad": aplicar_dif,
                    "aplicar_stock": aplicar_stock,
                    "aplicar_tecnologias": aplicar_tech,
                }
            )

        messages.success(request, f"Campos comunes aplicados exitosamente a {len(productos)} productos.")
        return redirect("gestion:productos_candidatos")

    context = {
        "productos": productos,
        "ids_param": ids_param,
        "categorias": categorias,
        "tecnologias": tecnologias,
        "dificultad_choices": Producto.NIVELES_DIFICULTAD,
        "stock_choices": Producto.ESTADOS_STOCK,
    }
    return render(request, "gestion/productos/curaduria_masiva_campos.html", context)
