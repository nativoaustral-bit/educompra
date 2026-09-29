"""
Gestión de correos electrónicos de EduCompra Humm.
Implementa el principio: GUARDAR PRIMERO, NOTIFICAR DESPUÉS.
Cualquier fallo de envío o conexión SMTP se registra en logs y no interrumpe el flujo.
"""

import logging
from django.conf import settings
from django.core.mail import send_mail

logger = logging.getLogger(__name__)


def _formatear_clp(monto):
    """Formatea un monto decimal como $X.XXX en formato chileno."""
    try:
        val = int(round(monto))
        return f"${val:,}".replace(",", ".")
    except Exception:
        return f"${monto}"


def enviar_correos_solicitud(solicitud, request=None):
    """
    Envía las notificaciones de correo tras la confirmación exitosa en base de datos.
    1. Correo de acuse de recibo al profesor / solicitante.
    2. Correo de alerta interna al equipo comercial y técnico de Humm.
    """
    items = list(solicitud.items.all())
    total_formateado = _formatear_clp(solicitud.total_referencial_estimado)

    # --------------------------------------------------------------------------
    # 1. Correo al Solicitante / Profesor
    # --------------------------------------------------------------------------
    asunto_docente = f"Recepción de Solicitud de Cotización [{solicitud.codigo_seguimiento}] — EduCompra Humm"
    
    lineas_items = []
    for item in items:
        precio_u = _formatear_clp(item.precio_referencial_unitario_snapshot)
        subt = _formatear_clp(item.subtotal_referencial_snapshot)
        lineas_items.append(
            f"- {item.cantidad} x {item.nombre_comercial_snapshot} ({item.unidad_comercial_snapshot}) — {precio_u} c/u | Subtotal: {subt}"
        )
    tabla_items_texto = "\n".join(lineas_items)

    cuerpo_docente = f"""Estimado(a) {solicitud.nombre_solicitante},

Hemos recibido exitosamente su solicitud de cotización para {solicitud.establecimiento}.

Código de Solicitud: {solicitud.codigo_seguimiento}

DETALLE DE PRODUCTOS SOLICITADOS:
----------------------------------------------------------------------
{tabla_items_texto}
----------------------------------------------------------------------
TOTAL REFERENCIAL ESTIMADO (IVA incluido): {total_formateado}

INFORMACIÓN IMPORTANTE:
Los valores indicados son referenciales con IVA incluido para efectos de presupuesto escolar y formulación de proyectos. Nuestro equipo técnico-comercial revisará disponibilidad de stock y emitirá su cotización formal en un plazo de 24 a 48 horas hábiles.

Si requiere canalizar esta compra mediante Mercado Público (Compra Ágil, Licitación, Convenio Marco) o fondos SEP / FAEP, por favor respóndanos a este correo para coordinar los antecedentes requeridos.

Atentamente,
Equipo EduCompra Humm
Tecnología Educativa
Sitio web: https://educompra.humm.cl
Contacto: {settings.DEFAULT_FROM_EMAIL}
"""

    try:
        send_mail(
            subject=asunto_docente,
            message=cuerpo_docente,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[solicitud.email],
            fail_silently=False,
        )
        logger.info("Correo al solicitante enviado para %s", solicitud.codigo_seguimiento)
    except Exception as e:
        logger.error(
            "Fallo al enviar correo al solicitante %s para solicitud %s: %s",
            solicitud.email,
            solicitud.codigo_seguimiento,
            str(e)
        )

    # --------------------------------------------------------------------------
    # 2. Correo de Notificación Interna a Humm
    # --------------------------------------------------------------------------
    admin_email = getattr(settings, "HUMM_COTIZACIONES_EMAIL", getattr(settings, "NOTIFICACIONES_ADMIN_EMAIL", "contacto@humm.cl"))
    asunto_admin = f"[NUEVA SOLICITUD] {solicitud.codigo_seguimiento} — {solicitud.establecimiento} ({solicitud.region})"

    alerta_validacion = ""
    if solicitud.requiere_validacion_tecnica:
        alerta_validacion = (
            "\n⚠️ ATENCIÓN: Esta solicitud contiene productos cuya especificación técnica "
            "neutra aún NO ha sido validada documentalmente por Humm. Se requiere validación técnica "
            "antes de emitir documentos para licitación o compra pública.\n"
        )

    cuerpo_admin = f"""Nueva solicitud de cotización recibida en EduCompra Humm.

Código: {solicitud.codigo_seguimiento}
UUID Token: {solicitud.token}
Fecha: {solicitud.created_at}
{alerta_validacion}
DATOS DEL SOLICITANTE:
- Nombre: {solicitud.nombre_solicitante}
- Cargo: {solicitud.cargo_solicitante or 'No indicado'}
- Email: {solicitud.email}
- Teléfono / WhatsApp: {solicitud.telefono}
- Establecimiento: {solicitud.establecimiento}
- Tipo Institución: {solicitud.tipo_institucion or 'No indicado'}
- Región: {solicitud.region}
- Comuna: {solicitud.comuna}
- Institución Responsable de Compra: {solicitud.institucion_responsable_compra or 'No indicado'}
- RUT Institución: {solicitud.rut_institucion or 'No indicado'}
- Encargado de Compras: {solicitud.contacto_adquisiciones_nombre or 'No indicado'} ({solicitud.contacto_adquisiciones_email or 'Sin email'})
- Proyecto Educativo: {solicitud.proyecto_educativo or 'No indicado'}
- Fecha Requerida Aprox: {solicitud.fecha_requerida_aproximada or 'No indicado'}

PRODUCTOS:
{tabla_items_texto}

TOTAL ESTIMADO REFERENCIAL: {total_formateado}

OBSERVACIONES DEL PROFESOR:
{solicitud.observaciones or 'Sin observaciones adicionales.'}

Administrar solicitud en el panel:
/admin/cotizaciones/solicitudcotizacion/{solicitud.id}/change/
"""

    try:
        send_mail(
            subject=asunto_admin,
            message=cuerpo_admin,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[admin_email],
            fail_silently=False,
        )
        logger.info("Correo interno enviado para %s a %s", solicitud.codigo_seguimiento, admin_email)
    except Exception as e:
        logger.error(
            "Fallo al enviar correo interno para solicitud %s: %s",
            solicitud.codigo_seguimiento,
            str(e)
        )
