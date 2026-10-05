"""
Vistas de gestión comercial de solicitudes de cotización (/gestion/solicitudes/).
Incluye vista dual Tabla / Tablero Kanban (Ajustes #19, #20, #21 y #29).
"""

from decimal import Decimal
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Q, Sum
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.decorators.http import require_POST

from apps.gestion.decorators import gestion_required, permiso_requerido
from apps.gestion.services_auditoria import registrar_actividad
from apps.cotizaciones.models import SolicitudCotizacion, CotizacionFormal
from apps.core.regiones_chile import REGIONES_CHILE


@gestion_required
@permiso_requerido("gestion.can_manage_solicitudes")
def solicitudes_lista_view(request):
    """
    Listado general de solicitudes con filtros comerciales avanzados.
    """
    qs = SolicitudCotizacion.objects.all().select_related("establecimiento_ref", "contacto_ref", "responsable")

    # Filtro de búsqueda por texto (código, colegio, profesor, email, comuna)
    q = request.GET.get("q", "").strip()
    if q:
        qs = qs.filter(
            Q(codigo_seguimiento__icontains=q)
            | Q(establecimiento__icontains=q)
            | Q(nombre_solicitante__icontains=q)
            | Q(email__icontains=q)
            | Q(comuna__icontains=q)
        )

    # Filtros
    estado = request.GET.get("estado")
    if estado:
        qs = qs.filter(estado=estado)

    region = request.GET.get("region")
    if region:
        qs = qs.filter(region__icontains=region)

    responsable_id = request.GET.get("responsable")
    if responsable_id == "sin_asignar":
        qs = qs.filter(responsable__isnull=True)
    elif responsable_id:
        qs = qs.filter(responsable_id=responsable_id)

    ver_pruebas = request.GET.get("ver_pruebas", "0")
    if ver_pruebas != "1":
        qs = qs.filter(es_prueba=False)

    orden = request.GET.get("orden", "-created_at")
    qs = qs.order_by(orden)

    total_solicitudes = qs.count()

    # Paginación
    paginator = Paginator(qs, 20)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    User = get_user_model()
    usuarios_staff = User.objects.filter(is_active=True).order_by("first_name", "username")

    context = {
        "page_obj": page_obj,
        "total_solicitudes": total_solicitudes,
        "estados": SolicitudCotizacion.ESTADOS,
        "regiones": REGIONES_CHILE,
        "usuarios_staff": usuarios_staff,
        "q": q,
        "estado_activo": estado,
        "region_activa": region,
        "responsable_activo": responsable_id,
        "ver_pruebas": ver_pruebas,
        "orden_activo": orden,
    }
    return render(request, "gestion/solicitudes/lista.html", context)


@gestion_required
@permiso_requerido("gestion.can_manage_solicitudes")
def solicitudes_kanban_view(request):
    """
    Vista Kanban comercial organizada por las 8 columnas del ciclo comercial escolar.
    """
    ver_pruebas = request.GET.get("ver_pruebas", "0")
    qs = SolicitudCotizacion.objects.all().select_related("establecimiento_ref", "contacto_ref", "responsable")
    if ver_pruebas != "1":
        qs = qs.filter(es_prueba=False)

    columnas_estados = [
        ("NUEVA", "Nueva Solicitud", "badge-nueva"),
        ("EN_REVISION", "En Revisión Técnica", "badge-revision"),
        ("REQUIERE_ANTECEDENTES", "Requiere Antecedentes", "badge-alerta"),
        ("LISTA_PARA_COTIZAR", "Lista para Cotizar", "badge-info"),
        ("COTIZACION_PREPARADA", "Cotización Preparada", "badge-info"),
        ("COTIZACION_ENVIADA", "Cotización Enviada", "badge-exito"),
        ("CERRADA", "Cerrada (Venta)", "badge-cerrada"),
        ("PERDIDA", "Perdida / Cancelada", "badge-perdida"),
    ]

    kanban_data = []
    for cod_estado, titulo, badge_class in columnas_estados:
        if cod_estado == "PERDIDA":
            items = qs.filter(estado__in=["PERDIDA", "CANCELADA"]).order_by("-updated_at")[:20]
        else:
            items = qs.filter(estado=cod_estado).order_by("-created_at")[:25]
        
        monto_columna = sum(item.total_referencial_estimado for item in items)
        kanban_data.append({
            "codigo": cod_estado,
            "titulo": titulo,
            "badge_class": badge_class,
            "items": items,
            "conteo": items.count(),
            "monto_total": monto_columna,
        })

    User = get_user_model()
    usuarios_staff = User.objects.filter(is_active=True).order_by("first_name", "username")

    context = {
        "kanban_data": kanban_data,
        "estados": SolicitudCotizacion.ESTADOS,
        "usuarios_staff": usuarios_staff,
        "ver_pruebas": ver_pruebas,
    }
    return render(request, "gestion/solicitudes/kanban.html", context)


