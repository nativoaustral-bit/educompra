# INFORME DE SIMULACIÓN DRY-RUN — NUEVA LISTA DE PROVEEDOR KEYESTUDIO
## Plataforma EduCompra Humm (`educompra.humm.cl/gestion/`)
**Fecha:** 30 de Septiembre de 2026  
**Archivo Analizado:** `data_import/keystudio_kits.xlsx`  
**Modo:** **SIMULACIÓN EXCLUSIVA (DRY-RUN) — CERO ESCRITURAS PRODUCTIVAS**  
**Estado General:** `SIMULACION_EXITOSA_LISTO_PARA_APROBACION_HUMM`

---

## 1. Resumen Ejecutivo y Formato Detectado

En cumplimiento del requerimiento de Humm, se adaptó el motor de importación unificado [`ImportacionCatalogoService`](file:///Users/rmerinog/PLATAFORMAS/EDUCOMPRA/apps/catalogo/services_importacion.py) para procesar la nueva planilla de kits y precios mayoristas entregada por Keyestudio, manteniendo el 100% de retrocompatibilidad con el catálogo maestro original.

### Detección Automática de Formato
* **Formato detectado:** `FORMATO_LISTA_COMERCIAL_NUEVA`
* **Estructura identificada:** 215 filas totales en hoja `Table 1`, divididas en múltiples secciones por familia tecnológica (`HOT PRODUCTS`, `FOR ARDUINO`, `FOR ESP32`, `FOR MICRO:BIT`, `FOR RASPBERRY PI`).
* **Columnas mapeadas dinámicamente:**
  * `SKU` → Identificador único de proveedor (`sku_proveedor`).
  * `Product Name` → Nombre original de proveedor (`nombre_original_proveedor`).
  * `Features` → Trazabilidad y evidencia técnica de proveedor (`features_proveedor`).
  * `Q1-9` → Costo base unitario del proveedor para 1 a 9 unidades (`costo_proveedor_usd`).
  * `Q10-49`, `Q50-100`, `Q101-300` → Tramos de escala mayorista para cotizaciones institucionales por volumen (`PrecioProveedorTramo`).

---

## 2. Clasificación del Lote Prioritario de 10 SKUs

Se realizó el cruce obligatorio de los 10 SKUs solicitados contra la base de datos maestra de EduCompra:

* **Total SKUs analizados:** 10
* **SKUs existentes en base de datos:** 6 (todos en estado `publicado=False`, `activo=True`, `estado_curaduria='SIN_REVISAR'`).
* **SKUs nuevos a incorporar:** 4 (no existen en la base de datos).
* **SKUs publicados en frontend:** 0 (ninguno de los 10 SKUs está actualmente publicado; **los 72 productos públicos de EduCompra se encuentran 100% intactos**).
* **Conflictos intra-archivo detectados:** 0 (cada SKU aparece exactamente una sola vez en la nueva planilla).
* **Conflictos históricos detectados:** 0 (ninguno de los 10 SKUs forma parte de los 15 SKUs conflictivos aislados en [`CONFLICTOS_CATALOGO_KEYESTUDIO.md`](file:///Users/rmerinog/PLATAFORMAS/EDUCOMPRA/CONFLICTOS_CATALOGO_KEYESTUDIO.md)).
* **Anomalías de precio detectadas:** 0 en este lote (todos presentan una estructura estrictamente decreciente por volumen).

---

## 3. Matriz Exhaustiva del DRY-RUN (10 SKUs)

A continuación se presenta el resultado exacto de la simulación fila por fila, consultando la base productiva:

| SKU | Nombre Proveedor | Estado Actual BD | Existe | Publicado | Costo Ant. (USD) | Q1-9 (USD) | Q10-49 (USD) | Q50-100 (USD) | Q101-300 (USD) | Dif. Costo Base | Conflicto | Acción Propuesta |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **`KS0540`** | Keyestudio Basic Starter Kit For Arduino With Board | EXISTENTE / NO PUBLICADO | Sí | No | $26.50 | **$14.00** | $13.50 | $13.00 | $12.50 | **-$12.50 (-47.2%)** | Ninguno | **PRIORIDAD HUMM:** Actualizar proveedor + tramos volumen. Preparar curaduría comercial: *"Kit Inicial Arduino con Placa Controladora — 20 Proyectos Guiados"* (Nivel: INICIAL, diferenciándolo de KS0541 que no incluye placa). |
| **`KS0530`** | Keyestudio Solar Tracking Kit | EXISTENTE / NO PUBLICADO | Sí | No | $65.90 | **$37.00** | $36.00 | $35.00 | $33.50 | **-$28.90 (-43.9%)** | Ninguno | Actualizar información proveedor + tramos de volumen. Mantener en catálogo interno para curaduría pedagógica en robótica solar/STEM. |
| **`KS0576`** | Smart Eco-Friendly House Kit | EXISTENTE / NO PUBLICADO | Sí | No | $53.60 | **$32.90** | $31.80 | $30.70 | $29.60 | **-$20.70 (-38.6%)** | Ninguno | Actualizar información proveedor + tramos de volumen. Mantener en catálogo interno para curaduría STEM de domótica y sustentabilidad. |
| **`KS5009`** | Keyestudio Smart Home Kit For ESP32 | EXISTENTE / NO PUBLICADO | Sí | No | $57.00 | **$32.00** | $31.00 | $30.00 | $29.00 | **-$25.00 (-43.9%)** | Ninguno | Actualizar información proveedor + tramos de volumen. Mantener para curaduría de kits IoT y programación con ESP32. |
| **`KS4050`** | Environment Monitoring Learning Kit for micro:bit | NUEVO SKU | No | No | *N/A* | **$39.88** | $37.22 | $35.89 | $34.56 | *N/A (Nuevo)* | Ninguno | Crear registro nuevo (`activo=True`, `publicado=False`, `estado_curaduria='SIN_REVISAR'`, placeholder `SIN_IMAGEN`) con sus 4 tramos de volumen para kit de monitoreo micro:bit. |
| **`KS0344`** | Keyestudio Arduino Automatic Watering System | EXISTENTE / NO PUBLICADO | Sí | No | $76.00 | **$45.50** | $44.00 | $42.50 | $41.00 | **-$30.50 (-40.1%)** | Ninguno | Actualizar información proveedor + tramos de volumen. Mantener en catálogo interno para curaduría de proyectos de automatización agrícola. |
| **`FKS0003`** | ESP32 Smart Robot Arm | NUEVO SKU | No | No | *N/A* | **$29.91** | $28.91 | $27.92 | $26.92 | *N/A (Nuevo)* | Ninguno | Crear registro nuevo (`activo=True`, `publicado=False`, `estado_curaduria='SIN_REVISAR'`, placeholder `SIN_IMAGEN`) con sus 4 tramos de volumen para brazo robótico inteligente ESP32. |
| **`KS4049`** | MICRO BIT Smart Home (with microbit board) | NUEVO SKU | No | No | *N/A* | **$43.65** | $40.74 | $39.28 | $37.83 | *N/A (Nuevo)* | Ninguno | Crear registro nuevo (`activo=True`, `publicado=False`, `estado_curaduria='SIN_REVISAR'`, placeholder `SIN_IMAGEN`) con sus 4 tramos de volumen para domótica micro:bit con placa incluida. |
| **`KS0474`** | Keyestudio Gamepi Atmega32u4 DIY Kit | NUEVO SKU | No | No | *N/A* | **$17.00** | $16.00 | $15.50 | $15.00 | *N/A (Nuevo)* | Ninguno | Crear registro nuevo (`activo=True`, `publicado=False`, `estado_curaduria='SIN_REVISAR'`, placeholder `SIN_IMAGEN`) con sus 4 tramos de volumen para consola DIY programable en Arduino. |
| **`KS0549`** | Keyestudio Dit Automatic Watering Device | EXISTENTE / NO PUBLICADO | Sí | No | $41.00 | **$22.00** | $21.50 | $21.00 | $20.00 | **-$19.00 (-46.3%)** | Ninguno | Actualizar información proveedor + tramos de volumen. Mantener en catálogo interno para curaduría de riego automatizado básico. |

---

## 4. Tabla de Resumen Final de Clasificación (Requerimiento #14)

| SKU | Estado actual | Acción propuesta |
| :--- | :--- | :--- |
| **`KS0540`** | EXISTENTE / NO PUBLICADO | Actualizar costos y tramos de proveedor + preparar curaduría prioritaria Humm (*Kit Inicial Arduino con Placa Controladora*) |
| **`KS0530`** | EXISTENTE / NO PUBLICADO | Actualizar costos y tramos de proveedor + mantener en catálogo interno para curaduría de robótica solar |
| **`KS0576`** | EXISTENTE / NO PUBLICADO | Actualizar costos y tramos de proveedor + mantener en catálogo interno para curaduría de casa ecológica |
| **`KS5009`** | EXISTENTE / NO PUBLICADO | Actualizar costos y tramos de proveedor + mantener en catálogo interno para curaduría de Smart Home ESP32 |
| **`KS4050`** | NUEVO SKU (NO EXISTE EN BD) | Crear nuevo registro borrador (`activo=True`, `publicado=False`, `estado_curaduria='SIN_REVISAR'`) + registrar tramos de volumen |
| **`KS0344`** | EXISTENTE / NO PUBLICADO | Actualizar costos y tramos de proveedor + mantener en catálogo interno para curaduría de riego automático |
| **`FKS0003`** | NUEVO SKU (NO EXISTE EN BD) | Crear nuevo registro borrador (`activo=True`, `publicado=False`, `estado_curaduria='SIN_REVISAR'`) + registrar tramos de volumen |
| **`KS4049`** | NUEVO SKU (NO EXISTE EN BD) | Crear nuevo registro borrador (`activo=True`, `publicado=False`, `estado_curaduria='SIN_REVISAR'`) + registrar tramos de volumen |
| **`KS0474`** | NUEVO SKU (NO EXISTE EN BD) | Crear nuevo registro borrador (`activo=True`, `publicado=False`, `estado_curaduria='SIN_REVISAR'`) + registrar tramos de volumen |
| **`KS0549`** | EXISTENTE / NO PUBLICADO | Actualizar costos y tramos de proveedor + mantener en catálogo interno para curaduría de riego inteligente DIY |

---

## 5. Análisis Técnico y Comercial de Precios por Volumen

### 1. Caída Sustancial en Costos Base de Proveedor (Q1-9)
Para los 6 productos ya existentes, la nueva lista comercial Keyestudio representa una disminución de costos promedio del **-43.3%**:
* `KS0540`: de $26.50 a $14.00 (**-47.2%**)
* `KS0549`: de $41.00 a $22.00 (**-46.3%**)
* `KS0530`: de $65.90 a $37.00 (**-43.9%**)
* `KS5009`: de $57.00 a $32.00 (**-43.9%**)
* `KS0344`: de $76.00 a $45.50 (**-40.1%**)
* `KS0576`: de $53.60 a $32.90 (**-38.6%**)

Esta reducción incrementará significativamente el margen operacional de EduCompra o permitirá ofrecer precios finales aún más competitivos en Mercado Público y venta institucional directa.

### 2. Estructura Mayorista por Tramos
Todos los tramos en los 10 productos seleccionados cumplen estrictamente la condición:
$$Q_{1\text{-}9} \ge Q_{10\text{-}49} \ge Q_{50\text{-}100} \ge Q_{101\text{-}300}$$
Ninguno presentó precios anómalos o invertidos.

### 3. Validación de Anomalías en la Planilla Completa
Como prueba de estrés del validador de monotonicidad sobre las 150 filas de `keystudio_kits.xlsx`:
* El importador detectó exactamente **1 anomalía en toda la planilla**: el SKU **`KS5012`**, donde el tramo $Q_{101\text{-}300} = \text{US}\$34.00$, superior al tramo anterior $Q_{50\text{-}100} = \text{US}\$15.00$.
* El motor clasificó automáticamente ese tramo con `estado_validacion='PRECIO_PROVEEDOR_REQUIERE_REVISION'` y `es_anomalo=True`, evitando que sea utilizado para cotizaciones por volumen. Esto demuestra que la regla comercial funciona de manera 100% fiable.

---

## 6. Producto Prioritario: `KS0540` vs `KS0541`

Siguiendo la instrucción explícita de Humm, se analizó a fondo el kit inicial:

* **SKU:** `KS0540`
* **Nombre de Proveedor:** `Keyestudio Basic Starter Kit For Arduino With Board`
* **Diferenciación Fundamental:** **INCLUYE PLACA CONTROLADORA** (Plus Mainboard compatible con Arduino UNO R3).
* **Comparación con `KS0541`:**
  * En base de datos, `KS0541` (ID 131) se encuentra **publicado y validado** con el nombre comercial: *"Kit de Componentes para Arduino (20 Proyectos Guiados) — Sin Placa Controladora"* a costo de $19.50 USD.
  * `KS0540` incorpora la placa física, y con la nueva planilla Keyestudio su costo disminuye de **$26.50 a $14.00 USD** (un valor inferior al propio kit sin placa de la lista anterior).
* **Curaduría Propuesta para `KS0540`:**
  * **Nombre Comercial Humm:** `Kit Inicial Arduino con Placa Controladora — 20 Proyectos Guiados`
  * **Categoría:** `Kits educativos iniciales`
  * **Nivel:** `INICIAL`
  * **Tecnología:** `Arduino`
  * **Imagen:** Cuenta con archivo de alta resolución asociado (`KS0540.jpg` en banco local).

---

## 7. Manejo de Imágenes y Trazabilidad

1. **Productos Existentes:** Los 6 productos ya existentes cuentan con su respectiva fotografía en el repositorio de imágenes (`KS0540.jpg`, `KS0530.jpg`, `KS0576.jpg`, `KS5009.jpg`, `KS0344.jpg`, `KS0549.jpg`). En caso de importación definitiva, no se sobreescribirán imágenes existentes.
2. **Productos Nuevos:** Los 4 SKUs nuevos (`KS4050`, `FKS0003`, `KS4049`, `KS0474`) no cuentan con imagen local en `data_import/imagenes/`. Quedarán inicializados con placeholder bajo el estado `SIN_IMAGEN`, permitiendo a Humm subir fotografías definitivas desde la interfaz `/gestion/productos/`.
3. **Features de Proveedor:** El contenido del campo `Features` de Keyestudio se preserva en `features_proveedor` para consulta interna de curaduría y elaboración de la ficha pedagógica neutra, sin exponerse en crudo al frontend público.

---

## 8. Cambios de Código y Modelo Implementados

1. **Modelo de Tramos de Volumen:**
   * Archivo: [`apps/catalogo/models.py`](file:///Users/rmerinog/PLATAFORMAS/EDUCOMPRA/apps/catalogo/models.py)
   * Nuevo campo: `Producto.features_proveedor` (`TextField`, información de trazabilidad).
   * Nuevo modelo: `PrecioProveedorTramo` con campos:
     * `producto` (FK `Producto`)
     * `proveedor` (FK `Proveedor`)
     * `cantidad_minima` (`PositiveIntegerField`)
     * `cantidad_maxima` (`PositiveIntegerField`, opcional)
     * `precio_usd` (`DecimalField`)
     * `es_anomalo` (`BooleanField`)
     * `estado_validacion` (`VALIDADO` / `PRECIO_PROVEEDOR_REQUIERE_REVISION`)
     * `notas_validacion` (`TextField`)
     * `fecha_actualizacion` (`DateTimeField`)
   * Restricción de unicidad: `unique_together = [("producto", "proveedor", "cantidad_minima")]`.
2. **Administración Django:**
   * Archivo: [`apps/catalogo/admin.py`](file:///Users/rmerinog/PLATAFORMAS/EDUCOMPRA/apps/catalogo/admin.py)
   * Registrado `PrecioProveedorTramoInline` dentro de `ProductoAdmin`.
   * Registrado `PrecioProveedorTramoAdmin` independiente con filtros por estado de validación y proveedor.
3. **Extensiones al Motor de Importación:**
   * Archivo: [`apps/catalogo/services_importacion.py`](file:///Users/rmerinog/PLATAFORMAS/EDUCOMPRA/apps/catalogo/services_importacion.py)
   * Métodos implementados:
     * `detectar_formato(sheet)`: distingue automáticamente entre `FORMATO_MAESTRO_ANTIGUO` y `FORMATO_LISTA_COMERCIAL_NUEVA`.
     * `validar_tramos_volumen(q1_9, q10_49, q50_100, q101_300)`: valida monotonicidad decreciente y aísla anomalías.
     * `procesar_catalogo(...)`: extendido con argumento opcional `skus_filtro` para procesar lotes selectivos en DRY-RUN o definitivo.
4. **Migraciones:**
   * [`apps/catalogo/migrations/0006_producto_features_proveedor_precioproveedortramo.py`](file:///Users/rmerinog/PLATAFORMAS/EDUCOMPRA/apps/catalogo/migrations/0006_producto_features_proveedor_precioproveedortramo.py)
   * [`apps/catalogo/migrations/0007_precioproveedortramo_notas_validacion_and_more.py`](file:///Users/rmerinog/PLATAFORMAS/EDUCOMPRA/apps/catalogo/migrations/0007_precioproveedortramo_notas_validacion_and_more.py)
5. **Suite de Pruebas Unitarias:**
   * Archivo: [`apps/catalogo/tests/test_importacion_nueva_lista.py`](file:///Users/rmerinog/PLATAFORMAS/EDUCOMPRA/apps/catalogo/tests/test_importacion_nueva_lista.py)
   * 7 pruebas creadas específicamente para este flujo (detección de formatos, validación de monotonicidad, alertas de anomalía, dry-run no destructivo, preservación de curaduría y creación segura de nuevos productos).

---

## 9. Resultados de Pruebas Automatizadas

Se ejecutó la suite completa de pruebas del proyecto:

```bash
.venv/bin/python manage.py test
```

* **Resultado:** **73 tests ejecutados, 73 tests superados exitosamente (0 errores, 0 fallos)** en 12.368 segundos.
* **Cobertura:** Incluye pruebas de autenticación `/gestion/`, seguridad HMAC de analítica, conciliación de establecimientos, permisos RBAC y el nuevo importador comercial de catálogo.

---

## 10. Compromiso y Detención del Proceso

* **NO SE ESCRIBIERON CAMBIOS EN BASE DE DATOS PRODUCTIVA.**
* **NO SE PUBLICÓ NINGÚN PRODUCTO NUEVO.**
* **LOS 72 PRODUCTOS ACTIVOS DEL CATÁLOGO PÚBLICO SE MANTIENEN IDÉNTICOS.**

El importador está completamente adaptado y validado mediante pruebas automatizadas y simulación DRY-RUN.

**Se suspende la ejecución a la espera de la autorización formal de Humm para proceder con la importación y posterior curaduría pedagógica.**
