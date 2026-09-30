"""
Servicio centralizado de publicación y despublicación controlada de productos (Ajustes #13 y #14 de Humm).
Valida todos los requisitos de calidad pedagógica y comercial antes de autorizar la exposición pública.
"""

from decimal import Decimal
from django.core.exceptions import ValidationError
from apps.gestion.services_auditoria import registrar_actividad


class ProductoPublicationService:
    @classmethod
    def validar_para_publicacion(cls, producto):
        """
        Verifica exhaustivamente que el producto cumpla los 8 requisitos de calidad Humm:
        1. activo == True
        2. estado_curaduria == 'VALIDADO'
        3. nombre_comercial no vacío
        4. categoria asignada y activa (distinta de 'Sin clasificar')
        5. descripcion_educativa no vacía
        6. al menos una imagen optimizada asociada
        7. precio_sugerido_total_clp mayor a cero
        8. unidad_compra poblada
        Retorna lista de motivos de rechazo (vacía si es apto).
        """
        motivos = []

        if not producto.activo:
            motivos.append("El producto está marcado como inactivo en el sistema maestro.")

        if producto.estado_curaduria != "VALIDADO":
            motivos.append(f"El estado de curaduría es '{producto.get_estado_curaduria_display()}' (requiere 'Curaduría pedagógica validada').")

        if not producto.nombre_comercial or not producto.nombre_comercial.strip():
            motivos.append("El nombre comercial está vacío.")

        if not producto.categoria:
            motivos.append("No tiene categoría asignada.")
        elif not producto.categoria.activa or producto.categoria.nombre.lower() in ("sin clasificar", "general"):
            motivos.append(f"La categoría '{producto.categoria.nombre}' no es válida para catálogo público.")

        if not producto.descripcion_educativa or len(producto.descripcion_educativa.strip()) < 15:
            motivos.append("Falta una descripción pedagógica explicativa para el docente.")

        # Verificar imágenes
        tiene_imagen = producto.imagenes.filter(archivo__isnull=False).exclude(archivo="").exists()
        if not tiene_imagen:
            motivos.append("No cuenta con ninguna fotografía o imagen asociada.")

        if producto.precio_sugerido_total_clp <= Decimal("0"):
            motivos.append("El precio referencial en pesos chilenos es cero o no calculable.")

        if not producto.unidad_compra or not producto.unidad_compra.strip():
            motivos.append("Falta definir la unidad de venta comercial (unidad, pack, set).")

        return motivos

    @classmethod
    def publicar(cls, producto, usuario=None, request=None):
        """
        Publica el producto en el catálogo escolar si satisface todos los requisitos.
        Registra la auditoría correspondiente.
        """
        motivos = cls.validar_para_publicacion(producto)
        if motivos:
            raise ValidationError(
                f"No se puede publicar el producto '{producto.sku_humm}': " + " | ".join(motivos)
            )

        if not producto.publicado:
            producto.publicado = True
            producto.save(update_fields=["publicado", "updated_at"])

            registrar_actividad(
                request=request,
                usuario=usuario,
                accion="PUBLICAR_PRODUCTO",
                modelo_afectado="Producto",
                objeto_id=producto.id,
                descripcion=f"Publicó '{producto.nombre_comercial}' [{producto.sku_humm}] en catálogo escolar.",
                detalles={
                    "sku_humm": producto.sku_humm,
                    "precio": str(producto.precio_sugerido_total_clp),
                    "categoria": producto.categoria.nombre if producto.categoria else None,
                }
            )
        return True

    @classmethod
    def despublicar(cls, producto, usuario=None, request=None, motivo=""):
        """
        Retira el producto del catálogo público sin alterar snapshots históricos ni solicitudes.
        Registra la auditoría correspondiente.
        """
        if producto.publicado:
            producto.publicado = False
            producto.save(update_fields=["publicado", "updated_at"])

            registrar_actividad(
                request=request,
                usuario=usuario,
                accion="DESPUBLICAR_PRODUCTO",
                modelo_afectado="Producto",
                objeto_id=producto.id,
                descripcion=f"Despublicó '{producto.nombre_comercial}' [{producto.sku_humm}]. Motivo: {motivo or 'Retiro operacional'}",
                detalles={
                    "sku_humm": producto.sku_humm,
                    "motivo": motivo or "Sin motivo especificado",
                }
            )
        return True