@gestion_required
@permiso_requerido("gestion.can_manage_solicitudes")
def solicitud_detalle_view(request, id):
    """
    Ficha de Solicitud 360° con snapshots, validación técnica y bitácora de seguimiento.
    """
    solicitud = get_object_or_404(
        SolicitudCotizacion.objects.select_related("establecimiento_ref", "contacto_ref", "responsable")
        .prefetch_related("items__producto"),
        id=id
    )

    items = solicitud.items.all().select_related("producto")
    User = get_user_model()
    usuarios_staff = User.objects.filter(is_active=True).order_by("first_name", "username")

    # Verificar si existe cotización formal asociada
    cotizacion_formal = getattr(solicitud, "cotizacion_formal", None)

    context = {
        "solicitud": solicitud,
        "items": items,
        "usuarios_staff": usuarios_staff,
        "estados": SolicitudCotizacion.ESTADOS,
        "subestados_cierre": SolicitudCotizacion.SUBESTADOS_CIERRE,
        "cotizacion_formal": cotizacion_formal,
        "requiere_validacion": solicitud.requiere_validacion_tecnica,
    }
    return render(request, "gestion/solicitudes/detalle.html", context)


@gestion_required
@permiso_requerido("gestion.can_manage_solicitudes")
@require_POST
def solicitud_cambiar_estado_view(request, id):
    """
    Actualiza el estado comercial, responsable o bitácora de una solicitud.
    """
    solicitud = get_object_or_404(SolicitudCotizacion, id=id)
    is_ajax = request.headers.get("x-requested-with") == "XMLHttpRequest"

    nuevo_estado = request.POST.get("estado")
    responsable_id = request.POST.get("responsable")
    nueva_nota = request.POST.get("nueva_nota", "").strip()
    subestado_cierre = request.POST.get("subestado_cierre", "").strip()
    monto_vendido_raw = request.POST.get("monto_final_vendido", "").strip()

    cambios = []
    detalles_log = {}

    if nuevo_estado and nuevo_estado != solicitud.estado:
        cambios.append(f"Estado: {solicitud.get_estado_display()} → {dict(SolicitudCotizacion.ESTADOS).get(nuevo_estado, nuevo_estado)}")
        detalles_log["estado_anterior"] = solicitud.estado
        detalles_log["estado_nuevo"] = nuevo_estado
        solicitud.estado = nuevo_estado

    if responsable_id is not None:
        User = get_user_model()
        if responsable_id == "" or responsable_id == "0":
            if solicitud.responsable:
                cambios.append("Responsable: Desasignado")
                solicitud.responsable = None
        else:
            resp_user = User.objects.filter(id=responsable_id).first()
            if resp_user and resp_user != solicitud.responsable:
                cambios.append(f"Responsable: {resp_user.get_full_name() or resp_user.username}")
                solicitud.responsable = resp_user

    if subestado_cierre:
        solicitud.subestado_cierre = subestado_cierre

    if monto_vendido_raw:
        try:
            solicitud.monto_final_vendido = Decimal(monto_vendido_raw)
            cambios.append(f"Monto vendido: ${solicitud.monto_final_vendido:,.0f} CLP")
        except Exception:
            pass

    if nueva_nota:
        from django.utils import timezone
        now = timezone.now()
        timestamp_str = f"[{now:%Y-%m-%d %H:%M} — {request.user.first_name or request.user.username}]:"
        nota_formateada = f"{timestamp_str} {nueva_nota}\n\n{solicitud.notas_internas_humm}"
        solicitud.notas_internas_humm = nota_formateada.strip()
        cambios.append("Nueva nota de bitácora añadida")

    # IDs Mercado Público opcionales
    id_lic = request.POST.get("id_licitacion_mp")
    if id_lic is not None:
        solicitud.id_licitacion_mp = id_lic.strip()
    id_ca = request.POST.get("id_compra_agil_mp")
    if id_ca is not None:
        solicitud.id_compra_agil_mp = id_ca.strip()
    id_oc = request.POST.get("id_orden_compra_mp")
    if id_oc is not None:
        solicitud.id_orden_compra_mp = id_oc.strip()

    # Guardar
    solicitud.save()

    if cambios:
        desc = f"Actualización solicitud {solicitud.codigo_seguimiento}: " + " | ".join(cambios)
        registrar_actividad(
            request=request,
            accion="CAMBIO_ESTADO_SOLICITUD",
            modelo_afectado="SolicitudCotizacion",
            objeto_id=solicitud.id,
            descripcion=desc,
            detalles=detalles_log
        )
        if not is_ajax:
            messages.success(request, desc)

    if is_ajax:
        return JsonResponse({
            "status": "ok",
            "mensaje": "Solicitud actualizada correctamente.",
            "estado": solicitud.estado,
            "estado_display": solicitud.get_estado_display(),
        })

    return redirect("gestion:solicitud_detalle", id=solicitud.id)


