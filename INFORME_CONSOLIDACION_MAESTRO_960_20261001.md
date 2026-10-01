# INFORME DE CONSOLIDACIÓN DE CATÁLOGO MAESTRO — 960 SKU KEYESTUDIO
## Plataforma EduCompra Humm (`educompra.humm.cl`)

**Fecha:** 1 de Octubre de 2026  
**Operación:** Mantenimiento y Evolución Fase 5A — Consolidación de Catálogo Maestro  
**Fuente Maestra:** `data_import/EduCompra_Base_Unificada_Keyestudio_20260930.xlsx` (960 SKU Únicos)  
**Lista Comercial de Kits:** `data_import/keystudio_kits.xlsx` (150 SKU con Escalas Mayoristas)  
**Catálogo Original:** `data_import/keyestudio_productos_completo.xlsx` (944 SKU Iniciales)  
**Estado General:** **CONSOLIDACIÓN EXITOSA — CATÁLOGO MAESTRO 100% CERRADO (960 SKU ÚNICOS)**

---

## 1. Resumen Ejecutivo de Métricas Clave

| Métrica | Antes de Consolidación | Después de Consolidación | Variación | Estado / Observación |
| :--- | :---: | :---: | :---: | :--- |
| **Total Productos Catálogo Maestro** | **939** | **960** | **+21** | Meta de 960 SKU únicos alcanzada exactamente |
| **SKU Únicos Keyestudio** | **939** | **960** | **+21** | 100% de unicidad validada (`sku_proveedor`) |
| **Productos Públicos en Tienda** | **77** | **77** | **0** | **Catálogo público estrictamente inalterado** |
| **Productos No Publicados (Maestro)** | **862** | **883** | **+21** | Conservados para curaduría futura de Humm |
| **Productos Activos en Sistema** | **939** | **958** | **+19** | Disponibles para curaduría pedagógica |
| **Productos en Cuarentena (Inactivos)** | **0** | **2** | **+2** | Aislados de abastecimiento (`costo=0.00`) |
| **Productos Sincronizados con Lista Nueva**| **16** | **150** | **+134** | Costos base Q1-9 actualizados y trazabilidad |
| **Productos con Tramos de Volumen** | **16** | **150** | **+134** | Escalas 1-9, 10-49, 50-100, 101-300 |
| **Total Tramos de Precios en BD** | **64** | **597** | **+533** | Tramos mayoristas persistidos y validados |
| **Anomalías de Precio Detectadas** | **0** | **1** | **+1** | Monitoreada en `KS5012` Q101-300 |
| **Duplicados (`proveedor + sku_proveedor`)**| **0** | **0** | **0** | Blindado con `UniqueConstraint` en base de datos |
| **Integridad de Base de Datos SQLite** | `ok` | `ok` | — | `PRAGMA integrity_check` verificado |
| **Batería de Pruebas Automatizadas** | 75 tests | 79 tests | +4 tests | 100% de tests pasando exitosamente |

---

## 2. Cumplimiento de Principios Fundamentales

1. **Separación de Catálogo Maestro vs. Catálogo Público:**
   * **Estar en el maestro NO significa estar publicado.**
   * Los 21 nuevos registros se incorporaron con `publicado=False`, `estado_curaduria='SIN_REVISAR'` y `estado_especificacion_neutral='NO_REVISADO'`.
   * El catálogo expuesto a los profesores se mantuvo en exactamente **77 productos públicos**.
2. **Blindaje de Unicidad en Base de Datos:**
   * Se aplicó la migración `catalogo.0008_producto_unique_proveedor_sku_proveedor`, implementando:
     ```python
     UniqueConstraint(fields=['proveedor', 'sku_proveedor'], name='unique_proveedor_sku_proveedor')
     ```
   * Impide físicamente cualquier inserción o importación accidental de SKU duplicados.
3. **No Destructividad de la Curaduría Humm:**
   * Para los 131 productos existentes sincronizados con la nueva lista comercial, se preservaron intactos: `nombre_comercial`, `descripcion_educativa`, `uso_educativo`, categorías Humm, niveles de dificultad, tecnologías compatibles, imágenes vinculadas, advertencias y especificaciones neutrales.
   * Únicamente se actualizaron campos originados en el fabricante: `nombre_original_proveedor`, `features_proveedor`, `costo_proveedor_usd` (Q1-9) y tramos de volumen.

