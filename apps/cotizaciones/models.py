import uuid
from decimal import Decimal
from django.conf import settings
from django.db import models
from apps.catalogo.models import Producto
from apps.core.normalizacion import normalizar_texto_busqueda, normalizar_email, normalizar_rut


class Establecimiento(models.Model):
    TIPOS_INSTITUCION = [
        ("MUNICIPAL_SLEP", "Municipal / Servicio Local de Educación (SLEP)"),
        ("PARTICULAR_SUBVENCIONADO", "Particular Subvencionado"),
        ("PARTICULAR_PAGADO", "Particular Pagado"),
        ("CORPORACION_FUNDACION", "Corporación / Fundación Educativa"),
        ("EDUCACION_SUPERIOR", "CFT / IP / Universidad"),
        ("OTRO", "Otro tipo de institución"),
    ]

    ESTADOS_CONCILIACION = [
        ("CONCILIADO", "Conciliado formal"),
        ("PENDIENTE_CONCILIACION", "Pendiente de conciliación manual"),
    ]

    nombre = models.CharField(max_length=200, db_index=True, verbose_name="Nombre de la Institución")
    nombre_normalizado = models.CharField(max_length=200, db_index=True, blank=True, editable=False)
    rut = models.CharField(max_length=20, blank=True, db_index=True, verbose_name="RUT Institución")
    rbd = models.CharField(max_length=20, blank=True, db_index=True, verbose_name="RBD Mineduc")
    tipo_institucion = models.CharField(max_length=60, choices=TIPOS_INSTITUCION, blank=True, verbose_name="Tipo de Institución")
    comuna = models.CharField(max_length=100, verbose_name="Comuna")
    region = models.CharField(max_length=100, db_index=True, verbose_name="Región")
    direccion = models.CharField(max_length=255, blank=True, verbose_name="Dirección")
    estado_conciliacion = models.CharField(max_length=30, choices=ESTADOS_CONCILIACION, default="CONCILIADO", db_index=True)
    activo = models.BooleanField(default=True, verbose_name="Activo")
    primera_interaccion = models.DateTimeField(null=True, blank=True, verbose_name="Primera Interacción")
    ultima_interaccion = models.DateTimeField(null=True, blank=True, verbose_name="Última Interacción")
    notas_internas = models.TextField(blank=True, verbose_name="Notas Internas Humm")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Establecimiento Educacional"
        verbose_name_plural = "Establecimientos Educacionales"
        ordering = ["nombre"]

    def __str__(self):
        return f"{self.nombre} ({self.comuna}, {self.region})"

    def save(self, *args, **kwargs):
        self.nombre_normalizado = normalizar_texto_busqueda(self.nombre)
        if self.rut:
            self.rut = normalizar_rut(self.rut)
        super().save(*args, **kwargs)


class Contacto(models.Model):
    establecimiento_principal = models.ForeignKey(
        Establecimiento,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="contactos",
        verbose_name="Establecimiento Principal"
    )
    nombre = models.CharField(max_length=150, verbose_name="Nombre Completo")
    cargo = models.CharField(max_length=100, blank=True, verbose_name="Cargo o Rol")
    email = models.EmailField(db_index=True, verbose_name="Correo Electrónico")
    telefono = models.CharField(max_length=50, blank=True, verbose_name="Teléfono / WhatsApp")
    es_encargado_compras = models.BooleanField(default=False, verbose_name="Es Encargado de Compras")
    posible_duplicado = models.BooleanField(default=False, verbose_name="Requiere Revisión de Duplicado")
    activo = models.BooleanField(default=True, verbose_name="Activo")
    primera_interaccion = models.DateTimeField(null=True, blank=True, verbose_name="Primera Interacción")
    ultima_interaccion = models.DateTimeField(null=True, blank=True, verbose_name="Última Interacción")
    observaciones_internas = models.TextField(blank=True, verbose_name="Observaciones Internas")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Contacto Docente / Institucional"
        verbose_name_plural = "Contactos Docentes / Institucionales"
        ordering = ["nombre"]

    def __str__(self):
        return f"{self.nombre} <{self.email}>"

    def save(self, *args, **kwargs):
        self.email = normalizar_email(self.email)
        super().save(*args, **kwargs)


