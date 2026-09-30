# INFORME DE INCORPORACIÓN Y CURADURÍA — SEGUNDO LOTE DE KITS NUEVOS
## Plataforma EduCompra Humm (`educompra.humm.cl/gestion/`)
**Fecha:** 30 de Septiembre de 2026  
**Operación:** Incorporación Controlada y Curaduría Pedagógica del Segundo Lote de Kits Nuevos (+6 SKUs Reales)  
**Meta Alcanzada:** **10 KITS NUEVOS REALES ACUMULADOS DESDE LA NUEVA LISTA PROVEEDOR**  
**Estado:** `SEGUNDO_LOTE_IMPORTADO_Y_CURADO_NO_PUBLICADO`

---

## 1. Resumen Ejecutivo de la Operación

En cumplimiento del requerimiento de Humm de incorporar **al menos 10 kits nuevos reales** provenientes de la nueva lista comercial Keyestudio (`data_import/keystudio_kits.xlsx`):

1. **Lote 1 (Anterior):** Resultó en 6 productos existentes actualizados y **+4 productos nuevos reales** (Catálogo: 929 → 933).
2. **Lote 2 (Presente Operación):** Se evaluaron y seleccionaron **6 candidatos genuinamente nuevos** (no existentes previamente en base de datos, sin conflictos históricos, sin anomalías de tramos y con alta diferenciación pedagógica).
3. **Resultado de Creación:** Se incorporaron con éxito **+6 productos nuevos** al catálogo maestro, alcanzando **939 productos maestros**.
4. **Cumplimiento de Meta Acumulada:**
   $$\text{Lote 1 (+4)} + \text{Lote 2 (+6)} = \mathbf{10\text{ KITS NUEVOS REALES INCORPORADOS}} \ge 10$$
5. **Protección del Catálogo Público:** Los 6 nuevos productos ingresaron estrictamente con `publicado=False`. El catálogo público en storefront se mantiene **100% intacto en exactamente 72 productos**.
6. **Curaduría Pedagógica y Comercial:** Se redactaron fichas pedagógicas individuales, asignando nombres comerciales Humm, categorías curriculares, niveles de dificultad, tecnologías y advertencias de seguridad escolar.
7. **Regla de No Invención:** La especificación técnica neutra se mantuvo en `NO_REVISADO` sin promover ningún kit a `VALIDADO_HUMM` automáticamente.
8. **Política de Imágenes:** Los 6 kits nuevos no cuentan con fotografía local; quedan catalogados con placeholder y bloqueados de publicación hasta contar con fotografía autorizada.

---

## 2. Métricas Globales del Catálogo (Antes vs Después)

| Indicador | Antes del Lote 2 | Después del Lote 2 | Variación Lote 2 | Meta / Condición | Estado |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Total Catálogo Maestro** | **933** | **939** | **+6** | $\ge +6$ productos nuevos | **Cumplido** |
| **Productos Públicos Activos** | **72** | **72** | **0** | Exactamente 72 | **Cumplido (Intacto)** |
| **Nuevos Kits Reales Acumulados** | 4 | **10** | **+6** | $\ge 10$ nuevos reales | **Cumplido** |
| **Tramos de Precios por Volumen Creados** | 40 | **64** | **+24** | 4 tramos por SKU nuevo | **Cumplido** |
| **Anomalías de Precios Detectadas** | 0 | **0** | 0 | 0 anomalías toleradas | **Cumplido** |
| **Conflictos de Importación** | 0 | **0** | 0 | 0 conflictos | **Cumplido** |
| **Integridad de Base de Datos SQLite** | `ok` | `ok` | 0 | `PRAGMA integrity_check` = `ok` | **Cumplido** |

---

## 3. Candidatos Evaluados y Selección Pedagógica

Se escanearon los productos disponibles en la nueva lista comercial Keyestudio (`FORMATO_LISTA_COMERCIAL_NUEVA`), verificando primero la lista prioritaria sugerida por Humm:

