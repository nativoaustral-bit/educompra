"""
Vistas de administración de Contactos Docentes e Institucionales (/gestion/contactos/).
"""

from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from apps.gestion.decorators import gestion_required, permiso_requerido
from apps.gestion.services_auditoria import registrar_actividad
from apps.cotizaciones.models import Contacto, Establecimiento


@gestion_required
@permiso_requerido("gestion.can_manage_establecimientos")
def contactos_lista_view(request):
    """
    Directorio de docentes y encargados de compras con filtros y alertas de duplicados.
    """
    qs = Contacto.objects.all().select_related("establecimiento_principal")

    q = request.GET.get("q", "").strip()
    if q:
        qs = qs.filter(
            Q(nombre__icontains=q)
            | Q(email__icontains=q)
            | Q(cargo__icontains=q)
            | Q(telefono__icontains=q)
            | Q(establecimiento_principal__nombre__icontains=q)
        )

    posible_duplicado = request.GET.get("posible_duplicado")
    if posible_duplicado in ("true", "1"):
        qs = qs.filter(posible_duplicado=True)

    orden = request.GET.get("orden", "-ultima_interaccion")
    qs = qs.order_by(orden)

    total_contactos = qs.count()

    paginator = Paginator(qs, 25)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "total_contactos": total_contactos,
        "q": q,
        "duplicados_activos": posible_duplicado,
        "orden_activo": orden,
    }
    return render(request, "gestion/contactos/lista.html", context)


@gestion_required
@permiso_requerido("gestion.can_manage_establecimientos")
def contacto_editar_view(request, id):
    """
    Edición de datos de un Contacto Docente o Institucional (/gestion/contactos/<id>/editar/).
    Permite modificar únicamente:
    - nombre
    - cargo
    - email
    - teléfono / WhatsApp
    - establecimiento principal
    - encargado de compras
    - posible duplicado
    - activo
    - observaciones internas
    No permite eliminar contactos.
    """
    contacto = get_object_or_404(
        Contacto.objects.select_related("establecimiento_principal"),
        id=id
    )
    establecimientos = Establecimiento.objects.filter(activo=True).order_by("nombre")

    if request.method == "POST":
        nombre = request.POST.get("nombre", "").strip()
        email = request.POST.get("email", "").strip()

        if not nombre or not email:
            messages.error(request, "El nombre completo y correo electrónico son obligatorios.")
        else:
            contacto.nombre = nombre
            contacto.cargo = request.POST.get("cargo", "").strip()
            contacto.email = email
            contacto.telefono = request.POST.get("telefono", "").strip()

            estab_id = request.POST.get("establecimiento_principal", "").strip()
            if estab_id:
                contacto.establecimiento_principal = Establecimiento.objects.filter(id=estab_id).first()
            else:
                contacto.establecimiento_principal = None

            contacto.es_encargado_compras = request.POST.get("es_encargado_compras") == "on"
            contacto.posible_duplicado = request.POST.get("posible_duplicado") == "on"
            contacto.activo = request.POST.get("activo") == "on"
            contacto.observaciones_internas = request.POST.get("observaciones_internas", "").strip()
            contacto.save()

            registrar_actividad(
                request=request,
                accion="CAMBIO_ESTADO_SOLICITUD",
                modelo_afectado="Contacto",
                objeto_id=str(contacto.id),
                descripcion=f"Edición de contacto docente: {contacto.nombre} ({contacto.email})",
                detalles={
                    "nombre": contacto.nombre,
                    "email": contacto.email,
                    "telefono": contacto.telefono,
                    "cargo": contacto.cargo,
                    "activo": contacto.activo,
                }
            )

            messages.success(request, f"Contacto '{contacto.nombre}' actualizado correctamente.")
            return redirect("gestion:contactos_lista")

    context = {
        "contacto": contacto,
        "establecimientos": establecimientos,
    }
    return render(request, "gestion/contactos/editar.html", context)

