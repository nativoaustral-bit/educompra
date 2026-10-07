"""
Vistas de la aplicación de cotizaciones docentes:
- Canasta 'Mi Cotización'
- Formulario de solicitud con idempotencia y honeypot
- Confirmación pública higienizada por token UUID
"""

import json
import logging
from decimal import Decimal

logger = logging.getLogger(__name__)
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseBadRequest, Http404
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.views.decorators.http import require_POST, require_http_methods
from apps.core.regiones_chile import REGIONES_CHILE, obtener_regiones_comunas_dict
from .models import SolicitudCotizacion
from .forms import SolicitudCotizacionForm
from .services import CartService, SubmissionService


def mi_cotizacion_view(request):
    """
    Despliega la canasta de cotización del docente.
    Revalida todos los precios y la disponibilidad en base de datos.
    """
    from apps.gestion.services_telemetria import TelemetriaService, capturar_utms_en_sesion
    capturar_utms_en_sesion(request)

    canasta_info = CartService.obtener_canasta_revalidada(request)

    TelemetriaService.registrar_evento(
        request,
        tipo_evento="VER_MI_COTIZACION",
        metadata={"cart_items_count": canasta_info["total_articulos"]}
    )

    if canasta_info["items_retirados"]:
        messages.warning(
            request,
            f"Aviso: {len(canasta_info['items_retirados'])} producto(s) ya no están disponibles en el catálogo y fueron retirados de su lista."
        )

    context = {
        "items": canasta_info["items"],
        "items_retirados": canasta_info["items_retirados"],
        "total_referencial": canasta_info["total_referencial"],
        "total_articulos": canasta_info["total_articulos"],
        "disclaimer_precios": "Precios referenciales en pesos chilenos con IVA incluido para fines de presupuesto y postulación a fondos. La cotización formal final será emitida por Humm confirmando disponibilidad y costos logísticos."
    }
    return render(request, "cotizaciones/mi_cotizacion.html", context)


@require_POST
def agregar_item_view(request):
    """
    Agrega un producto a la canasta mediante POST.
    Admite peticiones tradicionales (redirect) o Fetch/AJAX (JSON).
    """
    from apps.gestion.services_telemetria import TelemetriaService

    producto_id = request.POST.get("producto_id")
    cantidad = request.POST.get("cantidad", 1)

    is_ajax = (
        request.headers.get("x-requested-with") == "XMLHttpRequest"
        or "application/json" in request.headers.get("Accept", "")
    )

    try:
        producto, nueva_cant = CartService.agregar_item(request, producto_id, cantidad)
        TelemetriaService.registrar_evento(
            request,
            tipo_evento="AGREGAR_COTIZACION",
            producto=producto,
            categoria=producto.categoria,
            metadata={"cantidad": nueva_cant, "product_sku": producto.sku_humm}
        )
    except ValidationError as e:
        if is_ajax:
            return JsonResponse({"status": "error", "mensaje": str(e.message)}, status=400)
        messages.error(request, str(e.message))
        return redirect(request.META.get("HTTP_REFERER", "catalogo:lista"))

    if is_ajax:
        canasta_info = CartService.obtener_canasta_revalidada(request)
        return JsonResponse({
            "status": "ok",
            "mensaje": f"Se agregó '{producto.nombre_comercial}' a su cotización.",
            "total_articulos": canasta_info["total_articulos"],
            "total_referencial": int(round(canasta_info["total_referencial"])),
        })

    messages.success(request, f"Se agregó '{producto.nombre_comercial}' a su cotización.")
    return redirect("cotizaciones:mi_cotizacion")


@require_POST
def actualizar_cantidad_view(request):
    """Actualiza la cantidad de un ítem en la canasta."""
    producto_id = request.POST.get("producto_id")
    cantidad = request.POST.get("cantidad")

    is_ajax = (
        request.headers.get("x-requested-with") == "XMLHttpRequest"
        or "application/json" in request.headers.get("Accept", "")
    )

    try:
        CartService.actualizar_cantidad(request, producto_id, cantidad)
    except ValidationError as e:
        if is_ajax:
            return JsonResponse({"status": "error", "mensaje": str(e.message)}, status=400)
        messages.error(request, str(e.message))
        return redirect("cotizaciones:mi_cotizacion")

    if is_ajax:
        canasta_info = CartService.obtener_canasta_revalidada(request)
        return JsonResponse({
            "status": "ok",
            "total_articulos": canasta_info["total_articulos"],
            "total_referencial": int(round(canasta_info["total_referencial"])),
        })

    return redirect("cotizaciones:mi_cotizacion")