---

## 3. Incorporación de los 6 SKU Nuevos Faltantes (Sección 4)

Productos identificados exclusivamente en la lista comercial posterior de Keyestudio que no existían en el catálogo maestro previo:

| SKU Proveedor | SKU Humm | Nombre en Planilla Proveedor | Costo Q1-9 | Q10-49 | Q50-100 | Q101-300 | Imagen Asociada | Estado Inicial |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :--- | :--- |
| **`KS0402`** | `HUMM-KEY-KS0402` | Keyestudio Basic Starter V2 (No Board)Kit For Arduino | USD $14.00 | $13.50 | $13.00 | $12.50 | *Sin imagen en banco* | `activo=True`, `publicado=False`, `SIN_REVISAR` |
| **`KS4048`** | `HUMM-KEY-KS4048` | MICRO BIT Smart Home（without microbit board） | USD $23.04 | $22.27 | $21.51 | $20.74 | *Sin imagen en banco* | `activo=True`, `publicado=False`, `SIN_REVISAR` |
| **`KS3003`** | `HUMM-KEY-KS3003` | Raspberry Pi 4b Complete Kits With Us Plug (4GB) | USD $106.00 | $102.00 | $98.50 | $95.00 | *Sin imagen en banco* | `activo=True`, `publicado=False`, `SIN_REVISAR` |
| **`KS3006`** | `HUMM-KEY-KS3006` | Raspberry Pi 4b Complete Kits With Eu Plug (4GB) | USD $106.00 | $102.00 | $98.50 | $95.00 | *Sin imagen en banco* | `activo=True`, `publicado=False`, `SIN_REVISAR` |
| **`KS3009`** | `HUMM-KEY-KS3009` | Raspberry Pi 4b Complete Kits With Uk Plug (4GB) | USD $106.00 | $102.00 | $98.50 | $95.00 | *Sin imagen en banco* | `activo=True`, `publicado=False`, `SIN_REVISAR` |
| **`KS3012`** | `HUMM-KEY-KS3012` | Raspberry Pi 4b Complete Kits With Au Plug (4GB) | USD $106.00 | $102.00 | $98.50 | $95.00 | *Sin imagen en banco* | `activo=True`, `publicado=False`, `SIN_REVISAR` |

---

## 4. Resolución de los 13 Conflictos Históricos (Sección 5)

Los 13 SKUs que habían sido excluidos preventivamente de la importación inicial debido a discrepancias en el archivo maestro original fueron resueltos utilizando las definiciones explícitas y precios unitarios de la lista comercial posterior:

| SKU Proveedor | SKU Humm | Nombre Proveedor Incorporado | Q1-9 | Q10-49 | Q50-100 | Q101-300 | Imagen Asociada | Trazabilidad Interna |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :--- | :--- |
| **`KS0077`** | `HUMM-KEY-KS0077` | Keyestudio Super Learning Kit For Arduino (No Board) | USD $24.00 | $23.00 | $22.00 | $21.00 | `KS0077.jpg` | Con nota de trazabilidad histórica |
| **`KS0078`** | `HUMM-KEY-KS0078` | New Keyestudio Super Learning Kit With UNO R3 | USD $29.00 | $28.00 | $27.00 | $26.00 | `KS0078.jpg` | Con nota de trazabilidad histórica |
| **`KS0079`** | `HUMM-KEY-KS0079` | New Keyestudio Super Learning Kit With MEGA 2560 R3 | USD $39.00 | $37.50 | $36.00 | $35.00 | `KS0079.jpg` | Con nota de trazabilidad histórica |
| **`KS0080`** | `HUMM-KEY-KS0080` | Keyestudio Maker Learning Kit For Arduino (No Board) | USD $23.00 | $22.00 | $21.00 | $20.00 | `KS0080.jpg` | Con nota de trazabilidad histórica |
| **`KS0081`** | `HUMM-KEY-KS0081` | Keyestudio Maker Learning Kit For Arduino With UNO R3 | USD $29.00 | $28.00 | $27.00 | $26.00 | `KS0081.jpg` | Con nota de trazabilidad histórica |
| **`KS0082`** | `HUMM-KEY-KS0082` | Keyestudio Maker Learning Kit With MEGA 2560 R3 | USD $39.00 | $37.50 | $36.00 | $35.00 | `KS0082.jpg` | Con nota de trazabilidad histórica |
| **`KS0400`** | `HUMM-KEY-KS0400` | New Sensor Starter V2.0 Kit With UNO R3 37 In 1 | USD $37.50 | $36.50 | $35.00 | $34.00 | `KS0400.jpg` | Con nota de trazabilidad histórica |
| **`KS0401`** | `HUMM-KEY-KS0401` | New Sensor Starter V2.0 Kit With MEGA 2560 R3 37 In 1 | USD $49.60 | $48.00 | $46.50 | $44.80 | `KS0401.jpg` | Con nota de trazabilidad histórica |
| **`KS0536`** | `HUMM-KEY-KS0536` | Keyestudio Ultimate Starter Kit (Includes Plus Board) | USD $31.00 | $30.00 | $29.00 | $28.00 | `KS0536.jpg` | Con nota de trazabilidad histórica |
| **`KS0537`** | `HUMM-KEY-KS0537` | Keyestudio Ultimate Starter Kit (No Plus Board) | USD $26.00 | $25.00 | $24.00 | $23.00 | `KS0537.jpg` | Con nota de trazabilidad histórica |
| **`KS0801`** | `HUMM-KEY-KS0801` | Stem Programming Diybutton Piano Learning Kit | USD $13.70 | $13.20 | $12.80 | $12.30 | `KS0801.jpg` | Con nota de trazabilidad histórica |
| **`KS4031`** | `HUMM-KEY-KS4031` | Keyestudio 4wd Mecanum Robot Car With Microbit Board | USD $50.00 | $49.00 | $48.00 | $47.00 | `KS4031.jpg` | Con nota de trazabilidad histórica |
| **`KS4032`** | `HUMM-KEY-KS4032` | Keyestudio 4wd Mecanum Robot Car Without Microbit Board| USD $34.00 | $33.00 | $32.50 | $31.50 | `KS4032.jpg` | Con nota de trazabilidad histórica |

*Todos los registros incluyen en `observaciones_internas`:*  
> *"Producto anteriormente excluido por conflicto en catálogo maestro original. Incorporado utilizando definición y precios de lista comercial posterior de Keyestudio. Mantener trazabilidad del conflicto histórico."*

---

## 5. Protocolo de Aislamiento y Cuarentena de 2 SKU en Conflicto (Sección 6)

Los 2 SKUs que no aparecen en la lista comercial posterior y mantienen información contradictoria en el archivo maestro original fueron incorporados bajo cuarentena estricta para garantizar la integridad de los 960 SKU del universo Keyestudio sin tomar decisiones arbitrarias de costeo o configuración:

### 1. `KS0240` (HUMM-KEY-KS0240)
* **Estado:** `activo=False`, `publicado=False`
* **Costo Base Proveedor:** `USD $0.00`
* **Categoría:** `Sin clasificar`
* **Nombre Interno:** `[KS0240] — Pendiente resolución proveedor`
* **Imagen:** Vinculada como evidencia fotográfica (`KS0240.jpg`)
* **Observaciones Internas:**
  > *"Producto en cuarentena por conflicto de proveedor no resuelto en catálogo maestro original. Variantes históricas detectadas: (1) Keyestudio RJ11 EASY Plug Main Control Upgrade Board V2.0 Controller +USB Cable for Arduino STEAM a USD $19.00; (2) Keyestudio RJ11 RGB TCS34725 Color Sensor Module I2C interface for Arduino STEM a USD $7.20. Pendiente resolución formal con Keyestudio antes de clasificar, costear o publicar."*

### 2. `60720227` (HUMM-KEY-60720227)
* **Estado:** `activo=False`, `publicado=False`
* **Costo Base Proveedor:** `USD $0.00`
* **Categoría:** `Sin clasificar`
* **Nombre Interno:** `[60720227] — Pendiente resolución proveedor`
* **Imagen:** Vinculada como evidencia fotográfica (`60720227.jpg`)
* **Observaciones Internas:**
  > *"Producto en cuarentena por conflicto de proveedor no resuelto en catálogo maestro original. Variantes históricas detectadas: (1) 8M Memory Voice Prompter 1W Active speaker Lighting/Button Control a USD $10.90; (2) DC 5V Active Speaker Buzzer D Digital Power Amplifier For DIY Electronic a USD $7.85. Pendiente resolución formal con Keyestudio antes de clasificar, costear o publicar."*

