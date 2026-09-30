# PLAN DE IMPLEMENTACIÓN — FASE 5
## Plataforma de Administración, Gestión Comercial y Analítica
### Plataforma EduCompra Humm (`https://educompra.humm.cl/gestion/`)

**Documento:** `implementation_plan_fase_5_administracion.md`  
**Fecha de Elaboración:** 30 de Septiembre de 2026  
**Responsable Técnico:** Antigravity (Google DeepMind Pair Programmer)  
**Destinatario:** Equipo Directivo, Comercial, Operativo y Pedagógico de Humm  
**Estado:** **APROBADO CON AJUSTES OBLIGATORIOS POR HUMM — AUTORIZADA IMPLEMENTACIÓN DE FASE 5A**

---

> [!NOTE]
> ### RESOLUCIÓN DE APROBACIÓN DE HUMM
> El plan ha sido formalmente **Aprobado con Ajustes Obligatorios**. Se autoriza el inicio inmediato de la construcción de la **Fase 5A** con la instrumentación mínima de telemetría de Fase 5B incorporada desde el inicio. Todos los 30 ajustes obligatorios instruidos por Humm quedan reflejados en este documento y guían rigurosamente la implementación.

## 1. Contexto, Principio Rector y Objetivos

### 1.1 Estado Actual al Cierre de Fase 4
La Fase 4 puso en marcha con pleno éxito la experiencia pública de EduCompra Humm:
* **Catálogo Público en Producción:** 72 productos curados y activos, estructurados en 11 categorías formativas, accesibles en `https://educompra.humm.cl/catalogo/`.
* **Catálogo Maestro Protegido:** 857 productos permanecen resguardados (`publicado = False` y `SIN_REVISAR`) sin exposición pública.
* **Flujo Comercial Docente:** Canasta temporal en sesión (`/mi-cotizacion/`), formulario institucional con prevención de bots/idempotencia (`/solicitar-cotizacion/`) y comprobante seguro (`/solicitud-recibida/<token>/`).
* **Snapshots Inmutables:** Precios, nombres, unidades comerciales y descripciones congeladas al momento exacto de la solicitud en `SolicitudItem`.
* **Consola Técnica de Respaldo:** Django Admin operativo en `/admin/` con personalización visual institucional Humm.
* **Test Suite:** 46 pruebas automatizadas pasando al 100%.

### 1.2 Principio Rector de la Fase 5
A partir de este hito, EduCompra debe evolucionar de **“un catálogo que recibe solicitudes”** a **“una plataforma comercial educativa administrable, medible y orientada a decisiones”**.

La administración cotidiana de Humm **NO debe depender exclusivamente de Django Admin**. Django Admin se conservará de forma permanente como **HERRAMIENTA TÉCNICA Y DE RESPALDO OPERATIVO**, mientras que la operación comercial, la curaduría editorial, el análisis de demanda y el seguimiento de solicitudes migrarán a una plataforma propia:

```
┌────────────────────────────────────────────────────────────────────────┐
│               PLATAFORMA ADMINISTRATIVA EDUCOMPRA HUMM                 │
│               Ruta canónica: https://educompra.humm.cl/gestion/        │
│               Nombre visible: Administración EduCompra                 │
└────────────────────────────────────────────────────────────────────────┘
```

### 1.3 Preguntas Comerciales y Pedagógicas que Resolverá la Plataforma
La plataforma está diseñada específicamente para responder con inmediatez:
1. ¿Cuántos profesores están utilizando activamente EduCompra?
2. ¿Cuántos colegios y liceos están solicitando productos?
3. ¿Qué productos generan mayor interés y cuáles se solicitan efectivamente?
4. ¿Qué categorías temáticas concentran la demanda escolar?
5. **¿Qué buscan los docentes y no encuentran en nuestro catálogo? (Demanda No Cubierta)**
6. ¿Cuánto dinero se está solicitando en total? ¿Cuánto hemos cotizado formalmente? ¿Cuánto se ha cerrado como venta?
7. ¿Qué regiones y comunas de Chile presentan mayor dinamismo?
8. ¿Dónde abandonan los usuarios el flujo de solicitud (embudo de conversión)?
9. ¿Qué productos deberíamos incorporar, descatalogar o destacar en portada?
10. ¿Qué solicitudes requieren atención inmediata y cuáles exigen validación técnica de compra pública?
11. ¿Qué establecimientos son recurrentes y vuelven a cotizar con nosotros?

> [!IMPORTANT]
> ### EduCompra NO es un ERP ni un sistema contable
> La plataforma administrativa se mantendrá:
> * **Simple, rápida, visual y enfocada en gestión cotidiana.**
> * **Orientada a la toma de decisiones comerciales y educativas.**
> * **Desktop-first pero 100% responsiva** para revisión ejecutiva desde tablets y smartphones.
> * **Sin complejidades innecesarias:** sin facturación electrónica directa, sin contabilidad tributaria, sin inventario multi-bodega complejo, sin esquemas rígidos de permisos corporativos o SSO en esta etapa.

---

## 2. Delimitación de Fases: 5A, 5B y 5C

Para asegurar un desarrollo ordenado, robusto y sin regresiones, la Fase 5 se estructura en tres etapas claramente acotadas:

```mermaid
graph LR
    subgraph Fase 5A [FASE 5A — Administración Operacional]
        A1[Estructura /gestion/] --> A2[Dashboard Operativo]
        A2 --> A3[Catálogo & Productos]
        A3 --> A4[Importaciones Web DRY-RUN]
        A4 --> A5[Solicitudes & Kanban]
        A5 --> A6[Establecimientos & Contactos]
        A6 --> A7[Configuración Segura]
    end

    subgraph Fase 5B [FASE 5B — Instrumentación & Analítica]
        B1[Captura Pasiva EventoUso] --> B2[Deduplicación & Privacidad]
        B2 --> B3[Embudo de Conversión]
        B3 --> B4[Analítica de Búsquedas]
        B4 --> B5[Demanda No Cubierta]
        B5 --> B6[Matriz Alta Vista / Baja Solicitud]
    end

    subgraph Fase 5C [FASE 5C — Inteligencia Comercial Futura]
        C1[Sub-estados Cierre Venta] --> C2[Adjudicaciones MP]
        C2 --> C3[Rentabilidad & Márgenes]
        C3 --> C4[Conector Humm Control Center HCC]
    end

    Fase 5A --> Fase 5B
    Fase 5B -.-> Fase 5C
```

