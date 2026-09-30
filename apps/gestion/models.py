"""
Modelos de telemetría de primera parte, auditoría operativa y control de importaciones
para la plataforma de Administración EduCompra Humm (/gestion/).
"""

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.db import models
from apps.core.normalizacion import normalizar_texto_busqueda

# Almacenamiento privado seguro fuera de DocumentRoot y fuera de MEDIA_ROOT (Ajuste #10)
almacenamiento_privado_importaciones = FileSystemStorage(
    location=settings.PRIVATE_STORAGE_ROOT
)


class EventoUso(models.Model):
    """
    Telemetría soberana de primera parte (Ajustes Obligatorios #1, #2 y #3 de Humm).
    - Cero Google Analytics ni trackers invasivos.
    - Seudónimo: NUNCA almacena la session_key real, solo session_hash irreversible.
    - Metadata estrictamente controlada con lista blanca.
    """
    TIPOS_EVENTO = [
        ("VISITA", "Visita a página pública"),
        ("BUSQUEDA", "Búsqueda en catálogo"),
        ("VER_PRODUCTO", "Visualización de ficha de producto"),
        ("AGREGAR_COTIZACION", "Producto agregado a Mi Cotización"),
        ("QUITAR_COTIZACION", "Producto retirado de Mi Cotización"),
        ("VER_MI_COTIZACION", "Visualización de canasta"),
        ("INICIAR_SOLICITUD", "Formulario de solicitud abierto"),
        ("ENVIAR_SOLICITUD", "Solicitud de cotización enviada exitosamente"),
    ]

    # Whitelist estricta de claves permitidas en metadata (Ajuste Obligatorio #3)
    METADATA_WHITELIST = {
        "path",
        "query_params",
        "referrer_host",
        "product_sku",
        "cart_items_count",
        "filter_category",
        "filter_tech",
        "filter_difficulty",
        "order_by",
        "cantidad",
    }

    tipo_evento = models.CharField(max_length=30, choices=TIPOS_EVENTO, db_index=True)
    session_hash = models.CharField(
        max_length=64,
        db_index=True,
        verbose_name="Hash Seudónimo de Sesión (HMAC-SHA256)",
        help_text="Identificador irreversible generado con secreto de servidor. Nunca almacena la session_key real."
    )
    producto = models.ForeignKey(
        "catalogo.Producto",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="eventos_uso",
        verbose_name="Producto Asociado"
    )
    categoria = models.ForeignKey(
        "catalogo.Categoria",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="eventos_uso",
        verbose_name="Categoría Asociada"
    )
    termino_busqueda = models.CharField(max_length=255, blank=True, db_index=True)
    termino_busqueda_normalizado = models.CharField(max_length=255, blank=True, db_index=True)
    resultados_busqueda = models.PositiveIntegerField(null=True, blank=True)
    solicitud = models.ForeignKey(
        "cotizaciones.SolicitudCotizacion",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="eventos_asociados",
        verbose_name="Solicitud Asociada"
    )
    establecimiento = models.ForeignKey(
        "cotizaciones.Establecimiento",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="eventos_asociados",
        verbose_name="Establecimiento Asociado"
    )
    fuente = models.CharField(max_length=100, blank=True, verbose_name="Fuente / Referrer")
    utm_source = models.CharField(max_length=100, blank=True, verbose_name="UTM Source")
    utm_medium = models.CharField(max_length=100, blank=True, verbose_name="UTM Medium")
    utm_campaign = models.CharField(max_length=150, blank=True, verbose_name="UTM Campaign")
    metadata = models.JSONField(
        default=dict,
        blank=True,
        verbose_name="Metadata Controlada",
        help_text="Solo claves autorizadas de navegación. Prohibido almacenar datos personales o secretos."
    )
    created_at = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name="Fecha y Hora")

    class Meta:
        verbose_name = "Evento de Uso"
        verbose_name_plural = "Eventos de Uso"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["tipo_evento", "created_at"]),
            models.Index(fields=["session_hash", "created_at"]),
            models.Index(fields=["producto", "tipo_evento"]),
            models.Index(fields=["termino_busqueda_normalizado", "resultados_busqueda"]),
        ]

    def __str__(self):
        return f"[{self.tipo_evento}] {self.session_hash[:8]}... ({self.created_at:%Y-%m-%d %H:%M})"

    def save(self, *args, **kwargs):
        if self.termino_busqueda and not self.termino_busqueda_normalizado:
            self.termino_busqueda_normalizado = normalizar_texto_busqueda(self.termino_busqueda)
        # Filtrar metadata contra whitelist estricta (Ajuste #3)
        if isinstance(self.metadata, dict):
            self.metadata = {k: v for k, v in self.metadata.items() if k in self.METADATA_WHITELIST}
        super().save(*args, **kwargs)