@gestion_required
@permiso_requerido("gestion.can_manage_solicitudes")
def solicitud_eliminar_view(request, id):
    """
    Eliminación controlada y segura de solicitudes de prueba interna (es_prueba=True).
    Rechaza estrictamente la eliminación de solicitudes comerciales reales (es_prueba=False).
    Requiere confirmación explícita y se ejecuta mediante POST + CSRF.
    """
    solicitud = get_object_or_404(
        SolicitudCotizacion.objects.select_related("establecimiento_ref", "contacto_ref"),
        id=id
    )

    # REGLA DE SEGURIDAD OBLIGATORIA (Ajuste Humm):
    # El backend debe impedir completamente eliminar cualquier solicitud donde es_prueba == False.
    if not solicitud.es_prueba:
        raise PermissionDenied("Seguridad EduCompra: Las solicitudes comerciales reales no pueden ser eliminadas.")

    tiene_cotizacion = hasattr(solicitud, "cotizacion_formal") and solicitud.cotizacion_formal is not None

    if request.method == "POST":
        if request.POST.get("confirmar") != "1":
            messages.warning(request, "Confirmación no recibida. La solicitud de prueba no fue eliminada.")
            return redirect("gestion:solicitud_detalle", id=solicitud.id)

        # Doble verificación estricta en servidor
        if not solicitud.es_prueba:
            raise PermissionDenied("Seguridad EduCompra: Las solicitudes comerciales reales no pueden ser eliminadas.")

        codigo = solicitud.codigo_seguimiento
        sol_id = solicitud.id
        establecimiento_nombre = solicitud.establecimiento
        email_sol = solicitud.email
        fecha_creacion = solicitud.created_at.isoformat() if solicitud.created_at else None

        with transaction.atomic():
            # AUDITORÍA OBLIGATORIA ANTES DE ELIMINAR
            registrar_actividad(
                request=request,
                accion="CAMBIO_ESTADO_SOLICITUD",
                modelo_afectado="SolicitudCotizacion",
                objeto_id=str(sol_id),
                descripcion="ELIMINACIÓN CONTROLADA DE SOLICITUD DE PRUEBA",
                detalles={
                    "usuario": request.user.username if request.user.is_authenticated else "Sistema",
                    "codigo_seguimiento": codigo,
                    "id": sol_id,
                    "establecimiento": establecimiento_nombre,
                    "email": email_sol,
                    "fecha": fecha_creacion,
                    "existencia_cotizacion_asociada": tiene_cotizacion,
                }
            )
            solicitud.delete()

        messages.success(
            request,
            f"Solicitud de prueba {codigo} y sus registros dependientes fueron eliminados permanentemente."
        )
        return redirect(reverse("gestion:solicitudes_lista") + "?ver_pruebas=1")

    # GET: Mostrar pantalla de confirmación
    context = {
        "solicitud": solicitud,
        "codigo_seguimiento": solicitud.codigo_seguimiento,
        "nombre_solicitante": solicitud.nombre_solicitante,
        "establecimiento": solicitud.establecimiento,
        "fecha": solicitud.created_at,
        "cantidad_productos": solicitud.items.count(),
        "monto_referencial": solicitud.total_referencial_estimado,
        "tiene_cotizacion_formal": tiene_cotizacion,
    }
    return render(request, "gestion/solicitudes/confirmar_eliminar.html", context)