### FASE 5A — Administración Operacional (Alcance Inmediato)
* Estructura base en `/gestion/` con autenticación institucional y control de acceso.
* Dashboard operacional con tarjetas KPI del período seleccionado.
* Administración integral de catálogo (listado, filtros rápidos, switch de publicación, creación manual protegida, ficha administrativa modular por bloques).
* Módulo de Importaciones Web: ejecución de la lógica existente de `importar_catalogo_keyestudio` en un flujo asistido de 6 pasos con DRY-RUN obligatorio, visualización de estadísticas y preservación absoluta de curaduría.
* Gestión comercial de solicitudes: vista dual (Tabla y Kanban de estados comerciales), asignación de responsable Humm, bitácora interna y ficha técnica de solicitud.
* Entidades relacionales `Establecimiento` y `Contacto`, con migración no destructiva desde los snapshots de texto histórico.
* Administración segura de parámetros globales de pricing (`ConfiguracionPricing`).
* Auditoría básica de acciones relevantes (`RegistroActividad`).
* Exportación de datos a formato CSV.

### FASE 5B — Instrumentación y Analítica (Integrada desde 5A)
* Creación del modelo soberano de telemetría de primera parte `EventoUso`.
* Instrumentación pasiva y de mínimo impacto en vistas públicas (visitas, búsquedas, detalle de producto, canasta y solicitudes).
* Política de deduplicación ligera y estricta privacidad (cero datos personales en telemetría previa a la solicitud).
* Visualización de embudo comercial en 7 pasos (Visita → Producto visto → Agregado → Formulario iniciado → Solicitud enviada → Cotización enviada → Cierre).
* Módulo de Analítica de Búsquedas y bloque destacado de **Demanda No Cubierta** (términos con 0 resultados).
* Analítica de rendimiento de productos: rankings y alerta de productos con alta exposición pero baja conversión.

### FASE 5C — Inteligencia Comercial (Preparada conceptualmente, NO implementada en 5A)
* Modelos preparados con campos de enlace para: adjudicaciones de compra pública, registro formal de órdenes de compra recibidas, facturación y pagos.
* Estructura de identificadores lista para sincronización futura con **Humm Control Center (HCC)** sin generar acoplamiento prematuro.
* Informes históricos plurianuales y cálculos de margen comercial por línea de importación.

---

## 3. Matriz de Componentes del Sistema

A fin de cumplir rigurosamente el principio de **NO DUPLICAR LÓGICA EXISTENTE**, se define con exactitud qué se reutiliza, qué se modifica y qué se crea nuevo:

| Componente | Estado | Acción en Fase 5 | Justificación Técnica |
| :--- | :---: | :---: | :--- |
| `Producto` | Existe | **Reutilizar intacto** | Modelo maestro unificado. No se creará `ProductoGestion`. Se le consultará mediante select_related y anotaciones de métricas. |
| `Categoria`, `TecnologiaCompatible`, `Proveedor` | Existe | **Reutilizar intacto** | Entidades curriculares y de abastecimiento existentes. |
| `SolicitudCotizacion` | Existe | **Modificar (Extender)** | Se incorporan relaciones opcionales `establecimiento_ref`, `contacto_ref`, `responsable_humm`, campos UTM y sub-estados de cierre. Snapshots históricos permanecen inmutables. |
| `SolicitudItem` | Existe | **Reutilizar intacto** | Snapshots inmutables de precios y especificaciones. Se mantienen 100% compatibles. |
| `CotizacionFormal`, `CotizacionItem` | Existe | **Reutilizar intacto** | Base para `/gestion/cotizaciones/` respetando el candado de neutralidad documental (`VALIDADO_HUMM`). |
| `ConfiguracionPricing` | Existe | **Reutilizar intacto** | Se crea formulario web en `/gestion/configuracion/` para modificar sus valores de forma segura sin tocar `.env`. |
| Motor de Importación Keyestudio | Existe | **Reutilizar (Refactorizar)** | El núcleo analítico y transaccional de `importar_catalogo_keyestudio.py` se encapsula en `ImportacionCatalogoService` para ser invocado idénticamente por la web y la CLI. |
| CartService & SubmissionService | Existe | **Reutilizar + Instrumentar** | Se integran ganchos para disparo de eventos de telemetría (`AGREGAR_COTIZACION`, `ENVIAR_SOLICITUD`, UTMs). |
| Django Admin (`/admin/`) | Existe | **Mantener intacto** | Consola técnica de respaldo y emergencia para desarrolladores y superusuarios. |
| `Establecimiento` | Nuevo | **Crear modelo** | Entidad relacional para centralizar perfil institucional, comuna, región, RUT y estadísticas consolidadas. |
| `Contacto` | Nuevo | **Crear modelo** | Entidad relacional para docentes y encargados de compras, deduplicados por email. |
| `EventoUso` | Nuevo | **Crear modelo** | Telemetría soberana de primera parte (sin Google Analytics u otros terceros). |
| `RegistroActividad` | Nuevo | **Crear modelo** | Log simple de auditoría operativa para cambios de precio, publicación, estado y lotes de importación. |
| `LoteImportacion` | Nuevo | **Crear modelo** | Registro histórico de cargas masivas, simulaciones DRY-RUN, archivos asociados y estadísticas. |
| Módulo Django `apps.gestion` | Nuevo | **Crear app** | Contendrá todas las vistas, enrutamiento, formularios, decoradores y templates del nuevo backoffice `/gestion/`. |

---

## 4. Arquitectura de Datos: Modelos Nuevos y Modificaciones

### 4.1 Nuevos Modelos en `apps/cotizaciones/models.py`

#### A. Entidad `Establecimiento`
```python
class Establecimiento(models.Model):
    TIPOS_INSTITUCION = [
        ("MUNICIPAL_SLEP", "Municipal / Servicio Local de Educación (SLEP)"),
        ("PARTICULAR_SUBVENCIONADO", "Particular Subvencionado"),
        ("PARTICULAR_PAGADO", "Particular Pagado"),
        ("CORPORACION_FUNDACION", "Corporación / Fundación Educativa"),
        ("EDUCACION_SUPERIOR", "CFT / IP / Universidad"),
        ("OTRO", "Otro tipo de institución"),
    ]

    nombre = models.CharField(max_length=200, db_index=True, verbose_name="Nombre de la Institución")
    nombre_normalizado = models.CharField(max_length=200, db_index=True, editable=False)
    rut = models.CharField(max_length=20, blank=True, db_index=True, verbose_name="RUT Institución")
    tipo_institucion = models.CharField(max_length=60, choices=TIPOS_INSTITUCION, blank=True, verbose_name="Tipo de Institución")
    comuna = models.CharField(max_length=100, verbose_name="Comuna")
    region = models.CharField(max_length=100, db_index=True, verbose_name="Región")
    direccion = models.CharField(max_length=255, blank=True, verbose_name="Dirección")
    rbd = models.CharField(max_length=20, blank=True, verbose_name="RBD (Rol Base de Datos Mineduc)")
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
        from apps.core.normalizacion import normalizar_texto_busqueda
        self.nombre_normalizado = normalizar_texto_busqueda(self.nombre)
        super().save(*args, **kwargs)
```

