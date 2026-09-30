"""
Servicio soberano de captura y deduplicación de telemetría (Ajustes Obligatorios #1, #2 y #3 de Humm).
- Seudónimo estricto mediante HMAC-SHA256 (session_hash).
- Deduplicación en memoria de sesión para visitas, vistas de producto y búsquedas.
- Filtrado estricto por lista blanca en metadata.
"""

import time
import logging
from django.utils import timezone
from apps.core.normalizacion import generar_session_hash, normalizar_texto_busqueda
from apps.gestion.models import EventoUso

logger = logging.getLogger(__name__)


def capturar_utms_en_sesion(request):
    """
    Captura y persiste parámetros UTM en la sesión para atribución de solicitudes.
    """
    utms = {}
    for param in ("utm_source", "utm_medium", "utm_campaign", "utm_content"):
        val = request.GET.get(param)
        if val:
            utms[param] = str(val)[:150].strip()
    if utms:
        actuales = request.session.get("marketing_attribution", {})
        actuales.update(utms)
        request.session["marketing_attribution"] = actuales
        request.session.modified = True
    return request.session.get("marketing_attribution", {})


class TelemetriaService:
    @classmethod
    def obtener_session_hash(cls, request):
        """
        Asegura que exista session_key y retorna su hash seudónimo irreversible.
        """
        if not request.session.session_key:
            request.session.save()
        return generar_session_hash(request.session.session_key)

    @classmethod
    def registrar_evento(cls, request, tipo_evento, producto=None, categoria=None,
                         termino_busqueda="", resultados_busqueda=None, solicitud=None,
                         establecimiento=None, metadata=None):
        """
        Registra un evento de telemetría aplicando políticas de deduplicación y privacidad.
        Falla de forma silenciosa para jamás interrumpir la navegación del usuario.
        """
        try:
            session_hash = cls.obtener_session_hash(request)
            now_ts = time.time()

            # 1. Política de deduplicación de VISITA: máx 1 cada 30 minutos (1800 seg)
            if tipo_evento == "VISITA":
                last_visit = request.session.get("_telemetria_last_visit", 0)
                if now_ts - last_visit < 1800:
                    return None
                request.session["_telemetria_last_visit"] = now_ts
                request.session.modified = True

            # 2. Política de deduplicación de VER_PRODUCTO: máx 1 cada 10 minutos (600 seg) por producto
            elif tipo_evento == "VER_PRODUCTO" and producto:
                vistos = request.session.get("_telemetria_prods_vistos", {})
                prod_key = str(producto.id)
                last_time = vistos.get(prod_key, 0)
                if now_ts - last_time < 600:
                    return None
                vistos[prod_key] = now_ts
                request.session["_telemetria_prods_vistos"] = vistos
                request.session.modified = True

            # 3. Política de deduplicación de VER_MI_COTIZACION: máx 1 cada 5 minutos (300 seg)
            elif tipo_evento == "VER_MI_COTIZACION":
                last_cart = request.session.get("_telemetria_last_cart", 0)
                if now_ts - last_cart < 300:
                    return None
                request.session["_telemetria_last_cart"] = now_ts
                request.session.modified = True

            # Captura de parámetros UTM desde la sesión
            utms = request.session.get("marketing_attribution", {})
            utm_source = utms.get("utm_source", "") or request.GET.get("utm_source", "")
            utm_medium = utms.get("utm_medium", "") or request.GET.get("utm_medium", "")
            utm_campaign = utms.get("utm_campaign", "") or request.GET.get("utm_campaign", "")

            # Referrer host
            fuente = ""
            ref = request.META.get("HTTP_REFERER", "")
            if ref:
                from urllib.parse import urlparse
                fuente = urlparse(ref).netloc[:100]

            # Término normalizado
            termino_norm = normalizar_texto_busqueda(termino_busqueda) if termino_busqueda else ""

            # Metadata sanitizada con whitelist
            meta_limpia = {}
            if isinstance(metadata, dict):
                meta_limpia = {k: v for k, v in metadata.items() if k in EventoUso.METADATA_WHITELIST}

            return EventoUso.objects.create(
                tipo_evento=tipo_evento,
                session_hash=session_hash,
                producto=producto,
                categoria=categoria or (producto.categoria if producto else None),
                termino_busqueda=termino_busqueda[:255] if termino_busqueda else "",
                termino_busqueda_normalizado=termino_norm[:255] if termino_norm else "",
                resultados_busqueda=resultados_busqueda,
                solicitud=solicitud,
                establecimiento=establecimiento,
                fuente=fuente,
                utm_source=utm_source[:100],
                utm_medium=utm_medium[:100],
                utm_campaign=utm_campaign[:150],
                metadata=meta_limpia,
            )
        except Exception as e:
            logger.warning("Error registrando telemetría pasiva: %s", str(e))
            return None