class SolicitudCotizacion(models.Model):
    ESTADOS = [
        ("NUEVA", "Nueva solicitud recibida"),
        ("EN_REVISION", "En revisión técnica / stock"),
        ("REQUIERE_ANTECEDENTES", "Requiere contactar al docente por antecedentes"),
        ("LISTA_PARA_COTIZAR", "Lista para emitir cotización"),
        ("COTIZACION_PREPARADA", "Cotización formal preparada"),
        ("COTIZACION_ENVIADA", "Cotización enviada al colegio"),
        ("CERRADA", "Cerrada exitosamente (Venta realizada)"),
        ("PERDIDA", "Desestimada / Perdida"),
        ("CANCELADA", "Cancelada por el solicitante"),
    ]

    SUBESTADOS_CIERRE = [
        ("EN_NEGOCIACION", "En negociación final"),
        ("ADJUDICADA_MP", "Adjudicada en Mercado Público"),
        ("ORDEN_COMPRA_RECIBIDA", "Orden de Compra recibida"),
        ("FACTURADA", "Facturada"),
        ("PAGADA", "Pagada / Completada"),
    ]

    token = models.UUIDField(
        unique=True,
        null=True,
        blank=True,
        editable=False,
        db_index=True,
        verbose_name="Token de Confirmación Pública"
    )
    codigo_seguimiento = models.CharField(
        max_length=32,
        unique=True,
        db_index=True,
        verbose_name="Código de Solicitud",
        help_text="Identificador comercial amigable entregado al profesor (ej: EC-2026-A1B2C3)."
    )
    nombre_solicitante = models.CharField(max_length=150, verbose_name="Nombre del Solicitante / Profesor")
    email = models.EmailField(verbose_name="Correo Electrónico")
    telefono = models.CharField(max_length=50, verbose_name="Teléfono / WhatsApp")
    establecimiento = models.CharField(max_length=200, verbose_name="Colegio / Establecimiento Educacional")
    tipo_institucion = models.CharField(
        max_length=60,
        blank=True,
        verbose_name="Tipo de Institución",
        help_text="Dependencia institucional informada (ej: Municipal/SLEP, Particular Subvencionado, etc.)"
    )
    cargo_solicitante = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Cargo o Rol del Solicitante"
    )
    proyecto_educativo = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Nombre o Finalidad del Proyecto Educativo"
    )
    fecha_requerida_aproximada = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Fecha Aproximada Requerida"
    )
    comuna = models.CharField(max_length=100, verbose_name="Comuna")
    region = models.CharField(max_length=100, verbose_name="Región")
    institucion_responsable_compra = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Institución Responsable de Compra (si difiere, ej: DAEM, Corporación)"
    )
    rut_institucion = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="RUT Institución (Opcional)"
    )
    contacto_adquisiciones_nombre = models.CharField(
        max_length=150,
        blank=True,
        verbose_name="Nombre Encargado de Compras (Opcional)"
    )
    contacto_adquisiciones_email = models.EmailField(
        blank=True,
        verbose_name="Email Encargado de Compras (Opcional)"
    )
    observaciones = models.TextField(blank=True, verbose_name="Observaciones / Comentarios del Profesor")
    estado = models.CharField(max_length=40, choices=ESTADOS, default="NUEVA", db_index=True, verbose_name="Estado")
    total_referencial_estimado = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=Decimal("0.00"),
        verbose_name="Total Referencial Estimado (CLP)"
    )

    # Relaciones relacionales de Fase 5A (Opcionales para preservar 100% histórico)
    establecimiento_ref = models.ForeignKey(
        Establecimiento,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="solicitudes",
        verbose_name="Establecimiento Relacionado"
    )
    contacto_ref = models.ForeignKey(
        Contacto,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="solicitudes",
        verbose_name="Contacto Docente Principal"
    )

    # Responsable interno Humm (Ajuste #35)
    responsable = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="solicitudes_asignadas",
        verbose_name="Responsable Comercial Humm"
    )

    # Origen y Atribución Comercial (UTMs)
    fuente_origen = models.CharField(max_length=100, blank=True, default="Directo", verbose_name="Fuente de Tráfico")
    utm_source = models.CharField(max_length=100, blank=True, verbose_name="UTM Source")
    utm_medium = models.CharField(max_length=100, blank=True, verbose_name="UTM Medium")
    utm_campaign = models.CharField(max_length=150, blank=True, verbose_name="UTM Campaign")
    utm_content = models.CharField(max_length=150, blank=True, verbose_name="UTM Content")

    # Cierre comercial y ventas reales (Ajustes #18 y #33)
    monto_final_vendido = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Monto Final Vendido (CLP)"
    )
    subestado_cierre = models.CharField(
        max_length=50,
        blank=True,
        choices=SUBESTADOS_CIERRE,
        verbose_name="Sub-estado de Cierre Comercial"
    )
    fecha_cierre = models.DateField(null=True, blank=True, verbose_name="Fecha de Cierre Comercial")

    # Indicador de prueba interna (Ajuste Obligatorio #29)
    es_prueba = models.BooleanField(
        default=False,
        db_index=True,
        verbose_name="Es Solicitud de Prueba Interna",
        help_text="Marcar para excluir de métricas comerciales e indicadores del Dashboard."
    )

    # Campos de trazabilidad administrativa y compra pública
    id_licitacion_mp = models.CharField(max_length=50, blank=True, verbose_name="ID Licitación Mercado Público")
    id_compra_agil_mp = models.CharField(max_length=50, blank=True, verbose_name="ID Compra Ágil Mercado Público")
    id_orden_compra_mp = models.CharField(max_length=50, blank=True, verbose_name="ID Orden de Compra Mercado Público")

    notas_internas_humm = models.TextField(blank=True, verbose_name="Bitácora / Notas Internas Humm")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Última Actualización")

    class Meta:
        verbose_name = "Solicitud de Cotización"
        verbose_name_plural = "Solicitudes de Cotización"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.codigo_seguimiento} — {self.establecimiento} ({self.nombre_solicitante})"

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = uuid.uuid4()
        if not self.codigo_seguimiento:
            from django.utils import timezone
            anio = timezone.now().year
            correlativo = uuid.uuid4().hex[:6].upper()
            self.codigo_seguimiento = f"EC-{anio}-{correlativo}"
        super().save(*args, **kwargs)

    def recalcular_total_referencial(self):
        total = sum(item.subtotal_referencial_snapshot for item in self.items.all())
        self.total_referencial_estimado = total
        self.save(update_fields=["total_referencial_estimado"])

    @property
    def requiere_validacion_tecnica(self):
        """
        Retorna True si la solicitud contiene productos cuya especificación neutral
        aún no ha sido validada documentalmente (estado != VALIDADO_HUMM).
        """
        for item in self.items.all():
            if item.producto and not item.producto.puede_generar_cotizacion_formal():
                return True
        return False