#### B. Entidad `Contacto`
```python
class Contacto(models.Model):
    establecimiento = models.ForeignKey(
        Establecimiento,
        on_delete=models.CASCADE,
        related_name="contactos",
        null=True,
        blank=True,
        verbose_name="Establecimiento Principal"
    )
    nombre = models.CharField(max_length=150, verbose_name="Nombre Completo")
    cargo = models.CharField(max_length=100, blank=True, verbose_name="Cargo o Rol")
    email = models.EmailField(db_index=True, verbose_name="Correo Electrónico")
    telefono = models.CharField(max_length=50, blank=True, verbose_name="Teléfono / WhatsApp")
    es_encargado_compras = models.BooleanField(default=False, verbose_name="Es Encargado de Adquisiciones")
    activo = models.BooleanField(default=True, verbose_name="Activo")
    primera_interaccion = models.DateTimeField(auto_now_add=True, verbose_name="Primera Interacción")
    ultima_interaccion = models.DateTimeField(auto_now=True, verbose_name="Última Interacción")
    observaciones_internas = models.TextField(blank=True, verbose_name="Observaciones Internas")

    class Meta:
        verbose_name = "Contacto Docente / Institucional"
        verbose_name_plural = "Contactos Docentes / Institucionales"
        ordering = ["nombre"]

    def __str__(self):
        return f"{self.nombre} <{self.email}>"
```

### 4.2 Extensiones en `SolicitudCotizacion` (`apps/cotizaciones/models.py`)
Sin alterar ninguno de los campos existentes, se añaden las siguientes relaciones y campos de gestión:

```python
# --- Nuevos campos a añadir en SolicitudCotizacion ---

# Relaciones institucionales de Fase 5A (Opcionales para preservar histórico)
establecimiento_ref = models.ForeignKey(
    "Establecimiento",
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    related_name="solicitudes",
    verbose_name="Establecimiento Relacionado"
)
contacto_ref = models.ForeignKey(
    "Contacto",
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    related_name="solicitudes",
    verbose_name="Contacto Principal"
)

# Gestión interna Humm
responsable = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    related_name="solicitudes_asignadas",
    verbose_name="Responsable Comercial Humm"
)

# Trazabilidad de origen y campañas de marketing
fuente_origen = models.CharField(max_length=100, blank=True, default="Directo", verbose_name="Fuente de Tráfico")
utm_source = models.CharField(max_length=100, blank=True, verbose_name="UTM Source")
utm_medium = models.CharField(max_length=100, blank=True, verbose_name="UTM Medium")
utm_campaign = models.CharField(max_length=150, blank=True, verbose_name="UTM Campaign")
utm_content = models.CharField(max_length=150, blank=True, verbose_name="UTM Content")

# Cierre comercial e indicadores de venta (Fase 5A + base para 5C)
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
    choices=[
        ("EN_NEGOCIACION", "En negociación final"),
        ("ADJUDICADA_MP", "Adjudicada en Mercado Público"),
        ("ORDEN_COMPRA_RECIBIDA", "Orden de Compra recibida"),
        ("FACTURADA", "Facturada"),
        ("PAGADA", "Pagada / Completada"),
    ],
    verbose_name="Sub-estado de Cierre Comercial"
)
fecha_cierre = models.DateField(null=True, blank=True, verbose_name="Fecha de Cierre")
```

### 4.3 Nuevos Modelos en `apps/gestion/models.py`

#### A. Telemetría de Primera Parte (`EventoUso`)
```python
class EventoUso(models.Model):
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

    tipo_evento = models.CharField(max_length=30, choices=TIPOS_EVENTO, db_index=True)
    session_key = models.CharField(max_length=40, db_index=True, verbose_name="Clave de Sesión Anónima")
    producto = models.ForeignKey(
        "catalogo.Producto",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="eventos_uso"
    )
    categoria = models.ForeignKey(
        "catalogo.Categoria",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="eventos_uso"
    )
    termino_busqueda = models.CharField(max_length=255, blank=True, db_index=True)
    termino_busqueda_normalizado = models.CharField(max_length=255, blank=True, db_index=True)
    resultados_busqueda = models.PositiveIntegerField(null=True, blank=True)
    solicitud = models.ForeignKey(
        "cotizaciones.SolicitudCotizacion",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="eventos_asociados"
    )
    establecimiento = models.ForeignKey(
        "cotizaciones.Establecimiento",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="eventos_asociados"
    )
    fuente = models.CharField(max_length=100, blank=True)
    utm_source = models.CharField(max_length=100, blank=True)
    utm_medium = models.CharField(max_length=100, blank=True)
    utm_campaign = models.CharField(max_length=150, blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        verbose_name = "Evento de Uso"
        verbose_name_plural = "Eventos de Uso"
        indexes = [
            models.Index(fields=["tipo_evento", "created_at"]),
            models.Index(fields=["session_key", "created_at"]),
            models.Index(fields=["producto", "tipo_evento"]),
            models.Index(fields=["termino_busqueda_normalizado", "resultados_busqueda"]),
        ]
```

#### B. Registro de Auditoría Operativa (`RegistroActividad`)
```python
class RegistroActividad(models.Model):
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Usuario"
    )
    accion = models.CharField(
        max_length=50,
        choices=[
            ("PUBLICAR_PRODUCTO", "Publicar Producto"),
            ("DESPUBLICAR_PRODUCTO", "Despublicar Producto"),
            ("EDITAR_PRECIO", "Cambio de Precio/Costo"),
            ("CAMBIO_ESTADO_SOLICITUD", "Cambio de Estado de Solicitud"),
            ("ASIGNAR_RESPONSABLE", "Asignación de Responsable"),
            ("VALIDAR_TECNICA", "Validación Técnica Neutra"),
            ("IMPORTACION_EJECUTADA", "Importación Masiva de Catálogo"),
            ("MODIFICAR_PRICING", "Modificación de Parámetros Globales"),
        ],
        db_index=True
    )
    modelo_afectado = models.CharField(max_length=50)
    objeto_id = models.CharField(max_length=50, blank=True)
    descripcion = models.CharField(max_length=255)
    detalles = models.JSONField(default=dict, blank=True)
    ip_origen = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        verbose_name = "Registro de Actividad"
        verbose_name_plural = "Registros de Actividad"
        ordering = ["-created_at"]
```

