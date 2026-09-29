from decimal import Decimal, ROUND_HALF_UP
from django.db import models
from django.utils.text import slugify
from apps.core.models import ConfiguracionPricing

class Proveedor(models.Model):
    nombre = models.CharField(max_length=150, unique=True, verbose_name="Nombre del Proveedor")
    codigo = models.CharField(max_length=50, unique=True, verbose_name="Código Interno (ej: KEY)")
    moneda_origen = models.CharField(max_length=10, default="USD", verbose_name="Moneda Origen")
    sitio_web = models.URLField(blank=True, verbose_name="Sitio Web")
    activo = models.BooleanField(default=True, verbose_name="Activo")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores"
        ordering = ["nombre"]

    def __str__(self):
        return f"{self.nombre} ({self.codigo})"


class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Nombre")
    slug = models.SlugField(max_length=120, unique=True, blank=True, verbose_name="Slug URL")
    icono_svg = models.TextField(blank=True, verbose_name="Icono SVG / Identificador")
    descripcion = models.CharField(max_length=255, blank=True, verbose_name="Descripción Corta")
    orden = models.PositiveIntegerField(default=0, verbose_name="Orden de Despliegue")
    activa = models.BooleanField(default=True, verbose_name="Activa")

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        ordering = ["orden", "nombre"]

    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)


class TecnologiaCompatible(models.Model):
    """
    Estructura de tecnologías, plataformas o microcontroladores compatibles
    con los componentes del catálogo (ej: Arduino, ESP32, micro:bit, Raspberry Pi).
    """
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Tecnología Compatible")
    slug = models.SlugField(max_length=120, unique=True, blank=True, verbose_name="Slug URL")
    descripcion = models.CharField(max_length=255, blank=True, verbose_name="Descripción")
    orden = models.PositiveIntegerField(default=0, verbose_name="Orden de Despliegue")
    activa = models.BooleanField(default=True, verbose_name="Activa")

    class Meta:
        verbose_name = "Tecnología Compatible"
        verbose_name_plural = "Tecnologías Compatibles"
        ordering = ["orden", "nombre"]

    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)


class ProductoQuerySet(models.QuerySet):
    def publicables(self, user=None):
        """
        Regla única de visibilidad centralizada para EduCompra Humm.
        - Para público general: activo=True, estado_curaduria='VALIDADO', publicado=True.
        - Para administradores staff autenticados (Modo Preview seguro de Fase 4A):
          permite previsualizar en producción los productos curados (VALIDADO) antes del lanzamiento oficial.
        """
        qs = self.filter(activo=True, estado_curaduria="VALIDADO")
        if user and user.is_authenticated and user.is_staff:
            return qs
        return qs.filter(publicado=True)