@gestion_required
@permiso_requerido("gestion.can_manage_solicitudes")
def solicitudes_eliminar_masivo_view(request):
    """
    Limpieza masiva controlada de solicitudes de prueba seleccionadas.
    Solo acepta registros donde es_prueba=True.
    Requiere confirmación explícita y se ejecuta bajo transaction.atomic().
    """
    if request.method != "POST":
        return redirect(reverse("gestion:solicitudes_lista") + "?ver_pruebas=1")

    selected_ids = request.POST.getlist("selected_ids")
    if not selected_ids:
        messages.warning(request, "Debe seleccionar al menos una solicitud de prueba.")
        return redirect(reverse("gestion:solicitudes_lista") + "?ver_pruebas=1")

    # Obtener solicitudes seleccionadas
    solicitudes = SolicitudCotizacion.objects.filter(id__in=selected_ids)

    # REGLA DE SEGURIDAD OBLIGATORIA:
    # La selección solo debe aceptar registros es_prueba=True.
    if solicitudes.filter(es_prueba=False).exists():
        raise PermissionDenied(
            "Seguridad EduCompra: Se detectaron solicitudes comerciales reales en la selección. "
            "La eliminación masiva solo está autorizada para solicitudes de prueba."
        )

    solicitudes_pruebas = list(solicitudes.filter(es_prueba=True))
    if not solicitudes_pruebas:
        messages.warning(request, "No se encontraron solicitudes de prueba válidas en la selección.")
        return redirect(reverse("gestion:solicitudes_lista") + "?ver_pruebas=1")

    # Si viene con confirmación explícita, ejecutar dentro de transaction.atomic()
    if request.POST.get("confirmar") == "1":
        with transaction.atomic():
            conteo = len(solicitudes_pruebas)
            for sol in solicitudes_pruebas:
                tiene_cot = hasattr(sol, "cotizacion_formal") and sol.cotizacion_formal is not None
                registrar_actividad(
                    request=request,
                    accion="CAMBIO_ESTADO_SOLICITUD",
                    modelo_afectado="SolicitudCotizacion",
                    objeto_id=str(sol.id),
                    descripcion="ELIMINACIÓN CONTROLADA DE SOLICITUD DE PRUEBA",
                    detalles={
                        "usuario": request.user.username if request.user.is_authenticated else "Sistema",
                        "codigo_seguimiento": sol.codigo_seguimiento,
                        "id": sol.id,
                        "establecimiento": sol.establecimiento,
                        "email": sol.email,
                        "fecha": sol.created_at.isoformat() if sol.created_at else None,
                        "existencia_cotizacion_asociada": tiene_cot,
                        "eliminacion_masiva": True,
                    }
                )
                sol.delete()

        messages.success(request, f"Se eliminaron exitosamente {conteo} solicitudes de prueba seleccionadas.")
        return redirect(reverse("gestion:solicitudes_lista") + "?ver_pruebas=1")

    # Mostrar pantalla de confirmación masiva
    items_confirmacion = []
    for s in solicitudes_pruebas:
        tiene_cot = hasattr(s, "cotizacion_formal") and s.cotizacion_formal is not None
        items_confirmacion.append({
            "solicitud": s,
            "codigo": s.codigo_seguimiento,
            "fecha": s.created_at,
            "solicitante": s.nombre_solicitante,
            "email": s.email,
            "establecimiento": s.establecimiento,
            "tiene_cotizacion": tiene_cot,
        })

    context = {
        "solicitudes_confirmacion": items_confirmacion,
        "total_seleccionadas": len(solicitudes_pruebas),
        "selected_ids": [str(s.id) for s in solicitudes_pruebas],
    }
    return render(request, "gestion/solicitudes/confirmar_eliminar_masivo.html", context)