@require_POST
def eliminar_item_view(request):
    """Elimina un ítem de la canasta."""
    from apps.gestion.services_telemetria import TelemetriaService
    producto_id = request.POST.get("producto_id")
    CartService.eliminar_item(request, producto_id)
    TelemetriaService.registrar_evento(request, tipo_evento="QUITAR_COTIZACION")

    is_ajax = (
        request.headers.get("x-requested-with") == "XMLHttpRequest"
        or "application/json" in request.headers.get("Accept", "")
    )

    if is_ajax:
        canasta_info = CartService.obtener_canasta_revalidada(request)
        return JsonResponse({
            "status": "ok",
            "total_articulos": canasta_info["total_articulos"],
            "total_referencial": int(round(canasta_info["total_referencial"])),
        })

    messages.info(request, "Producto retirado de su cotización.")
    return redirect("cotizaciones:mi_cotizacion")


@require_POST
def vaciar_canasta_view(request):
    """Vacía todos los productos de la canasta."""
    from apps.gestion.services_telemetria import TelemetriaService
    CartService.vaciar_canasta(request)
    TelemetriaService.registrar_evento(request, tipo_evento="QUITAR_COTIZACION")
    messages.info(request, "Se ha vaciado su lista de cotización.")
    return redirect("cotizaciones:mi_cotizacion")


@require_http_methods(["GET", "POST"])
def solicitar_cotizacion_view(request):
    """
    Vista del formulario de envío de cotización.
    - Implementa token de idempotencia para evitar duplicados por doble clic o refresh.
    - Valida honeypot contra bots.
    - Procesa en transacción atómica y congela snapshots inmutables.
    """
    from apps.gestion.services_telemetria import TelemetriaService, capturar_utms_en_sesion
    capturar_utms_en_sesion(request)

    canasta_info = CartService.obtener_canasta_revalidada(request)

    if not canasta_info["items"]:
        messages.warning(request, "Su lista de cotización está vacía. Seleccione productos antes de solicitar cotización.")
        return redirect("catalogo:lista")

    if request.method == "GET":
        TelemetriaService.registrar_evento(
            request,
            tipo_evento="INICIAR_SOLICITUD",
            metadata={"cart_items_count": canasta_info["total_articulos"]}
        )

    regiones_comunas_map = obtener_regiones_comunas_dict()

    if request.method == "POST":
        idempotency_token = request.POST.get("idempotency_token")
        
        # Validar y consumir el token para prevenir doble envío
        if not SubmissionService.validar_y_consumir_token_idempotencia(request, idempotency_token):
            messages.warning(
                request,
                "Esta solicitud ya fue enviada o el token expiró. Si necesita generar una nueva solicitud, por favor revise sus productos."
            )
            return redirect("cotizaciones:mi_cotizacion")

        form = SolicitudCotizacionForm(request.POST)
        if form.is_valid():
            try:
                solicitud = SubmissionService.crear_solicitud_cotizacion(request, form.cleaned_data)
                return redirect("cotizaciones:solicitud_recibida", token=solicitud.token)
            except ValidationError as e:
                messages.error(request, str(e.message))
            except Exception:
                logger.exception(
                    "Error no controlado creando solicitud de cotización en /solicitar-cotizacion/"
                )
                messages.error(
                    request,
                    "Ocurrió un error al procesar su solicitud. Por favor intente nuevamente."
                )
        
        # Si el formulario fue inválido o falló la creación, generar un nuevo token de reintento
        nuevo_token = SubmissionService.generar_token_idempotencia(request)
    else:
        nuevo_token = SubmissionService.generar_token_idempotencia(request)
        form = SolicitudCotizacionForm(initial={"idempotency_token": nuevo_token})

    context = {
        "form": form,
        "items": canasta_info["items"],
        "total_referencial": canasta_info["total_referencial"],
        "total_articulos": canasta_info["total_articulos"],
        "regiones_json": json.dumps(regiones_comunas_map, ensure_ascii=False),
        "idempotency_token": nuevo_token,
    }
    return render(request, "cotizaciones/formulario.html", context)


def solicitud_recibida_view(request, token):
    """
    Vista de confirmación pública higienizada.
    Accedida mediante token UUID de alta entropía.
    NO muestra: email, teléfono, RUT, notas internas.
    Muestra: código de seguimiento, colegio, productos con snapshots, total y pasos siguientes.
    """
    solicitud = get_object_or_404(SolicitudCotizacion, token=token)

    context = {
        "solicitud": solicitud,
        "items": solicitud.items.all(),
        "total_referencial": solicitud.total_referencial_estimado,
        "disclaimer_precios": "Precios referenciales en pesos chilenos con IVA incluido para fines de presupuesto y postulación a fondos. La cotización formal final será emitida por Humm confirmando disponibilidad y costos logísticos."
    }
    return render(request, "cotizaciones/confirmacion.html", context)
