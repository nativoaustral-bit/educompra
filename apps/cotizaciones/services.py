"""
Capa de servicio para la gestión de canasta ('Mi Cotización'),
revalidación estricta de productos, idempotencia y creación de solicitudes.
"""

import uuid
import logging
from decimal import Decimal
from django.db import transaction
from django.core.exceptions import ValidationError
from apps.catalogo.models import Producto
from .models import SolicitudCotizacion, SolicitudItem
from .emails import enviar_correos_solicitud

logger = logging.getLogger(__name__)

SESSION_CART_KEY = "mi_cotizacion"
SESSION_IDEMPOTENCY_KEY = "form_idempotency_token"
MAX_CANTIDAD_POR_ITEM = 500


import re

def calcular_desglose_unidades(unidad_str, cantidad):
    """
    Calcula la representación clara de cantidad × presentación comercial.
    Ej: 'pack (3 unidades)' x 2 -> '2 packs (6 unidades en total)'
        'set (120 cables)' x 2 -> '2 sets (240 cables en total)'
        'unidad' x 2 -> '2 unidades'
    """
    if not unidad_str or unidad_str == "unidad":
        return f"{cantidad} unidad" if cantidad == 1 else f"{cantidad} unidades"

    match = re.search(r'(pack|set)\s*\(\s*(\d+)\s+([^)]+)\)', unidad_str.lower())
    if match:
        tipo = match.group(1)
        piezas = int(match.group(2))
        nombre_pieza = match.group(3).strip()
        tipo_label = tipo if cantidad == 1 else f"{tipo}s"
        total_piezas = cantidad * piezas
        return f"{cantidad} {tipo_label} — {total_piezas} {nombre_pieza} en total"

    return f"{cantidad} {unidad_str}"


