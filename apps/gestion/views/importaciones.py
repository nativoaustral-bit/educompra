"""
Vistas del asistente web de importaciones masivas de catálogo (/gestion/importaciones/).
Cumple con los Ajustes Obligatorios #10, #11, #12, #20 y #21 de Humm:
- Almacenamiento privado seguro fuera del DocumentRoot.
- Validación de seguridad anti-ZIP-bomb y path traversal.
- Flujo en 6 pasos con DRY-RUN obligatorio previo a cualquier escritura.
- Confirmación explícita antes de aplicar.
"""

import tempfile
from pathlib import Path
from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST

from apps.gestion.decorators import gestion_required, permiso_requerido
from apps.gestion.models import LoteImportacion
from apps.catalogo.services_importacion import ImportacionCatalogoService


@gestion_required
@permiso_requerido("gestion.can_run_importaciones")
def importaciones_lista_view(request):
    """
    Panel principal de importaciones: subida de archivos y listado de lotes históricos.
    """
    lotes = LoteImportacion.objects.all().select_related("usuario_creador").order_by("-created_at")[:20]
    return render(request, "gestion/importaciones/lista.html", {"lotes": lotes})


@gestion_required
@permiso_requerido("gestion.can_run_importaciones")
@require_POST
def importaciones_subir_view(request):
    """
    Paso 1 y 2: Recibe archivos en almacenamiento privado y ejecuta simulación DRY-RUN obligatoria.
    """
    excel_file = request.FILES.get("archivo_excel")
    zip_file = request.FILES.get("archivo_imagenes_zip")

    if not excel_file:
        messages.error(request, "Debe seleccionar un archivo Excel (.xlsx / .xls).")
        return redirect("gestion:importaciones")

    # Crear lote en almacenamiento privado
    lote = LoteImportacion(
        archivo_excel=excel_file,
        archivo_imagenes_zip=zip_file,
        estado="SUBIDO",
        es_dry_run=True,
        usuario_creador=request.user,
    )
    lote.save()

    # Validar y ejecutar DRY-RUN
    try:
        # Descomprimir imágenes en directorio temporal privado si se subió ZIP
        temp_img_dir = None
        if lote.archivo_imagenes_zip:
            temp_extract = Path(tempfile.mkdtemp(prefix="educompra_zip_"))
            ImportacionCatalogoService.validar_y_descomprimir_zip(lote.archivo_imagenes_zip.path, temp_extract)
            temp_img_dir = str(temp_extract)

        # Ejecutar simulación DRY-RUN
        resumen = ImportacionCatalogoService.procesar_catalogo(
            excel_path=lote.archivo_excel.path,
            imagenes_dir=temp_img_dir,
            is_dry_run=True,
            actualizar_costos=True,
            usuario=request.user,
            lote=lote,
            request=request,
        )

        messages.success(request, f"Simulación DRY-RUN completada para Lote #{lote.id}. Revise el resumen antes de aprobar.")
        return redirect("gestion:importacion_detalle", id=lote.id)

    except ValidationError as e:
        lote.estado = "FALLIDO"
        lote.save()
        messages.error(request, f"Error de validación en archivo: {e}")
        return redirect("gestion:importaciones")
    except Exception as e:
        lote.estado = "FALLIDO"
        lote.save()
        messages.error(request, f"Error durante la simulación DRY-RUN: {e}")
        return redirect("gestion:importaciones")


@gestion_required
@permiso_requerido("gestion.can_run_importaciones")
def importacion_detalle_view(request, id):
    """
    Paso 3 y 4: Muestra el informe estadístico del DRY-RUN y lista de conflictos detectados.
    """
    lote = get_object_or_404(LoteImportacion, id=id)
    resumen = lote.resumen_json or {}

    tiene_conflictos = lote.conflictos_detectados > 0
    tiene_nuevos = lote.productos_nuevos > 0

    context = {
        "lote": lote,
        "resumen": resumen,
        "tiene_conflictos": tiene_conflictos,
        "tiene_nuevos": tiene_nuevos,
    }
    return render(request, "gestion/importaciones/detalle.html", context)


@gestion_required
@permiso_requerido("gestion.can_run_importaciones")
@require_POST
def importacion_aprobar_view(request, id):
    """
    Paso 5 y 6: Aprobación explícita y ejecución productiva en base de datos.
    """
    lote = get_object_or_404(LoteImportacion, id=id)

    if lote.estado == "APLICADO":
        messages.warning(request, "Este lote ya fue importado previamente en la base de datos.")
        return redirect("gestion:importacion_detalle", id=lote.id)

    confirmacion = request.POST.get("confirmacion_aprobacion")
    if confirmacion != "SI_APROBAR":
        messages.error(request, "Debe marcar la confirmación de aprobación para ejecutar la importación definitiva.")
        return redirect("gestion:importacion_detalle", id=lote.id)

    try:
        temp_img_dir = None
        if lote.archivo_imagenes_zip:
            temp_extract = Path(tempfile.mkdtemp(prefix="educompra_zip_prod_"))
            ImportacionCatalogoService.validar_y_descomprimir_zip(lote.archivo_imagenes_zip.path, temp_extract)
            temp_img_dir = str(temp_extract)

        # Ejecución definitiva real (is_dry_run=False)
        resumen = ImportacionCatalogoService.procesar_catalogo(
            excel_path=lote.archivo_excel.path,
            imagenes_dir=temp_img_dir,
            is_dry_run=False,
            actualizar_costos=True,
            usuario=request.user,
            lote=lote,
            request=request,
        )

        messages.success(
            request,
            f"¡Importación definitiva ejecutada con éxito! "
            f"Se crearon {resumen['productos_nuevos']} productos nuevos (en borrador) y se actualizaron {resumen['productos_actualizados']} costos."
        )
        return redirect("gestion:importacion_detalle", id=lote.id)

    except Exception as e:
        messages.error(request, f"Error al ejecutar la importación productiva: {e}")
        return redirect("gestion:importacion_detalle", id=lote.id)