class Producto(models.Model):
    objects = ProductoQuerySet.as_manager()

    ESTADOS_STOCK = [
        ("disponible", "Disponible entrega inmediata"),
        ("importacion", "A pedido / Importación (15-20 días)"),
        ("consultar", "Consultar disponibilidad"),
    ]

    ESTADOS_CURADURIA = [
        ("SIN_REVISAR", "Sin revisar"),
        ("CANDIDATO", "Candidato a catálogo público"),
        ("DESCARTADO_CATALOGO_PUBLICO", "Descartado para catálogo público (conservar en maestro)"),
        ("EN_CURADURIA", "En proceso de curaduría pedagógica"),
        ("VALIDADO", "Curaduría pedagógica validada"),
        ("LISTO_PARA_PUBLICAR", "Listo para publicar"),
    ]

    ESTADOS_ESPECIFICACION_NEUTRAL = [
        ("NO_REVISADO", "No revisado (Borrador automático)"),
        ("BORRADOR", "En redacción técnica"),
        ("VALIDADO_HUMM", "Validado técnicamente por Humm (Apto compra pública)"),
    ]

    NIVELES_DIFICULTAD = [
        ("NO_DEFINIDO", "No definido"),
        ("INICIAL", "Inicial"),
        ("INTERMEDIO", "Intermedio"),
        ("AVANZADO", "Avanzado"),
    ]

    # Identificación Interna y Abastecimiento
    slug = models.SlugField(
        max_length=150,
        unique=True,
        null=True,
        blank=True,
        db_index=True,
        verbose_name="Slug URL",
        help_text="Identificador semántico para URL amigable del catálogo."
    )
    sku_humm = models.CharField(
        max_length=64,
        unique=True,
        verbose_name="SKU Humm",
        help_text="Identificador único interno de Humm (ej: HUMM-KEY-KS0011)."
    )
    sku_proveedor = models.CharField(
        max_length=64,
        db_index=True,
        verbose_name="SKU Proveedor",
        help_text="Código del fabricante (ej: KS0011). Utilizado para mapeo de imágenes y actualización de costos."
    )
    proveedor = models.ForeignKey(
        Proveedor,
        on_delete=models.PROTECT,
        related_name="productos",
        verbose_name="Proveedor"
    )
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="productos",
        verbose_name="Categoría"
    )

    # Curaduría Pedagógica y Calidad
    estado_curaduria = models.CharField(
        max_length=35,
        choices=ESTADOS_CURADURIA,
        default="SIN_REVISAR",
        db_index=True,
        verbose_name="Estado de Curaduría",
        help_text="Estado del proceso de evaluación pedagógica y selección para el catálogo público."
    )
    estado_especificacion_neutral = models.CharField(
        max_length=20,
        choices=ESTADOS_ESPECIFICACION_NEUTRAL,
        default="NO_REVISADO",
        db_index=True,
        verbose_name="Estado Especificación Neutra",
        help_text="Validación de neutralidad técnica para compra pública. Requiere VALIDADO_HUMM para emitir cotización formal."
    )
    nivel_dificultad = models.CharField(
        max_length=20,
        choices=NIVELES_DIFICULTAD,
        default="NO_DEFINIDO",
        verbose_name="Nivel de Dificultad / Uso",
        help_text="Complejidad técnica del uso del componente (Inicial, Intermedio, Avanzado)."
    )
    tecnologias_compatibles = models.ManyToManyField(
        TecnologiaCompatible,
        blank=True,
        related_name="productos",
        verbose_name="Tecnologías Compatibles Propuestas",
        help_text="Plataformas compatibles propuestas pedagógicamente para proyectos de aula."
    )
    tecnologias_verificadas = models.ManyToManyField(
        TecnologiaCompatible,
        blank=True,
        related_name="productos_verificados",
        verbose_name="Tecnologías Compatibles Verificadas",
        help_text="Compatibilidad técnica respaldada explícitamente por el fabricante o evidencia registrada."
    )
    uso_educativo = models.TextField(
        blank=True,
        verbose_name="Uso Educativo y Proyectos de Aula",
        help_text="¿Qué podrían hacer o aprender los estudiantes con este producto?"
    )
    apto_para_kit = models.BooleanField(
        default=False,
        db_index=True,
        verbose_name="Apto para Kits Educativos",
        help_text="Indica si este producto es un componente potencial para kits temáticos de Humm."
    )

    # Información Comercial (Visible para el Profesor)
    marca = models.CharField(max_length=100, default="Keyestudio", verbose_name="Marca")
    modelo = models.CharField(max_length=100, blank=True, verbose_name="Modelo")
    nombre_comercial = models.CharField(
        max_length=255,
        verbose_name="Nombre Comercial",
        help_text="Nombre amigable presentado al docente (ej: Sensor de Humedad de Suelo Keyestudio para Arduino)."
    )
    nombre_original_proveedor = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Nombre Original en Catálogo Fabricante"
    )
    descripcion_corta = models.CharField(max_length=300, blank=True, verbose_name="Descripción Corta")
    descripcion_educativa = models.TextField(
        blank=True,
        verbose_name="Descripción Pedagógica / Educativa",
        help_text="Texto explicativo para el profesor: qué es, para qué sirve y contexto de aplicación."
    )
    advertencia_uso = models.TextField(
        blank=True,
        verbose_name="Advertencia de Uso Educativo / Seguridad",
        help_text="Advertencia de seguridad o condiciones pedagógicas de uso (voltaje, gases, fuego, uso médico, supervisión)."
    )
    unidad_compra = models.CharField(max_length=50, default="unidad", verbose_name="Unidad de Medida")

    # Información para Compra Pública / Mercado Público (Especificación Neutra)
    titulo_especificacion_neutral = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Título Neutro para Compra Pública",
        help_text="Denominación genérica sin marca ni modelo (ej: Módulo Sensor de Humedad para Suelo)."
    )
    especificacion_tecnica_neutral = models.TextField(
        blank=True,
        verbose_name="Especificación Técnica Neutra",
        help_text="Descripción funcional y eléctrica sin marcas ni SKUs que permite equivalencias técnicas según Ley 19.886."
    )
    criterios_equivalencia = models.TextField(
        blank=True,
        default="O producto técnicamente equivalente compatible.",
        verbose_name="Criterios y Cláusula de Equivalencia Técnica"
    )

    # Trazabilidad y Evidencia Técnica (Punto de Control Fase 3)
    fuente_tecnica = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Fuente Técnica / Fabricante",
        help_text="Hoja de datos, wiki oficial o manual del fabricante."
    )
    referencia_tecnica_url = models.URLField(
        blank=True,
        verbose_name="URL de Referencia Técnica",
        help_text="Enlace a documentación técnica verificable."
    )
    fecha_revision_tecnica = models.DateField(
        null=True,
        blank=True,
        verbose_name="Fecha de Revisión Técnica"
    )
    responsable_revision_tecnica = models.CharField(
        max_length=150,
        blank=True,
        verbose_name="Responsable de Validación Técnica"
    )
    observaciones_tecnicas = models.TextField(
        blank=True,
        verbose_name="Observaciones de Validación Técnica",
        help_text="Evidencias, notas de laboratorio o pruebas físicas."
    )

    # Costos y Precios Sugeridos
    costo_proveedor_usd = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00"),
        verbose_name="Costo Proveedor (USD)"
    )
    costo_puesto_chile_clp = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00"),
        verbose_name="Costo Estimado Puesto en Chile (CLP)"
    )
    porcentaje_recargo = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Recargo Específico (%)",
        help_text="Si se deja vacío, se aplicará el Recargo General configurado en los parámetros de pricing."
    )
    precio_sugerido_neto_clp = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00"),
        verbose_name="Precio Sugerido Neto (CLP)"
    )
    precio_sugerido_total_clp = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00"),
        verbose_name="Precio Referencial Sugerido con IVA (CLP)",
        help_text="Precio referencial que visualiza el profesor en el catálogo."
    )

    # Gestión y Publicación
    publicado = models.BooleanField(
        default=False,
        db_index=True,
        verbose_name="Publicado en EduCompra",
        help_text="Indica si este producto forma parte del catálogo activo curado para colegios."
    )
    activo = models.BooleanField(default=True, verbose_name="Activo en Sistema")
    destacado = models.BooleanField(default=False, verbose_name="Destacado en Portada")
    estado_stock = models.CharField(
        max_length=50,
        choices=ESTADOS_STOCK,
        default="disponible",
        verbose_name="Disponibilidad"
    )
    dias_entrega_estimados = models.PositiveIntegerField(default=5, verbose_name="Días de Entrega Estimados")
    observaciones_internas = models.TextField(blank=True, verbose_name="Observaciones Internas Humm")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ["-destacado", "nombre_comercial"]

    def __str__(self):
        return f"{self.nombre_comercial} [{self.sku_humm}]"

    @property
    def imagen_principal_url(self):
        """Retorna la URL de la imagen principal o el placeholder institucional si no tiene imagen."""
        img = self.imagenes.filter(es_principal=True).first() or self.imagenes.first()
        if img and img.archivo:
            return img.archivo.url
        return "/static/img/placeholder_producto.svg"

    def puede_generar_cotizacion_formal(self):
        """
        Regla obligatoria de Humm: Un producto solo puede emitir cotización formal
        institucional y documentos de compra pública si su especificación técnica neutra
        ha sido expresamente validada por Humm (estado == VALIDADO_HUMM).
        """
        return self.estado_especificacion_neutral == "VALIDADO_HUMM"

    def calcular_precios_sugeridos(self, config=None):
        """
        Calcula el costo internado y el precio referencial sugerido utilizando los parámetros
        configurables de ConfiguracionPricing.
        No sobrescribe precios definitivos emitidos en cotizaciones formales.
        """
        if config is None:
            config = ConfiguracionPricing.get_solo()

        tc = config.tipo_cambio_usd_clp
        factor_internacion = Decimal("1.00") + (config.factor_internacion_flete_porcentaje / Decimal("100.00"))
        recargo_pct = self.porcentaje_recargo if self.porcentaje_recargo is not None else config.recargo_general_porcentaje
        factor_recargo = Decimal("1.00") + (recargo_pct / Decimal("100.00"))
        factor_iva = Decimal("1.00") + (config.iva_porcentaje / Decimal("100.00"))

        # 1. Costo puesto en Chile (USD * TC * factor internación)
        costo_chile = self.costo_proveedor_usd * tc * factor_internacion
        self.costo_puesto_chile_clp = costo_chile.quantize(Decimal("1"), rounding=ROUND_HALF_UP).quantize(Decimal("1.00"))

        # 2. Precio sugerido neto
        precio_neto = self.costo_puesto_chile_clp * factor_recargo
        self.precio_sugerido_neto_clp = precio_neto.quantize(Decimal("1"), rounding=ROUND_HALF_UP).quantize(Decimal("1.00"))

        # 3. Precio sugerido total con IVA (redondeado a pesos enteros)
        precio_total = self.precio_sugerido_neto_clp * factor_iva
        self.precio_sugerido_total_clp = precio_total.quantize(Decimal("1"), rounding=ROUND_HALF_UP).quantize(Decimal("1.00"))

    def save(self, *args, **kwargs):
        # Asegurar slug semántico único si no existe
        if not self.slug:
            base = slugify(f"{self.sku_proveedor}-{self.nombre_comercial}")[:145]
            if not base:
                base = slugify(self.sku_humm)[:145]
            self.slug = base

        # Asegurar cálculo de precios sugeridos al guardar si hay costo
        if self.costo_proveedor_usd > 0:
            self.calcular_precios_sugeridos()
        super().save(*args, **kwargs)


class ProductoImagen(models.Model):
    producto = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE,
        related_name="imagenes",
        verbose_name="Producto"
    )
    archivo = models.ImageField(
        upload_to="catalogo/originales/",
        blank=True,
        null=True,
        verbose_name="Archivo de Imagen"
    )
    nombre_archivo_original = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Nombre Original del Archivo (ej: KS0011.jpg)"
    )
    es_principal = models.BooleanField(default=False, verbose_name="Imagen Principal")
    orden = models.PositiveIntegerField(default=0, verbose_name="Orden")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Imagen de Producto"
        verbose_name_plural = "Imágenes de Productos"
        ordering = ["-es_principal", "orden", "id"]

    def __str__(self):
        return f"Imagen para {self.producto.sku_humm} ({'Principal' if self.es_principal else 'Secundaria'})"