#### C. Control de Importaciones Masivas (`LoteImportacion`)
```python
class LoteImportacion(models.Model):
    ESTADOS = [
        ("SUBIDO", "Archivo subido — Pendiente DRY-RUN"),
        ("SIMULADO", "DRY-RUN completado con éxito"),
        ("CON_CONFLICTOS", "DRY-RUN completado con advertencias/conflictos"),
        ("APROBADO", "Aprobado para importación"),
        ("APLICADO", "Importación productiva ejecutada"),
        ("FALLIDO", "Error en ejecución"),
    ]

    archivo_excel = models.FileField(upload_to="importaciones_gestion/excel/")
    archivo_imagenes_zip = models.FileField(upload_to="importaciones_gestion/zip/", blank=True, null=True)
    estado = models.CharField(max_length=30, choices=ESTADOS, default="SUBIDO", db_index=True)
    es_dry_run = models.BooleanField(default=True)
    usuario_creador = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    
    # Métricas consolidadas del procesamiento
    filas_leidas = models.PositiveIntegerField(default=0)
    skus_detectados = models.PositiveIntegerField(default=0)
    productos_nuevos = models.PositiveIntegerField(default=0)
    productos_actualizados = models.PositiveIntegerField(default=0)
    productos_sin_cambios = models.PositiveIntegerField(default=0)
    conflictos_detectados = models.PositiveIntegerField(default=0)
    productos_sin_imagen = models.PositiveIntegerField(default=0)
    imagenes_sin_producto = models.PositiveIntegerField(default=0)
    
    resumen_json = models.JSONField(default=dict, blank=True)
    registro_conflictos_md = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Lote de Importación"
        verbose_name_plural = "Lotes de Importación"
        ordering = ["-created_at"]
```

---

## 5. Estrategia de Migración Segura de Datos Históricos

El sistema cuenta con solicitudes reales y de prueba en `SolicitudCotizacion` generadas en fases anteriores. Dichas solicitudes tienen datos valiosos en los campos de texto `establecimiento`, `comuna`, `region`, `nombre_solicitante`, `email` y `telefono`.

### 5.1 Reglas de Inviolabilidad Histórica
1. **Los campos existentes de `SolicitudCotizacion` y `SolicitudItem` jamás se alteran ni eliminan.**
2. La relación `solicitud.establecimiento_ref` es **estrictamente opcional (`null=True, blank=True`)**.
3. Las vistas administrativas desplegarán con prioridad el nombre de `establecimiento_ref.nombre`, pero si el campo es nulo, desplegarán de forma transparente y sin error el texto congelado original `solicitud.establecimiento`.
4. El precio, nombre comercial y especificación neutra en `SolicitudItem` se mantienen blindados en sus snapshots.

### 5.2 Algoritmo de Conciliación y Migración Automática
Se creará una migración de datos o comando de gestión:
`python manage.py conciliar_establecimientos_historicos`

El script ejecuta los siguientes pasos bajo transacción segura:
```
1. Lee cada SolicitudCotizacion en orden cronológico ascendente (-created_at).
2. Normaliza el nombre del establecimiento (trim, mayúsculas, eliminación de sufijos redundantes como 'colegio', 'liceo', 'escuela' para efectos de match).
3. Busca si ya existe un Establecimiento con mismo nombre_normalizado y misma comuna.
   - Si existe: vincula la solicitud -> solicitud.establecimiento_ref = est_existente.
   - Si no existe: crea el nuevo registro Establecimiento con nombre, región, comuna, tipo_institucion y primera_interaccion = solicitud.created_at.
4. Busca si existe un Contacto con el email del solicitante:
   - Si no existe: crea Contacto asociado al establecimiento, nombre, cargo, teléfono y email.
   - Si existe: actualiza su ultima_interaccion.
   - Vincula la solicitud -> solicitud.contacto_ref = contacto.
5. Actualiza las fechas de primera_interaccion y ultima_interaccion del Establecimiento.
```

---

## 6. Arquitectura de Telemetría Soberana y Control de Privacidad

### 6.1 Principio de Privacidad Estricta
* **Sin trackers externos:** Cero Google Analytics, Meta Pixel ni scripts invasivos que ralenticen la carga escolar o recopilen datos de menores de edad.
* **Anonimato inicial garantizado:** Mientras el visitante navega por el catálogo, solo se registra el identificador técnico de sesión (`request.session.session_key`).
* **Prohibición de datos sensibles:** El modelo `EventoUso` jamás registrará RUT, números de teléfono, correos electrónicos ni contenidos de formularios previos a la confirmación de la solicitud.
* **Asociación consentida:** Únicamente al enviarse una solicitud de cotización formal, el sistema relaciona internamente el `solicitud_id` con el `session_key` de navegación.

### 6.2 Política de Deduplicación de Eventos
Para evitar datos basura provocados por recargas accidentales (F5) o doble clics:

| Tipo Evento | Disparador en Frontend / Backend | Regla de Deduplicación (Throttling) |
| :--- | :--- | :--- |
| `VISITA` | Carga de portada (`/`) o catálogo (`/catalogo/`) | Máximo **1 evento por sesión cada 30 minutos**. Almacenado en `request.session['_last_visit_event']`. |
| `VER_PRODUCTO` | Carga de ficha `/catalogo/<slug>/` | Máximo **1 evento por producto por sesión cada 10 minutos**. Almacenado en diccionario en sesión `request.session['_viewed_prods']`. |
| `BUSQUEDA` | Búsqueda con parámetro `?q=` | Registra el término normalizado solo al cambiar el texto de búsqueda. Omitido en cambios de página de paginación (`?page=2`). |
| `AGREGAR_COTIZACION` | POST exitoso a `/mi-cotizacion/agregar/` | 1 evento por cada adición confirmada en base de datos. |
| `QUITAR_COTIZACION` | POST a `/mi-cotizacion/eliminar/` o vaciar | 1 evento por cada eliminación. |
| `VER_MI_COTIZACION` | Carga de `/mi-cotizacion/` | 1 evento por visita a la canasta (máximo 1 cada 5 minutos). |
| `INICIAR_SOLICITUD` | Carga de `/solicitar-cotizacion/` | 1 evento al desplegar el formulario. |
| `ENVIAR_SOLICITUD` | Creación exitosa en `SubmissionService` | 1 evento único, vinculado directamente a la `SolicitudCotizacion` creada. |

### 6.3 Desempeño y Retención
* **Escritura eficiente:** Inserciones directas en base de datos mediante método optimizado `TelemetriaService.registrar_evento(...)` con captura de excepciones para asegurar que ningún error de telemetría afecte la navegación del docente.
* **Comando de Depuración:** Comando `python manage.py depurar_telemetria --dias=180` para purgar eventos antiguos conservando las solicitudes y métricas consolidadas.

---

## 7. Mapa de Rutas de la Administración (`/gestion/`)