| SKU Proveedor | Product Name en Planilla | Existencia en BD | Conflicto Histórico | Variación / Decisión | Justificación Pedagógica y de Mercado |
| :--- | :--- | :---: | :---: | :---: | :--- |
| **`FKS0004`** | Micro: bit basic learning kit | **NO (Nuevo)** | No | **SELECCIONADO** | Kit inicial micro:bit con placa incluida y tarjetas ilustradas. |
| **`FKS0005`** | Keyestudio Micro:bit Smart Game Controller Kit | **NO (Nuevo)** | No | **SELECCIONADO** | Mando tipo gamepad programable para robótica y videojuegos. |
| **`KS4036F`** | Keyestudio Smart Robot Car for Micro:bit | **NO (Nuevo)** | No | **SELECCIONADO** | Robótica móvil con chasis, sensores de línea y ultrasonido. |
| **`KS0562F`** | Keyestudio Student Starter Learning Kit With Mainboard | **NO (Nuevo)** | No | **SELECCIONADO** | Kit escolar de electrónica y código con placa controladora. |
| **`KT0193F`** | 37 in1 sensor kit for Arduino | **NO (Nuevo)** | No | **SELECCIONADO** | Laboratorio modular de 37 sensores/actuadores para ferias STEAM. |
| **`KS0403`** | Keyestudio Basic Starter V2 (With UNO R3 Board) | **NO (Nuevo)** | No | **SELECCIONADO** | Starter kit V2 estructurado con placa UNO R3, LCD y servo. |
| *`KS0078`* | Super Learning Kit With UNO R3 | NO | **SÍ (Conflicto)** | Descartado | Registrado en lista de conflictos históricos no resueltos. |
| *`KS0801`* | DIY Button Piano Learning Kit | NO | **SÍ (Conflicto)** | Descartado | Registrado en lista de conflictos históricos no resueltos. |
| *`KS4048`* | Micro:bit Smart Home (Without board) | NO | No | Descartado | Redundante con `KS4049` (con placa) ya importado en Lote 1. |

Los 6 candidatos seleccionados cubren de forma balanceada: iniciación Arduino, ecosistema micro:bit, robótica móvil, sensado científico y dispositivos de interacción.

---

## 4. Matriz Exhaustiva Fila por Fila del Segundo Lote (+6 SKUs Creados)

| SKU Humm / ID | SKU Prov. | Costo Q1-9 | PVP CLP (IVA inc.) | Tramos de Volumen Proveedor (USD) | Nombre Comercial Curado Humm | Categoría Asignada | Nivel | Tecno | Img | Curaduría | Esp. Neutra | Pub. |
| :--- | :---: | :---: | :---: | :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **`HUMM-KEY-FKS0004`**<br>(ID 934) | `FKS0004` | **$31.91** | **$74.675** | **Q1-9:** $31.91<br>**Q10-49:** $29.78<br>**Q50-100:** $28.71<br>**Q101-300:** $27.65 | **Kit Básico de Aprendizaje con Tarjeta BBC micro:bit Incluida** | Micro:bit y accesorios | INICIAL | micro:bit | 0 | `VALIDADO` | `NO_REVISADO` | **False** |
| **`HUMM-KEY-FKS0005`**<br>(ID 936) | `FKS0005` | **$8.86** | **$20.735** | **Q1-9:** $8.86<br>**Q10-49:** $8.57<br>**Q50-100:** $8.27<br>**Q101-300:** $7.98 | **Controlador Gamepad Inteligente DIY para micro:bit (Sin Placa)** | Pantallas e interacción | INICIAL | micro:bit | 0 | `VALIDADO` | `NO_REVISADO` | **False** |
| **`HUMM-KEY-KS4036F`**<br>(ID 935) | `KS4036F` | **$15.51** | **$36.296** | **Q1-9:** $15.51<br>**Q10-49:** $14.99<br>**Q50-100:** $14.48<br>**Q101-300:** $13.96 | **Auto Robot Educativo Inteligente para micro:bit** | Robótica y vehículos | INTERMEDIO | micro:bit | 0 | `VALIDADO` | `NO_REVISADO` | **False** |
| **`HUMM-KEY-KS0562F`**<br>(ID 937) | `KS0562F` | **$20.00** | **$46.803** | **Q1-9:** $20.00<br>**Q10-49:** $19.30<br>**Q50-100:** $18.60<br>**Q101-300:** $17.90 | **Kit de Iniciación Escolar en Electrónica y Programación con Placa Incluida** | Kits educativos iniciales | INICIAL | Arduino | 0 | `VALIDADO` | `NO_REVISADO` | **False** |
| **`HUMM-KEY-KT0193F`**<br>(ID 938) | `KT0193F` | **$23.93** | **$56.000** | **Q1-9:** $23.93<br>**Q10-49:** $23.13<br>**Q50-100:** $22.33<br>**Q101-300:** $21.54 | **Laboratorio Escolar de 37 Sensores y Actuadores Modulares** | Sensores y módulos | INTERMEDIO | Arduino | 0 | `VALIDADO` | `NO_REVISADO` | **False** |
| **`HUMM-KEY-KS0403`**<br>(ID 939) | `KS0403` | **$21.50** | **$50.313** | **Q1-9:** $21.50<br>**Q10-49:** $21.00<br>**Q50-100:** $20.50<br>**Q101-300:** $19.50 | **Kit Básico Starter V2 con Placa UNO R3 y Pantalla LCD** | Kits educativos iniciales | INICIAL | Arduino | 0 | `VALIDADO` | `NO_REVISADO` | **False** |

