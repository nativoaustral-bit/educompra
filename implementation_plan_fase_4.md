# PLAN DE IMPLEMENTACIÓN — FASE 4
## Catálogo Público, Experiencia Docente y Solicitud de Cotización
### Plataforma EduCompra Humm (`educompra.humm.cl`)

**Documento:** `implementation_plan_fase_4.md`  
**Fecha de Elaboración:** 29 de Septiembre de 2026  
**Responsable Técnico:** Antigravity (Google DeepMind Pair Programmer)  
**Destinatario:** Equipo Directivo, Comercial y Pedagógico de Humm  
**Estado:** **PROPUESTA PARA REVISIÓN Y APROBACIÓN PREVIA — NO IMPLEMENTAR TODAVÍA**

---

## 1. Contexto, Objetivos y Principios Rectores

### 1.1 Estado Inicial al Cierre de Fase 3
La Fase 3 finalizó con el sellado definitivo del catálogo educativo inicial:
* **Catálogo Maestro:** 929 productos físicos ingresados en SQLite.
* **Catálogo Curado Aprobado:** **72 productos** en `estado_curaduria = 'VALIDADO'`.
* **Catálogo Latente / Descartado:** 854 productos en `SIN_REVISAR` y 3 en `DESCARTADO_CATALOGO_PUBLICO`.
* **Catálogo Público:** **0 productos publicados** (`publicado = False` en los 929 registros).
* **Candado de Compra Pública:** **0 productos en `VALIDADO_HUMM`** (`estado_especificacion_neutral = 'NO_REVISADO'`). La función `puede_generar_cotizacion_formal()` bloquea la emisión formal de bases técnicas.
* **Seguridad y Compatibilidad:** Separación estricta entre compatibilidad tecnológica `VERIFICADA` y `PROPUESTA`; campo `advertencia_uso` poblado en 11 productos críticos.
* **Calidad y Consistencia:** 100% de coincidencia auditada entre [`CATALOGO_CURADO_FASE_3.md`](file:///Users/rmerinog/PLATAFORMAS/EDUCOMPRA/CATALOGO_CURADO_FASE_3.md) y base de datos (`auditar_consistencia_curaduria` exitoso y 24 tests pasando).

---

### 1.2 Objetivo General de la Fase 4
Construir y verificar en [https://educompra.humm.cl](https://educompra.humm.cl) la primera experiencia pública comercial de EduCompra Humm: **simple, rápida, visual y orientada a profesores y establecimientos educacionales**.

El flujo operativo central será:
$$\text{Explorar} \longrightarrow \text{Encontrar} \longrightarrow \text{Revisar} \longrightarrow \text{Agregar} \longrightarrow \text{Solicitar cotización}$$

> [!IMPORTANT]
> ### EduCompra NO es un ecommerce tradicional
> En la Fase 4 **NO se implementará**:
> * Pago online (Webpay, tarjetas o transferencias automáticas).
> * Carrito tradicional de checkout transaccional.
> * Cuentas obligatorias ni login para docentes.
> * Consulta de stock en tiempo real.
> * Integración directa con Mercado Público.
> * Generación automática de bases de licitación.
> * Emisión automática de PDF formal de cotización vinculante.

---

### 1.3 Principio de Experiencia y Usuario Objetivo
El profesor o encargado de tecnología que visita EduCompra:
* No necesita conocer el SKU del fabricante (`KS...`, `MD...`), los procesos aduaneros, la estructura de fábrica de Keyestudio ni los estados internos de curaduría.
* Debe poder pensar simplemente:
  > *"Necesito componentes para mi proyecto, los selecciono y Humm me cotiza."*
* **Perfil de Usuario:** Profesor de aula, encargado de laboratorio de computación/enlaces, o coordinador STEM/robótica.
* **Dispositivos Clave:** Celulares, notebooks institucionales y tablets escolares.
* **Criterio de Diseño:** Mobile-first, tiempos de carga inferiores a 1 segundo, tipografía legible y funcionamiento fluido en computadores escolares antiguos.

---

## 2. Arquitectura Pública Propuesta y Enrutamiento SSR

Se utilizará una arquitectura limpia **Django Server-Side Rendering (SSR)** con templates semánticos, Vanilla CSS y JavaScript nativo mínimo para micro-interacciones, evitando frameworks SPA pesados.

```
┌────────────────────────────────────────────────────────────────────────┐
│                        MAPA DE RUTAS PÚBLICAS                          │
├───────────────────────────────┬────────────────────────────────────────┤
│ /                             │ Página de Inicio EduCompra             │
│ /catalogo/                    │ Catálogo interactivo con filtros       │
│ /catalogo/<slug>/             │ Ficha pedagógica de producto           │
│ /mi-cotizacion/               │ Lista temporal de productos agregados  │
│ /solicitar-cotizacion/        │ Formulario institucional de solicitud  │
│ /solicitud-recibida/<token>/  │ Confirmación de recepción con resumen  │
└───────────────────────────────┴────────────────────────────────────────┘
```

---

## 3. Detalle de Páginas y Componentes

### 3.1 Página de Inicio (`/`)
Diseñada para comunicar la propuesta de valor en menos de 5 segundos:

* **Hero Section:**
  * **Título Principal:** *Tecnología educativa para tus proyectos, lista para cotizar.*
  * **Bajada:** *Encuentra componentes, sensores, robótica y kits para tus clases. Selecciona lo que necesitas y solicita una cotización a Humm.*
  * **CTA Principal:** `Explorar catálogo` (redirige a `/catalogo/`).
  * **CTA Secundario:** `Cómo funciona` (scroll suave a la sección explicativa).
* **Sección "Cómo Funciona":**
  3 pasos simples e ilustrados:
  1. **1. Explora:** *Encuentra componentes para tus proyectos educativos.*
  2. **2. Selecciona:** *Agrega los productos y cantidades que necesita tu establecimiento.*
  3. **3. Solicita:** *Envía la solicitud y Humm prepara la cotización.*
* **Grid de Categorías Curadas:**
  * Despliega exclusivamente las **11 categorías curadas oficiales** de Fase 3.
  * No muestra categorías vacías ni categorías internas de fábrica ("Sin clasificar").
  * Cada tarjeta incluye ícono educativo, nombre formativo y conteo de productos disponibles.
* **Sección de Productos Destacados:**
  * Selección administrada desde Django Admin mediante el campo existente `destacado = True`.
  * Cero rankings algorítmicos complejos; control editorial humano directo por Humm.

---

### 3.2 Catálogo Público Interactivo (`/catalogo/`)

#### A. Regla Estricta de Publicación
Para que un producto aparezca en el catálogo público, el QuerySet debe aplicar obligatoriamente:
```python
Producto.objects.filter(
    activo=True,
    estado_curaduria='VALIDADO',
    publicado=True
)
```
> [!CAUTION]
> **Blindaje Absoluto:** Los 857 productos restantes del catálogo maestro (`SIN_REVISAR` y `DESCARTADO_CATALOGO_PUBLICO`) jamás deben ser accesibles ni expuestos por búsqueda o URL directa (deben retornar `Http404`).

#### B. Buscador y Filtros Simples (Adaptados a 72 Productos)
Dado que el catálogo inicial cuenta con 72 productos, los filtros deben ser livianos y directos:
* **Búsqueda por texto:** Coincidencia en `nombre_comercial`, `descripcion_educativa` y `posible_uso_educativo`.
* **Filtro por Categoría:** Selector rápido de las 11 categorías formativas.
* **Filtro por Tecnología:** `Arduino`, `micro:bit`, `Raspberry Pi`, `ESP32`, `Otros`.
* **Filtro por Nivel de Uso:** `Inicial`, `Intermedio`, `Avanzado`.
* **Filtros Opcionales:** Switch *"Apto para armar kits"* (`apto_para_kit = True`) y selector de rango de presupuesto referencial en CLP.

#### C. Tarjeta de Producto (Product Card)
Cada tarjeta en la grilla contendrá únicamente:
* **Fotografía optimizada** (thumbnail WebP/JPEG generado en Fase 2, nunca la imagen original pesada).
* **Nombre Comercial Humm** (ej: *Placa Keyestudio PLUS con USB-C compatible con Arduino Uno R3*).
* **Categoría docente** (badge sutil).
* **Nivel de complejidad** (`Inicial`, `Intermedio`, `Avanzado`).
* **Tecnologías principales** (chips visuales: Arduino, micro:bit, etc.).
* **Precio Referencial con IVA** (ej: *$26.912 CLP con IVA*).
* **Botones de Acción:**
  * `Ver producto` (enlace al detalle).
  * `Agregar a mi cotización` (agrega 1 unidad comercial a la sesión con feedback visual).

#### D. Política y Leyenda de Precios Públicos
* Siempre se rotulará como **"Precio referencial con IVA"** (evitando la palabra aislada "Precio").
* Se incluirá una leyenda general visible en el pie del catálogo y en la ficha:
  > *"Los precios publicados son referenciales y pueden variar según disponibilidad, tipo de cambio, cantidad, importación y condiciones de entrega. El valor definitivo será informado en la cotización formal emitida por Humm."*
* **Protección de Datos Internos:** Queda estrictamente prohibido renderizar costo de proveedor (USD), factor de internación, recargo comercial o pricing interno Humm en cualquier template público.

---

### 3.3 Ficha Detallada del Producto (`/catalogo/<slug>/`)
Estructurada con una jerarquía pedagógica orientada a responder las preguntas del docente:

1. **Fotografía:** Imagen principal destacada con carga diferida (`loading="lazy"`) y previsualización de tomas complementarias.
2. **Nombre Comercial Humm:** Título claro y comprensible.
3. **Precio Referencial con IVA:** Destacado prominentemente, acompañado del precio neto referencial desglosado.
4. **Para qué sirve:** Descripción educativa breve y amigable.
5. **Ideas para usarlo:** 1 o 2 ejemplos concretos de proyectos escolares de aula (ej: estación meteorológica escolar, robot seguidor de línea, sistema de riego automatizado).
6. **Qué incluye:** Sección crítica para evitar malentendidos:
   * Detalle explícito en kits, packs y sets (ej: *Set de prototipado: incluye 1 fuente 3.3V/5V, 1 protoboard de 830 pts y 65 cables de conexión*).
   * Advertencia de productos sin microcontrolador (ej: *Chasis 4WD: no incluye placa controladora ni pilas*).
7. **Compatible con:**
   * **Compatibilidad indicada por fabricante:** Plataformas certificadas por fábrica.
   * **Integraciones sugeridas por Humm:** Propuestas formativas de aula (claramente diferenciadas).
8. **Nivel de uso:** Badge informativo (`Inicial`, `Intermedio`, `Avanzado`).
9. **Advertencia de uso:** Renderizado condicional exclusivo para productos donde `advertencia_uso` tiene contenido:
   * *Gases MQ:* módulo didáctico, no reemplaza detectores normados.
   * *Llama:* óptica experimental, no es alarma de incendios.
   * *Pulso:* bioseñales didácticas, **no es dispositivo médico**.
   * *2 Relés:* cargas de baja tensión escolar (5V/12V), tensión 220V prohibida para alumnos.
   * *Multímetros:* circuitos educativos de baja tensión (hasta 24V).
   * *Baterías y chasis:* comprobación estricta de polaridad para evitar cortocircuitos.
10. **Unidad de Compra y Selector de Cantidad:**
    * El selector numérico (+ / -) representa **unidades comerciales** (unidades, packs o sets).
    * Ejemplo: Si el producto es `Pack de 3 servomotores SG90`, seleccionar cantidad `2` indica explícitamente: **2 packs = 6 servomotores**.
11. **CTA Principal:** Botón prominente `Agregar a mi cotización`.

---

### 3.4 "Mi Cotización" — Selección Temporal sin Login (`/mi-cotizacion/`)

#### A. Principios de Interacción
* Se utilizará la expresión **"Mi cotización"** (prohibido utilizar términos de ecommerce transaccional como "carrito" o "checkout").
* **Persistencia sin Cuentas:** Se almacena en sesión de Django (`request.session['mi_cotizacion']`), serializada en JSON:
  ```json
  {
    "KS0486": {"cantidad": 2, "precio_unitario_total": 26912.00, "unidad": "unidad"},
    "KS0326": {"cantidad": 1, "precio_unitario_total": 21039.00, "unidad": "pack (3 unidades)"}
  }
  ```
* El docente puede navegar, cerrar la pestaña y regresar sin perder su selección durante la sesión.

#### B. Funcionalidades de la Vista (`/mi-cotizacion/`)
* Tabla clara con fotografía, nombre comercial, unidad de compra y empaque.
* Modificación reactiva de cantidades (+ / -) con actualización inmediata del subtotal.
* Eliminación individual de productos.
* Botón de retorno al catálogo (`Seguir explorando`).
* Subtotal referencial por producto y **Total referencial acumulado (CLP con IVA)**.
* Botón CTA principal: **Solicitar cotización** (conduce a `/solicitar-cotizacion/`).

---

### 3.5 Formulario de Solicitud Institucional (`/solicitar-cotizacion/`)

Diseñado para solicitar exclusivamente la información indispensable para preparar la propuesta formal:

#### A. Campos Requeridos
* **Datos del Contacto:**
  * Nombre y Apellido.
  * Correo electrónico (validación de formato).
  * Teléfono / WhatsApp (para coordinación rápida).
* **Datos de la Institución:**
  * Nombre del establecimiento educacional / organización.
  * Región (selector de las 16 regiones de Chile).
  * Comuna (selector dinámico según región).

#### B. Campos Opcionales (No Obligatorios)
* Cargo o rol del solicitante (Profesor/a, UTP, Encargado/a de Adquisiciones, etc.).
* RUT del establecimiento o sostenedor.
* Nombre del proyecto educativo o destino de los materiales.
* Fecha aproximada en que se requieren los productos.
* Comentarios u observaciones adicionales.

#### C. Cláusula de Privacidad y Contacto
* Aceptación explícita y sencilla:
  > *"Autorizo a Humm a contactarme para gestionar esta solicitud de cotización."*
* **Regla Ética:** Prohibido utilizar casillas pre-marcadas. La solicitud no suscribe automáticamente a listas de mailing ni publicidad masiva.

---

### 3.6 Persistencia, Snapshots y Código de Seguimiento

#### A. Reutilización de Modelos Existentes
Se utilizarán los modelos ya creados en `apps/cotizaciones/models.py`:
* **`SolicitudCotizacion`:** Cabecera de la solicitud.
* **`SolicitudItem`:** Detalle de productos con arquitectura de **snapshots inmutables**.

#### B. Lógica de Persistencia Robusta
1. Al presionar "Enviar Solicitud", se crea primero la transacción en base de datos.
2. Cada ítem guarda una copia congelada (`snapshot`) de:
   * `sku_humm_snapshot`, `sku_proveedor`, `nombre_comercial_snapshot`.
   * `precio_referencial_unitario_snapshot`, `subtotal_referencial_snapshot`.
   * `especificacion_neutra_snapshot` (borrador vigente).
3. **Independencia Histórica:** Si en el futuro un producto cambia de precio o se modifica en el catálogo maestro, las cotizaciones previas permanecen inmutables.
4. **Resiliencia ante Fallos de Correo:**
   * La notificación por correo electrónico es **estrictamente secundaria**.
   * Si el servidor SMTP falla, la solicitud **permanece registrada en base de datos**, se captura la excepción en log y al usuario se le muestra su pantalla de confirmación exitosa con su código.

#### C. Identificador Comercial Legible
* Se generará un código amigable para el docente en formato:
  $$\text{EC-2026-XXXXXX} \quad (\text{ej: } \text{EC-2026-000123})$$
* Para la visualización pública se utilizará un token seguro (`uuid4`) en la URL:
  `/solicitud-recibida/<token>/` evitando exponer IDs numéricos secuenciales directos de base de datos.

---

### 3.7 Página de Confirmación (`/solicitud-recibida/<token>/`)
* Mensaje principal: **Solicitud recibida con éxito**.
* Número de solicitud comercial destacado (`EC-2026-XXXXXX`).
* Nombre del colegio o institución solicitante.
* Resumen de productos seleccionados, unidades comerciales y total referencial estimado.
* Mensaje de expectativas claro (sin promesas rígidas de plazos automáticos):
  > *"Recibimos tu solicitud EC-2026-XXXXXX. Humm revisará disponibilidad, cantidades y condiciones de entrega antes de preparar la cotización definitiva."*
* Enlace para volver al catálogo o imprimir el comprobante.

---

### 3.8 Notificaciones por Correo Electrónico
* **Al Equipo de Humm:**
  * Notificación inmediata con datos del colegio, contacto y productos solicitados.
  * Destinatario configurable mediante variable de entorno `HUMM_COTIZACIONES_EMAIL` (prohibido hardcodear correos personales).
* **Al Solicitante:**
  * Correo automático de confirmación con el resumen de su solicitud si SMTP está activo.
  * El fallo en el envío nunca cancela ni revierte la solicitud en base de datos.

---

### 3.9 Administración de Solicitudes y Candado de Compra Pública (`apps/cotizaciones/admin.py`)

#### A. Pipeline de Estados Comerciales
Se actualizarán los estados de `SolicitudCotizacion` al flujo escolar real:
```python
ESTADOS_SOLICITUD = [
    ("NUEVA", "Nueva solicitud recibida"),
    ("EN_REVISION", "En revisión de stock / factibilidad"),
    ("REQUIERE_ANTECEDENTES", "Requiere contactar al docente por antecedentes"),
    ("LISTA_PARA_COTIZAR", "Lista para emitir cotización"),
    ("COTIZACION_PREPARADA", "Cotización formal preparada"),
    ("COTIZACION_ENVIADA", "Cotización enviada al colegio"),
    ("CERRADA", "Cerrada exitosamente (Venta realizada)"),
    ("PERDIDA", "Desestimada / Perdida"),
    ("CANCELADA", "Cancelada por el solicitante"),
]
```

#### B. Candado de Compra Pública en Django Admin
* El docente puede cotizar productos con especificación en `NO_REVISADO`.
* **Regla Humm:** La emisión de bases técnicas o documentación formal para licitaciones públicas (Mercado Público / Ley 19.886) exige `VALIDADO_HUMM`.
* En la vista administrativa de cada solicitud:
  * Si la solicitud contiene productos con `estado_especificacion_neutral != 'VALIDADO_HUMM'`, se desplegará una alerta prominente:
    > ⚠️ **Atención:** Esta solicitud incluye productos que requieren validación técnica individual antes de emitir documentación formal de compra pública.
  * Esto permite que los ingenieros curadores de Humm validen documentalmente las fichas necesarias **de manera progresiva según demanda comercial real**.

---

## 4. Activación y Publicación Controlada del Catálogo

Durante el desarrollo y pruebas de la Fase 4:
* Todos los productos permanecerán con `publicado = False`.
* Se creará el comando de publicación controlada:
  ```bash
  python manage.py activar_catalogo_publico_fase_4 --dry-run
  python manage.py activar_catalogo_publico_fase_4
  ```
* **Condiciones indispensables para que un producto pase a `publicado = True`:**
  1. `activo == True`.
  2. `estado_curaduria == 'VALIDADO'`.
  3. `nombre_comercial` poblado.
  4. `categoria` asignada (distinta de "Sin clasificar").
  5. `descripcion_educativa` poblada.
  6. Al menos una imagen optimizada asociada.
  7. Precio referencial calculable.
* **Punto de Control:** La ejecución real de este comando será el **Hito Final de Autorización de Humm**.

---

## 5. Rendimiento, Seguridad y SEO Básico

### 5.1 Rendimiento y Optimización Móvil
* **Carga de Imágenes:** Uso de miniaturas (thumbnails) optimizadas generadas en Fase 2. Las imágenes en grillas no superarán los 400px de ancho con compresión WebP/JPEG.
* **Lazy Loading:** Atributo nativo `loading="lazy"` en todas las tarjetas de producto.
* **Paginación / Límite Inicial:** Grilla paginada o segmentada de 24 productos por vista para navegación ultrarrápida.
* **Assets:** Vanilla CSS compacto (< 40 KB) y JavaScript vanilla sin frameworks externos.

### 5.2 Seguridad del Formulario
* Token de protección contra ataques CSRF (`{% csrf_token %}`) en todos los formularios POST.
* Validación estricta en backend de emails, números de teléfono y límites de caracteres.
* Campo trampa anti-spam (**Honeypot**) invisible en CSS para detectar bots sin molestar al profesor con captchas difíciles.
* Sanitización contra XSS en todos los campos de texto libre.

### 5.3 SEO Básico
* Etiquetas `<title>` y `<meta name="description">` semánticas y atractivas para buscadores en cada página.
* URLs amigables con slug autogenerado a partir del nombre comercial:
  `/catalogo/placa-keyestudio-plus-usb-c/` (con fallback transparente por SKU proveedor).
* Etiquetas Open Graph (`og:title`, `og:image`, `og:description`) para que las fichas se vean atractivas al ser compartidas en WhatsApp o redes docentes.
* Archivo `robots.txt` y sitemap XML básico (`/sitemap.xml`).

### 5.4 Métricas Mínimas de Gestión
Registro estructurado en base de datos para análisis directivo:
* Solicitudes generadas por semana y mes.
* Monto total referencial demandado.
* Productos y categorías más cotizadas.
* Distribución de solicitudes por región y tipo de establecimiento.
* Estructura desacoplada y lista para integración futura con *Humm Control Center (HCC)* (sin implementar HCC en Fase 4).

---

## 6. Plan de Pruebas Automatizadas Obligatorias

Se desarrollará una suite integral en `apps/catalogo/tests/test_fase4_publico.py` y `apps/cotizaciones/tests/test_fase4_solicitud.py`:

| # | Caso de Prueba Requerido | Condición Verificada |
| :-: | :--- | :--- |
| **1** | Solo productos autorizados visibles | Exactamente los productos con `publicado=True` y `VALIDADO` aparecen en `/catalogo/`. |
| **2** | Bloqueo de catálogo latente | Productos con `publicado=False` retornan `HTTP 404` si se intenta acceder por URL directa. |
| **3** | Productos no curados jamás aparecen | Productos en `SIN_REVISAR` o `DESCARTADO` nunca se exponen en vistas públicas. |
| **4** | Agregar producto a "Mi cotización" | La petición POST guarda el SKU y cantidad en `request.session`. |
| **5** | Modificar cantidad | El incremento o decremento actualiza la sesión y el subtotal referencial. |
| **6** | Eliminar producto | El ítem se remueve limpiamente de la sesión. |
| **7** | Persistencia de "Mi cotización" | La selección se mantiene entre distintas solicitudes HTTP sin requerir login. |
| **8** | Cálculo exacto de subtotales | Multiplicación exacta de precio unitario con IVA por cantidad. |
| **9** | Cálculo exacto del total | Sumatoria precisa de los subtotales en CLP. |
| **10** | Unidades tipo pack y set | El selector de cantidad opera sobre el pack comercial (ej: 2 packs de 3 servos = 6 servos). |
| **11** | Creación exitosa de Solicitud | Formulario válido crea registro en `SolicitudCotizacion` y genera código `EC-2026-XXXXXX`. |
| **12** | Congelamiento de Snapshots | `SolicitudItem` guarda copia inmutable de nombre, precio referencial y especificación. |
| **13** | Validación de formulario inválido | Errores en email o campos requeridos vacíos no guardan registros y muestran feedback. |
| **14** | Prevención de doble envío | Envío duplicado no genera múltiples solicitudes idénticas. |
| **15** | Resiliencia ante fallo SMTP | Fallo simulado en envío de correo **no aborta** la creación de la solicitud en base de datos. |
| **16** | Protección CSRF | Peticiones POST sin token CSRF son rechazadas con `HTTP 403`. |
| **17** | Advertencias de uso educativo | Fichas de los 11 productos sensibles despliegan la caja de alerta obligatoria. |
| **18** | Candado de cotización formal | `puede_generar_cotizacion_formal()` retorna `False` para productos en `NO_REVISADO`. |

---

## 7. Criterios de Aceptación para el Cierre de Fase 4

La Fase 4 se considerará formalmente completada cuando se cumplan y auditen los siguientes 17 criterios:
1. **Catálogo público funcional:** Grilla de 72 productos operativa en `/catalogo/`.
2. **Buscador operativo:** Búsqueda rápida por nombre y aplicación educativa.
3. **Filtros pedagógicos operativos:** Navegación por las 11 categorías, tecnologías y niveles.
4. **Detalle de producto pedagógico:** Ficha clara con fotos, qué incluye y proyectos escolares.
5. **"Mi cotización" operativa:** Visualización de insumos seleccionados sin lenguaje de checkout tradicional.
6. **Cantidades editables:** Selector claro respetando unidades de empaque (packs, sets y unidades).
7. **Total referencial transparente:** Desglose en pesos chilenos con IVA y leyenda no vinculante.
8. **Selección sin login:** Cero fricción para el docente (sesión Django).
9. **Persistencia garantizada:** Solicitud guardada en base de datos bajo transacción segura.
10. **Snapshots inmutables:** Precios y nombres históricos congelados en cada ítem de solicitud.
11. **Administración en Django Admin:** Panel para revisión comercial de solicitudes recibidas.
12. **Emails como canal secundario:** La caída de SMTP jamás revierte una solicitud guardada.
13. **Candado de compra pública vigente:** Especificaciones en `NO_REVISADO` siguen bloqueadas para licitaciones.
14. **Productos no autorizados bloqueados:** Cero exposición accidental de los 857 productos restantes.
15. **Suite de pruebas pasando:** 100% de tests unitarios e integrados pasando sin errores.
16. **Rendimiento móvil verificado:** Navegación fluida y responsiva en smartphones y tablets.
17. **Despliegue verificado en producción:** Operativo en [https://educompra.humm.cl](https://educompra.humm.cl).

---

## 8. Próximos Pasos y Punto de Control

> [!IMPORTANT]
> **ESTADO ACTUAL: DETENIDO EN PUNTO DE CONTROL**
> * No se ha implementado código de la Fase 4.
> * El catálogo maestro permanece en su estado seguro de Fase 3 (`publicado = False` en los 929 registros).
> * Quedo a la espera de la revisión, observaciones o aprobación del presente plan por parte del Equipo Directivo de Humm antes de iniciar la construcción.