class SolicitudItem(models.Model):
    solicitud = models.ForeignKey(
        SolicitudCotizacion,
        related_name="items",
        on_delete=models.CASCADE,
        verbose_name="Solicitud"
    )
    producto = models.ForeignKey(
        Producto,
        related_name="solicitudes_item",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Producto de Referencia"
    )

    # =========================================================================
    # CAMPOS DE SNAPSHOT INMUTABLE (Preservación histórica obligatoria)
    # Estos campos se congelan al registrar la solicitud y jamás se alteran,
    # aunque el producto original cambie o sea eliminado del catálogo.
    # =========================================================================
    sku_humm_snapshot = models.CharField(max_length=64, verbose_name="SKU Humm (Snapshot)")
    sku_proveedor_snapshot = models.CharField(max_length=64, blank=True, verbose_name="SKU Proveedor (Snapshot)")
    marca_snapshot = models.CharField(max_length=100, verbose_name="Marca (Snapshot)")
    modelo_snapshot = models.CharField(max_length=100, blank=True, verbose_name="Modelo (Snapshot)")
    nombre_comercial_snapshot = models.CharField(max_length=255, verbose_name="Nombre Comercial (Snapshot)")
    especificacion_neutra_snapshot = models.TextField(
        blank=True,
        verbose_name="Especificación Neutra (Snapshot)",
        help_text="Copia inmutable de la especificación técnica neutra vigente al cotizar."
    )
    unidad_comercial_snapshot = models.CharField(
        max_length=50,
        default="unidad",
        verbose_name="Unidad Comercial (Snapshot)",
        help_text="Unidad de venta comercial congelada (ej: unidad, pack (3 unidades), set (120 cables))."
    )
    cantidad = models.PositiveIntegerField(default=1, verbose_name="Cantidad")
    precio_referencial_unitario_snapshot = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00"),
        verbose_name="Precio Referencial Unitario Sugerido (Snapshot)"
    )
    subtotal_referencial_snapshot = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=Decimal("0.00"),
        verbose_name="Subtotal Referencial (Snapshot)"
    )

    class Meta:
        verbose_name = "Ítem de Solicitud"
        verbose_name_plural = "Ítems de Solicitud"

    def __str__(self):
        return f"{self.cantidad}x {self.nombre_comercial_snapshot} ({self.sku_humm_snapshot})"

    def save(self, *args, **kwargs):
        # Si hay producto vinculado y los snapshots están vacíos, congelar datos actuales
        if self.producto and not self.sku_humm_snapshot:
            self.sku_humm_snapshot = self.producto.sku_humm
            self.sku_proveedor_snapshot = self.producto.sku_proveedor
            self.marca_snapshot = self.producto.marca
            self.modelo_snapshot = self.producto.modelo
            self.nombre_comercial_snapshot = self.producto.nombre_comercial
            self.unidad_comercial_snapshot = self.producto.unidad_compra or "unidad"
            self.especificacion_neutra_snapshot = self.producto.especificacion_tecnica_neutral
            if self.precio_referencial_unitario_snapshot == 0:
                self.precio_referencial_unitario_snapshot = self.producto.precio_sugerido_total_clp

        # Calcular subtotal del snapshot
        self.subtotal_referencial_snapshot = self.cantidad * self.precio_referencial_unitario_snapshot
        super().save(*args, **kwargs)

    @property
    def desglose_unidades(self):
        from apps.cotizaciones.services import calcular_desglose_unidades
        return calcular_desglose_unidades(self.unidad_comercial_snapshot, self.cantidad)