*Gate de Seguridad:* Ambos productos están físicamente bloqueados contra publicación (`activo=False`, `costo=0.00`).

---

## 6. Sincronización y Tramos de Volumen de los 150 SKU Comerciales

* **Productos Sincronizados:** 150 productos (131 existentes actualizados de forma no destructiva + 19 nuevos incorporados).
* **Tramos Registrados:** 597 tramos mayoristas en el modelo `PrecioProveedorTramo` (149 productos con 4 tramos Q1-9, Q10-49, Q50-100, Q101-300 + 1 producto `FB0004` con tramo único Q1-9).
* **Aislamiento de Anomalía en `KS5012`:**
  * En `KS5012`, el tramo $Q_{101\text{-}300} = \text{USD } \$34.00$, superior al tramo anterior $Q_{50\text{-}100} = \text{USD } \$15.00$.
  * **Tratamiento aplicado:** El tramo fue registrado con `es_anomalo=True`, `estado_validacion='PRECIO_PROVEEDOR_REQUIERE_REVISION'` y `notas_validacion='Anomalía en Q101-300: precio USD $34.00 excede el tramo previo ($15.00).'`.
  * Los demás tramos de `KS5012` (Q1-9 a $16.00, Q10-49 a $15.50, Q50-100 a $15.00) fueron validados normalmente.

---

## 7. Verificación de Integridad y Respaldo SQLite

1. **Respaldo Pre-Ejecución:**
   * Archivo: `backups/db_backup_pre_consolidacion_960_20261001.sqlite3` (3.7 MB).
2. **Comprobación de Integridad SQLite:**
   * Antes de ejecución: `PRAGMA integrity_check` $\rightarrow$ `ok`.
   * Después de ejecución: `PRAGMA integrity_check` $\rightarrow$ `ok`.
3. **Comando de Verificación de Producción:**
   * Ejecutado: `python manage.py verificar_estado_catalogo_produccion --assert-960`
   * Resultado:
     ```
     ======================================================================
     EDUCOMPRA HUMM — ESTADO DE BASE DE DATOS Y CATÁLOGO
     ======================================================================
     • Total Productos:                          960
     • Productos Activos:                        958
     • Curaduría Pedagógica 'VALIDADO':          88
     • Publicados (Catálogo Abierto):            77
     • No Publicados (En Espera/Descartados):    883
     • Especificación Neutral 'VALIDADO_HUMM':   0
     ======================================================================
     ✔ AUDITORÍA EXITOSA: Exactamente 960 productos en catálogo maestro y 77 publicados.
     ```
4. **Batería de Pruebas:**
   * Total ejecutado: 79 tests (incluyendo 4 tests unitarios de blindaje de unicidad y consolidación 960).
   * Resultado: `Ran 79 tests in 12.166s — OK`.

---

## 8. Estado del Repositorio y Despliegue

* **Archivos Modificados / Nuevos:**
  * `apps/catalogo/models.py`: Incorporación de `UniqueConstraint(proveedor, sku_proveedor)`.
  * `apps/catalogo/migrations/0008_producto_unique_proveedor_sku_proveedor.py`: Migración de unicidad aplicada.
  * `apps/catalogo/management/commands/consolidar_catalogo_maestro_960.py`: Comando maestro de consolidación (soporta `--dry-run` y `--aplicar`).
  * `apps/catalogo/management/commands/verificar_estado_catalogo_produccion.py`: Adición de `--assert-960`.
  * `apps/catalogo/tests/test_consolidacion_maestro_960.py`: Batería de 4 tests de blindaje y validación.
  * `data_import/EduCompra_Base_Unificada_Keyestudio_20260930.xlsx`: Planilla física unificada con los 960 SKU.
  * `README.md`: Métricas actualizadas (960 maestro, 77 públicos, 883 resguardo, 2 cuarentena).
  * `backups/db_backup_pre_consolidacion_960_20261001.sqlite3`: Respaldo preventivo antes de cambios.

---

## 9. Detención y Próximos Pasos

En estricto cumplimiento de la instrucción de Humm:
* **FASE 5A COMPLETADA Y CERRADA.**
* **NO se inició la Fase 5B.**
* **NO se publicaron nuevos productos.**
* **NO se alteró la interfaz de `/gestion/`.**
* La plataforma se encuentra lista para recibir la siguiente instrucción de Humm referente a la **simplificación de gestión y selección masiva de productos para catálogo público**.
