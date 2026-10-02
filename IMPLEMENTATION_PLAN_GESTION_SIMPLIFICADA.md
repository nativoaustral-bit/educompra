# PLAN DE IMPLEMENTACIÓN — SIMPLIFICACIÓN DE GESTIÓN EDUCOMPRA HUMM
## Plataforma de Administración Operativa (`/gestion/`)

**Fecha de Elaboración:** 1 de Octubre de 2026  
**Fase de Desarrollo:** Mantenimiento y Evolución — Post Fase 5A  
**Responsable Técnico:** Antigravity (Google DeepMind)  
**Estado:** **PROPUESTA TÉCNICA FINAL — EN ESPERA DE REVISIÓN Y APROBACIÓN DE HUMM**  
**Punto de Control:** **DETENCIÓN OBLIGATORIA (Cero escrituras en producción previo a confirmación)**

---

## 1. Contexto y Estado Base de Producción

EduCompra opera actualmente sobre una base de datos consolidada, validada y blindada:

* **Catálogo Maestro:** **960 SKU únicos** Keyestudio (blindado mediante `UniqueConstraint(proveedor, sku_proveedor)`).
* **Productos Activos en Sistema:** **958 productos** disponibles para curaduría y selección.
* **Productos en Cuarentena:** **2 productos** (`KS0240` y `60720227`), aislados con `activo=False` y `costo=0.00`.
* **Catálogo Público en Tienda:** **77 productos publicados** (expuestos en [educompra.humm.cl/catalogo/](https://educompra.humm.cl/catalogo/)).
* **Productos no Publicados (Maestro):** **883 productos** en resguardo operativo (`publicado=False`).
* **Curaduría Pedagógica `VALIDADO`:** **88 productos** validados técnicamente por Humm.
* **Tramos de Volumen Mayorista:** **150 productos** con 597 tramos en `PrecioProveedorTramo` (1 anomalía monitoreada en `KS5012`).

### Principio Fundamental
> **Estar en el maestro NO significa estar publicado.**  
> El Catálogo Maestro comprende los 960 SKU conocidos del proveedor. El Catálogo Público comprende exclusivamente aquellos productos que Humm decida evaluar, curar y publicar formalmente para los colegios.

---

## 2. Objetivos y Flujos Operacionales Principales

La simplificación de `/gestion/` busca que un administrador de Humm trabaje de forma ágil sobre 960 productos sin requerir conocimientos técnicos ni navegar individualmente ficha por ficha:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                                 FLUJO DE CATÁLOGO                                      │
│                                                                                        │
│   [Catálogo Maestro] ──> [Selección SKU] ──> [CANDIDATO] ──> [Curaduría] ──> [Gate]    │
│       (960 SKU)          (Pegar lista)       (Bolsa de        (Borrador o     (8 reqs) │
│                                                Trabajo)         Validar)         │     │
│                                                                                  │     │
│                                                                                  ▼     │
│                                                         [PUBLICADO EN TIENDA]          │
│                                                            (Catálogo Público)          │
└────────────────────────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────────────────────────┐
│                                 FLUJO DE PRICING                                       │
│                                                                                        │
│   [Parámetros Pricing] ──> [Ajuste Recargo] ──> [SIMULACIÓN] ──> [Confirmar] ──>       │
│    (TC, Flete, Recargo)    (Global/Categoría/   (Comparativa de  (Recálculo    [Nuevos │
│                              Selección)          Precios CLP)     Central)      Precios]│
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Principio de Reutilización de Arquitectura (Cero Migraciones)

En estricto cumplimiento del requerimiento #43, **no se crearán nuevos modelos ni se alterará el esquema de base de datos**. El diseño se apoya al 100% en las estructuras existentes:

| Estructura Existente | Uso en la Nueva Gestión Simplificada |
| :--- | :--- |
| **`Producto.estado_curaduria`** | Utiliza los estados ya modelados: `SIN_REVISAR`, `CANDIDATO`, `EN_CURADURIA`, `VALIDADO`, `LISTO_PARA_PUBLICAR`, `DESCARTADO_CATALOGO_PUBLICO`. |
| **`Producto.porcentaje_recargo`** | Permite recargos específicos por producto o por selección sin alterar el recargo general. |
| **`Producto.calcular_precios_sugeridos()`** | Fuente **única e inalterada** de cálculo de costos CLP, precios netos y totales. |
| **`ProductoPublicationService`** | Validador del **Gate de Calidad de 8 puntos** y ejecutor atómico de publicación/despublicación con auditoría. |
| **`ConfiguracionPricing`** | Administrador central de tipo de cambio, flete/internación, recargo comercial general e IVA. |
| **`PrecioProveedorTramo`** | Repositorio de escalas mayoristas de proveedor y control de anomalías (`es_anomalo=True`). |
| **`registrar_actividad()`** | Logger de auditoría para trazabilidad de usuario, fecha, productos afectados y variaciones. |
| **Permisos Nativos Django** | `gestion.can_manage_catalogo` (catálogo y pricing) y `gestion.can_publish_producto` (publicación). |

**Migraciones requeridas:** **0 (Cero).**

---

## 4. Mapa de Rutas y Módulos URL Propuestos

Se mantendrán y extenderán las URLs de `apps/gestion/` sin romper las vistas existentes:

```python
# apps/gestion/urls.py

# 1. Catálogo y Selección
path("productos/", productos.productos_lista_view, name="productos_lista"),
path("productos/seleccion-sku/", productos_seleccion.seleccion_sku_view, name="productos_seleccion_sku"),
path("productos/candidatos/", productos.productos_candidatos_view, name="productos_candidatos"),

# 2. Curaduría por Lote
path("productos/curaduria-lote/", productos_curaduria.curaduria_lote_view, name="productos_curaduria_lote"),
path("productos/curaduria-masiva-campos/", productos_curaduria.curaduria_masiva_campos_view, name="productos_curaduria_masiva_campos"),

# 3. Publicación y Despublicación por Lote
path("productos/publicacion-lote/", productos_publicacion.publicacion_lote_view, name="productos_publicacion_lote"),
path("productos/despublicacion-lote/", productos_publicacion.despublicacion_lote_view, name="productos_despublicacion_lote"),

# 4. Módulo de Precios y Simulador
path("precios/", precios.precios_dashboard_view, name="precios_dashboard"),
path("precios/simular-global/", precios.precios_simular_global_view, name="precios_simular_global"),
path("precios/aplicar-global/", precios.precios_aplicar_global_view, name="precios_aplicar_global"),
path("precios/ajuste-seleccion/", precios.precios_ajuste_seleccion_view, name="precios_ajuste_seleccion"),
```

---

## 5. Diseño Detallado por Bloques de Implementación

### BLOQUE A — Vista Principal Simplificada y Dashboard de Productos
**Ubicación:** `apps/gestion/views/productos.py` y `templates/gestion/productos/lista.html`

1. **Header Métrico Dinámico (7 Tarjetas Compactas):**
   * **Maestro:** `960`
   * **Publicados:** Dinámico (actualmente 77)
   * **Candidatos:** Dinámico (estado `CANDIDATO`)
   * **Validados no publicados:** Dinámico (`VALIDADO` + `publicado=False`)
   * **Sin revisar:** Dinámico (`SIN_REVISAR`)
   * **Sin imagen:** Dinámico (`imagenes__count=0`)
   * **Cuarentena:** `2` (badge distintivo de advertencia)
2. **Barra de Herramientas Principal:**
   * **Buscador Multicriterio:** Consulta unificada e instantánea sobre `sku_proveedor`, `sku_humm`, `nombre_comercial`, `nombre_original_proveedor`, `marca` y `modelo`.
   * **Pestañas Rápidas de Universo:**
     * `[Todos (Maestro 960)]`
     * `[Publicados en Tienda (77)]`
     * `[Candidatos a Catálogo (XX)]`
     * `[Validados Pendientes (XX)]`
     * `[Cuarentena (2)]`
   * **Filtros Laterales/Desplegables:**
     * Curaduría: *Sin revisar, Candidato, En curaduría, Validado, Listo para publicar, Descartado*.
     * Imagen: *Con imagen, Sin imagen*.
     * Categoría Humm, Proveedor, Tecnología compatible.
3. **Tabla Compacta Operacional:**
   * Columnas: `[Checkbox]` | `[Miniatura]` | `[SKU Proveedor / Humm]` | `[Nombre]` | `[Categoría]` | `[Costo USD]` | `[Precio Referencial CLP]` | `[Curaduría]` | `[Publicado]` | `[Acciones Rápidas]`.
   * Filas densas aptas para notebooks y tablets.
   * Botonera fija de acciones sobre seleccionados:
     * *Marcar como Candidatos*
     * *Curar Selección por Lote*
     * *Verificar Gate para Publicar*
     * *Ajustar Recargo de Selección*

---

### BLOQUE B — Motor de Selección Masiva por SKU
**Ubicación:** `apps/gestion/views/productos_seleccion.py` y `templates/gestion/productos/seleccion_sku.html`

1. **Entrada de Datos Flexible:**
   * Área de texto grande (`<textarea>`) donde el administrador puede pegar hasta 500 SKUs directamente desde correos, hojas de cálculo o minutas.
   * Parser robusto que tolera:
     * Un SKU por línea (`\n`, `\r\n`).
     * Separación por comas (`,`) o punto y coma (`;`).
     * Tabulaciones y espacios accidentales (`KS0540 `, `  ks0078`).
   * Normalización automática: mayúsculas (`upper()`), eliminación de espacios y deduplicación conservando el orden de ingreso.
2. **Análisis Previo sin Modificaciones (Fase de Inspección):**
   * El sistema procesa la lista contra el Catálogo Maestro y genera un informe instantáneo:
     * Total SKUs ingresados.
     * SKUs encontrados en maestro.
     * SKUs inexistentes (con listado explícito de advertencia).
     * Ya publicados (no requieren acción).
     * Ya validados pero no publicados (listos para publicar).
     * Candidatos existentes.
     * Sin revisar (aptos para ser candidatos).
     * En cuarentena (`KS0240`, `60720227` bloqueados con advertencia visual).
     * Sin fotografía asociada.
3. **Tabla de Previsualización:**
   * Lista detallada de cada SKU con badge de estado, fotografía, precio referencial actual y diagnóstico.
4. **Acción Segura "Marcar Selección como Candidatos":**
   * Aplica cambio de estado **únicamente** a los productos elegibles (`SIN_REVISAR → CANDIDATO`).
   * **Exclusiones estrictas:** No altera productos ya `VALIDADO`, ya `publicado=True`, `DESCARTADO_CATALOGO_PUBLICO`, ni registros en cuarentena (`activo=False`).
   * **Auditoría:** Registra la acción `MARCAR_CANDIDATOS_MASIVO` con el detalle de los SKUs afectados.
   * **Regla de oro:** Esta acción **NO publica ningún producto**.

---

### BLOQUE C — Flujo de Curaduría de Candidatos y Curaduría por Lote
**Ubicación:** `apps/gestion/views/productos_curaduria.py` y `templates/gestion/productos/curaduria_lote.html`

1. **Vista de Trabajo Focalizada (`/gestion/productos/candidatos/`):**
   * Vista filtrada que aísla los productos en estado `CANDIDATO` o `EN_CURADURIA`, evitando que el equipo se pierda entre los 960 registros del maestro.
2. **Interfaz de Curaduría Asistida Consecutiva:**
   * Panel dividido en dos columnas:
     * **Evidencia del Fabricante:** Miniatura HD, SKU, nombre original en inglés, características técnicas originales (`features_proveedor`), costo USD, tramos mayoristas.
     * **Formulario de Curaduría Pedagógica Humm:**
       * Nombre comercial amigable en español.
       * Categoría sugerida (selector).
       * Nivel de dificultad (Inicial, Intermedio, Avanzado).
       * Tecnologías compatibles (Arduino, ESP32, micro:bit, etc.).
       * Descripción pedagógica para el profesor (qué es y qué incluye).
       * Uso educativo sugerido (proyectos de aula STEM).
       * Advertencia de uso/seguridad.
3. **Sugerencias Asistidas Automáticas (Borrador):**
   * El sistema propone automáticamente borradores basados en la traducción técnica del catálogo Keyestudio (ej: *"Kit Básico..."*, nivel *"INICIAL"* si contiene *"Starter"*, etc.).
   * **Control ético:** Las sugerencias se rotulan explícitamente como `[PROPUESTA SISTEMA — REQUIERE REVISIÓN HUMANA]`. Ningún producto pasa a `VALIDADO` de forma automática.
4. **Acciones Rápidas por Producto:**
   * **[Guardar Borrador]:** Pasa a `estado_curaduria='EN_CURADURIA'`.
   * **[Validar Pedagógicamente]:** Pasa a `estado_curaduria='VALIDADO'` (habilita el producto para el Gate de Publicación).
   * **[Descartar de Catálogo Público]:** Pasa a `estado_curaduria='DESCARTADO_CATALOGO_PUBLICO'`.
     * *Garantía:* Permanece intacto en el maestro con sus costos e imágenes; simplemente sale de la cola de trabajo de curaduría.
5. **Curaduría Masiva de Atributos Comunes (Sin tocar textos diferenciados):**
   * Permite seleccionar 10 o 20 productos y aplicarles masivamente solo campos generales: categoría, nivel, tecnologías, unidad de medida, disponibilidad o días de entrega.
   * **Prohibición estricta (#13):** La interfaz bloquea explícitamente la edición masiva de nombres comerciales, descripciones, usos educativos, advertencias y especificaciones técnicas neutras.

---

### BLOQUE D — Publicación y Despublicación por Lote con Gate de Calidad
**Ubicación:** `apps/gestion/views/productos_publicacion.py` y `templates/gestion/productos/publicacion_lote.html`

1. **Selección Flexible de Publicación:**
   * Permite enviar a publicación por lote productos seleccionados desde: lista principal, vista de candidatos, vista de validados o mediante pegado de lista SKU.
2. **Evaluación Estricta del Gate de Publicación:**
   * El servicio ejecuta individualmente `ProductoPublicationService.validar_para_publicacion(producto)` sobre cada producto seleccionado, evaluando los 8 puntos de control:
     1. `activo == True`
     2. `estado_curaduria == 'VALIDADO'`
     3. `nombre_comercial` presente
     4. `categoria` válida y activa (distinta de "Sin clasificar")
     5. `descripcion_educativa` con contenido pedagógico ($\ge 15$ caracteres)
     6. Al menos una imagen optimizada vinculada
     7. `precio_sugerido_total_clp > 0`
     8. `unidad_compra` definida
3. **Previsualización de Aptitud (Semáforo Operacional):**
   * **Grupo LISTOS:** Productos 100% conformes que se publicarán al presionar el botón.
   * **Grupo BLOQUEADOS:** Productos no conformes, mostrando en rojo el motivo exacto (ej: *"Falta fotografía"*, *"Categoría es Sin clasificar"*, *"Curaduría aún en borrador"*).
   * **Regla de resiliencia (#16):** Los productos bloqueados no detienen la publicación de los productos aptos.
4. **Ejecución y Confirmación Atómica:**
   * Botón claro: `[PUBLICAR X PRODUCTOS APTOS]`.
   * Ejecuta en bucle individual:
     ```python
     for prod in productos_aptos:
         ProductoPublicationService.publicar(prod, usuario=request.user, request=request)
     ```
   * **Prohibido:** `Producto.objects.filter(...).update(publicado=True)`.
   * Al finalizar informa: `X publicados exitosamente`, `Y permanecen no publicados`.
5. **Despublicación Masiva Controlada:**
   * Vista de retiro de catálogo con advertencia explícita:
     > *"Esta acción retirará X productos de la tienda pública, pero NO los eliminará del catálogo maestro. Toda su información histórica permanecerá intacta."*
   * Ejecuta individualmente `ProductoPublicationService.despublicar(prod, usuario=request.user, request=request, motivo=motivo)`.

---

### BLOQUE E — Módulo de Precios y Simulador de Recargos Comerciales
**Ubicación:** `apps/gestion/views/precios.py` y `templates/gestion/precios/dashboard.html`

1. **Nomenclatura Comercial Precisa (#20):**
   * En toda la interfaz se utilizará exclusivamente el término **RECARGO COMERCIAL** (nunca "margen" ni "rentabilidad"), dado que la fórmula vigente es:
     $$\text{Precio Neto CLP} = \text{Costo Puesto Chile CLP} \times (1 + \text{Recargo Comercial})$$
     $$\text{Precio Total CLP} = \text{Precio Neto CLP} \times 1.19 \quad (\text{IVA incluido})$$
2. **Visualización de Parámetros Vigentes (`ConfiguracionPricing`):**
   * **Tipo de Cambio:** ej: `$950 CLP/USD`.
   * **Internación y Flete:** ej: `15%`.
   * **Recargo Comercial General:** ej: `80%`.
   * **IVA:** `19%`.
3. **Simulador de Impacto Financiero Previo (#21, #22):**
   * Permite al usuario modificar temporalmente parámetros (ej: probar qué ocurre si el Recargo General baja de 80% a 65%, o si el TC sube a $980).
   * **Cero escrituras durante la simulación:** Se ejecuta en memoria instanciando objetos temporales.
   * **Métricas de la Simulación:**
     * Total de productos afectados en catálogo maestro.
     * Total de productos públicos afectados en tienda.
     * Precio promedio referencial antes vs. después.
     * Variación porcentual promedio.
     * Tabla comparativa con 10 productos emblemáticos de muestra (Kit Arduino, Smart Home ESP32, Sensores, etc.).
4. **Confirmación y Recálculo Centralizado (#23):**
   * Tras la simulación, el botón `[APLICAR CAMBIO DE PRECIOS]` requiere confirmación modal.
   * El recálculo delega estrictamente en la lógica del modelo:
     ```python
     for prod in productos_a_recalcular:
         prod.calcular_precios_sugeridos(config=nueva_config)
         prod.save(update_fields=["costo_puesto_chile_clp", "precio_sugerido_neto_clp", "precio_sugerido_total_clp", "updated_at"])
     ```
   * **Snapshots de cotizaciones:** No se tocan las cotizaciones históricas emitidas en `apps/cotizaciones`.
5. **Gestión de Recargos Específicos por Producto / Selección (#24, #25, #26):**
   * **Respeto a excepciones:** Los productos con `porcentaje_recargo` específico (diferente de None) no reciben el recargo general a menos que el usuario marque explícitamente *"Sobrescribir recargos específicos"*.
   * **Ajuste por Selección o Categoría:**
     * Permite fijar un recargo específico (ej: 60%) para todos los kits de una categoría o una lista de SKUs seleccionados.
     * Permite *"Restablecer al Recargo General"* (pone `porcentaje_recargo = None` y recalcula con la tasa general).
6. **Evidencia de Costos de Proveedor por Volumen y Anomalías (#28, #29):**
   * Los tramos Q1-9, Q10-49, Q50-100, Q101-300 se exhiben como referencia de abastecimiento, sin afectar el precio sugerido unitario general (que usa Q1-9).
   * Si un tramo tiene `es_anomalo=True` (ej: `KS5012`), se muestra con badge de advertencia `[PRECIO PROVEEDOR REQUIERE REVISIÓN]` y queda bloqueado para cotizaciones por volumen.

---

### BLOQUE F — Auditoría, Permisos y Seguridad Operacional
**Ubicación:** `apps/gestion/services_auditoria.py` y `apps/gestion/decorators.py`

1. **Matriz de Permisos de Gestión:**
   * `@permiso_requerido("gestion.can_manage_catalogo")`: Requerido para ver catálogo maestro, seleccionar candidatos, editar curaduría, clasificar y acceder al módulo de precios.
   * `@permiso_requerido("gestion.can_publish_producto")`: Requerido exclusivamente para ejecutar publicación y despublicación en lote o individual.
2. **Eventos de Auditoría Registrados (`registrar_actividad`):**
   * `MARCAR_CANDIDATOS_MASIVO`: Lista de SKUs seleccionados y total procesado.
   * `CURADURIA_VALIDADA`: SKU, cambios pedagógicos efectuados y usuario responsable.
   * `DESCARTAR_PRODUCTO_PUBLICO`: SKU y justificación interna.
   * `PUBLICAR_LOTE_PRODUCTOS`: Total enviados, publicados y bloqueados.
   * `DESPUBLICAR_LOTE_PRODUCTOS`: Total retirados de catálogo público y motivo.
   * `MODIFICAR_PRICING_GLOBAL`: Parámetros modificados y productos recalculados.
   * `AJUSTAR_RECARGO_ESPECIFICO_SELECCION`: SKUs afectados y tasa aplicada.
3. **Blindaje de Cuarentena Permanente (#33):**
   * Los registros `KS0240` y `60720227` están protegidos a nivel de vista y servicio:
     * Excluidos de cualquier selección masiva de candidatos.
     * Excluidos de la curaduría por lote.
     * Excluidos del gate de publicación (bloqueo por `activo=False`).
     * Excluidos de simulaciones de precios (costo USD = 0).
     * Señalizados con badge permanente: `[CUARENTENA — PENDIENTE PROVEEDOR]`.

---

## 6. Plan de Pruebas Automatizadas (Test Matrix)

Se implementará una suite exhaustiva en `apps/gestion/tests/test_gestion_simplificada.py` con cobertura completa:

```
apps/gestion/tests/test_gestion_simplificada.py
├── TestSeleccionMasivaSKU
│   ├── test_parser_normaliza_mayusculas_y_espacios()
│   ├── test_parser_elimina_duplicados_respetando_orden()
│   ├── test_diagnostico_detecta_skus_inexistentes()
│   ├── test_diagnostico_detecta_productos_en_cuarentena()
│   ├── test_marcar_candidatos_solo_afecta_sin_revisar()
│   └── test_marcar_candidatos_no_altera_publicados_ni_validados()
├── TestCuraduriaLote
│   ├── test_curaduria_asistida_propone_borrador_sin_auto_validar()
│   ├── test_descarte_de_catalogo_preserva_maestro_y_costos()
│   ├── test_curaduria_masiva_campos_comunes_preserva_textos_diferenciados()
│   └── test_bloqueo_edicion_masiva_de_descripcion_y_nombre()
├── TestPublicacionLote
│   ├── test_publicacion_lote_con_todos_aptos()
│   ├── test_publicacion_lote_parcial_publica_aptos_y_retiene_bloqueados()
│   ├── test_bloqueo_producto_sin_imagen()
│   ├── test_bloqueo_producto_sin_descripcion_o_categoria_sin_clasificar()
│   ├── test_bloqueo_producto_en_cuarentena_o_inactivo()
│   └── test_despublicacion_lote_preserva_historial_y_snapshots()
└── TestPreciosYSimulador
    ├── test_simulacion_precios_no_escribe_en_base_de_datos()
    ├── test_recalculo_global_actualiza_precios_sugeridos_correctamente()
    ├── test_recargo_especifico_prevalece_sobre_recargo_general()
    ├── test_ajuste_recargo_por_seleccion_y_reversion_a_general()
    ├── test_anomalia_ks5012_aislada_de_calculos_comerciales()
    └── test_snapshots_cotizaciones_historicas_intactos()
```

---

## 7. Matriz de Riesgos y Mitigaciones Operacionales

| Riesgo Identificado | Nivel | Mitigación Técnica en la Arquitectura |
| :--- | :---: | :--- |
| **Publicación accidental de productos incompletos** | Crítico | Validación obligatoria de los 8 requisitos por `ProductoPublicationService`. Imposibilidad técnica de publicar sin imagen, sin curaduría o con categoría inválida. |
| **Sobrescritura masiva de descripciones pedagógicas curadas** | Alto | Bloqueo estricto a nivel de vista y template: la curaduría masiva solo admite campos comunes (categoría, nivel, disponibilidad). Textos diferenciados son siempre individuales. |
| **Pérdida de recargos específicos en recálculo global** | Medio | Lógica que verifica `if prod.porcentaje_recargo is not None:` y omite el recargo general, salvo orden explícita del usuario. |
| **Contaminación de cotizaciones históricas emitidas** | Crítico | Las solicitudes y cotizaciones almacenan snapshots desacoplados en `DetalleSolicitudCotizacion`. `Producto.calcular_precios_sugeridos()` solo actualiza precios referenciales futuros. |
| **Acciones sobre productos en cuarentena** | Alto | Filtro explícito en queries (`exclude(sku_proveedor__in=['KS0240', '60720227'])`) en todas las operaciones masivas de selección, curaduría y pricing. |
| **Tiempo de respuesta en recálculo de 960 productos** | Bajo | La operación sobre SQLite con 960 registros tarda menos de 0.8 segundos en transacción atómica (`update_fields`). Se ejecuta con barra de progreso y feedback visual. |

---

## 8. Estrategia de Despliegue y Verificación en Servidor

1. **Ambiente Local:**
   * Ejecución de suite de tests completa (`python manage.py test`).
   * Verificación de catálogo inalterado: `python manage.py verificar_estado_catalogo_produccion --assert-960`.
2. **Commit y Versionamiento Git:**
   * Archivos nuevos empaquetados en Git respetando `.gitignore` (cero bases de datos ni archivos multimedia en commits).
3. **Pipeline CI/CD HostGator:**
   * Ejecución automática de GitHub Actions vía SCP limpio (`deploy.yml`).
   * Verificación post-deploy: `verificar_estado_catalogo_produccion --assert-960` confirma que el catálogo público permanece exactamente en **77 productos**.

---

## 9. Cronograma de Construcción Propuesto

Una vez aprobada esta propuesta por Humm, el desarrollo se ejecutará en los 6 bloques secuenciales:

| Bloque | Componentes a Implementar | Tiempo Estimado | Entregable |
| :---: | :--- | :---: | :--- |
| **Bloque A** | Rediseño visual de `/gestion/productos/`, tarjetas dinámicas y tabla densa | 2 h | Vistas y templates de lista optimizados |
| **Bloque B** | Vista `/gestion/productos/seleccion-sku/`, parser y diagnóstico | 2 h | Motor de pegado y selección por SKU |
| **Bloque C** | Vista `/gestion/productos/candidatos/` y curaduría consecutiva/lote | 3 h | Interfaz de curaduría asistida |
| **Bloque D** | Vistas de publicación y despublicación por lote con semáforo de gate | 2 h | Motor de publicación masiva segura |
| **Bloque E** | Módulo `/gestion/precios/`, simulador y recálculo con recargos específicos | 3 h | Simulador financiero y pricing masivo |
| **Bloque F** | Tests automatizados, registro de auditoría y verificación general | 2 h | Suite de tests passing (85+ tests) |

---

## 10. Punto de Control y Detención Obligatoria

> [!IMPORTANT]
> **ESTADO ACTUAL: DETENIDO.**  
> En cumplimiento estricto del requerimiento #44 de la instrucción de Humm:
> * **NO se ha modificado ninguna vista productiva.**
> * **NO se ha ejecutado ninguna migración.**
> * **NO se ha alterado ningún dato en la base de datos.**
> * **Se espera la revisión, comentarios y autorización explícita de Humm sobre este Implementation Plan antes de iniciar la construcción del código.**