class RegistroActividad(models.Model):
    """
    Log estructurado de auditoría operativa para acciones críticas en /gestion/ (Ajuste #30).
    """
    ACCIONES = [
        ("PUBLICAR_PRODUCTO", "Publicar Producto"),
        ("DESPUBLICAR_PRODUCTO", "Despublicar Producto"),
        ("CREAR_PRODUCTO", "Crear Producto Manual"),
        ("EDITAR_PRODUCTO", "Editar Ficha de Producto"),
        ("EDITAR_PRECIO", "Cambio de Precio / Costo"),
        ("CAMBIO_ESTADO_SOLICITUD", "Cambio de Estado de Solicitud"),
        ("ASIGNAR_RESPONSABLE", "Asignación de Responsable Humm"),
        ("ACTUALIZAR_NOTAS_SOLICITUD", "Actualización de Bitácora Solicitud"),
        ("VALIDAR_TECNICA", "Validación Técnica Neutra"),
        ("IMPORTACION_DRY_RUN", "Simulación DRY-RUN de Catálogo"),
        ("IMPORTACION_EJECUTADA", "Importación Productiva de Catálogo"),
        ("MODIFICAR_PRICING", "Modificación de Parámetros de Pricing"),
        ("RECALCULAR_PRECIOS_MASIVO", "Recálculo Masivo de Precios"),
        ("CONCILIACION_ESTABLECIMIENTOS", "Ejecución de Conciliación Histórica"),
    ]

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Usuario Responsable"
    )
    accion = models.CharField(max_length=60, choices=ACCIONES, db_index=True, verbose_name="Acción")
    modelo_afectado = models.CharField(max_length=60, verbose_name="Modelo Afectado")
    objeto_id = models.CharField(max_length=60, blank=True, verbose_name="ID Objeto")
    descripcion = models.CharField(max_length=255, verbose_name="Descripción de la Acción")
    detalles = models.JSONField(
        default=dict,
        blank=True,
        verbose_name="Detalles Estructurados",
        help_text="Registro de cambios (valor anterior/nuevo). Cero contraseñas, secretos o datos sensibles."
    )
    ip_origen = models.GenericIPAddressField(null=True, blank=True, verbose_name="IP de Origen")
    created_at = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name="Fecha y Hora")

    class Meta:
        verbose_name = "Registro de Actividad"
        verbose_name_plural = "Registros de Actividad"
        ordering = ["-created_at"]
        permissions = [
            ("can_view_gestion", "Puede acceder a la plataforma de administración EduCompra"),
            ("can_manage_catalogo", "Puede administrar catálogo de productos"),
            ("can_publish_producto", "Puede publicar o despublicar productos"),
            ("can_run_importaciones", "Puede ejecutar importaciones masivas de catálogo"),
            ("can_manage_solicitudes", "Puede gestionar solicitudes comerciales"),
            ("can_manage_cotizaciones", "Puede gestionar cotizaciones formales"),
            ("can_manage_establecimientos", "Puede gestionar establecimientos y contactos"),
            ("can_view_analitica", "Puede visualizar analítica y telemetría"),
            ("can_manage_configuracion", "Puede modificar parámetros de pricing y configuración"),
        ]

    def __str__(self):
        usr = self.usuario.username if self.usuario else "Sistema"
        return f"{self.created_at:%Y-%m-%d %H:%M} | {usr} | {self.accion} | {self.descripcion}"


class LoteImportacion(models.Model):
    """
    Control de importaciones web masivas de catálogo con almacenamiento privado (Ajustes #10, #11 y #12).
    """
    ESTADOS = [
        ("SUBIDO", "Archivo subido — Pendiente DRY-RUN"),
        ("SIMULADO", "DRY-RUN completado con éxito"),
        ("CON_CONFLICTOS", "DRY-RUN completado con advertencias/conflictos"),
        ("APROBADO", "Aprobado para importación"),
        ("APLICADO", "Importación productiva ejecutada"),
        ("FALLIDO", "Error en ejecución"),
    ]

    archivo_excel = models.FileField(
        storage=almacenamiento_privado_importaciones,
        upload_to="excel/%Y/%m/",
        verbose_name="Archivo Excel (.xlsx / .xls)"
    )
    archivo_imagenes_zip = models.FileField(
        storage=almacenamiento_privado_importaciones,
        upload_to="zip/%Y/%m/",
        blank=True,
        null=True,
        verbose_name="Archivo ZIP de Imágenes"
    )
    estado = models.CharField(max_length=30, choices=ESTADOS, default="SUBIDO", db_index=True, verbose_name="Estado")
    es_dry_run = models.BooleanField(default=True, verbose_name="Es Simulación (DRY-RUN)")
    usuario_creador = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Usuario que Subió el Lote"
    )

    # Métricas consolidadas del procesamiento
    filas_leidas = models.PositiveIntegerField(default=0, verbose_name="Filas Leídas")
    skus_detectados = models.PositiveIntegerField(default=0, verbose_name="SKUs Detectados")
    productos_nuevos = models.PositiveIntegerField(default=0, verbose_name="Productos Nuevos")
    productos_actualizados = models.PositiveIntegerField(default=0, verbose_name="Productos Actualizados")
    productos_sin_cambios = models.PositiveIntegerField(default=0, verbose_name="Productos sin Cambios")
    conflictos_detectados = models.PositiveIntegerField(default=0, verbose_name="Conflictos Detectados")
    productos_sin_imagen = models.PositiveIntegerField(default=0, verbose_name="Productos sin Imagen")
    imagenes_sin_producto = models.PositiveIntegerField(default=0, verbose_name="Imágenes sin Producto")

    resumen_json = models.JSONField(default=dict, blank=True, verbose_name="Resumen JSON")
    registro_conflictos_md = models.TextField(blank=True, verbose_name="Registro de Conflictos Markdown")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Última Actualización")

    class Meta:
        verbose_name = "Lote de Importación"
        verbose_name_plural = "Lotes de Importación"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Lote #{self.id} ({self.created_at:%Y-%m-%d %H:%M}) — {self.get_estado_display()}"