Toda la plataforma administrativa estará agrupada bajo el prefijo canónico `/gestion/` y enrutada mediante la aplicación `apps.gestion`:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        MAPA DE RUTAS ADMINISTRATIVAS (/gestion/)                       │
├───────────────────────────────┬──────────────────────────┬─────────────────────────────┤
│ RUTA                          │ NOMBRE DE URL            │ PROPÓSITO / DESCRIPCIÓN     │
├───────────────────────────────┼──────────────────────────┼─────────────────────────────┤
│ /gestion/login/               │ gestion:login            │ Inicio de sesión admin      │
│ /gestion/logout/              │ gestion:logout           │ Cierre de sesión seguro     │
│ /gestion/                     │ gestion:dashboard        │ Dashboard principal KPIs    │
│                               │                          │                             │
│ --- CATÁLOGO ---              │                          │                             │
│ /gestion/productos/           │ gestion:productos_lista  │ Tabla general con filtros   │
│ /gestion/productos/nuevo/     │ gestion:producto_crear   │ Alta manual (publicado=0)   │
│ /gestion/productos/<id>/      │ gestion:producto_detalle │ Ficha modular del producto  │
│ /gestion/productos/<id>/edit/ │ gestion:producto_editar  │ Edición comercial/técnica   │
│ /gestion/productos/<id>/toggle│ gestion:producto_toggle  │ Switch publicar/despublicar │
│ /gestion/categorias/          │ gestion:categorias_lista │ Gestión de categorías       │
│ /gestion/tecnologias/         │ gestion:tecnologias_lista│ Gestión de tecnologías      │
│ /gestion/importaciones/       │ gestion:importaciones    │ Asistente DRY-RUN 6 pasos   │
│ /gestion/importaciones/<id>/  │ gestion:importacion_ver  │ Reporte y aprobación lote   │
│                               │                          │                             │
│ --- COMERCIAL ---             │                          │                             │
│ /gestion/solicitudes/         │ gestion:solicitudes_lista│ Tabla de solicitudes        │
│ /gestion/solicitudes/kanban/  │ gestion:solicitudes_kanban│ Tablero Kanban de estados  │
│ /gestion/solicitudes/<id>/    │ gestion:solicitud_detalle│ Ficha 360° de solicitud     │
│ /gestion/solicitudes/<id>/est/│ gestion:solicitud_estado │ Cambio de estado / notas    │
│ /gestion/establecimientos/    │ gestion:establecimientos │ Directorio de colegios      │
│ /gestion/establecimientos/<id>│ gestion:establecimiento_ver│ Ficha e historial colegio │
│ /gestion/contactos/           │ gestion:contactos_lista  │ Directorio de docentes      │
│ /gestion/cotizaciones/        │ gestion:cotizaciones     │ Control cotizaciones PDF    │
│                               │                          │                             │
│ --- ANALÍTICA ---             │                          │                             │
│ /gestion/analitica/           │ gestion:analitica_uso    │ Telemetría y uso global     │
│ /gestion/analitica/productos/ │ gestion:analitica_prods  │ Rankings de demanda         │
│ /gestion/analitica/busquedas/ │ gestion:analitica_search │ Búsquedas y términos        │
│ /gestion/analitica/embudo/    │ gestion:analitica_embudo │ Visualización de embudo     │
│                               │                          │                             │
│ --- TÉCNICA & CONFIGURACIÓN --│                          │                             │
│ /gestion/validacion-tecnica/  │ gestion:validacion_tecnica│ Control compra pública     │
│ /gestion/configuracion/       │ gestion:configuracion    │ Parámetros de Pricing       │
│ /gestion/exportar/<recurso>/  │ gestion:exportar_csv     │ Descargas seguras en CSV    │
└───────────────────────────────┴──────────────────────────┴─────────────────────────────┘
```

---

## 8. Arquitectura Visual y Experiencia de Usuario (UI/UX)

### 8.1 Principios de Interfaz
* **Paleta de Identidad Humm:** Fondo blanco marfil/gris pizarra (`#f8fafc`), acentos en Azul Humm institucional (`#1e3a8a` / `#2563eb`), verde esmeralda para conversiones exitosas (`#059669`) y ámbar de advertencia técnica (`#d97706`).
* **Sidebar Fija con Navegación Colapsable:** Menú lateral siempre accesible en computadores de escritorio, transformable en menú off-canvas en tablets y móviles.
* **Topbar Contextual:** Despliega el nombre del usuario autenticado, selector global de período y badge de solicitudes pendientes.
* **Componentes de Alto Rendimiento:** Gráficos e indicadores construidos mediante HTML semántico y SVG inline ligero, garantizando carga en menos de 300 ms sin librerías JS pesadas.

### 8.2 Estructura del Menú Lateral
```
[ HUMM ] EduCompra Gestión

• Dashboard

CATÁLOGO
  ├── Productos
  ├── Categorías
  ├── Tecnologías
  └── Importaciones (Excel/ZIP)

COMERCIAL
  ├── Solicitudes (Tabla / Kanban)
  ├── Cotizaciones Formales
  ├── Establecimientos Educacionales
  └── Contactos Docentes

ANALÍTICA
  ├── Uso de la Plataforma
  ├── Demanda de Productos
  ├── Búsquedas & Términos
  └── Embudo de Conversión

TÉCNICA
  └── Validación Compra Pública

CONFIGURACIÓN
  └── Parámetros de Pricing
```

---

## 9. Detalle Funcional de los Módulos Principales

### 9.1 Dashboard Principal (`/gestion/`)

#### A. Selector de Período Temporal
Ubicado en la cabecera superior, permite filtrar métricas en:
* **Hoy**
* **Últimos 7 días**
* **Últimos 30 días** (Predeterminado)
* **Este mes**
* **Mes anterior**
* **Personalizado** (rango entre dos fechas)

#### B. Tarjetas KPI Operativas
Cada tarjeta despliega el valor consolidado del período o la leyenda explícita **`Sin datos todavía`** si no existen registros. **Queda terminantemente prohibido inventar o extrapolar cifras:**

1. **Sesiones Activas:** Conteo de `session_key` únicos con eventos en el período.
2. **Solicitudes Recibidas:** Total de registros en `SolicitudCotizacion`.
3. **Establecimientos con Solicitudes:** Cantidad de colegios únicos con solicitudes.
4. **Monto Referencial Solicitado:** Sumatoria de `total_referencial_estimado` en pesos chilenos con formato miles.
5. **Cotizaciones Formales Enviadas:** Conteo de solicitudes en estado `COTIZACION_ENVIADA`.
6. **Monto Formalmente Cotizado:** Sumatoria de `CotizacionFormal.total`.
7. **Ventas / Cierres Exitosos:** Conteo de solicitudes en estado `CERRADA`.
8. **Monto Final Vendido:** Sumatoria de `monto_final_vendido`.
9. **Ticket Promedio Solicitado:** Monto solicitado dividido por el total de solicitudes.
10. **Tasa de Conversión Global:** Porcentaje exacto de `(Solicitudes Enviadas / Sesiones Activas) * 100`.