class CartService:
    @staticmethod
    def _obtener_canasta_sesion(request):
        """Retorna el diccionario de la sesión { 'producto_id': {'cantidad': int} }."""
        canasta = request.session.get(SESSION_CART_KEY)
        if not isinstance(canasta, dict):
            canasta = {}
            request.session[SESSION_CART_KEY] = canasta
        return canasta

    @classmethod
    def agregar_item(cls, request, producto_id, cantidad=1):
        """
        Agrega un producto a la canasta.
        Valida que el producto exista, esté activo y sea publicable.
        Valida que la cantidad sea un entero válido entre 1 y MAX_CANTIDAD_POR_ITEM.
        """
        try:
            cantidad = int(cantidad)
        except (ValueError, TypeError):
            raise ValidationError("La cantidad debe ser un número entero.")

        if cantidad <= 0:
            raise ValidationError("La cantidad debe ser mayor a 0.")
        if cantidad > MAX_CANTIDAD_POR_ITEM:
            raise ValidationError(f"La cantidad máxima permitida por producto es {MAX_CANTIDAD_POR_ITEM}.")

        # Revalidar producto en BD con regla de visibilidad pública
        producto = Producto.objects.publicables(user=request.user).filter(id=producto_id).first()
        if not producto:
            raise ValidationError("El producto no existe o no está disponible para cotización.")

        canasta = cls._obtener_canasta_sesion(request)
        prod_key = str(producto.id)
        
        cant_actual = canasta.get(prod_key, {}).get("cantidad", 0) if isinstance(canasta.get(prod_key), dict) else 0
        nueva_cant = cant_actual + cantidad

        if nueva_cant > MAX_CANTIDAD_POR_ITEM:
            nueva_cant = MAX_CANTIDAD_POR_ITEM

        canasta[prod_key] = {"cantidad": nueva_cant}
        request.session[SESSION_CART_KEY] = canasta
        request.session.modified = True
        return producto, nueva_cant

    @classmethod
    def actualizar_cantidad(cls, request, producto_id, cantidad):
        """Actualiza la cantidad de un producto o lo elimina si la cantidad es 0."""
        try:
            cantidad = int(cantidad)
        except (ValueError, TypeError):
            raise ValidationError("La cantidad debe ser un número entero.")

        if cantidad < 0:
            raise ValidationError("La cantidad no puede ser negativa.")
        if cantidad > MAX_CANTIDAD_POR_ITEM:
            raise ValidationError(f"La cantidad máxima permitida es {MAX_CANTIDAD_POR_ITEM}.")

        canasta = cls._obtener_canasta_sesion(request)
        prod_key = str(producto_id)

        if cantidad == 0:
            if prod_key in canasta:
                del canasta[prod_key]
                request.session.modified = True
            return 0

        # Verificar que el producto sea publicable
        producto = Producto.objects.publicables(user=request.user).filter(id=producto_id).first()
        if not producto:
            if prod_key in canasta:
                del canasta[prod_key]
                request.session.modified = True
            raise ValidationError("El producto no se encuentra disponible actualmente.")

        canasta[prod_key] = {"cantidad": cantidad}
        request.session[SESSION_CART_KEY] = canasta
        request.session.modified = True
        return cantidad

    @classmethod
    def eliminar_item(cls, request, producto_id):
        """Elimina un producto de la canasta."""
        canasta = cls._obtener_canasta_sesion(request)
        prod_key = str(producto_id)
        if prod_key in canasta:
            del canasta[prod_key]
            request.session.modified = True
            return True
        return False

    @classmethod
    def vaciar_canasta(cls, request):
        """Vacía completamente la canasta."""
        request.session[SESSION_CART_KEY] = {}
        request.session.modified = True

    @classmethod
    def obtener_canasta_revalidada(cls, request):
        """
        Consulta la base de datos para reconstruir la canasta completa.
        - NO confía en precios en sesión (siempre toma precio vigente en BD).
        - Elimina de la sesión productos que ya no sean publicables y los reporta.
        - Calcula subtotales y total referencial con IVA.
        """
        canasta_raw = cls._obtener_canasta_sesion(request)
        if not canasta_raw:
            return {
                "items": [],
                "total_referencial": Decimal("0"),
                "total_articulos": 0,
                "items_retirados": [],
            }

        # Extraer IDs y cantidades deseadas
        id_cant_map = {}
        for k, v in canasta_raw.items():
            try:
                p_id = int(k)
                cant = int(v.get("cantidad", 1)) if isinstance(v, dict) else int(v)
                if 1 <= cant <= MAX_CANTIDAD_POR_ITEM:
                    id_cant_map[p_id] = cant
            except (ValueError, TypeError):
                continue

        # Consultar productos publicables actuales desde BD
        productos = Producto.objects.publicables(user=request.user).filter(
            id__in=id_cant_map.keys()
        ).select_related("categoria")

        encontrados_map = {p.id: p for p in productos}
        items = []
        items_retirados = []
        total_referencial = Decimal("0")
        total_articulos = 0
        nueva_canasta_sesion = {}

        # Reconstruir canasta y detectar productos despublicados o eliminados
        for p_id, cant in id_cant_map.items():
            producto = encontrados_map.get(p_id)
            if producto:
                precio_unitario = producto.precio_sugerido_total_clp
                subtotal = precio_unitario * cant
                total_referencial += subtotal
                total_articulos += cant
                nueva_canasta_sesion[str(p_id)] = {"cantidad": cant}

                # Descripción de unidad comercial detallada
                unidad = producto.unidad_compra or "unidad"
                items.append({
                    "producto": producto,
                    "cantidad": cant,
                    "unidad": unidad,
                    "desglose_unidades": calcular_desglose_unidades(unidad, cant),
                    "precio_unitario": precio_unitario,
                    "subtotal": subtotal,
                })
            else:
                # El producto estaba en sesión pero ya no es publicable
                items_retirados.append(p_id)

        # Si hubo productos retirados, actualizar la sesión limpia
        if items_retirados:
            request.session[SESSION_CART_KEY] = nueva_canasta_sesion
            request.session.modified = True

        return {
            "items": items,
            "total_referencial": total_referencial,
            "total_articulos": total_articulos,
            "items_retirados": items_retirados,
        }


