"""
Servicio centralizado de auditoría operativa para /gestion/ (Ajuste Obligatorio #30 de Humm).
Registra cambios críticos sanitizando detalles para excluir secretos o contraseñas.
"""

from apps.gestion.models import RegistroActividad

# Lista negra de claves que jamás deben persistirse en detalles de auditoría
CLAVES_PROHIBIDAS = {
    "password", "secret", "token", "csrftoken", "api_key", "secret_key",
    "authorization", "session_key", "contraseña", "credencial"
}


def sanitizar_detalles(detalles):
    """
    Filtra recursivamente cualquier clave sensible o valor prohibido.
    """
    if not isinstance(detalles, dict):
        return {}
    sanitizado = {}
    for k, v in detalles.items():
        k_str = str(k).lower().strip()
        if any(bad in k_str for bad in CLAVES_PROHIBIDAS):
            sanitizado[k] = "[REDACTADO]"
        elif isinstance(v, dict):
            sanitizado[k] = sanitizar_detalles(v)
        elif isinstance(v, (str, int, float, bool, type(None))):
            sanitizado[k] = v
        else:
            sanitizado[k] = str(v)[:255]
    return sanitizado


def registrar_actividad(request=None, accion="", modelo_afectado="", objeto_id="", descripcion="", detalles=None, usuario=None):
    """
    Registra una acción administrativa relevante en RegistroActividad.
    """
    if usuario is None and request:
        usuario = getattr(request, "user", None)
    if usuario and not usuario.is_authenticated:
        usuario = None

    ip = None
    if request:
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0].strip()
        else:
            ip = request.META.get("REMOTE_ADDR")

    detalles_limpios = sanitizar_detalles(detalles or {})

    return RegistroActividad.objects.create(
        usuario=usuario,
        accion=accion,
        modelo_afectado=modelo_afectado,
        objeto_id=str(objeto_id)[:60],
        descripcion=descripcion[:255],
        detalles=detalles_limpios,
        ip_origen=ip,
    )