#### C. Embudo Comercial Visual (Funnel)
Representación gráfica proporcional de 7 etapas:
$$\text{Visita} \longrightarrow \text{Producto visto} \longrightarrow \text{Agregado a Mi Cotización} \longrightarrow \text{Formulario iniciado} \longrightarrow \text{Solicitud enviada} \longrightarrow \text{Cotización enviada} \longrightarrow \text{Venta / Cierre}$$
Despliega cantidad de eventos y tasa porcentual de retención entre cada etapa contigua.

#### D. Tablero de Alertas Operativas
Tres recuadros de atención inmediata:
* **Solicitudes Nuevas sin Asignar:** Alerta de solicitudes en estado `NUEVA` o sin responsable asignado.
* **Candado Técnico Activado:** Solicitudes que contienen productos cuya especificación técnica requiere `VALIDADO_HUMM` antes de cotizar.
* **Alertas de Catálogo:** Productos con stock en estado "consultar" presentes en solicitudes activas.

---

### 9.2 Gestión de Catálogo y Productos (`/gestion/productos/`)

#### A. Listado y Filtros
Tabla operativa con paginación de 25 productos por página:
* Miniatura de imagen optimizada.
* SKU Humm y SKU Proveedor.
* Nombre comercial y Categoría.
* Precio referencial sugerido (CLP con IVA).
* Badges de estado: `Curaduría` (`VALIDADO`, `EN_CURADURIA`, etc.), `Validación Técnica` (`VALIDADO_HUMM`, `NO_REVISADO`), `Disponibilidad` (`disponible`, `importacion`).
* Switch visual para `Publicado` (activa/desactiva mediante llamada AJAX segura con token CSRF y confirmación).
* Conteo acumulado de solicitudes en las que participa el producto.

**Filtros multicriterio:**
* Por Categoría.
* Por Proveedor.
* Por Estado de Publicación (Todos, Publicados, No Publicados).
* Por Estado de Curaduría Pedagógica.
* Por Estado de Validación Técnica (Aptos para Compra Pública vs No Validados).
* Por Estado de Stock.
* Buscador en tiempo real por SKU, nombre comercial, marca y modelo.

#### B. Ficha Administrativa Modular (`/gestion/productos/<id>/`)
La ficha de cada producto se organiza en 6 bloques temáticos:

```
┌────────────────────────────────────────────────────────────────────────┐
│ FICHA DE PRODUCTO: [ HUMM-KEY-KS0011 ] Sensor de Humedad para Suelo    │
├────────────────────────────────────────────────────────────────────────┤
│ 1. BLOQUE COMERCIAL                                                    │
│    Nombre Comercial | Categoría | Unidad de Venta | Precio Referencial │
│    Disponibilidad | Destacado en Portada | Publicado en Catálogo       │
├────────────────────────────────────────────────────────────────────────┤
│ 2. BLOQUE EDUCATIVO & PEDAGÓGICO                                       │
│    Descripción para el Docente | Uso Educativo y Proyectos de Aula     │
│    Nivel de Dificultad | Tecnologías Propuestas | Tecnologías Verificadas│
│    Advertencias de Seguridad / Uso                                     │
├────────────────────────────────────────────────────────────────────────┤
│ 3. BLOQUE DE ABASTECIMIENTO & COSTOS                                   │
│    Proveedor | SKU Proveedor | Costo USD | Factor Internación | TC USD │
│    Costo Chile Neto | Recargo Comercial % | Días de Entrega Estimados  │
├────────────────────────────────────────────────────────────────────────┤
│ 4. BLOQUE TÉCNICO & COMPRA PÚBLICA (MERCADO PÚBLICO)                   │
│    Título Neutro | Especificación Neutra | Cláusula de Equivalencia    │
│    Fuente Técnica / Datasheep | URL Verificación | Estado Validación   │
│    Responsable Técnico Humm | Fecha de Validación Documental           │
├────────────────────────────────────────────────────────────────────────┤
│ 5. BLOQUE DE FOTOGRAFÍAS & MULTIMEDIA                                  │
│    Galería de Imágenes | Selector de Imagen Principal | Subida de Foto │
├────────────────────────────────────────────────────────────────────────┤
│ 6. BLOQUE DE RENDIMIENTO COMERCIAL & ANALÍTICA                         │
│    Vistas Totales | Agregados a Canasta | Solicitudes que lo Contienen │
│    Unidades Solicitadas | Monto Acumulado | Tasa Vista -> Cotización % │
└────────────────────────────────────────────────────────────────────────┘
```

#### C. Creación Manual Segura (`/gestion/productos/nuevo/`)
Formulario que permite dar de alta un producto no existente en Keyestudio (ej: marcas alternativas, servicios o kits especiales):
* **Regla Invariable:** Todo producto nuevo manual se crea obligatoriamente con `publicado = False` y `estado_curaduria = 'SIN_REVISAR'`.
* La interfaz no permitirá marcar `publicado = True` durante la creación. Solo podrá publicarse tras completar la curaduría mínima y validación.

---

### 9.3 Módulo de Importaciones Web Asistidas (`/gestion/importaciones/`)

Este módulo traslada el motor existente en `importar_catalogo_keyestudio.py` al navegador, permitiendo al equipo Humm actualizar costos o incorporar catálogos sin tocar la terminal.

#### A. Flujo de 6 Pasos con Candado DRY-RUN Inviolable
```
[ 1. Subir Excel/ZIP ]
         │
         ▼
[ 2. Ejecutar Simulación DRY-RUN Automática ]
         │
         ▼
[ 3. Desplegar Resumen Estadístico Completo ]
         │
         ▼
[ 4. Revisión de Conflictos y Variaciones de Costo ]
         │
         ▼
[ 5. Aprobación Explícita por Administrador ]
         │
         ▼
[ 6. Ejecución Definitiva en BD bajo Transacción Atómica ]
```

> [!CAUTION]
> **Prohibida la Escritura Directa:** Ningún archivo cargado por la interfaz web podrá aplicarse directamente sobre la base de datos sin haber superado previamente la fase de simulación DRY-RUN y la confirmación explícita del usuario.

#### B. Resumen de Estadísticas Pre-Aprobación
La interfaz presentará una tarjeta comparativa idéntica al estándar del comando CLI:
* Filas totales leídas en el Excel.
* SKUs únicos detectados.
* Productos nuevos que se crearían.
* Productos existentes con cambios de costo USD.
* Productos sin cambios de costo.
* Conflictos de duplicidad con inconsistencias (excluidos automáticamente).
* Productos sin fotografía en banco.
* Imágenes huérfanas en el archivo ZIP.
* Errores de formato en precios.