class CotizacionFormal(models.Model):
    solicitud = models.OneToOneField(
        SolicitudCotizacion,
        related_name="cotizacion_formal",
        on_delete=models.CASCADE,
        verbose_name="Solicitud de Origen"
    )
    numero_cotizacion = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Número de Cotización Oficial (ej: COT-HUMM-2026-0001)"
    )
    fecha_emision = models.DateField(auto_now_add=True, verbose_name="Fecha de Emisión")
    validez_dias = models.PositiveIntegerField(default=30, verbose_name="Días de Validez Comercial")
    subtotal_neto = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal("0.00"))
    iva = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal("0.00"))
    costo_despacho = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    total = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal("0.00"))
    condiciones_comerciales = models.TextField(blank=True, verbose_name="Condiciones Comerciales y Despacho")
    documento_pdf = models.FileField(upload_to="cotizaciones_pdf/", blank=True, null=True, verbose_name="PDF Oficial")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Cotización Formal Humm"
        verbose_name_plural = "Cotizaciones Formales Humm"
        ordering = ["-fecha_emision", "-id"]

    def __str__(self):
        return f"{self.numero_cotizacion} (${self.total:,.0f} CLP)"


class CotizacionItem(models.Model):
    cotizacion = models.ForeignKey(
        CotizacionFormal,
        related_name="items",
        on_delete=models.CASCADE,
        verbose_name="Cotización Formal"
    )
    producto = models.ForeignKey(
        Producto,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Producto de Origen (Trazabilidad Interna)"
    )

    # REGLA OBLIGATORIA DE NEUTRALIDAD DOCUMENTAL:
    # La descripción en la cotización formal externa NUNCA expone marcas comerciales ni SKU del fabricante.
    descripcion_tecnica_neutra_utilizada = models.TextField(
        verbose_name="Descripción Técnica Neutra Utilizada",
        help_text="Texto neutro oficial incluido en el documento entregado al colegio. Sin marcas comerciales ni SKUs de fabricante."
    )
    cantidad = models.PositiveIntegerField(default=1, verbose_name="Cantidad")
    unidad_medida = models.CharField(max_length=50, default="unidad", verbose_name="Unidad")
    precio_unitario_neto_definitivo = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name="Precio Unitario Neto Definitivo (CLP)",
        help_text="Precio fijado y validado por el administrador Humm para esta cotización específica."
    )
    subtotal_neto = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=Decimal("0.00"),
        verbose_name="Subtotal Neto (CLP)"
    )

    class Meta:
        verbose_name = "Ítem de Cotización Formal"
        verbose_name_plural = "Ítems de Cotización Formal"

    def __str__(self):
        return f"{self.cantidad}x {self.descripcion_tecnica_neutra_utilizada[:40]}... (${self.subtotal_neto:,.0f} CLP)"

    def save(self, *args, **kwargs):
        self.subtotal_neto = self.cantidad * self.precio_unitario_neto_definitivo
        super().save(*args, **kwargs)
