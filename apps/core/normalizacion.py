"""
Utilidades de normalización de texto y hashes seudónimos para EduCompra Humm.
"""

import hmac
import hashlib
import unicodedata
from django.conf import settings


def normalizar_texto_busqueda(texto):
    """
    Normaliza texto para comparación y búsqueda:
    - Pasa a minúsculas
    - Remueve tildes y diacríticos
    - Colapsa espacios múltiples
    - PRESERVA palabras institucionales (colegio, liceo, escuela, etc.) según Ajuste Obligatorio #5 de Humm.
    """
    if not texto:
        return ""
    texto = str(texto).strip().lower()
    # Normalizar caracteres unicode (eliminar tildes)
    texto = "".join(
        c for c in unicodedata.normalize("NFD", texto)
        if unicodedata.category(c) != "Mn"
    )
    # Colapsar espacios
    return " ".join(texto.split())


def normalizar_email(email):
    """
    Normaliza una dirección de correo electrónico a minúsculas limpias.
    """
    if not email:
        return ""
    return str(email).strip().lower()


def normalizar_rut(rut):
    """
    Normaliza un RUT chileno eliminando puntos y espacios, manteniendo guion y dígito verificador en mayúscula.
    Ej: '12.345.678-k' -> '12345678-K'
    """
    if not rut:
        return ""
    limpio = str(rut).strip().upper().replace(".", "").replace(" ", "")
    if "-" not in limpio and len(limpio) >= 2:
        limpio = f"{limpio[:-1]}-{limpio[-1]}"
    return limpio


def generar_session_hash(session_key, hmac_key=None):
    """
    Genera un hash seudónimo irreversible de una session_key mediante HMAC-SHA256
    utilizando ANALYTICS_HMAC_KEY (clave independiente de SECRET_KEY, Ajuste Final Fase 5A).
    Permite agrupar eventos analíticos sin persistir jamás el identificador real de la sesión Django.
    """
    if not session_key:
        return ""
    if hmac_key is None:
        hmac_key = getattr(settings, "ANALYTICS_HMAC_KEY", "dev-insecure-analytics-hmac-key-educompra-local-test-only")
    if isinstance(hmac_key, str):
        hmac_key = hmac_key.encode("utf-8")
    h = hmac.new(hmac_key, str(session_key).encode("utf-8"), hashlib.sha256)
    return h.hexdigest()