#### C. Preservación Estricta de la Curaduría Docente
Al actualizar productos existentes desde el archivo del proveedor, el motor **PRESERVA INTACTO**:
* `nombre_comercial` (redactado por Humm).
* `descripcion_educativa` y `descripcion_corta`.
* `categoria` asignada.
* `tecnologias_compatibles` y `tecnologias_verificadas`.
* `advertencia_uso`.
* `unidad_compra`.
* `titulo_especificacion_neutral` y `especificacion_tecnica_neutral`.
* `publicado` y `estado_curaduria`.

**Únicos campos que se actualizan:**
* `costo_proveedor_usd`.
* `costo_puesto_chile_clp` (recalculado).
* `precio_sugerido_neto_clp` y `precio_sugerido_total_clp` (recalculados).
* Vinculación de nuevas imágenes físicas si se aportan en el ZIP.

---

### 9.4 Gestión Comercial de Solicitudes (`/gestion/solicitudes/`)

#### A. Vista Dual: Tabla y Tablero Kanban
El usuario puede alternar instantáneamente entre dos visualizaciones:
1. **Vista Tabla:** Lista cronológica con columnas para Código (`EC-2026-XXXXXX`), Fecha, Docente, Establecimiento, Comuna, Región, Ítems, Total Referencial, Estado, Responsable y Alerta de Validación Técnica.
2. **Vista Kanban Comercial:** 8 columnas correspondientes al ciclo comercial escolar:
   * `Nueva`
   * `En revisión de stock`
   * `Requiere antecedentes`
   * `Lista para cotizar`
   * `Cotización preparada`
   * `Cotización enviada`
   * `Cerrada (Venta)`
   * `Perdida / Cancelada`
   * *Mecanismo de cambio:* Selector desplegable rápido en cada tarjeta sin requerir librerías externas de drag-and-drop en la primera fase.

#### B. Ficha de Solicitud 360° (`/gestion/solicitudes/<id>/`)
* **Contacto:** Nombre, cargo docente, email con enlace `mailto:`, teléfono con botón directo `WhatsApp Web`.
* **Establecimiento:** Nombre institucional, dependencia, comuna, región, RUT e hipervínculo a la ficha consolidada del establecimiento.
* **Detalle de Productos:** Tabla con los snapshots inmutables guardados al momento de solicitar (SKU Humm, SKU proveedor, nombre comercial, unidad, cantidad, precio referencial unitario y subtotal).
* **Gestión Interna:** Selector de responsable Humm, selector de estado y bitácora de notas internas de seguimiento con timestamp.
* **Candado de Compra Pública:** Alerta destacada indicando qué productos cuentan con `VALIDADO_HUMM` y cuáles requieren redacción técnica antes de emitir la cotización formal.
* **Campos Mercado Público:** Registro de ID de Licitación, ID de Compra Ágil o ID de Orden de Compra.

---

### 9.5 Módulo de Establecimientos y Contactos

#### A. Directorio y Ficha de Establecimiento (`/gestion/establecimientos/<id>/`)
Concentra la historia comercial de cada colegio o liceo:
* Datos de cabecera: Nombre oficial, RBD, dependencia institucional, comuna y región.
* Directorio de contactos vinculados (profesores de robótica, coordinadores de enlaces, directores, encargados DAEM).
* Historial de solicitudes recibidas en el tiempo.
* Métricas del colegio:
  * Número total de solicitudes emitidas.
  * Monto histórico solicitado (CLP).
  * Monto formalmente cotizado (CLP).
  * Monto final cerrado/vendido (CLP).
  * Ticket promedio por solicitud.
  * Productos más requeridos por la institución.
  * Fecha de la última interacción.

#### B. Directorio de Contactos (`/gestion/contactos/`)
* Lista de profesores y directivos con búsqueda rápida por nombre, email o colegio.
* Prevención de duplicados por email normalizado.

---

### 9.6 Analítica de Demanda y Búsquedas

#### A. Analítica de Rendimiento de Productos (`/gestion/analitica/productos/`)
Rankings interactivos filtrables por período:
1. **Productos Más Vistos:** Por volumen de eventos `VER_PRODUCTO`.
2. **Productos Más Agregados:** Por volumen de eventos `AGREGAR_COTIZACION`.
3. **Productos Más Solicitados:** Por unidades demandadas en `SolicitudItem`.
4. **Mayor Monto Demandado:** Por sumatoria de pesos chilenos requeridos.
5. **Más Vendidos:** Por solicitudes con estado `CERRADA`.
6. **Matriz de Alerta: Alta Vista / Baja Solicitud:** Identifica productos con alto tráfico pero nulo agregado a cotización, señalando potenciales desajustes de precio sugerido, descripción formativa confusa o falta de compatibilidad visible.

#### B. Analítica de Búsquedas y Demanda No Cubierta (`/gestion/analitica/busquedas/`)
* Total de búsquedas realizadas en el catálogo público.
* Desglose: búsquedas exitosas vs búsquedas con 0 resultados.
* **Panel Destacado: “¿Qué buscan los profesores y no tenemos?”**
  Tabla de términos con cero resultados rankeados por frecuencia:
  ```
  | Término Buscado       | Veces Buscado | Última Búsqueda     | Acción Comercial Sugerida        |
  | :-------------------- | :-----------: | :------------------ | :------------------------------- |
  | Impresora 3D Ender    |      28       | 30-09-2026 11:20    | Evaluar incorporación catálogo   |
  | Sensor CO2 NDIR       |      19       | 29-09-2026 16:45    | Buscar equivalente en proveedor  |
  | Kit robótica solar    |      14       | 28-09-2026 09:12    | Diseñar kit temático Humm        |
  ```

---

### 9.7 Configuración Segura de Parámetros de Pricing (`/gestion/configuracion/`)

Permite a los administradores autorizados ajustar los parámetros económicos del modelo `ConfiguracionPricing`:
* **Tipo de Cambio (USD a CLP):** Valor referencial del dólar.
* **Recargo Comercial Sugerido (%):** Margen referencial predeterminado.
* **Factor de Flete e Internación (%):** Costos de aduana y logística internacional.
* **IVA (%):** Impuesto vigente en Chile.
* **Correo de Notificaciones:** Destinatario de avisos de solicitudes entrantes.

> [!CAUTION]
> **Seguridad Estricta de Configuración:** La interfaz de configuración **NUNCA** expondrá secretos del sistema, claves de base de datos, `SECRET_KEY`, credenciales SSH ni variables de entorno del servidor. Toda modificación queda registrada en `RegistroActividad`.

---

## 10. Seguridad, Control de Acceso y Auditoría