---

## 5. Fichas de Curaduría Pedagógica y Comercial

### 1. `FKS0004` (ID 934) — Kit Básico de Aprendizaje con Tarjeta BBC micro:bit Incluida
* **Información del Proveedor:** "This learning kit covers sensors and components as well as a Micro:bit board, and the included animation card makes experiments more exquisite and beautiful."
* **Interpretación Pedagógica Humm:** Solución integral de iniciación a las ciencias de la computación y electrónica básica para educación primaria y secundaria temprana. Incluye la placa BBC micro:bit y componentes guiados con tarjetas visuales para programar en MakeCode o Python sin soldaduras.
* **Uso Escolar:** Talleres STEAM, pensamiento computacional y proyectos de sensado inicial.
* **Advertencia de Uso:** Contiene componentes pequeños y tarjeta micro:bit. Usar bajo supervisión docente en aula; no exponer al agua ni a humedad excesiva.

### 2. `FKS0005` (ID 936) — Controlador Gamepad Inteligente DIY para micro:bit (Sin Placa)
* **Información del Proveedor:** "Based on the Micro:bit board, this smart gamepad kit integrates various electronic components, which enables users to build many interesting DIY projects, like small cars and robots control."
* **Interpretación Pedagógica Humm:** Mando de control ergonómico para proyectos interactivos. Permite enseñar a los alumnos a programar el mapeo bidireccional (ejes X/Y) de un joystick, la lectura de pulsadores de acción y la retroalimentación háptica (vibración) y acústica en robótica y videojuegos escolares.
* **Uso Escolar:** Teleoperación de robots móviles, interfaces para videojuegos escolares y proyectos de interacción física.
* **Advertencia de Uso:** Requiere tarjeta micro:bit externa (no incluida) y pilas para funcionamiento autónomo.

### 3. `KS4036F` (ID 935) — Auto Robot Educativo Inteligente para micro:bit
* **Información del Proveedor:** "Keyestudio Mini Robot Car is a multifunctional car based on BBC micro:bit. It is equipped with a wealth of sensors and peripherals... leaves lot of universal jacks of building block holes for easy connection."
* **Interpretación Pedagógica Humm:** Plataforma móvil didáctica para abordar desafíos de cinemática diferencial y robótica autónoma (seguidor de líneas, evasión de obstáculos con sensor ultrasónico, control lumínico y expansión estructural con bloques de encastre estándar).
* **Uso Escolar:** Asignatura de tecnología, electivos de robótica escolar y preparación para olimpiadas tecnológicas.
* **Advertencia de Uso:** Requiere tarjeta BBC micro:bit externa (no incluida) y baterías recargables recomendadas por fabricante.

### 4. `KS0562F` (ID 937) — Kit de Iniciación Escolar en Electrónica y Programación con Placa Incluida
* **Información del Proveedor:** "* Start coding instantly with our comprehensive starter kit. * Learn electronics fundamentals through hands-on projects. * Explore creative circuits with included Keyestudio mainboard."
* **Interpretación Pedagógica Humm:** Maletín formativo orientado a estudiantes de enseñanza media y educación media técnico-profesional (EMTP). Contiene placa controladora compatible con Arduino UNO, protoboard y componentes esenciales para aprender circuitos eléctricos, ley de Ohm y código estructurado en C++/Arduino IDE.
* **Uso Escolar:** Laboratorios de física eléctrica y talleres de iniciación tecnológica en colegios y liceos.
* **Advertencia de Uso:** Placa y componentes operan a baja tensión segura (5V DC). Manejar piezas pequeñas bajo supervisión.