class SubmissionService:
    @staticmethod
    def generar_token_idempotencia(request):
        """Genera un nuevo token de idempotencia y lo almacena en la sesión."""
        token = str(uuid.uuid4())
        request.session[SESSION_IDEMPOTENCY_KEY] = token
        request.session.modified = True
        return token

    @staticmethod
    def validar_y_consumir_token_idempotencia(request, token_recibido):
        """
        Valida que el token recibido coincida con el de la sesión y lo consume.
        Retorna True si es válido y único, False si ya fue consumido o es inválido.
        """
        if not token_recibido:
            return False
        token_guardado = request.session.get(SESSION_IDEMPOTENCY_KEY)
        if token_guardado and token_guardado == token_recibido:
            # Consumir el token inmediatamente para prevenir reenvíos por doble clic/refresh
            del request.session[SESSION_IDEMPOTENCY_KEY]
            request.session.modified = True
            return True
        return False

    @classmethod
    def crear_solicitud_cotizacion(cls, request, form_data):
        """
        Crea la solicitud de cotización dentro de una transacción atómica:
        1. Revalida que la canasta tenga ítems y todos sean publicables en BD.
        2. Crea SolicitudCotizacion con token público único y código EC-{año}-{correlativo}.
        3. Congela SolicitudItem con snapshots inmutables de precios y datos vigentes.
        4. Calcula total referencial.
        5. Vacía la canasta de la sesión.
        6. Tras el commit exitoso, dispara los correos en un bloque seguro.
        """
        canasta_info = CartService.obtener_canasta_revalidada(request)
        items = canasta_info["items"]

        if not items:
            raise ValidationError("Su lista de cotización está vacía o los productos seleccionados ya no están disponibles.")

        with transaction.atomic():
            solicitud = SolicitudCotizacion(
                nombre_solicitante=form_data["nombre_solicitante"].strip(),
                email=form_data["email"].strip().lower(),
                telefono=form_data["telefono"].strip(),
                establecimiento=form_data["establecimiento"].strip(),
                tipo_institucion=form_data.get("tipo_institucion", "").strip(),
                cargo_solicitante=form_data.get("cargo_solicitante", "").strip(),
                region=form_data["region"].strip(),
                comuna=form_data["comuna"].strip(),
                institucion_responsable_compra=form_data.get("institucion_responsable_compra", "").strip(),
                rut_institucion=form_data.get("rut_institucion", "").strip(),
                contacto_adquisiciones_nombre=form_data.get("nombre_encargado_compras", "").strip(),
                contacto_adquisiciones_email=form_data.get("email_encargado_compras", "").strip(),
                proyecto_educativo=form_data.get("proyecto_educativo", "").strip(),
                fecha_requerida_aproximada=form_data.get("fecha_requerida_aproximada", "").strip(),
                observaciones=form_data.get("observaciones", "").strip(),
                total_referencial_estimado=Decimal("0"),
            )
            # Atribución UTM desde sesión (Ajuste #34)
            utms = request.session.get("marketing_attribution", {})
            solicitud.utm_source = utms.get("utm_source", "")[:100]
            solicitud.utm_medium = utms.get("utm_medium", "")[:100]
            solicitud.utm_campaign = utms.get("utm_campaign", "")[:150]
            solicitud.utm_content = utms.get("utm_content", "")[:150]
            if utms.get("utm_source"):
                solicitud.fuente_origen = utms.get("utm_source")[:100]

            solicitud.save()

            # Vincular o registrar establecimiento y contacto (Ajustes #5, #7, #8, #9)
            est_obj, contacto_obj = cls._vincular_o_crear_entidades(solicitud, form_data)
            solicitud.establecimiento_ref = est_obj
            solicitud.contacto_ref = contacto_obj

            total_calculado = Decimal("0")
            for item in items:
                prod = item["producto"]
                cant = item["cantidad"]
                precio_unitario = prod.precio_sugerido_total_clp
                subtotal = precio_unitario * cant
                total_calculado += subtotal

                SolicitudItem.objects.create(
                    solicitud=solicitud,
                    producto=prod,
                    sku_humm_snapshot=prod.sku_humm,
                    sku_proveedor_snapshot=prod.sku_proveedor,
                    marca_snapshot=prod.marca,
                    modelo_snapshot=prod.modelo,
                    nombre_comercial_snapshot=prod.nombre_comercial,
                    unidad_comercial_snapshot=prod.unidad_compra or "unidad",
                    cantidad=cant,
                    precio_referencial_unitario_snapshot=precio_unitario,
                    subtotal_referencial_snapshot=subtotal,
                    especificacion_neutra_snapshot=prod.especificacion_tecnica_neutral or "",
                )

            solicitud.total_referencial_estimado = total_calculado
            solicitud.save(update_fields=["total_referencial_estimado", "establecimiento_ref", "contacto_ref"])

            # Vaciar la sesión
            CartService.vaciar_canasta(request)

        # Telemetría de envío de solicitud (Ajuste Obligatorio #1)
        try:
            from apps.gestion.services_telemetria import TelemetriaService
            TelemetriaService.registrar_evento(
                request,
                tipo_evento="ENVIAR_SOLICITUD",
                solicitud=solicitud,
                establecimiento=solicitud.establecimiento_ref,
                metadata={"cart_items_count": len(items)}
            )
        except Exception:
            pass

        # Regla: GUARDAR PRIMERO, NOTIFICAR DESPUÉS.
        # Commit de BD ya garantizado. Notificar por correo de forma resiliente.
        try:
            enviar_correos_solicitud(solicitud, request=request)
        except Exception as e:
            logger.error(
                "Error al enviar correos para solicitud %s: %s",
                solicitud.codigo_seguimiento,
                str(e),
                exc_info=True
            )

        return solicitud

    @classmethod
    def _vincular_o_crear_entidades(cls, solicitud, form_data):
        from apps.cotizaciones.models import Establecimiento, Contacto
        from apps.core.normalizacion import normalizar_texto_busqueda, normalizar_email, normalizar_rut
        from django.utils import timezone

        now = timezone.now()
        nombre_est = form_data["establecimiento"].strip()
        nombre_norm = normalizar_texto_busqueda(nombre_est)
        comuna = form_data["comuna"].strip()
        region = form_data["region"].strip()
        rut_est = normalizar_rut(form_data.get("rut_institucion", ""))
        tipo_inst = form_data.get("tipo_institucion", "").strip()

        # Jerarquía de match (Ajuste Obligatorio #5 de Humm):
        # Nivel 1: Identificador fuerte si existe RUT
        est = None
        if rut_est:
            est = Establecimiento.objects.filter(rut=rut_est).first()

        # Nivel 2: Coincidencia segura (nombre completo normalizado + comuna) sin quitar palabras institucionales
        if not est and nombre_norm and comuna:
            est = Establecimiento.objects.filter(nombre_normalizado=nombre_norm, comuna__iexact=comuna).first()

        if est:
            est.ultima_interaccion = now
            if rut_est and not est.rut:
                est.rut = rut_est
            est.save(update_fields=["ultima_interaccion", "rut", "updated_at"])
        else:
            est = Establecimiento.objects.create(
                nombre=nombre_est,
                tipo_institucion=tipo_inst,
                comuna=comuna,
                region=region,
                rut=rut_est,
                primera_interaccion=now,
                ultima_interaccion=now,
            )

        # Contacto (Ajustes #7 y #8)
        email_contacto = normalizar_email(form_data["email"])
        nombre_contacto = form_data["nombre_solicitante"].strip()
        telefono = form_data["telefono"].strip()
        cargo = form_data.get("cargo_solicitante", "").strip()

        contacto = Contacto.objects.filter(email=email_contacto).first()
        if contacto:
            contacto.ultima_interaccion = now
            if not contacto.establecimiento_principal:
                contacto.establecimiento_principal = est
            contacto.save(update_fields=["ultima_interaccion", "establecimiento_principal", "updated_at"])
        else:
            contacto = Contacto.objects.create(
                establecimiento_principal=est,
                nombre=nombre_contacto,
                cargo=cargo,
                email=email_contacto,
                telefono=telefono,
                primera_interaccion=now,
                ultima_interaccion=now,
            )

        return est, contacto