### 10.1 Esquema de Permisos
Se utilizará el sistema nativo de autenticación de Django (`django.contrib.auth`), definiendo 3 perfiles de acceso:
1. **Superadministrador (`is_superuser = True`):** Acceso total a `/gestion/`, `/admin/`, auditoría y configuración de pricing.
2. **Administrador EduCompra (Grupo `Administradores EduCompra`):** Gestión de catálogo, importaciones, solicitudes, establecimientos, contactos y analítica. Sin acceso a Django Admin.
3. **Comercial EduCompra (Grupo `Comercial EduCompra`):** Gestión de solicitudes, cotizaciones, establecimientos y contactos. Acceso de solo lectura a catálogo y sin acceso a importaciones ni configuración.

### 10.2 Decoradores de Acceso y Protección de Vistas
* `@gestion_required`: Decorador personalizado que valida usuario autenticado, activo y perteneciente al staff o a los grupos autorizados. Redirige a `/gestion/login/` con parámetro `next`.
* `@permiso_requerido('permiso')`: Control de acciones restringidas (ej: ejecutar importaciones o publicar productos).
* `@require_POST` y verificación obligatoria de token CSRF (`{% csrf_token %}`) en todos los formularios de edición, switches de estado y acciones masivas.

---

## 11. Plan de Pruebas Automatizadas (Test Suite Fase 5)

Se desarrollará una suite exhaustiva de pruebas en `apps/gestion/tests/`:

| # | Caso de Prueba Requerido | Condición Verificada |
| :-: | :--- | :--- |
| **1** | Protección de rutas administrativas | Petición anónima a `/gestion/` o cualquier sub-ruta es redirigida a `/gestion/login/`. |
| **2** | Autenticación y control de roles | Usuario comercial no puede acceder a `/gestion/importaciones/` ni `/gestion/configuracion/`. |
| **3** | Cálculo exacto de KPIs en Dashboard | Las tarjetas suman exactamente solicitudes y montos según el período seleccionado. |
| **4** | Manejo de "Sin datos todavía" | Métricas sin eventos retornan la leyenda institucional en lugar de 0 inventado. |
| **5** | Filtros de período temporal | El selector filtra con precisión los eventos de "Hoy", "Últimos 7 días" y "Últimos 30 días". |
| **6** | Creación manual de producto protegida | Un producto creado en `/gestion/productos/nuevo/` se guarda siempre con `publicado=False` y `SIN_REVISAR`. |
| **7** | Switch AJAX de publicación | Cambiar estado de publicación actualiza el registro en BD y registra la auditoría. |
| **8** | Importación Web DRY-RUN | La carga de un Excel ejecuta la simulación sin modificar la base de datos real. |
| **9** | Preservación de curaduría en importación | Una actualización masiva de costos no altera nombres comerciales ni descripciones curadas. |
| **10** | Detección de conflictos en importación | SKUs conflictivos son detectados y excluidos de la importación productiva. |
| **11** | Transición de estados en solicitudes | El cambio de estado en Kanban o tabla actualiza `SolicitudCotizacion.estado` y genera log en auditoría. |
| **12** | Inmutabilidad de snapshots históricos | Modificar o eliminar un producto de catálogo no altera los ítems de solicitudes pasadas. |
| **13** | Normalización de Establecimientos | Creación o match inteligente de establecimientos por nombre normalizado y comuna. |
| **14** | Deduplicación de Contactos | Docente con mismo email en solicitudes sucesivas no duplica el registro `Contacto`. |
| **15** | Captura y deduplicación de telemetría | Refrescar una ficha 10 veces en 2 minutos genera exactamente 1 evento `VER_PRODUCTO`. |
| **16** | Telemetría privada y anónima | Los eventos `EventoUso` no registran RUT, correos ni datos sensibles del usuario. |
| **17** | Bloque de Demanda No Cubierta | Búsquedas públicas con 0 resultados aparecen consolidadas en el ranking de analítica. |
| **18** | Candado de Compra Pública | Intento de cotizar formalmente productos sin `VALIDADO_HUMM` activa la alerta de bloqueo. |
| **19** | Separación estricta de montos | El sistema reporta por separado Monto Solicitado, Monto Cotizado y Monto Vendido. |
| **20** | Exportación segura CSV | La descarga de productos o solicitudes genera archivo CSV válido con codificación UTF-8 BOM para Excel. |

---

## 12. Estrategia de Despliegue en Producción (HostGator / Passenger WSGI)

El despliegue en `https://educompra.humm.cl` seguirá un protocolo riguroso y sin interrupción de servicio:

1. **Paso 1: Respaldo Preventivo de Base de Datos**
   ```bash
   cp /home1/paulocis/apps/educompra/data/db.sqlite3 /home1/paulocis/apps/educompra/backups/db_backup_pre_fase5_$(date +%Y%m%d_%H%M%S).sqlite3
   ```
2. **Paso 2: Sincronización de Código (Git pull)**
   Incorporación de la nueva app `apps.gestion`, templates y static assets.
3. **Paso 3: Ejecución de Migraciones Estructuradas**
   ```bash
   python manage.py makemigrations cotizaciones
   python manage.py makemigrations gestion
   python manage.py migrate
   ```
4. **Paso 4: Migración de Datos Históricos**
   ```bash
   python manage.py conciliar_establecimientos_historicos
   ```
5. **Paso 5: Creación de Grupos y Roles Predeterminados**
   ```bash
   python manage.py crear_roles_gestion
   ```
6. **Paso 6: Recopilación de Archivos Estáticos**
   ```bash
   python manage.py collectstatic --noinput
   ```
7. **Paso 7: Reinicio Limpio de Passenger WSGI**
   ```bash
   touch tmp/restart.txt
   ```
8. **Paso 8: Smoke Tests en Vivo**
   * Verificación de catálogo público operativo en `https://educompra.humm.cl/catalogo/`.
   * Verificación de acceso restringido en `https://educompra.humm.cl/gestion/`.
   * Verificación de Django Admin intacto en `https://educompra.humm.cl/admin/`.

---

## 13. Declaración de No-Implementación y Punto de Control

> [!IMPORTANT]
> ### ESTADO ACTUAL: DETENIDO EN PUNTO DE CONTROL (SECCIÓN 48)
> En estricto cumplimiento de las instrucciones de Humm:
> * **NO se ha modificado la base de datos.**
> * **NO se han ejecutado migraciones ni creado modelos.**
> * **NO se ha modificado el catálogo público ni el flujo de solicitudes.**
> * **NO se ha alterado el Django Admin técnico existente.**
> * El presente documento constituye el diseño de arquitectura integral sometido a la revisión, observaciones y aprobación formal del equipo directivo de Humm antes de iniciar la construcción de código.