### 5. `KT0193F` (ID 938) — Laboratorio Escolar de 37 Sensores y Actuadores Modulares
* **Información del Proveedor:** "This sensor kit contains 37 kinds of commonly used sensor modules for microcontroller projects... compatible with various microcontrollers and Raspberry Pi."
* **Interpretación Pedagógica Humm:** Set integral de sensado para convertir magnitudes físicas del entorno (luz, calor, inclinación, sonido, gas, campos magnéticos) en señales digitales y analógicas procesables por microcontroladores escolares.
* **Uso Escolar:** Ferias científicas escolares, estaciones meteorológicas, proyectos ecológicos y robótica de percepción.
* **Advertencia de Uso:** Requiere placa microcontroladora externa. El módulo relé debe emplearse exclusivamente con cargas escolares seguras de corriente continua (máx. 12V/24V DC; prohibida su conexión a 220V de red domiciliaria en entornos escolares).

### 6. `KS0403` (ID 939) — Kit Básico Starter V2 con Placa UNO R3 y Pantalla LCD
* **Información del Proveedor:** "* Learn Arduino basics and control the physical world with sensors using this comprehensive starter kit. * Features an UNO R3 V4.0 board, various sensors, displays, servo, and essential electronic components."
* **Interpretación Pedagógica Humm:** Kit escolar de segunda generación que integra placa UNO R3, pantalla alfanumérica LCD 1602 con módulo I2C y servomotor de precisión de 9g para más de 30 proyectos guiados paso a paso.
* **Uso Escolar:** Asignatura de tecnología escolar, interfaces de visualización en proyectos de ciencias y control mecatrónico.
* **Advertencia de Uso:** Incluye microcontrolador listo para usar con cable USB escolar (5V).

---

## 6. Política de Imágenes y Bloqueo de Publicación

* **Situación de Imágenes:** Ninguno de los 6 kits nuevos dispone actualmente de archivo fotográfico local en `data_import/imagenes/`.
* **Asignación:** Se asignó placeholder del sistema y etiqueta interna `SIN_IMAGEN`.
* **Condición Estricta:**
  > **NINGUNO DE ESTOS 6 KITS PUEDE SER PUBLICADO EN EL FRONTEND DE EDUCOMPRA MIENTRAS NO SE INCORPORE UNA FOTOGRAFÍA PRODUCTIVA VALIDADA DESDE `/gestion/productos/`.**
  
* Todos los kits se mantienen con `publicado=False`.

---

## 7. Acumulado de Kits Nuevos desde la Nueva Lista Proveedor

$$\begin{aligned}
\text{Lote 1 (Autorizado 30/09/2026):} & \quad \text{KS4050, FKS0003, KS4049, KS0474} & \mathbf{+4\text{ nuevos}} \\
\text{Lote 2 (Autorizado 30/09/2026):} & \quad \text{FKS0004, FKS0005, KS4036F, KS0562F, KT0193F, KS0403} & \mathbf{+6\text{ nuevos}} \\
\hline
\mathbf{Total\ Acumulado\ Nuevos\ Kits:} & & \mathbf{10\text{ KITS NUEVOS}}
\end{aligned}$$

Se cumple cabalmente la meta estratégica de Humm: **$\ge 10$ nuevos kits reales incorporados al catálogo maestro.**

---

## 8. Verificaciones Técnicas, Integridad y Despliegue

1. **Integridad de Base de Datos:**
   * Respaldo previo: `backups/db_backup_pre_importacion_lote2_20260930.sqlite3` (`PRAGMA integrity_check = ok`).
   * Verificación post-operación en `db.sqlite3`: `PRAGMA integrity_check = ok`.

2. **Suite Completa de Pruebas Automatizadas:**
   * Comando: `.venv/bin/python manage.py test`
   * **Resultado:** **74 tests ejecutados, 74 aprobados (0 fallos, 0 errores)** en 12.6s.

3. **Control de Versiones en Git:**
   * Commit previo: `253e424`
   * Nuevo commit: [`e326f85` / posterior]

4. **Monitoreo de Producción:**
   * `https://educompra.humm.cl/health/` responde `{"status": "ok", "db": "ok"}`.
   * `https://educompra.humm.cl/catalogo/` continúa sirviendo exactamente **72 productos públicos**.

---

# 🛑 9. PUNTO DE CONTROL FINAL (DETENCIÓN TOTAL)

- **TODOS LOS KITS NUEVOS SE ENCUENTRAN CON `publicado=False`.**
- **EL CATÁLOGO PÚBLICO CONTINÚA CON EXACTAMENTE 72 PRODUCTOS.**
- **NO SE HA INICIADO FASE 5B.**
- **SE DETIENE LA EJECUCIÓN A LA ESPERA DE LA AUTORIZACIÓN EXPLÍCITA DE HUMM RESPECTO A PUBLICACIONES FUTURAS.**
