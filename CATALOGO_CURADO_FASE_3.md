# EDUCOMPRA HUMM — TERCER PUNTO DE CONTROL FASE 3
## Catálogo Curado Oficial: 72 Productos Aprobados (A + B)
### Curaduría Comercial, Pedagógica, Compatibilidad Diferenciada y Seguridad

**Fecha de Cierre:** 29 de Septiembre de 2026  
**Plataforma:** EduCompra Humm (`educompra.humm.cl`)  
**Total Productos Curados:** **72 productos** (100% aprobados A + B por Humm)  
**Estado de Curaduría:** `VALIDADO` (Curaduría pedagógica y comercial validada)  
**Estado Especificación Neutra:** `NO_REVISADO` (Borradores automáticos, validación técnica progresiva posterior)  
**Estado de Publicación:** **`publicado = False` (0 productos publicados)**  
**Estado General:** **FASE 3 — CIERRE DEFINITIVO AUTORIZADO**  

---

## 1. Marco Metodológico: Separación de Información y Trazabilidad

En conformidad con el cierre definitivo de Fase 3, la información de cada producto se estructura en tres capas independientes:

> [!IMPORTANT]
> ### 1. CAPA A — INFORMACIÓN FUENTE DIRECTA DEL PROVEEDOR
> Datos técnicos provenientes exclusivamente del catálogo maestro Keyestudio (SKU original, descripción textual del fabricante, precio base en USD).
> **Regla de Oro:** Si un dato no figura explícitamente en el texto del fabricante, **no se asume ni se inventa**.

> [!TIP]
> ### 2. CAPA B — INTERPRETACIÓN Y CURADURÍA EDUCATIVA HUMM
> Nombre comercial amigable y honesto, empaque real explicitado, categoría docente, nivel de complejidad de uso (`INICIAL`, `INTERMEDIO`, `AVANZADO`), proyectos escolares posibles, advertencias pedagógicas de seguridad y aptitud para kits temáticos escolares.

> [!CAUTION]
> ### 3. CAPA C — ESPECIFICACIÓN TÉCNICA NEUTRAL (EN ESPERA DOCUMENTAL)
> Denominación técnica neutra sin marcas según Ley N° 19.886 para compra pública.
> **Estado:** Todos los productos mantienen su especificación en `NO_REVISADO`. No se bloquea el catálogo comercial por la redacción técnica. La promoción a `VALIDADO_HUMM` se ejecutará de forma individual según demanda comercial y con respaldo documental registrado.

---

## 2. Diferenciación de Compatibilidad Tecnológica y Reglas de Seguridad

### Compatibilidad Verificada vs. Compatibilidad Propuesta
Para evitar inferencias técnicas no respaldadas, se independizaron dos niveles de compatibilidad:

- **Compatibilidad Tecnológica Verificada:** Plataformas microcontroladoras o computacionales explícitamente respaldadas por la descripción del proveedor o documentación técnica de fábrica (ej: si el proveedor dice *for Arduino*, la única verificada es Arduino).
- **Compatibilidad Tecnológica Propuesta (Aula):** Plataformas viables desde el punto de vista pedagógico y eléctrico sugeridas por Humm para el desarrollo de proyectos interdisciplinarios en el colegio.

### Reglas de Seguridad y Advertencias de Uso Educativo
Se implementó el campo `advertencia_uso` en el modelo `Producto`, visible solo cuando corresponda:

1. **Sensores MQ de Gas (`KS0040`, `KS0047`):** Presentados exclusivamente como módulos didácticos para experimentación y aprendizaje escolar sobre gases. Se advierte explícitamente que no reemplazan detectores certificados de gas ni sistemas de prevención de incendios.
2. **Sensor de Llama (`KS0116`):** Presentado para robótica educativa y demostraciones de óptica. No constituye un sistema profesional de alarma contra incendios.
3. **Sensor de Pulso Fisiológico (`KS0171`):** Diseñado para experimentos educativos de biología y deporte. Se añade advertencia obligatoria: *'Uso educativo. No es un dispositivo médico ni debe utilizarse para diagnóstico.'*
4. **Relés (`KS0057`):** Orientados a cargas de baja tensión (baterías, bombas 5V/12V). Se advierte que el trabajo con tensión de red domiciliaria (220V) no es apto para manipulación directa por estudiantes y exige personal competente con supervisión adecuada.
5. **Multímetros (`49500005`, `49500004`):** Se orientan las actividades estudiantiles a circuitos formativos de baja tensión (hasta 24V).
6. **Fuentes y Chasis con Baterías (`KS0332`, `CR0011`, `CR0019`, `CR0033 CR0034`):** Advertencia de comprobación de polaridad para evitar cortocircuitos en protoboard.

### Depuración de Afirmaciones no Respaldadas
Se eliminaron afirmaciones institucionales no sustentadas documentalmente (ej: en `MB0110` se removió la alusión a 'estándar oficial del Mineduc' reemplazándola por descripción pedagógica neutral).

---

## 3. Resumen Consolidado del Catálogo Curado por Categoría

| Categoría Curada | Cantidad | Rango Precios (CLP) | Nivel Predominante | Compatibilidad Verificada | Compatibilidad Propuesta Aula |
| :--- | :---: | :---: | :---: | :--- | :--- |
| **Arduino y controladores** | **8** | $14,510 a $44,859 CLP | Inicial / Intermedio | Arduino, ESP8266 | Arduino, ESP8266 |
| **Sensores y módulos** | **20** | $4,656 a $19,423 CLP | Inicial / Intermedio | Arduino, Otros, micro:bit | Arduino, ESP32, Raspberry Pi, micro:bit |
| **Robótica y vehículos** | **4** | $35,080 a $98,286 CLP | Inicial / Intermedio | Arduino, Raspberry Pi, micro:bit | Arduino, ESP32, Raspberry Pi, micro:bit |
| **Motores y movimiento** | **5** | $6,785 a $21,039 CLP | Inicial / Intermedio | Arduino, Otros | Arduino, ESP32, Raspberry Pi, micro:bit |
| **Electrónica y prototipado** | **8** | $5,802 a $25,719 CLP | Inicial / Intermedio | Arduino, Otros | Arduino, ESP32, Otros, Raspberry Pi, micro:bit |
| **Pantallas e interacción** | **6** | $6,998 a $22,935 CLP | Inicial / Intermedio | Arduino, Otros, micro:bit | Arduino, ESP32, Raspberry Pi, micro:bit |
| **Micro:bit y accesorios** | **5** | $11,701 a $150,705 CLP | Inicial / Intermedio | micro:bit | micro:bit |
| **Raspberry Pi y accesorios** | **4** | $11,701 a $38,612 CLP | Inicial / Intermedio | Raspberry Pi | Raspberry Pi |
| **IoT y comunicación** | **6** | $5,850 a $25,719 CLP | Inicial / Intermedio | Arduino, ESP8266 | Arduino, ESP32, ESP8266, Raspberry Pi, micro:bit |
| **Kits educativos iniciales** | **3** | $45,633 a $142,749 CLP | Inicial / Intermedio | Arduino, ESP32 | Arduino, ESP32, Raspberry Pi, micro:bit |
| **Herramientas y accesorios** | **3** | $9,478 a $35,103 CLP | Inicial / Intermedio | Arduino, Otros | Arduino, Otros |
| **TOTAL CATÁLOGO CURADO** | **72** | **$4,656 a $150,705 CLP** | **Multinivel Escolar** | **Arduino, micro:bit, RPi, ESP8266, ESP32** | **Universal Educativo** |

---

## 4. Fichas Individuales Detalladas de los 72 Productos Curados

### Arduino y controladores (8 productos)

#### [01] `KS0486` — Placa Keyestudio PLUS con USB-C compatible con Arduino Uno R3 + Cable USB

- **SKU Proveedor:** `KS0486` | **SKU Humm:** `HUMM-KEY-KS0486`
- **Nombre Comercial Humm:** **Placa Keyestudio PLUS con USB-C compatible con Arduino Uno R3 + Cable USB**
- **Categoría:** Arduino y controladores
- **Precio Referencial Sugerido:** **$26,912 CLP** (Costo Base: $11.50 USD)
- **Nivel de Complejidad / Uso:** `INICIAL`
- **Compatibilidad Tecnológica Verificada:** `Arduino` *(respaldo fabricante)*
- **Compatibilidad Tecnológica Propuesta (Aula):** `Arduino` *(interpretación pedagógica Humm)*
- **Contenido Real del Pack / Empaque:** 1 placa Keyestudio PLUS (conector USB Tipo C) + 1 cable USB Tipo C.
- **Unidad de Medida:** `unidad`
- **Apto Potencial para Kit:** **Sí**
- **Estado de Curaduría:** `VALIDADO`
- **Estado Especificación Técnica Neutra:** `NO_REVISADO` *(validación técnica documental progresiva)*
- **Descripción Educativa (Humm):** Placa microcontroladora estándar de desarrollo escolar con conector moderno USB Tipo C. Es el punto de partida fundamental para la alfabetización digital, el pensamiento computacional y proyectos de automatización en el aula.
- **Posible Uso / Proyecto Escolar:** Iniciación a la programación en C++ y entornos por bloques; proyectos de semáforos, control de LEDs, lectura de sensores analógicos y robótica escolar básica.
- **Observaciones y Trazabilidad:** Clasificación A. Incluye cable USB Tipo C en el empaque original.

#### [02] `KS0502` — Placa Keyestudio MEGA 2560 PRO compatible con Arduino Mega 2560

- **SKU Proveedor:** `KS0502` | **SKU Humm:** `HUMM-KEY-KS0502`
- **Nombre Comercial Humm:** **Placa Keyestudio MEGA 2560 PRO compatible con Arduino Mega 2560**
- **Categoría:** Arduino y controladores
- **Precio Referencial Sugerido:** **$44,859 CLP** (Costo Base: $19.17 USD)
- **Nivel de Complejidad / Uso:** `AVANZADO`
- **Compatibilidad Tecnológica Verificada:** `Arduino` *(respaldo fabricante)*
- **Compatibilidad Tecnológica Propuesta (Aula):** `Arduino` *(interpretación pedagógica Humm)*
- **Contenido Real del Pack / Empaque:** 1 placa Keyestudio MEGA 2560 PRO.
- **Unidad de Medida:** `unidad`
- **Apto Potencial para Kit:** **Sí**
- **Estado de Curaduría:** `VALIDADO`
- **Estado Especificación Técnica Neutra:** `NO_REVISADO` *(validación técnica documental progresiva)*
- **Descripción Educativa (Humm):** Placa microcontroladora de alta capacidad con 54 pines de entrada/salida digital y 16 entradas analógicas. Diseñada para proyectos que superan la capacidad de una placa básica, como robots complejos o impresoras 3D.
- **Posible Uso / Proyecto Escolar:** Robótica multiactuador, brazos mecánicos con múltiples servomotores, paneles de control con pantallas gráficas y proyectos técnicos de especialidad electrónica.
- **Observaciones y Trazabilidad:** Clasificación A. No especifica cable USB en el empaque primario.

#### [03] `KS0547` — Placa Keyestudio Nano Plus con USB-C compatible con Arduino Nano

- **SKU Proveedor:** `KS0547` | **SKU Humm:** `HUMM-KEY-KS0547`
- **Nombre Comercial Humm:** **Placa Keyestudio Nano Plus con USB-C compatible con Arduino Nano**
- **Categoría:** Arduino y controladores
- **Precio Referencial Sugerido:** **$21,062 CLP** (Costo Base: $9.00 USD)
- **Nivel de Complejidad / Uso:** `INTERMEDIO`
- **Compatibilidad Tecnológica Verificada:** `Arduino` *(respaldo fabricante)*
- **Compatibilidad Tecnológica Propuesta (Aula):** `Arduino` *(interpretación pedagógica Humm)*
- **Contenido Real del Pack / Empaque:** 1 placa Nano Plus con pines soldados.
- **Unidad de Medida:** `unidad`
- **Apto Potencial para Kit:** **Sí**
- **Estado de Curaduría:** `VALIDADO`
- **Estado Especificación Técnica Neutra:** `NO_REVISADO` *(validación técnica documental progresiva)*
- **Descripción Educativa (Humm):** Microcontrolador de factor de forma compacto con pines macho inferiores para inserción directa en protoboards. Ofrece las mismas prestaciones básicas de un Uno en una fracción de su tamaño.
- **Posible Uso / Proyecto Escolar:** Prototipado rápido en protoboard, dispositivos portátiles para ferias científicas y circuitos embebidos de tamaño reducido.
- **Observaciones y Trazabilidad:** Clasificación A. Incorpora conector USB Tipo C.

#### [04] `KS0503` — Placa Keyestudio Pro Micro 5V (ATmega32U4) con USB Nativo

- **SKU Proveedor:** `KS0503` | **SKU Humm:** `HUMM-KEY-KS0503`
- **Nombre Comercial Humm:** **Placa Keyestudio Pro Micro 5V (ATmega32U4) con USB Nativo**
- **Categoría:** Arduino y controladores
- **Precio Referencial Sugerido:** **$25,742 CLP** (Costo Base: $11.00 USD)
- **Nivel de Complejidad / Uso:** `INTERMEDIO`
- **Compatibilidad Tecnológica Verificada:** `Arduino` *(respaldo fabricante)*
- **Compatibilidad Tecnológica Propuesta (Aula):** `Arduino` *(interpretación pedagógica Humm)*
- **Contenido Real del Pack / Empaque:** 1 placa Pro Micro 5V/16MHz.
- **Unidad de Medida:** `unidad`
- **Apto Potencial para Kit:** **Sí**
- **Estado de Curaduría:** `VALIDADO`
- **Estado Especificación Técnica Neutra:** `NO_REVISADO` *(validación técnica documental progresiva)*
- **Descripción Educativa (Humm):** Microcontrolador con comunicación USB nativa directa que permite emular periféricos de computadora como teclado, ratón o joystick (HID).
- **Posible Uso / Proyecto Escolar:** Creación de mandos de videojuegos personalizados, interfaces de accesibilidad para estudiantes con discapacidad motriz y teclados macro para laboratorios.
- **Observaciones y Trazabilidad:** Clasificación A. Basada en ATmega32U4.

#### [05] `KS0247` — Placa Keyestudio Pro Mini 5V/16MHz (Requiere Programador USB)

- **SKU Proveedor:** `KS0247` | **SKU Humm:** `HUMM-KEY-KS0247`
- **Nombre Comercial Humm:** **Placa Keyestudio Pro Mini 5V/16MHz (Requiere Programador USB)**
- **Categoría:** Arduino y controladores
- **Precio Referencial Sugerido:** **$17,551 CLP** (Costo Base: $7.50 USD)
- **Nivel de Complejidad / Uso:** `AVANZADO`
- **Compatibilidad Tecnológica Verificada:** `Arduino` *(respaldo fabricante)*
- **Compatibilidad Tecnológica Propuesta (Aula):** `Arduino` *(interpretación pedagógica Humm)*
- **Contenido Real del Pack / Empaque:** 1 placa Pro Mini 5V (sin puerto USB integrado).
- **Unidad de Medida:** `unidad`
- **Apto Potencial para Kit:** **No**
- **Estado de Curaduría:** `VALIDADO`
- **Estado Especificación Técnica Neutra:** `NO_REVISADO` *(validación técnica documental progresiva)*
- **Descripción Educativa (Humm):** Placa microcontroladora miniatura de bajo costo y consumo mínimo sin interfaz USB integrada. Requiere un módulo adaptador USB-Serial (como MD0118) para cargar el código.
- **Posible Uso / Proyecto Escolar:** Proyectos definitivos o permanentes que se instalan de forma autónoma con baterías o energía solar una vez programados.
- **Observaciones y Trazabilidad:** Clasificación B. Advertencia explícita: no tiene puerto USB integrado, requiere conversor USB-TTL.

#### [06] `KS0004` — Shield de Expansión de Sensores V5 para Arduino Uno y Leonardo

- **SKU Proveedor:** `KS0004` | **SKU Humm:** `HUMM-KEY-KS0004`
- **Nombre Comercial Humm:** **Shield de Expansión de Sensores V5 para Arduino Uno y Leonardo**
- **Categoría:** Arduino y controladores
- **Precio Referencial Sugerido:** **$15,446 CLP** (Costo Base: $6.60 USD)
- **Nivel de Complejidad / Uso:** `INICIAL`
- **Compatibilidad Tecnológica Verificada:** `Arduino` *(respaldo fabricante)*
- **Compatibilidad Tecnológica Propuesta (Aula):** `Arduino` *(interpretación pedagógica Humm)*
- **Contenido Real del Pack / Empaque:** 1 placa Sensor Shield V5.
- **Unidad de Medida:** `unidad`
- **Apto Potencial para Kit:** **Sí**
- **Estado de Curaduría:** `VALIDADO`
- **Estado Especificación Técnica Neutra:** `NO_REVISADO` *(validación técnica documental progresiva)*
- **Descripción Educativa (Humm):** Placa de expansión que se monta sobre Arduino Uno para duplicar cada pin en un cabezal de 3 pines estándar (Tierra, Voltaje y Señal), facilitando la conexión rápida de sensores y servos.
- **Posible Uso / Proyecto Escolar:** Montaje limpio de sensores y actuadores en talleres escolares sin enredos de cables ni necesidad de protoboard auxiliar.
- **Observaciones y Trazabilidad:** Clasificación A. Accesorio indispensable para talleres de robótica.

#### [07] `KS0003` — Protoshield para Arduino Uno con Mini Protoboard Autoadhesiva

- **SKU Proveedor:** `KS0003` | **SKU Humm:** `HUMM-KEY-KS0003`
- **Nombre Comercial Humm:** **Protoshield para Arduino Uno con Mini Protoboard Autoadhesiva**
- **Categoría:** Arduino y controladores
- **Precio Referencial Sugerido:** **$14,510 CLP** (Costo Base: $6.20 USD)
- **Nivel de Complejidad / Uso:** `INTERMEDIO`
- **Compatibilidad Tecnológica Verificada:** `Arduino` *(respaldo fabricante)*
- **Compatibilidad Tecnológica Propuesta (Aula):** `Arduino` *(interpretación pedagógica Humm)*
- **Contenido Real del Pack / Empaque:** 1 placa Protoshield + 1 mini protoboard autoadhesiva de 170 contactos.
- **Unidad de Medida:** `unidad`
- **Apto Potencial para Kit:** **Sí**
- **Estado de Curaduría:** `VALIDADO`
- **Estado Especificación Técnica Neutra:** `NO_REVISADO` *(validación técnica documental progresiva)*
- **Descripción Educativa (Humm):** Placa de prototipado que se acopla directamente sobre Arduino Uno, incorporando una pequeña área de pruebas sin soldadura y pistas perforadas para soldar circuitos definitivos.
- **Posible Uso / Proyecto Escolar:** Prácticas de electrónica intermedia, creación de shields personalizados y montaje compacto de circuitos experimentales.
- **Observaciones y Trazabilidad:** Clasificación A. Incluye mini protoboard autoadhesiva.

#### [08] `KS5013` — Placa Keyestudio 328 WIFI PLUS (Arduino Uno R3 + Wi-Fi ESP8266)

- **SKU Proveedor:** `KS5013` | **SKU Humm:** `HUMM-KEY-KS5013`
- **Nombre Comercial Humm:** **Placa Keyestudio 328 WIFI PLUS (Arduino Uno R3 + Wi-Fi ESP8266)**
- **Categoría:** Arduino y controladores
- **Precio Referencial Sugerido:** **$32,738 CLP** (Costo Base: $13.99 USD)
- **Nivel de Complejidad / Uso:** `INTERMEDIO`
- **Compatibilidad Tecnológica Verificada:** `Arduino, ESP8266` *(respaldo fabricante)*
- **Compatibilidad Tecnológica Propuesta (Aula):** `Arduino, ESP8266` *(interpretación pedagógica Humm)*
- **Contenido Real del Pack / Empaque:** 1 placa híbrida 328 WIFI PLUS.
- **Unidad de Medida:** `unidad`
- **Apto Potencial para Kit:** **Sí**
- **Estado de Curaduría:** `VALIDADO`
- **Estado Especificación Técnica Neutra:** `NO_REVISADO` *(validación técnica documental progresiva)*
- **Descripción Educativa (Humm):** Placa multifuncional con factor de forma Arduino Uno que integra dos microcontroladores en el mismo circuito: ATmega328P para control físico y chip ESP8266 para conectividad Wi-Fi a internet.
- **Posible Uso / Proyecto Escolar:** Proyectos de Internet de las Cosas (IoT), envío de datos de sensores escolares a plataformas web y tableros en la nube.
- **Observaciones y Trazabilidad:** Clasificación B. Corrección auditada: microcontrolador dual ATmega328P + ESP8266 (no es ESP32).

---

### Sensores y módulos (20 productos)

#### [09] `KS0034` — Sensor Digital de Temperatura y Humedad DHT11 Keyestudio

- **SKU Proveedor:** `KS0034` | **SKU Humm:** `HUMM-KEY-KS0034`
- **Nombre Comercial Humm:** **Sensor Digital de Temperatura y Humedad DHT11 Keyestudio**
- **Categoría:** Sensores y módulos
- **Precio Referencial Sugerido:** **$10,063 CLP** (Costo Base: $4.30 USD)
- **Nivel de Complejidad / Uso:** `INICIAL`
- **Compatibilidad Tecnológica Verificada:** `Arduino` *(respaldo fabricante)*
- **Compatibilidad Tecnológica Propuesta (Aula):** `Arduino, micro:bit, ESP32, Raspberry Pi` *(interpretación pedagógica Humm)*
- **Contenido Real del Pack / Empaque:** 1 módulo sensor DHT11 en PCB con conector de 3 pines.
- **Unidad de Medida:** `unidad`
- **Apto Potencial para Kit:** **Sí**
- **Estado de Curaduría:** `VALIDADO`
- **Estado Especificación Técnica Neutra:** `NO_REVISADO` *(validación técnica documental progresiva)*
- **Descripción Educativa (Humm):** Sensor ambiental digital económico para medición simultánea de temperatura ambiente y porcentaje de humedad relativa del aire mediante un solo pin digital.
- **Posible Uso / Proyecto Escolar:** Estaciones meteorológicas escolares, monitoreo ambiental en salas de clase y registro de variables en ciencias naturales.
- **Observaciones y Trazabilidad:** Clasificación A. Estándar educativo internacional.

#### [10] `KS0430` — Sensor Digital de Temperatura y Humedad DHT22 (AM2302) de Precisión

- **SKU Proveedor:** `KS0430` | **SKU Humm:** `HUMM-KEY-KS0430`
- **Nombre Comercial Humm:** **Sensor Digital de Temperatura y Humedad DHT22 (AM2302) de Precisión**
- **Categoría:** Sensores y módulos
- **Precio Referencial Sugerido:** **$19,423 CLP** (Costo Base: $8.30 USD)
- **Nivel de Complejidad / Uso:** `INTERMEDIO`
- **Compatibilidad Tecnológica Verificada:** `Arduino` *(respaldo fabricante)*
- **Compatibilidad Tecnológica Propuesta (Aula):** `Arduino, ESP32, micro:bit, Raspberry Pi` *(interpretación pedagógica Humm)*
- **Contenido Real del Pack / Empaque:** 1 módulo sensor DHT22 con PCB de soporte de 3 pines.
- **Unidad de Medida:** `unidad`
- **Apto Potencial para Kit:** **Sí**
- **Estado de Curaduría:** `VALIDADO`
- **Estado Especificación Técnica Neutra:** `NO_REVISADO` *(validación técnica documental progresiva)*
- **Descripción Educativa (Humm):** Sensor ambiental digital de mayor precisión y rango de medición que el DHT11, ideal para experimentos científicos que requieran lecturas más exactas.
- **Posible Uso / Proyecto Escolar:** Invernaderos escolares automatizados, laboratorios de ecología y registro de confort térmico en recintos educativos.
- **Observaciones y Trazabilidad:** Clasificación A. Mayor rango y resolución que DHT11.

#### [11] `KS0049` — Sensor de Humedad de Suelo para Arduino y micro:bit Keyestudio

- **SKU Proveedor:** `KS0049` | **SKU Humm:** `HUMM-KEY-KS0049`
- **Nombre Comercial Humm:** **Sensor de Humedad de Suelo para Arduino y micro:bit Keyestudio**
- **Categoría:** Sensores y módulos
- **Precio Referencial Sugerido:** **$8,894 CLP** (Costo Base: $3.80 USD)
- **Nivel de Complejidad / Uso:** `INICIAL`
- **Compatibilidad Tecnológica Verificada:** `Arduino` *(respaldo fabricante)*
- **Compatibilidad Tecnológica Propuesta (Aula):** `Arduino, micro:bit, ESP32` *(interpretación pedagógica Humm)*
- **Contenido Real del Pack / Empaque:** 1 módulo sensor con sonda de dos pistas expuestas.
- **Unidad de Medida:** `unidad`
- **Apto Potencial para Kit:** **Sí**
- **Estado de Curaduría:** `VALIDADO`
- **Estado Especificación Técnica Neutra:** `NO_REVISADO` *(validación técnica documental progresiva)*
- **Descripción Educativa (Humm):** Sensor que detecta el nivel de humedad en la tierra midiendo la conductividad eléctrica entre dos pistas metálicas que se entierran en el sustrato.
- **Posible Uso / Proyecto Escolar:** Proyectos de huertos escolares inteligentes, sistemas de riego automatizado con bombas pequeñas y experimentos de botánica.
- **Observaciones y Trazabilidad:** Clasificación A. Insumo clave para huertos STEM.

#### [12] `KS0052` — Sensor Infrarrojo Pasivo de Movimiento PIR Keyestudio

- **SKU Proveedor:** `KS0052` | **SKU Humm:** `HUMM-KEY-KS0052`
- **Nombre Comercial Humm:** **Sensor Infrarrojo Pasivo de Movimiento PIR Keyestudio**
- **Categoría:** Sensores y módulos
- **Precio Referencial Sugerido:** **$10,063 CLP** (Costo Base: $4.30 USD)
- **Nivel de Complejidad / Uso:** `INICIAL`
- **Compatibilidad Tecnológica Verificada:** `Arduino` *(respaldo fabricante)*
- **Compatibilidad Tecnológica Propuesta (Aula):** `Arduino, micro:bit, ESP32, Raspberry Pi` *(interpretación pedagógica Humm)*
- **Contenido Real del Pack / Empaque:** 1 módulo PIR con lente Fresnel y potenciómetros de ajuste.
- **Unidad de Medida:** `unidad`
- **Apto Potencial para Kit:** **Sí**
- **Estado de Curaduría:** `VALIDADO`
- **Estado Especificación Técnica Neutra:** `NO_REVISADO` *(validación técnica documental progresiva)*
- **Descripción Educativa (Humm):** Sensor de detección de presencia humana mediante radiación infrarroja emitida por cuerpos cálidos en movimiento. Cuenta con ajustes de sensibilidad y tiempo.
- **Posible Uso / Proyecto Escolar:** Sistemas de alarma escolar, iluminación automática para ahorro energético y proyectos de domótica.
- **Observaciones y Trazabilidad:** Clasificación A. Detección de presencia confiable.

#### [13] `KS0040` — Sensor de Gas Combustible y Humo MQ-2 Keyestudio

- **SKU Proveedor:** `KS0040` | **SKU Humm:** `HUMM-KEY-KS0040`
- **Nombre Comercial Humm:** **Sensor de Gas Combustible y Humo MQ-2 Keyestudio**
- **Categoría:** Sensores y módulos
- **Precio Referencial Sugerido:** **$10,999 CLP** (Costo Base: $4.70 USD)
- **Nivel de Complejidad / Uso:** `INTERMEDIO`
- **Compatibilidad Tecnológica Verificada:** `Arduino` *(respaldo fabricante)*
- **Compatibilidad Tecnológica Propuesta (Aula):** `Arduino, ESP32` *(interpretación pedagógica Humm)*
- **Contenido Real del Pack / Empaque:** 1 módulo MQ-2 con salidas analógica y digital.
- **Unidad de Medida:** `unidad`
- **Apto Potencial para Kit:** **Sí**
- **Estado de Curaduría:** `VALIDADO`
- **Estado Especificación Técnica Neutra:** `NO_REVISADO` *(validación técnica documental progresiva)*
- **Descripción Educativa (Humm):** Sensor electroquímico MQ-2 para experimentación y aprendizaje didáctico sobre detección de gases combustibles (GLP, metano) y humo en proyectos escolares de ciencias y automatización.
- **Posible Uso / Proyecto Escolar:** Maquetas de prevención de riesgos escolares, detectores de fugas en laboratorios y proyectos de seguridad ciudadana.
- **⚠️ Advertencia de Uso y Seguridad:** *Módulo para experimentación y aprendizaje didáctico sobre gases. No reemplaza un detector de gas certificado ni debe emplearse en sistemas críticos de prevención de incendios o fugas de gas.*
- **Observaciones y Trazabilidad:** Clasificación A. Requiere alimentación adecuada y precalentamiento operativo.

#### [14] `KS0028` — Módulo Sensor de Luz Fotorresistencia (LDR) Keyestudio

- **SKU Proveedor:** `KS0028` | **SKU Humm:** `HUMM-KEY-KS0028`
- **Nombre Comercial Humm:** **Módulo Sensor de Luz Fotorresistencia (LDR) Keyestudio**
- **Categoría:** Sensores y módulos
- **Precio Referencial Sugerido:** **$8,894 CLP** (Costo Base: $3.80 USD)
- **Nivel de Complejidad / Uso:** `INICIAL`
- **Compatibilidad Tecnológica Verificada:** `Otros` *(respaldo fabricante)*
- **Compatibilidad Tecnológica Propuesta (Aula):** `Arduino, micro:bit, ESP32` *(interpretación pedagógica Humm)*
- **Contenido Real del Pack / Empaque:** 1 módulo LDR con potenciómetro y salidas A0/D0.
- **Unidad de Medida:** `unidad`
- **Apto Potencial para Kit:** **Sí**
- **Estado de Curaduría:** `VALIDADO`
- **Estado Especificación Técnica Neutra:** `NO_REVISADO` *(validación técnica documental progresiva)*
- **Descripción Educativa (Humm):** Sensor de intensidad lumínica basado en una resistencia variable por luz (LDR), con circuito comparador para salida analógica proporcional y digital de umbral.
- **Posible Uso / Proyecto Escolar:** Alumbrado público inteligente, seguidores solares mecánicos y despertadores automáticos con luz natural.
- **Observaciones y Trazabilidad:** Clasificación A. Básico de alfabetización electrónica.

#### [15] `KS0105` — Sensor de Sonido Analógico Keyestudio EASY Plug (Conector RJ11)

- **SKU Proveedor:** `KS0105` | **SKU Humm:** `HUMM-KEY-KS0105`
- **Nombre Comercial Humm:** **Sensor de Sonido Analógico Keyestudio EASY Plug (Conector RJ11)**
- **Categoría:** Sensores y módulos
- **Precio Referencial Sugerido:** **$11,232 CLP** (Costo Base: $4.80 USD)
- **Nivel de Complejidad / Uso:** `INICIAL`
- **Compatibilidad Tecnológica Verificada:** `Arduino` *(respaldo fabricante)*
- **Compatibilidad Tecnológica Propuesta (Aula):** `Arduino` *(interpretación pedagógica Humm)*
- **Contenido Real del Pack / Empaque:** 1 módulo con micrófono y puerto telefónico RJ11 hembra integrado.
- **Unidad de Medida:** `unidad`
- **Apto Potencial para Kit:** **No**
- **Estado de Curaduría:** `VALIDADO`
- **Estado Especificación Técnica Neutra:** `NO_REVISADO` *(validación técnica documental progresiva)*
- **Descripción Educativa (Humm):** Sensor acústico con micrófono de condensador que detecta ondas sonoras y aplausos. Incorpora el conector tipo telefónico RJ11 de la serie EASY Plug para conexión rápida sin soldadura.
- **Posible Uso / Proyecto Escolar:** Interruptores activados por aplauso, monitores de nivel de ruido en salas de clases y alarmas acústicas.
- **Observaciones y Trazabilidad:** Clasificación B. Advertencia: conector RJ11 EASY Plug (requiere cable/shield RJ11).

#### [16] `KS0116` — Sensor de Llama Keyestudio EASY Plug (Conector RJ11)

- **SKU Proveedor:** `KS0116` | **SKU Humm:** `HUMM-KEY-KS0116`
- **Nombre Comercial Humm:** **Sensor de Llama Keyestudio EASY Plug (Conector RJ11)**
- **Categoría:** Sensores y módulos
- **Precio Referencial Sugerido:** **$11,232 CLP** (Costo Base: $4.80 USD)
- **Nivel de Complejidad / Uso:** `INICIAL`
- **Compatibilidad Tecnológica Verificada:** `Arduino` *(respaldo fabricante)*
- **Compatibilidad Tecnológica Propuesta (Aula):** `Arduino` *(interpretación pedagógica Humm)*
- **Contenido Real del Pack / Empaque:** 1 módulo sensor de llama con puerto RJ11 hembra.
- **Unidad de Medida:** `unidad`
- **Apto Potencial para Kit:** **No**
- **Estado de Curaduría:** `VALIDADO`
- **Estado Especificación Técnica Neutra:** `NO_REVISADO` *(validación técnica documental progresiva)*
- **Descripción Educativa (Humm):** Sensor óptico sensible a la radiación infrarroja de la llama, diseñado para robótica educativa móvil (robots apagafuegos didácticos) y experimentos de óptica.
- **Posible Uso / Proyecto Escolar:** Robots móviles apagafuegos, sistemas de alarma contra incendios y maquetas de seguridad escolar.
- **⚠️ Advertencia de Uso y Seguridad:** *Sensor óptico para detección experimental en robótica escolar y demostraciones de óptica. No constituye un sistema profesional de alarma contra incendios ni reemplaza detectores normados.*
- **Observaciones y Trazabilidad:** Clasificación B. Advertencia: conector RJ11 EASY Plug.

#### [17] `KS0050` — Sensor Seguidor de Línea Infrarrojo Keyestudio (Pines 2.54mm)

- **SKU Proveedor:** `KS0050` | **SKU Humm:** `HUMM-KEY-KS0050`
- **Nombre Comercial Humm:** **Sensor Seguidor de Línea Infrarrojo Keyestudio (Pines 2.54mm)**
- **Categoría:** Sensores y módulos
- **Precio Referencial Sugerido:** **$8,894 CLP** (Costo Base: $3.80 USD)
- **Nivel de Complejidad / Uso:** `INICIAL`
- **Compatibilidad Tecnológica Verificada:** `Arduino` *(respaldo fabricante)*
- **Compatibilidad Tecnológica Propuesta (Aula):** `Arduino, micro:bit, ESP32` *(interpretación pedagógica Humm)*
- **Contenido Real del Pack / Empaque:** 1 módulo óptico reflectivo con potenciómetro de umbral.
- **Unidad de Medida:** `unidad`
- **Apto Potencial para Kit:** **Sí**
- **Estado de Curaduría:** `VALIDADO`
- **Estado Especificación Técnica Neutra:** `NO_REVISADO` *(validación técnica documental progresiva)*
- **Descripción Educativa (Humm):** Sensor reflectivo infrarrojo que distingue superficies claras y oscuras según la cantidad de luz reflejada. Cuenta con pines estándar para cables Dupont comunes.
- **Posible Uso / Proyecto Escolar:** Construcción de autos seguidores de línea para ferias y competencias de robótica escolar.
- **Observaciones y Trazabilidad:** Clasificación A. Insumo básico de robótica móvil.

#### [18] `KS0120` — Sensor de Obstáculos Infrarrojo Keyestudio EASY Plug (Conector RJ11)

- **SKU Proveedor:** `KS0120` | **SKU Humm:** `HUMM-KEY-KS0120`
- **Nombre Comercial Humm:** **Sensor de Obstáculos Infrarrojo Keyestudio EASY Plug (Conector RJ11)**
- **Categoría:** Sensores y módulos
- **Precio Referencial Sugerido:** **$11,701 CLP** (Costo Base: $5.00 USD)
- **Nivel de Complejidad / Uso:** `INICIAL`
- **Compatibilidad Tecnológica Verificada:** `Arduino` *(respaldo fabricante)*
- **Compatibilidad Tecnológica Propuesta (Aula):** `Arduino` *(interpretación pedagógica Humm)*
- **Contenido Real del Pack / Empaque:** 1 módulo sensor de obstáculos con puerto RJ11 hembra.
- **Unidad de Medida:** `unidad`
- **Apto Potencial para Kit:** **No**
- **Estado de Curaduría:** `VALIDADO`
- **Estado Especificación Técnica Neutra:** `NO_REVISADO` *(validación técnica documental progresiva)*
- **Descripción Educativa (Humm):** Módulo de detección de obstáculos por proximidad infrarroja a corta distancia con ajuste por potenciómetro y conexión tipo telefónica RJ11 EASY Plug.
- **Posible Uso / Proyecto Escolar:** Prevención de colisiones en carritos robóticos y detección de paso de objetos en cintas transportadoras.
- **Observaciones y Trazabilidad:** Clasificación B. Advertencia: conector RJ11 EASY Plug.

#### [19] `19720010` — Sonda de Temperatura Sumergible en Acero Inoxidable DS18B20 (Cable 1m)

- **SKU Proveedor:** `19720010` | **SKU Humm:** `HUMM-KEY-19720010`
- **Nombre Comercial Humm:** **Sonda de Temperatura Sumergible en Acero Inoxidable DS18B20 (Cable 1m)**
- **Categoría:** Sensores y módulos
- **Precio Referencial Sugerido:** **$4,656 CLP** (Costo Base: $1.99 USD)
- **Nivel de Complejidad / Uso:** `INTERMEDIO`
- **Compatibilidad Tecnológica Verificada:** `Arduino` *(respaldo fabricante)*
- **Compatibilidad Tecnológica Propuesta (Aula):** `Arduino, micro:bit, ESP32, Raspberry Pi` *(interpretación pedagógica Humm)*
- **Contenido Real del Pack / Empaque:** 1 sonda sumergible de acero inoxidable con cable de 100 cm.
- **Unidad de Medida:** `unidad`
- **Apto Potencial para Kit:** **Sí**
- **Estado de Curaduría:** `VALIDADO`
- **Estado Especificación Técnica Neutra:** `NO_REVISADO` *(validación técnica documental progresiva)*
- **Descripción Educativa (Humm):** Sonda digital de temperatura impermeable sellada en tubo de acero inoxidable con cable de un metro. Utiliza protocolo 1-Wire para lectura precisa en líquidos.
- **Posible Uso / Proyecto Escolar:** Experimentos de temperatura de agua en química, acuarios escolares, estaciones de compostaje y medición de temperatura de suelos.
- **Observaciones y Trazabilidad:** Clasificación A. Requiere resistencia pull-up de 4.7kΩ para operar (no incluida en el cable desnudo).

#### [20] `KS6057` — Sensor Inercial IMU MPU6050 (Acelerómetro + Giroscopio) Formato Bloque

- **SKU Proveedor:** `KS6057` | **SKU Humm:** `HUMM-KEY-KS6057`
- **Nombre Comercial Humm:** **Sensor Inercial IMU MPU6050 (Acelerómetro + Giroscopio) Formato Bloque**
- **Categoría:** Sensores y módulos
- **Precio Referencial Sugerido:** **$12,871 CLP** (Costo Base: $5.50 USD)
- **Nivel de Complejidad / Uso:** `INTERMEDIO`
- **Compatibilidad Tecnológica Verificada:** `Arduino` *(respaldo fabricante)*
- **Compatibilidad Tecnológica Propuesta (Aula):** `Arduino, ESP32, micro:bit` *(interpretación pedagógica Humm)*
- **Contenido Real del Pack / Empaque:** 1 módulo MPU6050 en carcasa tipo bloque compatible con Lego.
- **Unidad de Medida:** `unidad`
- **Apto Potencial para Kit:** **Sí**
- **Estado de Curaduría:** `VALIDADO`
- **Estado Especificación Técnica Neutra:** `NO_REVISADO` *(validación técnica documental progresiva)*
- **Descripción Educativa (Humm):** Unidad de medición inercial de 6 grados de libertad (acelerómetro y giroscopio de 3 ejes con comunicación I2C) integrada en una carcasa de plástico compatible con piezas de construcción.
- **Posible Uso / Proyecto Escolar:** Enseñanza de cinemática, registro de aceleración en planos inclinados, péndulos físicos y robots de equilibrio.
- **Observaciones y Trazabilidad:** Clasificación A. Compatible mecánicamente con piezas de encastre tipo Lego.

#### [21] `KS0031` — Módulo Sensor Táctil Capacitivo Digital Keyestudio

- **SKU Proveedor:** `KS0031` | **SKU Humm:** `HUMM-KEY-KS0031`
- **Nombre Comercial Humm:** **Módulo Sensor Táctil Capacitivo Digital Keyestudio**
- **Categoría:** Sensores y módulos
- **Precio Referencial Sugerido:** **$8,894 CLP** (Costo Base: $3.80 USD)
- **Nivel de Complejidad / Uso:** `INICIAL`
- **Compatibilidad Tecnológica Verificada:** `Arduino` *(respaldo fabricante)*
- **Compatibilidad Tecnológica Propuesta (Aula):** `Arduino, micro:bit, ESP32` *(interpretación pedagógica Humm)*
- **Contenido Real del Pack / Empaque:** 1 módulo táctil capacitivo de 3 pines.
- **Unidad de Medida:** `unidad`
- **Apto Potencial para Kit:** **Sí**
- **Estado de Curaduría:** `VALIDADO`
- **Estado Especificación Técnica Neutra:** `NO_REVISADO` *(validación técnica documental progresiva)*
- **Descripción Educativa (Humm):** Interruptor táctil de estado sólido que detecta el contacto del dedo a través de superficies no metálicas (plástico, vidrio, madera delgada) sin piezas móviles.
- **Posible Uso / Proyecto Escolar:** Paneles de control modernos, pulsadores higiénicos y maquetas interactivas para exposiciones escolares.
- **Observaciones y Trazabilidad:** Clasificación A. Chip detector TTP223.

#### [22] `KS0048` — Módulo Sensor de Nivel de Agua y Detección de Gotas Keyestudio

- **SKU Proveedor:** `KS0048` | **SKU Humm:** `HUMM-KEY-KS0048`
- **Nombre Comercial Humm:** **Módulo Sensor de Nivel de Agua y Detección de Gotas Keyestudio**
- **Categoría:** Sensores y módulos
- **Precio Referencial Sugerido:** **$8,894 CLP** (Costo Base: $3.80 USD)
- **Nivel de Complejidad / Uso:** `INICIAL`
- **Compatibilidad Tecnológica Verificada:** `Arduino` *(respaldo fabricante)*
- **Compatibilidad Tecnológica Propuesta (Aula):** `Arduino, micro:bit, ESP32` *(interpretación pedagógica Humm)*
- **Contenido Real del Pack / Empaque:** 1 módulo con pistas conductoras expuestas.
- **Unidad de Medida:** `unidad`
- **Apto Potencial para Kit:** **Sí**
- **Estado de Curaduría:** `VALIDADO`
- **Estado Especificación Técnica Neutra:** `NO_REVISADO` *(validación técnica documental progresiva)*
- **Descripción Educativa (Humm):** Sensor analógico compuesto por pistas paralelas expuestas que varían su resistencia al entrar en contacto con agua líquida o gotas de lluvia.
- **Posible Uso / Proyecto Escolar:** Alarmas escolares contra inundaciones, medición de nivel de líquido en recipientes y detectores de lluvia para invernaderos.
- **Observaciones y Trazabilidad:** Clasificación A. Salida analógica proporcional al nivel de inmersión.

#### [23] `KS0494` — Sensor de Color I2C TCS34725 Keyestudio Honeycomb para micro:bit

- **SKU Proveedor:** `KS0494` | **SKU Humm:** `HUMM-KEY-KS0494`
- **Nombre Comercial Humm:** **Sensor de Color I2C TCS34725 Keyestudio Honeycomb para micro:bit**
- **Categoría:** Sensores y módulos
- **Precio Referencial Sugerido:** **$16,359 CLP** (Costo Base: $6.99 USD)
- **Nivel de Complejidad / Uso:** `INTERMEDIO`
- **Compatibilidad Tecnológica Verificada:** `micro:bit` *(respaldo fabricante)*
- **Compatibilidad Tecnológica Propuesta (Aula):** `micro:bit, Arduino` *(interpretación pedagógica Humm)*
- **Contenido Real del Pack / Empaque:** 1 módulo Honeycomb con sensor TCS34725 y orificios para caimanes.
- **Unidad de Medida:** `unidad`
- **Apto Potencial para Kit:** **Sí**
- **Estado de Curaduría:** `VALIDADO`
- **Estado Especificación Técnica Neutra:** `NO_REVISADO` *(validación técnica documental progresiva)*
- **Descripción Educativa (Humm):** Sensor óptico de color con iluminación LED incorporada que mide los componentes Rojo, Verde, Azul y Luz Blanca de objetos. Su formato Honeycomb permite conectarlo con pinzas cocodrilo a micro:bit.
- **Posible Uso / Proyecto Escolar:** Clasificadores automáticos de objetos por color, líneas de selección fabril a escala escolar y experimentos sobre óptica y reflexión.
- **Observaciones y Trazabilidad:** Clasificación B. Optimizado para micro:bit mediante pads Honeycomb para caimanes.

#### [24] `KS0492` — Sensor Magnético de Efecto Hall Keyestudio Honeycomb para micro:bit

- **SKU Proveedor:** `KS0492` | **SKU Humm:** `HUMM-KEY-KS0492`
- **Nombre Comercial Humm:** **Sensor Magnético de Efecto Hall Keyestudio Honeycomb para micro:bit**
- **Categoría:** Sensores y módulos
- **Precio Referencial Sugerido:** **$9,829 CLP** (Costo Base: $4.20 USD)
- **Nivel de Complejidad / Uso:** `INICIAL`
- **Compatibilidad Tecnológica Verificada:** `micro:bit` *(respaldo fabricante)*
- **Compatibilidad Tecnológica Propuesta (Aula):** `micro:bit, Arduino` *(interpretación pedagógica Humm)*
- **Contenido Real del Pack / Empaque:** 1 módulo Honeycomb con sensor Hall.
- **Unidad de Medida:** `unidad`
- **Apto Potencial para Kit:** **Sí**
- **Estado de Curaduría:** `VALIDADO`
- **Estado Especificación Técnica Neutra:** `NO_REVISADO` *(validación técnica documental progresiva)*
- **Descripción Educativa (Humm):** Sensor que detecta la presencia y polaridad de campos magnéticos sin contacto físico directo. Formato hexagonal con orificios amplios para cables con pinza caimán.
- **Posible Uso / Proyecto Escolar:** Tacómetros para medir velocidad de ruedas y aspas de molino, sensores de puerta abierta y experimentos de electromagnetismo.
- **Observaciones y Trazabilidad:** Clasificación B. Serie Honeycomb para micro:bit.

#### [25] `KS0272` — Sensor Piezoeléctrico Cerámico Analógico de Vibración Keyestudio

- **SKU Proveedor:** `KS0272` | **SKU Humm:** `HUMM-KEY-KS0272`
- **Nombre Comercial Humm:** **Sensor Piezoeléctrico Cerámico Analógico de Vibración Keyestudio**
- **Categoría:** Sensores y módulos
- **Precio Referencial Sugerido:** **$8,658 CLP** (Costo Base: $3.70 USD)
- **Nivel de Complejidad / Uso:** `INICIAL`
- **Compatibilidad Tecnológica Verificada:** `Arduino` *(respaldo fabricante)*
- **Compatibilidad Tecnológica Propuesta (Aula):** `Arduino, micro:bit, ESP32` *(interpretación pedagógica Humm)*
- **Contenido Real del Pack / Empaque:** 1 módulo con disco cerámico piezoeléctrico soldado.
- **Unidad de Medida:** `unidad`
- **Apto Potencial para Kit:** **Sí**
- **Estado de Curaduría:** `VALIDADO`
- **Estado Especificación Técnica Neutra:** `NO_REVISADO` *(validación técnica documental progresiva)*
- **Descripción Educativa (Humm):** Sensor de vibración que utiliza el efecto piezoeléctrico de un disco cerámico para generar un voltaje analógico proporcional a la magnitud del golpe, choque o deformación.
- **Posible Uso / Proyecto Escolar:** Construcción de sismógrafos escolares para registrar sismos simulados, instrumentos musicales electrónicos de percusión y alarmas contra golpes.
- **Observaciones y Trazabilidad:** Clasificación B. Corrección auditada: es sensor piezoeléctrico cerámico analógico (no es interruptor de resorte).

#### [26] `KS0171` — Sensor Óptico de Pulso Cardíaco XD-58C Keyestudio

- **SKU Proveedor:** `KS0171` | **SKU Humm:** `HUMM-KEY-KS0171`
- **Nombre Comercial Humm:** **Sensor Óptico de Pulso Cardíaco XD-58C Keyestudio**
- **Categoría:** Sensores y módulos
- **Precio Referencial Sugerido:** **$10,999 CLP** (Costo Base: $4.70 USD)
- **Nivel de Complejidad / Uso:** `INTERMEDIO`
- **Compatibilidad Tecnológica Verificada:** `Otros` *(respaldo fabricante)*
- **Compatibilidad Tecnológica Propuesta (Aula):** `Arduino, micro:bit, ESP32` *(interpretación pedagógica Humm)*
- **Contenido Real del Pack / Empaque:** 1 sensor de pulso con cinta de velcro y cable de conexión.
- **Unidad de Medida:** `unidad`
- **Apto Potencial para Kit:** **Sí**
- **Estado de Curaduría:** `VALIDADO`
- **Estado Especificación Técnica Neutra:** `NO_REVISADO` *(validación técnica documental progresiva)*
- **Descripción Educativa (Humm):** Sensor óptico de fotopletismografía para proyectos interdisciplinarios de Biología y Educación Física, orientado a experimentos didácticos de frecuencia cardíaca durante actividades escolares.
- **Posible Uso / Proyecto Escolar:** Proyectos interdisciplinarios de Biología y Educación Física para medir frecuencia cardíaca en reposo y tras actividad deportiva.
- **⚠️ Advertencia de Uso y Seguridad:** *Uso didáctico. Dispositivo diseñado exclusivamente para experimentos educativos de adquisición de señales fisiológicas. No es un dispositivo médico ni debe utilizarse para diagnóstico o monitoreo de salud real.*
- **Observaciones y Trazabilidad:** Clasificación A. Aplicación pedagógica en ciencias de la salud.

#### [27] `KS0047` — Sensor de Calidad de Aire MQ-135 Keyestudio

- **SKU Proveedor:** `KS0047` | **SKU Humm:** `HUMM-KEY-KS0047`
- **Nombre Comercial Humm:** **Sensor de Calidad de Aire MQ-135 Keyestudio**
- **Categoría:** Sensores y módulos
- **Precio Referencial Sugerido:** **$10,999 CLP** (Costo Base: $4.70 USD)
- **Nivel de Complejidad / Uso:** `INTERMEDIO`
- **Compatibilidad Tecnológica Verificada:** `Otros` *(respaldo fabricante)*
- **Compatibilidad Tecnológica Propuesta (Aula):** `Arduino, ESP32` *(interpretación pedagógica Humm)*
- **Contenido Real del Pack / Empaque:** 1 módulo sensor MQ-135.
- **Unidad de Medida:** `unidad`
- **Apto Potencial para Kit:** **Sí**
- **Estado de Curaduría:** `VALIDADO`
- **Estado Especificación Técnica Neutra:** `NO_REVISADO` *(validación técnica documental progresiva)*
- **Descripción Educativa (Humm):** Sensor MQ-135 para experimentación didáctica y proyectos escolares de ventilación ambiental en salas de clases y monitoreo del aire interior.
- **Posible Uso / Proyecto Escolar:** Semáforos de ventilación en salas de clases para prevenir acumulación de aire viciado y proyectos escolares de salud ambiental.
- **⚠️ Advertencia de Uso y Seguridad:** *Módulo para experimentación y aprendizaje didáctico sobre gases y calidad del aire. No reemplaza un sistema normado de monitoreo de seguridad ambiental ni detectores industriales certificados.*
- **Observaciones y Trazabilidad:** Clasificación A. Requiere tiempo de calentamiento del elemento calefactor interno.

#### [28] `KS0275` — Módulo Divisor de Tensión para Medición de Voltaje (Hasta 25V) Keyestudio

- **SKU Proveedor:** `KS0275` | **SKU Humm:** `HUMM-KEY-KS0275`
- **Nombre Comercial Humm:** **Módulo Divisor de Tensión para Medición de Voltaje (Hasta 25V) Keyestudio**
- **Categoría:** Sensores y módulos
- **Precio Referencial Sugerido:** **$8,894 CLP** (Costo Base: $3.80 USD)
- **Nivel de Complejidad / Uso:** `INICIAL`
- **Compatibilidad Tecnológica Verificada:** `Arduino` *(respaldo fabricante)*
- **Compatibilidad Tecnológica Propuesta (Aula):** `Arduino, ESP32, micro:bit` *(interpretación pedagógica Humm)*
- **Contenido Real del Pack / Empaque:** 1 módulo divisor resistivo con bornera y cabezal de 3 pines.
- **Unidad de Medida:** `unidad`
- **Apto Potencial para Kit:** **Sí**
- **Estado de Curaduría:** `VALIDADO`
- **Estado Especificación Técnica Neutra:** `NO_REVISADO` *(validación técnica documental progresiva)*
- **Descripción Educativa (Humm):** Módulo con divisor resistivo de precisión (factor 5:1) que permite medir voltajes de corriente continua de hasta 25V utilizando entradas analógicas seguras de 5V.
- **Posible Uso / Proyecto Escolar:** Monitoreo del voltaje generado por paneles solares escolares, control del estado de carga de baterías y enseñanza práctica de la Ley de Ohm.
- **Observaciones y Trazabilidad:** Clasificación A. Factor 5 a 1.

---

### Robótica y vehículos (4 productos)

#### [29] `CR0011` — Chasis de Robot Móvil 4WD con 4 Motores DC y Encoders (Sin Microcontrolador)

- **SKU Proveedor:** `CR0011` | **SKU Humm:** `HUMM-KEY-CR0011`
- **Nombre Comercial Humm:** **Chasis de Robot Móvil 4WD con 4 Motores DC y Encoders (Sin Microcontrolador)**
- **Categoría:** Robótica y vehículos
- **Precio Referencial Sugerido:** **$39,783 CLP** (Costo Base: $17.00 USD)
- **Nivel de Complejidad / Uso:** `INTERMEDIO`
- **Compatibilidad Tecnológica Verificada:** `Arduino` *(respaldo fabricante)*
- **Compatibilidad Tecnológica Propuesta (Aula):** `Arduino, ESP32, micro:bit, Raspberry Pi` *(interpretación pedagógica Humm)*
- **Contenido Real del Pack / Empaque:** Kit chasis acrílico: 4 motores DC con caja reductora, 4 ruedas de goma, 4 discos encoder ópticos, portapilas y tornillos. NO incluye placa de control ni drivers.
- **Unidad de Medida:** `unidad`
- **Apto Potencial para Kit:** **Sí**
- **Estado de Curaduría:** `VALIDADO`
- **Estado Especificación Técnica Neutra:** `NO_REVISADO` *(validación técnica documental progresiva)*
- **Descripción Educativa (Humm):** Plataforma mecánica de robótica móvil con tracción independiente en las 4 ruedas y discos de codificación óptica para medición de velocidad y distancia.
- **Posible Uso / Proyecto Escolar:** Enseñanza de cinemática de vehículos terrestres, robótica autónoma, control por Bluetooth y evasión de obstáculos con ultrasonido.
- **⚠️ Advertencia de Uso y Seguridad:** *Verificar la polaridad de las baterías en el portapilas para evitar daños en los controladores o sobrecalentamiento del cableado.*
- **Observaciones y Trazabilidad:** Clasificación A. Chasis mecánico: la electrónica de control se adquiere por separado.

#### [30] `CR0019` — Chasis de Robot Móvil 2WD de Dos Niveles con Rueda Loca (Sin Microcontrolador)

- **SKU Proveedor:** `CR0019` | **SKU Humm:** `HUMM-KEY-CR0019`
- **Nombre Comercial Humm:** **Chasis de Robot Móvil 2WD de Dos Niveles con Rueda Loca (Sin Microcontrolador)**
- **Categoría:** Robótica y vehículos
- **Precio Referencial Sugerido:** **$35,080 CLP** (Costo Base: $14.99 USD)
- **Nivel de Complejidad / Uso:** `INICIAL`
- **Compatibilidad Tecnológica Verificada:** `Arduino` *(respaldo fabricante)*
- **Compatibilidad Tecnológica Propuesta (Aula):** `Arduino, micro:bit, ESP32, Raspberry Pi` *(interpretación pedagógica Humm)*
- **Contenido Real del Pack / Empaque:** Kit chasis 2 niveles de acrílico: 2 motores DC con reductora, 2 ruedas, 1 rueda loca giratoria, portapilas y tornillería. NO incluye tarjeta de control.
- **Unidad de Medida:** `unidad`
- **Apto Potencial para Kit:** **Sí**
- **Estado de Curaduría:** `VALIDADO`
- **Estado Especificación Técnica Neutra:** `NO_REVISADO` *(validación técnica documental progresiva)*
- **Descripción Educativa (Humm):** Plataforma móvil clásica de tracción diferencial con dos ruedas motrices y una rueda loca de apoyo. Su estructura de doble piso ofrece espacio amplio para colocar placas y baterías.
- **Posible Uso / Proyecto Escolar:** Iniciación a la robótica móvil escolar, algoritmos de navegación por giros diferenciales y seguidores de línea.
- **⚠️ Advertencia de Uso y Seguridad:** *Comprobar la polaridad de las baterías antes de encender el interruptor para prevenir cortocircuitos en el chasis móvil.*
- **Observaciones y Trazabilidad:** Clasificación A. Opción accesible y ágil para colegios.

#### [31] `CR0033 CR0034` — Chasis de Aluminio 4WD con Ruedas Mecanum para Arduino y Raspberry Pi

- **SKU Proveedor:** `CR0033 CR0034` | **SKU Humm:** `HUMM-KEY-CR0033 CR0034`
- **Nombre Comercial Humm:** **Chasis de Aluminio 4WD con Ruedas Mecanum para Arduino y Raspberry Pi**
- **Categoría:** Robótica y vehículos
- **Precio Referencial Sugerido:** **$50,546 CLP** (Costo Base: $21.60 USD)
- **Nivel de Complejidad / Uso:** `AVANZADO`
- **Compatibilidad Tecnológica Verificada:** `Arduino, Raspberry Pi` *(respaldo fabricante)*
- **Compatibilidad Tecnológica Propuesta (Aula):** `Arduino, Raspberry Pi` *(interpretación pedagógica Humm)*
- **Contenido Real del Pack / Empaque:** Chasis metálico de aleación de aluminio: 4 motores DC con reductora y 4 ruedas Mecanum omnidireccionales especiales. NO incluye controlador.
- **Unidad de Medida:** `unidad`
- **Apto Potencial para Kit:** **Sí**
- **Estado de Curaduría:** `VALIDADO`
- **Estado Especificación Técnica Neutra:** `NO_REVISADO` *(validación técnica documental progresiva)*
- **Descripción Educativa (Humm):** Chasis reforzado con cuatro ruedas omnidireccionales Mecanum que permiten movimiento holonómico: avance hacia adelante, atrás, diagonal y traslación lateral sin girar la orientación del chasis.
- **Posible Uso / Proyecto Escolar:** Robótica competitiva avanzada, algoritmos de cinemática omnidireccional y navegación en espacios reducidos con visión por computador.
- **⚠️ Advertencia de Uso y Seguridad:** *Verificar la correcta polaridad de conexión de las baterías y asegurar la firmeza mecánica de los motores antes de pruebas de desplazamiento lateral.*
- **Observaciones y Trazabilidad:** Clasificación B. Corrección auditada: compatibilidad con Arduino y Raspberry Pi (eliminado micro:bit).

#### [32] `KS4039` — Brazo Robótico 4DOF para micro:bit — Sin Placa micro:bit

- **SKU Proveedor:** `KS4039` | **SKU Humm:** `HUMM-KEY-KS4039`
- **Nombre Comercial Humm:** **Brazo Robótico 4DOF para micro:bit — Sin Placa micro:bit**
- **Categoría:** Robótica y vehículos
- **Precio Referencial Sugerido:** **$98,286 CLP** (Costo Base: $42.00 USD)
- **Nivel de Complejidad / Uso:** `INTERMEDIO`
- **Compatibilidad Tecnológica Verificada:** `micro:bit` *(respaldo fabricante)*
- **Compatibilidad Tecnológica Propuesta (Aula):** `micro:bit` *(interpretación pedagógica Humm)*
- **Contenido Real del Pack / Empaque:** Kit de piezas estructurales de brazo 4DOF, 4 servomotores, placa shield de expansión para micro:bit y tornillería. NO INCLUYE LA TARJETA MICRO:BIT.
- **Unidad de Medida:** `unidad`
- **Apto Potencial para Kit:** **Sí**
- **Estado de Curaduría:** `VALIDADO`
- **Estado Especificación Técnica Neutra:** `NO_REVISADO` *(validación técnica documental progresiva)*
- **Descripción Educativa (Humm):** Manipulador robótico articulado de 4 grados de libertad con pinza de agarre, diseñado específicamente para conectarse y programarse con una tarjeta BBC micro:bit.
- **Posible Uso / Proyecto Escolar:** Simulación de brazos industriales de clasificación, trigonometría aplicada, robótica espacial y automatización de cadenas de montaje.
- **Observaciones y Trazabilidad:** Clasificación B. Corrección auditada: diseñado para micro:bit (no Arduino). Indicar explícitamente que no incluye la tarjeta micro:bit.

---

### Motores y movimiento (5 productos)

#### [33] `KS0326` — Pack de 3 Servomotores Micro SG90 9g Keyestudio

- **SKU Proveedor:** `KS0326` | **SKU Humm:** `HUMM-KEY-KS0326`
- **Nombre Comercial Humm:** **Pack de 3 Servomotores Micro SG90 9g Keyestudio**
- **Categoría:** Motores y movimiento
- **Precio Referencial Sugerido:** **$21,039 CLP** (Costo Base: $8.99 USD)
- **Nivel de Complejidad / Uso:** `INICIAL`
- **Compatibilidad Tecnológica Verificada:** `Arduino` *(respaldo fabricante)*
- **Compatibilidad Tecnológica Propuesta (Aula):** `Arduino, micro:bit, ESP32, Raspberry Pi` *(interpretación pedagógica Humm)*
- **Contenido Real del Pack / Empaque:** Pack con exactamente 3 servomotores SG90 9g con sus respectivos juegos de brazos de plástico y tornillos.
- **Unidad de Medida:** `pack (3 unidades)`
- **Apto Potencial para Kit:** **Sí**
- **Estado de Curaduría:** `VALIDADO`
- **Estado Especificación Técnica Neutra:** `NO_REVISADO` *(validación técnica documental progresiva)*
- **Descripción Educativa (Humm):** Microactuadores rotativos estándar con engranajes internos y control de posición angular de 0° a 180° mediante modulación por ancho de pulso (PWM).
- **Posible Uso / Proyecto Escolar:** Mecanismos articulados, barreras de peaje automáticas, apertura de compuertas en maquetas y articulaciones robóticas livianas.
- **Observaciones y Trazabilidad:** Clasificación B. Corrección de pack: el precio corresponde al conjunto de 3 unidades.

#### [34] `OR0428` — Servomotor de Rotación Continua 360° en Bloque Compatible Lego

- **SKU Proveedor:** `OR0428` | **SKU Humm:** `HUMM-KEY-OR0428`
- **Nombre Comercial Humm:** **Servomotor de Rotación Continua 360° en Bloque Compatible Lego**
- **Categoría:** Motores y movimiento
- **Precio Referencial Sugerido:** **$19,658 CLP** (Costo Base: $8.40 USD)
- **Nivel de Complejidad / Uso:** `INICIAL`
- **Compatibilidad Tecnológica Verificada:** `Arduino` *(respaldo fabricante)*
- **Compatibilidad Tecnológica Propuesta (Aula):** `Arduino, micro:bit, ESP32` *(interpretación pedagógica Humm)*
- **Contenido Real del Pack / Empaque:** 1 servomotor de rotación continua 360° encapsulado en carcasa tipo bloque Lego.
- **Unidad de Medida:** `unidad`
- **Apto Potencial para Kit:** **Sí**
- **Estado de Curaduría:** `VALIDADO`
- **Estado Especificación Técnica Neutra:** `NO_REVISADO` *(validación técnica documental progresiva)*
- **Descripción Educativa (Humm):** Actuador motorizado donde la señal PWM controla la velocidad y sentido de giro continuo en lugar del ángulo fijo. Su carcasa exterior permite encastre directo con piezas tipo Lego.
- **Posible Uso / Proyecto Escolar:** Tracción directa de ruedas en autos robóticos modulares, molinos, cintas transportadoras y mecanismos giratorios continuos.
- **Observaciones y Trazabilidad:** Clasificación A. Rotación continua 360° con encastre mecánico estándar.

#### [35] `KS0140` — Motor Paso a Paso 28BYJ-48 (5V) con Módulo Controlador ULN2003

- **SKU Proveedor:** `KS0140` | **SKU Humm:** `HUMM-KEY-KS0140`
- **Nombre Comercial Humm:** **Motor Paso a Paso 28BYJ-48 (5V) con Módulo Controlador ULN2003**
- **Categoría:** Motores y movimiento
- **Precio Referencial Sugerido:** **$14,041 CLP** (Costo Base: $6.00 USD)
- **Nivel de Complejidad / Uso:** `INTERMEDIO`
- **Compatibilidad Tecnológica Verificada:** `Otros` *(respaldo fabricante)*
- **Compatibilidad Tecnológica Propuesta (Aula):** `Arduino, Raspberry Pi, ESP32` *(interpretación pedagógica Humm)*
- **Contenido Real del Pack / Empaque:** 1 motor paso a paso 28BYJ-48 de 5V + 1 módulo controlador ULN2003 con 4 LEDs de estado.
- **Unidad de Medida:** `set (2 piezas)`
- **Apto Potencial para Kit:** **Sí**
- **Estado de Curaduría:** `VALIDADO`
- **Estado Especificación Técnica Neutra:** `NO_REVISADO` *(validación técnica documental progresiva)*
- **Descripción Educativa (Humm):** Sistema de posicionamiento angular preciso compuesto por un motor paso a paso con reductora interna y su placa excitadora basada en el array Darlington ULN2003.
- **Posible Uso / Proyecto Escolar:** Enseñanza de control angular discreto, posicionamiento de punteros de reloj, escáneres giratorios y dosificadores automáticos.
- **Observaciones y Trazabilidad:** Clasificación A. Set completo motor + driver.

#### [36] `MD0140` — Módulo Controlador Dual de Motores DC Puente H L9110S

- **SKU Proveedor:** `MD0140` | **SKU Humm:** `HUMM-KEY-MD0140`
- **Nombre Comercial Humm:** **Módulo Controlador Dual de Motores DC Puente H L9110S**
- **Categoría:** Motores y movimiento
- **Precio Referencial Sugerido:** **$6,785 CLP** (Costo Base: $2.90 USD)
- **Nivel de Complejidad / Uso:** `INICIAL`
- **Compatibilidad Tecnológica Verificada:** `Arduino` *(respaldo fabricante)*
- **Compatibilidad Tecnológica Propuesta (Aula):** `Arduino, micro:bit, ESP32, Raspberry Pi` *(interpretación pedagógica Humm)*
- **Contenido Real del Pack / Empaque:** 1 módulo driver L9110S con borneras para motores.
- **Unidad de Medida:** `unidad`
- **Apto Potencial para Kit:** **Sí**
- **Estado de Curaduría:** `VALIDADO`
- **Estado Especificación Técnica Neutra:** `NO_REVISADO` *(validación técnica documental progresiva)*
- **Descripción Educativa (Humm):** Controlador de potencia compacto basado en chips L9110 que permite controlar el sentido de giro y la velocidad (PWM) de 2 motores DC independientes o 1 motor paso a paso bipolar.
- **Posible Uso / Proyecto Escolar:** Manejo de tracción de carritos robóticos escolares de dos motores sin disipadores voluminosos.
- **Observaciones y Trazabilidad:** Clasificación A. Económico y de bajo consumo.

#### [37] `KS0057` — Módulo de 2 Relés con Optoacoplador (5V) Keyestudio

- **SKU Proveedor:** `KS0057` | **SKU Humm:** `HUMM-KEY-KS0057`
- **Nombre Comercial Humm:** **Módulo de 2 Relés con Optoacoplador (5V) Keyestudio**
- **Categoría:** Motores y movimiento
- **Precio Referencial Sugerido:** **$15,913 CLP** (Costo Base: $6.80 USD)
- **Nivel de Complejidad / Uso:** `INTERMEDIO`
- **Compatibilidad Tecnológica Verificada:** `Arduino, Otros` *(respaldo fabricante)*
- **Compatibilidad Tecnológica Propuesta (Aula):** `Arduino, ESP32, micro:bit, Raspberry Pi` *(interpretación pedagógica Humm)*
- **Contenido Real del Pack / Empaque:** 1 módulo con 2 relés electromecánicos y aislamiento por optoacoplador.
- **Unidad de Medida:** `unidad`
- **Apto Potencial para Kit:** **Sí**
- **Estado de Curaduría:** `VALIDADO`
- **Estado Especificación Técnica Neutra:** `NO_REVISADO` *(validación técnica documental progresiva)*
- **Descripción Educativa (Humm):** Módulo de 2 relés con optoacoplador para control de cargas de baja tensión en proyectos escolares de automatización, riego y domótica.
- **Posible Uso / Proyecto Escolar:** Automatización de riego en huertos escolares, control de iluminación de maquetas y conmutación de artefactos eléctricos en proyectos domóticos.
- **⚠️ Advertencia de Uso y Seguridad:** *Recomendado para proyectos escolares con cargas de baja tensión (baterías, bombas de 5V o 12V). El trabajo con tensión de red domiciliaria (220V) no es apto para manipulación directa por estudiantes y requiere personal competente con supervisión técnica adecuada.*
- **Observaciones y Trazabilidad:** Clasificación A. Aislamiento óptico para proteger el microcontrolador.

---

### Electrónica y prototipado (8 productos)

#### [38] `60320025` — Protoboard Transparente de 830 Puntos de Contacto

- **SKU Proveedor:** `60320025` | **SKU Humm:** `HUMM-KEY-60320025`
- **Nombre Comercial Humm:** **Protoboard Transparente de 830 Puntos de Contacto**
- **Categoría:** Electrónica y prototipado
- **Precio Referencial Sugerido:** **$5,802 CLP** (Costo Base: $2.48 USD)
- **Nivel de Complejidad / Uso:** `INICIAL`
- **Compatibilidad Tecnológica Verificada:** `Otros` *(respaldo fabricante)*
- **Compatibilidad Tecnológica Propuesta (Aula):** `Otros` *(interpretación pedagógica Humm)*
- **Contenido Real del Pack / Empaque:** 1 protoboard de 830 contactos (165 x 55 mm) con cuerpo transparente y bandas de alimentación.
- **Unidad de Medida:** `unidad`
- **Apto Potencial para Kit:** **Sí**
- **Estado de Curaduría:** `VALIDADO`
- **Estado Especificación Técnica Neutra:** `NO_REVISADO` *(validación técnica documental progresiva)*
- **Descripción Educativa (Humm):** Placa de inserción sin soldadura de tamaño estándar para montaje de circuitos medianos y grandes. Su acabado transparente permite apreciar la estructura interna de los contactos metálicos.
- **Posible Uso / Proyecto Escolar:** Insumo universal para prácticas de laboratorio de física y tecnología, montaje de circuitos con compuertas lógicas, transistores y microcontroladores.
- **Observaciones y Trazabilidad:** Clasificación A. Insumo de primera necesidad.

#### [39] `KS0331` — Pack de 3 Protoboards de 400 Puntos Keyestudio

- **SKU Proveedor:** `KS0331` | **SKU Humm:** `HUMM-KEY-KS0331`
- **Nombre Comercial Humm:** **Pack de 3 Protoboards de 400 Puntos Keyestudio**
- **Categoría:** Electrónica y prototipado
- **Precio Referencial Sugerido:** **$21,039 CLP** (Costo Base: $8.99 USD)
- **Nivel de Complejidad / Uso:** `INICIAL`
- **Compatibilidad Tecnológica Verificada:** `Otros` *(respaldo fabricante)*
- **Compatibilidad Tecnológica Propuesta (Aula):** `Otros` *(interpretación pedagógica Humm)*
- **Contenido Real del Pack / Empaque:** Pack con exactamente 3 protoboards de 400 puntos en empaques individuales Keyestudio.
- **Unidad de Medida:** `pack (3 unidades)`
- **Apto Potencial para Kit:** **Sí**
- **Estado de Curaduría:** `VALIDADO`
- **Estado Especificación Técnica Neutra:** `NO_REVISADO` *(validación técnica documental progresiva)*
- **Descripción Educativa (Humm):** Placas de pruebas medianas de 400 contactos con dos pistas de alimentación laterales. Su tamaño equilibrado es ideal para puestos individuales de trabajo escolar.
- **Posible Uso / Proyecto Escolar:** Prácticas de laboratorio individuales donde el espacio del mesón es acotado; proyectos con Arduino Nano y módulos de sensores.
- **Observaciones y Trazabilidad:** Clasificación B. Corrección de pack: el precio corresponde a 3 unidades de 400 puntos.

#### [40] `KT0072` — Set de 120 Cables de Conexión Dupont de 10 cm (M-M, M-H, H-H)

- **SKU Proveedor:** `KT0072` | **SKU Humm:** `HUMM-KEY-KT0072`
- **Nombre Comercial Humm:** **Set de 120 Cables de Conexión Dupont de 10 cm (M-M, M-H, H-H)**
- **Categoría:** Electrónica y prototipado
- **Precio Referencial Sugerido:** **$6,998 CLP** (Costo Base: $2.99 USD)
- **Nivel de Complejidad / Uso:** `INICIAL`
- **Compatibilidad Tecnológica Verificada:** `Arduino, Otros` *(respaldo fabricante)*
- **Compatibilidad Tecnológica Propuesta (Aula):** `Otros, Arduino, micro:bit, Raspberry Pi, ESP32` *(interpretación pedagógica Humm)*
- **Contenido Real del Pack / Empaque:** Set de 120 cables dividido en 3 cintas de 40 vías: 40 Macho-Macho, 40 Macho-Hembra y 40 Hembra-Hembra.
- **Unidad de Medida:** `set (120 cables)`
- **Apto Potencial para Kit:** **Sí**
- **Estado de Curaduría:** `VALIDADO`
- **Estado Especificación Técnica Neutra:** `NO_REVISADO` *(validación técnica documental progresiva)*
- **Descripción Educativa (Humm):** Cables flexibles con terminales normalizados de 2.54 mm en las tres combinaciones posibles, indispensables para conectar microcontroladores, protoboards y sensores.
- **Posible Uso / Proyecto Escolar:** Interconexión general en todo tipo de proyectos de aula sin necesidad de soldadura ni herramientas complejas.
- **Observaciones y Trazabilidad:** Clasificación A. Insumo indispensable para todo laboratorio.

#### [41] `KT0065` — Set de 120 Cables de Conexión Dupont Largos de 30 cm (M-M, M-H, H-H)

- **SKU Proveedor:** `KT0065` | **SKU Humm:** `HUMM-KEY-KT0065`
- **Nombre Comercial Humm:** **Set de 120 Cables de Conexión Dupont Largos de 30 cm (M-M, M-H, H-H)**
- **Categoría:** Electrónica y prototipado
- **Precio Referencial Sugerido:** **$8,894 CLP** (Costo Base: $3.80 USD)
- **Nivel de Complejidad / Uso:** `INICIAL`
- **Compatibilidad Tecnológica Verificada:** `Arduino, Otros` *(respaldo fabricante)*
- **Compatibilidad Tecnológica Propuesta (Aula):** `Otros, Arduino, micro:bit, Raspberry Pi, ESP32` *(interpretación pedagógica Humm)*
- **Contenido Real del Pack / Empaque:** Set de 120 cables largos de 30 cm (40 M-M, 40 M-H, 40 H-H).
- **Unidad de Medida:** `set (120 cables)`
- **Apto Potencial para Kit:** **Sí**
- **Estado de Curaduría:** `VALIDADO`
- **Estado Especificación Técnica Neutra:** `NO_REVISADO` *(validación técnica documental progresiva)*
- **Descripción Educativa (Humm):** Cables de puente de longitud extendida (30 cm) diseñados para unir componentes distantes en maquetas arquitectónicas, brazos robóticos o chasis grandes.
- **Posible Uso / Proyecto Escolar:** Conexión de sensores y actuadores situados en extremos de maquetas, brazos mecánicos y autos robóticos donde los cables comunes de 10 o 20 cm quedan cortos.
- **Observaciones y Trazabilidad:** Clasificación A. Longitud de 30 cm.

#### [42] `KS0014` — Módulo Potenciómetro Rotativo Analógico 10k Keyestudio

- **SKU Proveedor:** `KS0014` | **SKU Humm:** `HUMM-KEY-KS0014`
- **Nombre Comercial Humm:** **Módulo Potenciómetro Rotativo Analógico 10k Keyestudio**
- **Categoría:** Electrónica y prototipado
- **Precio Referencial Sugerido:** **$9,361 CLP** (Costo Base: $4.00 USD)
- **Nivel de Complejidad / Uso:** `INICIAL`
- **Compatibilidad Tecnológica Verificada:** `Arduino` *(respaldo fabricante)*
- **Compatibilidad Tecnológica Propuesta (Aula):** `Arduino, Otros` *(interpretación pedagógica Humm)*
- **Contenido Real del Pack / Empaque:** 1 módulo potenciómetro de 10k lineal con perilla y conector de 3 pines.
- **Unidad de Medida:** `unidad`
- **Apto Potencial para Kit:** **Sí**
- **Estado de Curaduría:** `VALIDADO`
- **Estado Especificación Técnica Neutra:** `NO_REVISADO` *(validación técnica documental progresiva)*
- **Descripción Educativa (Humm):** Resistencia variable de giro continuo con perilla plástica montada en PCB con cabezal de 3 pines, facilitando su conexión analógica sin soldar resistencias adicionales.
- **Posible Uso / Proyecto Escolar:** Control manual de brillo de LEDs, regulación de volumen sonoro, control de velocidad de motores y enseñanza de entradas analógicas.
- **Observaciones y Trazabilidad:** Clasificación A. Básico de interacción física.

#### [43] `KS0029` — Módulo Pulsador Digital de Botón Momentáneo Keyestudio

- **SKU Proveedor:** `KS0029` | **SKU Humm:** `HUMM-KEY-KS0029`
- **Nombre Comercial Humm:** **Módulo Pulsador Digital de Botón Momentáneo Keyestudio**
- **Categoría:** Electrónica y prototipado
- **Precio Referencial Sugerido:** **$8,894 CLP** (Costo Base: $3.80 USD)
- **Nivel de Complejidad / Uso:** `INICIAL`
- **Compatibilidad Tecnológica Verificada:** `Arduino` *(respaldo fabricante)*
- **Compatibilidad Tecnológica Propuesta (Aula):** `Arduino, Otros` *(interpretación pedagógica Humm)*
- **Contenido Real del Pack / Empaque:** 1 módulo pulsador con botón de tacto y resistencia integrada.
- **Unidad de Medida:** `unidad`
- **Apto Potencial para Kit:** **Sí**
- **Estado de Curaduría:** `VALIDADO`
- **Estado Especificación Técnica Neutra:** `NO_REVISADO` *(validación técnica documental progresiva)*
- **Descripción Educativa (Humm):** Pulsador montado en tarjeta modular con resistencia de polarización integrada, entregando una señal limpia (HIGH/LOW) sin riesgo de lecturas flotantes.
- **Posible Uso / Proyecto Escolar:** Botones de inicio/parada de máquinas, pulsadores para timbres escolares y botones de respuesta para concursos de preguntas en el aula.
- **Observaciones y Trazabilidad:** Clasificación A. Señal digital estable sin circuito antirrebote externo.

#### [44] `KS0018` — Módulo Zumbador Activo (Buzzer) de Señal Acústica Directa Keyestudio

- **SKU Proveedor:** `KS0018` | **SKU Humm:** `HUMM-KEY-KS0018`
- **Nombre Comercial Humm:** **Módulo Zumbador Activo (Buzzer) de Señal Acústica Directa Keyestudio**
- **Categoría:** Electrónica y prototipado
- **Precio Referencial Sugerido:** **$8,894 CLP** (Costo Base: $3.80 USD)
- **Nivel de Complejidad / Uso:** `INICIAL`
- **Compatibilidad Tecnológica Verificada:** `Arduino` *(respaldo fabricante)*
- **Compatibilidad Tecnológica Propuesta (Aula):** `Arduino, micro:bit, ESP32, Raspberry Pi` *(interpretación pedagógica Humm)*
- **Contenido Real del Pack / Empaque:** 1 módulo con zumbador activo piezoeléctrico.
- **Unidad de Medida:** `unidad`
- **Apto Potencial para Kit:** **Sí**
- **Estado de Curaduría:** `VALIDADO`
- **Estado Especificación Técnica Neutra:** `NO_REVISADO` *(validación técnica documental progresiva)*
- **Descripción Educativa (Humm):** Emisor acústico con oscilador interno incorporado que produce un tono sonoro continuo con solo aplicar una señal digital HIGH (5V), sin necesidad de generar ondas de frecuencia por código.
- **Posible Uso / Proyecto Escolar:** Señalización sonora de advertencia, avisadores de fin de proceso, alarmas escolares y timbres de puerta.
- **Observaciones y Trazabilidad:** Clasificación A. Zumbador activo (no requiere modulación por tonos).

#### [45] `KS0332` — Set de Prototipado 3 en 1: Fuente 3.3V/5V + Protoboard 830 Pts + 65 Cables

- **SKU Proveedor:** `KS0332` | **SKU Humm:** `HUMM-KEY-KS0332`
- **Nombre Comercial Humm:** **Set de Prototipado 3 en 1: Fuente 3.3V/5V + Protoboard 830 Pts + 65 Cables**
- **Categoría:** Electrónica y prototipado
- **Precio Referencial Sugerido:** **$25,719 CLP** (Costo Base: $10.99 USD)
- **Nivel de Complejidad / Uso:** `INICIAL`
- **Compatibilidad Tecnológica Verificada:** `Arduino, Otros` *(respaldo fabricante)*
- **Compatibilidad Tecnológica Propuesta (Aula):** `Otros, Arduino` *(interpretación pedagógica Humm)*
- **Contenido Real del Pack / Empaque:** 1 módulo de alimentación regulada para protoboard (3.3V/5V) + 1 protoboard de 830 puntos + 1 set de 65 cables flexibles de distintos largos.
- **Unidad de Medida:** `set (3 piezas)`
- **Apto Potencial para Kit:** **Sí**
- **Estado de Curaduría:** `VALIDADO`
- **Estado Especificación Técnica Neutra:** `NO_REVISADO` *(validación técnica documental progresiva)*
- **Descripción Educativa (Humm):** Conjunto integral para montaje de circuitos experimentales con fuente de alimentación regulable que se inserta directamente en los buses de la protoboard.
- **Posible Uso / Proyecto Escolar:** Equipamiento de mesas de trabajo en laboratorios de ciencias y tecnología, permitiendo alimentar circuitos con 3.3V o 5V de manera independiente.
- **⚠️ Advertencia de Uso y Seguridad:** *Verificar la correcta polaridad de conexión de baterías y fuentes de alimentación para evitar sobrecalentamiento o cortocircuitos accidentales en el banco de prototipo.*
- **Observaciones y Trazabilidad:** Clasificación A. Excelente relación costo/beneficio para equipamiento de bancos de trabajo.

---

### Pantallas e interacción (6 productos)

#### [46] `KS0061` — Pantalla LCD 1602 con Módulo I2C Integrado (Fondo Azul) Keyestudio

- **SKU Proveedor:** `KS0061` | **SKU Humm:** `HUMM-KEY-KS0061`
- **Nombre Comercial Humm:** **Pantalla LCD 1602 con Módulo I2C Integrado (Fondo Azul) Keyestudio**
- **Categoría:** Pantallas e interacción
- **Precio Referencial Sugerido:** **$17,551 CLP** (Costo Base: $7.50 USD)
- **Nivel de Complejidad / Uso:** `INICIAL`
- **Compatibilidad Tecnológica Verificada:** `Arduino` *(respaldo fabricante)*
- **Compatibilidad Tecnológica Propuesta (Aula):** `Arduino, ESP32, Raspberry Pi, micro:bit` *(interpretación pedagógica Humm)*
- **Contenido Real del Pack / Empaque:** 1 pantalla LCD 16x2 con interfaz I2C soldada en la parte posterior.
- **Unidad de Medida:** `unidad`
- **Apto Potencial para Kit:** **Sí**
- **Estado de Curaduría:** `VALIDADO`
- **Estado Especificación Técnica Neutra:** `NO_REVISADO` *(validación técnica documental progresiva)*
- **Descripción Educativa (Humm):** Pantalla alfanumérica de 2 líneas por 16 caracteres con fondo azul retroiluminado. Incorpora módulo I2C que reduce el cableado a solo 4 cables (VCC, GND, SDA, SCL).
- **Posible Uso / Proyecto Escolar:** Despliegue de datos de sensores ambientales, contadores de personas, relojes digitales escolares y mensajes de estado en proyectos robóticos.
- **Observaciones y Trazabilidad:** Clasificación A. El display escolar por excelencia.

#### [47] `KS0271` — Pantalla Gráfica OLED 0.96 Pulgadas I2C (128x64 Píxeles) Keyestudio

- **SKU Proveedor:** `KS0271` | **SKU Humm:** `HUMM-KEY-KS0271`
- **Nombre Comercial Humm:** **Pantalla Gráfica OLED 0.96 Pulgadas I2C (128x64 Píxeles) Keyestudio**
- **Categoría:** Pantallas e interacción
- **Precio Referencial Sugerido:** **$12,871 CLP** (Costo Base: $5.50 USD)
- **Nivel de Complejidad / Uso:** `INTERMEDIO`
- **Compatibilidad Tecnológica Verificada:** `Arduino` *(respaldo fabricante)*
- **Compatibilidad Tecnológica Propuesta (Aula):** `Arduino, ESP32, Raspberry Pi, micro:bit` *(interpretación pedagógica Humm)*
- **Contenido Real del Pack / Empaque:** 1 pantalla gráfica OLED de 0.96'' monocromática con conector I2C de 4 pines.
- **Unidad de Medida:** `unidad`
- **Apto Potencial para Kit:** **Sí**
- **Estado de Curaduría:** `VALIDADO`
- **Estado Especificación Técnica Neutra:** `NO_REVISADO` *(validación técnica documental progresiva)*
- **Descripción Educativa (Humm):** Pantalla gráfica miniatura de tecnología OLED que emite su propia luz sin necesidad de retroiluminación. Permite dibujar textos de diversos tamaños, curvas analógicas e íconos.
- **Posible Uso / Proyecto Escolar:** Instrumentación científica escolar, graficación en tiempo real de datos de sensores y diseño de interfaces visuales compactas.
- **Observaciones y Trazabilidad:** Clasificación A. Alta resolución y nitidez de contraste.

#### [48] `KS0481` — Módulo Joystick Analógico de 2 Ejes Honeycomb para micro:bit

- **SKU Proveedor:** `KS0481` | **SKU Humm:** `HUMM-KEY-KS0481`
- **Nombre Comercial Humm:** **Módulo Joystick Analógico de 2 Ejes Honeycomb para micro:bit**
- **Categoría:** Pantallas e interacción
- **Precio Referencial Sugerido:** **$9,829 CLP** (Costo Base: $4.20 USD)
- **Nivel de Complejidad / Uso:** `INICIAL`
- **Compatibilidad Tecnológica Verificada:** `micro:bit` *(respaldo fabricante)*
- **Compatibilidad Tecnológica Propuesta (Aula):** `micro:bit, Arduino` *(interpretación pedagógica Humm)*
- **Contenido Real del Pack / Empaque:** 1 módulo Honeycomb con palanca tipo gamepad de 2 ejes ortogonales y botón pulsador.
- **Unidad de Medida:** `unidad`
- **Apto Potencial para Kit:** **Sí**
- **Estado de Curaduría:** `VALIDADO`
- **Estado Especificación Técnica Neutra:** `NO_REVISADO` *(validación técnica documental progresiva)*
- **Descripción Educativa (Humm):** Mando analógico de control direccional con dos potenciómetros perpendiculares (X, Y) y un pulsador central al presionar la palanca. Formato Honeycomb con bornes para pinzas caimán.
- **Posible Uso / Proyecto Escolar:** Telecontrol de autos robóticos, manejo de brazos mecánicos y creación de controladores de videojuegos educativos en Scratch o MakeCode.
- **Observaciones y Trazabilidad:** Clasificación B. Serie Honeycomb adaptada para micro:bit.

#### [49] `MD0089` — Pack de 3 Teclados Matriciales de Membrana 4x3 (12 Teclas)

- **SKU Proveedor:** `MD0089` | **SKU Humm:** `HUMM-KEY-MD0089`
- **Nombre Comercial Humm:** **Pack de 3 Teclados Matriciales de Membrana 4x3 (12 Teclas)**
- **Categoría:** Pantallas e interacción
- **Precio Referencial Sugerido:** **$6,998 CLP** (Costo Base: $2.99 USD)
- **Nivel de Complejidad / Uso:** `INTERMEDIO`
- **Compatibilidad Tecnológica Verificada:** `Arduino, Otros` *(respaldo fabricante)*
- **Compatibilidad Tecnológica Propuesta (Aula):** `Arduino, ESP32, Raspberry Pi` *(interpretación pedagógica Humm)*
- **Contenido Real del Pack / Empaque:** Pack con exactamente 3 teclados planos de membrana autoadhesivos con 12 teclas (0-9, *, #).
- **Unidad de Medida:** `pack (3 unidades)`
- **Apto Potencial para Kit:** **Sí**
- **Estado de Curaduría:** `VALIDADO`
- **Estado Especificación Técnica Neutra:** `NO_REVISADO` *(validación técnica documental progresiva)*
- **Descripción Educativa (Humm):** Teclado numérico ultrafino autoadhesivo de 12 teclas configuradas en matriz de 4 filas por 3 columnas, permitiendo capturar datos numéricos con solo 7 pines digitales.
- **Posible Uso / Proyecto Escolar:** Sistemas de control de acceso por clave secreta, calculadoras escolares, cajas de seguridad simuladas y sistemas de votación en aula.
- **Observaciones y Trazabilidad:** Clasificación B. Corrección de pack: el precio corresponde a 3 unidades de teclado.

#### [50] `KS0163` — Shield de 40 LEDs RGB Direccionables WS2812 para Arduino Uno

- **SKU Proveedor:** `KS0163` | **SKU Humm:** `HUMM-KEY-KS0163`
- **Nombre Comercial Humm:** **Shield de 40 LEDs RGB Direccionables WS2812 para Arduino Uno**
- **Categoría:** Pantallas e interacción
- **Precio Referencial Sugerido:** **$22,935 CLP** (Costo Base: $9.80 USD)
- **Nivel de Complejidad / Uso:** `INTERMEDIO`
- **Compatibilidad Tecnológica Verificada:** `Arduino` *(respaldo fabricante)*
- **Compatibilidad Tecnológica Propuesta (Aula):** `Arduino` *(interpretación pedagógica Humm)*
- **Contenido Real del Pack / Empaque:** 1 shield para Arduino Uno con matriz de 40 LEDs RGB direccionables.
- **Unidad de Medida:** `unidad`
- **Apto Potencial para Kit:** **Sí**
- **Estado de Curaduría:** `VALIDADO`
- **Estado Especificación Técnica Neutra:** `NO_REVISADO` *(validación técnica documental progresiva)*
- **Descripción Educativa (Humm):** Placa de expansión con 40 píxeles LED inteligentes multicolor controlables individualmente en brillo y color a través de una única línea de datos.
- **Posible Uso / Proyecto Escolar:** Proyectos STEAM que combinan arte y programación: animaciones gráficas de caras expresivas, ecualizadores visuales y carteles de señalización dinámica.
- **Observaciones y Trazabilidad:** Clasificación A. Requiere librerías para control Neopixel/WS2812.

#### [51] `KS0310` — Módulo Semáforo Escolar con LEDs Rojo, Amarillo y Verde Keyestudio

- **SKU Proveedor:** `KS0310` | **SKU Humm:** `HUMM-KEY-KS0310`
- **Nombre Comercial Humm:** **Módulo Semáforo Escolar con LEDs Rojo, Amarillo y Verde Keyestudio**
- **Categoría:** Pantallas e interacción
- **Precio Referencial Sugerido:** **$9,361 CLP** (Costo Base: $4.00 USD)
- **Nivel de Complejidad / Uso:** `INICIAL`
- **Compatibilidad Tecnológica Verificada:** `Arduino` *(respaldo fabricante)*
- **Compatibilidad Tecnológica Propuesta (Aula):** `Arduino, micro:bit, ESP32, Raspberry Pi` *(interpretación pedagógica Humm)*
- **Contenido Real del Pack / Empaque:** 1 módulo semáforo con 3 LEDs integrados (R, Y, G) y terminal de 4 pines.
- **Unidad de Medida:** `unidad`
- **Apto Potencial para Kit:** **Sí**
- **Estado de Curaduría:** `VALIDADO`
- **Estado Especificación Técnica Neutra:** `NO_REVISADO` *(validación técnica documental progresiva)*
- **Descripción Educativa (Humm):** Módulo compacto que integra tres LEDs independientes simulando un semáforo de tránsito real, con cátodo común y resistencias protectoras en la placa.
- **Posible Uso / Proyecto Escolar:** Enseñanza de secuencias temporizadas, diagramas de flujo y educación vial escolar en educación básica y media inicial.
- **Observaciones y Trazabilidad:** Clasificación A. Muy formativo para primeros pasos en programación.

---

### Micro:bit y accesorios (5 productos)

#### [52] `KS0434` — Placa de Expansión de Pines I/O para BBC micro:bit Keyestudio

- **SKU Proveedor:** `KS0434` | **SKU Humm:** `HUMM-KEY-KS0434`
- **Nombre Comercial Humm:** **Placa de Expansión de Pines I/O para BBC micro:bit Keyestudio**
- **Categoría:** Micro:bit y accesorios
- **Precio Referencial Sugerido:** **$11,701 CLP** (Costo Base: $5.00 USD)
- **Nivel de Complejidad / Uso:** `INICIAL`
- **Compatibilidad Tecnológica Verificada:** `micro:bit` *(respaldo fabricante)*
- **Compatibilidad Tecnológica Propuesta (Aula):** `micro:bit` *(interpretación pedagógica Humm)*
- **Contenido Real del Pack / Empaque:** 1 placa de expansión con zócalo vertical para conector de borde de micro:bit.
- **Unidad de Medida:** `unidad`
- **Apto Potencial para Kit:** **Sí**
- **Estado de Curaduría:** `VALIDADO`
- **Estado Especificación Técnica Neutra:** `NO_REVISADO` *(validación técnica documental progresiva)*
- **Descripción Educativa (Humm):** Adaptador que se encaja en el conector de borde de la tarjeta micro:bit para distribuir todos sus pines a cabezales estándar de 3 pines (Tierra, Voltaje y Señal), facilitando conectar módulos comunes.
- **Posible Uso / Proyecto Escolar:** Ampliación de proyectos de micro:bit con servomotores, potenciómetros y sensores externos sin necesidad de pinzas caimán.
- **Observaciones y Trazabilidad:** Clasificación A. Accesorio básico para llevar micro:bit más allá de sus sensores integrados.

#### [53] `MB0110` — Kit Oficial BBC micro:bit V2 Go (Tarjeta + Cable + Portapilas)

- **SKU Proveedor:** `MB0110` | **SKU Humm:** `HUMM-KEY-MB0110`
- **Nombre Comercial Humm:** **Kit Oficial BBC micro:bit V2 Go (Tarjeta + Cable + Portapilas)**
- **Categoría:** Micro:bit y accesorios
- **Precio Referencial Sugerido:** **$66,929 CLP** (Costo Base: $28.60 USD)
- **Nivel de Complejidad / Uso:** `INICIAL`
- **Compatibilidad Tecnológica Verificada:** `micro:bit` *(respaldo fabricante)*
- **Compatibilidad Tecnológica Propuesta (Aula):** `micro:bit` *(interpretación pedagógica Humm)*
- **Contenido Real del Pack / Empaque:** Caja oficial micro:bit V2 Go: 1 tarjeta micro:bit V2 original, 1 cable USB, 1 portapilas con 2 baterías AAA y folleto de inicio.
- **Unidad de Medida:** `unidad`
- **Apto Potencial para Kit:** **Sí**
- **Estado de Curaduría:** `VALIDADO`
- **Estado Especificación Técnica Neutra:** `NO_REVISADO` *(validación técnica documental progresiva)*
- **Descripción Educativa (Humm):** Kit oficial completo con la tarjeta microcontroladora educativa BBC micro:bit V2, que integra acelerómetro, brújula, micrófono, altavoz, matriz de 25 LEDs y botones táctiles. Ampliamente adoptada en colegios para la enseñanza del pensamiento computacional mediante bloques (MakeCode) o Python.
- **Posible Uso / Proyecto Escolar:** El estándar oficial del Mineduc y programas mundiales para la enseñanza del pensamiento computacional en educación básica y media mediante MakeCode por bloques o Python.
- **Observaciones y Trazabilidad:** Clasificación A. Kit oficial de referencia con micro:bit V2 original.

#### [54] `KS4038` — Brazo Robótico 4DOF para micro:bit — Con Placa micro:bit Incluida

- **SKU Proveedor:** `KS4038` | **SKU Humm:** `HUMM-KEY-KS4038`
- **Nombre Comercial Humm:** **Brazo Robótico 4DOF para micro:bit — Con Placa micro:bit Incluida**
- **Categoría:** Micro:bit y accesorios
- **Precio Referencial Sugerido:** **$150,705 CLP** (Costo Base: $64.40 USD)
- **Nivel de Complejidad / Uso:** `INTERMEDIO`
- **Compatibilidad Tecnológica Verificada:** `micro:bit` *(respaldo fabricante)*
- **Compatibilidad Tecnológica Propuesta (Aula):** `micro:bit` *(interpretación pedagógica Humm)*
- **Contenido Real del Pack / Empaque:** Kit de estructura de brazo 4DOF, servomotores, shield de expansión Y 1 TARJETA MICRO:BIT INCLUIDA en la caja.
- **Unidad de Medida:** `unidad`
- **Apto Potencial para Kit:** **Sí**
- **Estado de Curaduría:** `VALIDADO`
- **Estado Especificación Técnica Neutra:** `NO_REVISADO` *(validación técnica documental progresiva)*
- **Descripción Educativa (Humm):** Set robótico completo de brazo articulado de 4 grados de libertad con pinza de agarre, que incluye la tarjeta microcontroladora BBC micro:bit para comenzar a operar de inmediato.
- **Posible Uso / Proyecto Escolar:** Talleres integrales de robótica para colegios que no cuentan con tarjetas micro:bit previas; proyectos de manipulación y clasificación automatizada.
- **Observaciones y Trazabilidad:** Clasificación A. Incluye la tarjeta micro:bit en el empaque.

#### [55] `KS0802` — Kit Didáctico Creativo Crocodile con Pinzas Caimán — Con Tarjeta micro:bit

- **SKU Proveedor:** `KS0802` | **SKU Humm:** `HUMM-KEY-KS0802`
- **Nombre Comercial Humm:** **Kit Didáctico Creativo Crocodile con Pinzas Caimán — Con Tarjeta micro:bit**
- **Categoría:** Micro:bit y accesorios
- **Precio Referencial Sugerido:** **$101,889 CLP** (Costo Base: $43.54 USD)
- **Nivel de Complejidad / Uso:** `INICIAL`
- **Compatibilidad Tecnológica Verificada:** `micro:bit` *(respaldo fabricante)*
- **Compatibilidad Tecnológica Propuesta (Aula):** `micro:bit` *(interpretación pedagógica Humm)*
- **Contenido Real del Pack / Empaque:** Kit educativo completo con módulos, cables caimán y 1 tarjeta micro:bit incluida.
- **Unidad de Medida:** `unidad`
- **Apto Potencial para Kit:** **Sí**
- **Estado de Curaduría:** `VALIDADO`
- **Estado Especificación Técnica Neutra:** `NO_REVISADO` *(validación técnica documental progresiva)*
- **Descripción Educativa (Humm):** Kit de inicio lúdico orientado a primeros ciclos escolares, diseñado para conectar sensores y actuadores mediante cables con pinzas cocodrilo sin soldadura ni protoboard.
- **Posible Uso / Proyecto Escolar:** Experimentos de conductividad eléctrica de frutas, agua con sal, plastilina conductora, instrumentos musicales táctiles y circuitos en papel.
- **Observaciones y Trazabilidad:** Clasificación A. Incluye la tarjeta micro:bit en el kit.

#### [56] `KT0284` — Pack de 4 Motores DC / Servos Continuos de Eje Doble para micro:bit

- **SKU Proveedor:** `KT0284` | **SKU Humm:** `HUMM-KEY-KT0284`
- **Nombre Comercial Humm:** **Pack de 4 Motores DC / Servos Continuos de Eje Doble para micro:bit**
- **Categoría:** Micro:bit y accesorios
- **Precio Referencial Sugerido:** **$51,483 CLP** (Costo Base: $22.00 USD)
- **Nivel de Complejidad / Uso:** `INICIAL`
- **Compatibilidad Tecnológica Verificada:** `micro:bit` *(respaldo fabricante)*
- **Compatibilidad Tecnológica Propuesta (Aula):** `micro:bit` *(interpretación pedagógica Humm)*
- **Contenido Real del Pack / Empaque:** Pack con exactamente 4 motores azules de eje pasante doble compatibles con micro:bit y ruedas Lego.
- **Unidad de Medida:** `pack (4 unidades)`
- **Apto Potencial para Kit:** **Sí**
- **Estado de Curaduría:** `VALIDADO`
- **Estado Especificación Técnica Neutra:** `NO_REVISADO` *(validación técnica documental progresiva)*
- **Descripción Educativa (Humm):** Motores de rotación continua con caja reductora y doble eje estriado compatible con orificios de ruedas de bloques de construcción, controlables por micro:bit.
- **Posible Uso / Proyecto Escolar:** Construcción de autos robóticos móviles, molinos y vehículos didácticos programados mediante bloques en MakeCode.
- **Observaciones y Trazabilidad:** Clasificación B. Corrección de pack: contiene 4 motores de eje doble.

---

### Raspberry Pi y accesorios (4 productos)

#### [57] `KS0219` — Adaptador GPIO en T con Cable de 40 Pines y Protoboard para Raspberry Pi

- **SKU Proveedor:** `KS0219` | **SKU Humm:** `HUMM-KEY-KS0219`
- **Nombre Comercial Humm:** **Adaptador GPIO en T con Cable de 40 Pines y Protoboard para Raspberry Pi**
- **Categoría:** Raspberry Pi y accesorios
- **Precio Referencial Sugerido:** **$21,529 CLP** (Costo Base: $9.20 USD)
- **Nivel de Complejidad / Uso:** `INTERMEDIO`
- **Compatibilidad Tecnológica Verificada:** `Raspberry Pi` *(respaldo fabricante)*
- **Compatibilidad Tecnológica Propuesta (Aula):** `Raspberry Pi` *(interpretación pedagógica Humm)*
- **Contenido Real del Pack / Empaque:** 1 placa adaptadora tipo 'T' (T-Cobbler) + 1 cable plano flexible de 40 vías + 1 protoboard de 400 puntos.
- **Unidad de Medida:** `set (3 piezas)`
- **Apto Potencial para Kit:** **Sí**
- **Estado de Curaduría:** `VALIDADO`
- **Estado Especificación Técnica Neutra:** `NO_REVISADO` *(validación técnica documental progresiva)*
- **Descripción Educativa (Humm):** Conjunto de conexión que traslada ordenadamente los 40 pines del puerto GPIO de Raspberry Pi a una protoboard, rotulando claramente el nombre de cada pin para evitar cortocircuitos.
- **Posible Uso / Proyecto Escolar:** Prácticas de programación en Python interactuando con circuitos físicos (lectura de sensores, encendido de LEDs) bajo sistema operativo Linux.
- **Observaciones y Trazabilidad:** Clasificación A. La forma más segura y económica de experimentar con GPIO en Raspberry Pi.

#### [58] `SMP0023` — Cámara 5MP 1080p con Cable Plano CSI para Raspberry Pi

- **SKU Proveedor:** `SMP0023` | **SKU Humm:** `HUMM-KEY-SMP0023`
- **Nombre Comercial Humm:** **Cámara 5MP 1080p con Cable Plano CSI para Raspberry Pi**
- **Categoría:** Raspberry Pi y accesorios
- **Precio Referencial Sugerido:** **$18,019 CLP** (Costo Base: $7.70 USD)
- **Nivel de Complejidad / Uso:** `AVANZADO`
- **Compatibilidad Tecnológica Verificada:** `Raspberry Pi` *(respaldo fabricante)*
- **Compatibilidad Tecnológica Propuesta (Aula):** `Raspberry Pi` *(interpretación pedagógica Humm)*
- **Contenido Real del Pack / Empaque:** 1 módulo de cámara 5MP con sensor OV5647 y cable plano flexible CSI de 15 pines.
- **Unidad de Medida:** `unidad`
- **Apto Potencial para Kit:** **Sí**
- **Estado de Curaduría:** `VALIDADO`
- **Estado Especificación Técnica Neutra:** `NO_REVISADO` *(validación técnica documental progresiva)*
- **Descripción Educativa (Humm):** Módulo de cámara digital con conexión directa al puerto de cámara CSI nativo de placas Raspberry Pi, permitiendo captura de fotos fijas y grabación de video en alta definición sin sobrecargar el bus USB.
- **Posible Uso / Proyecto Escolar:** Proyectos de visión por computador, reconocimiento de imágenes con OpenCV/Python, cámaras de seguridad escolar y registro fotográfico timelapse de plantas.
- **Observaciones y Trazabilidad:** Clasificación B. Conector nativo de 15 pines para Raspberry Pi 1, 2, 3 y 4. (En Pi 5 o Pi Zero requiere cable adaptador de 22 a 15 pines).

#### [59] `60520146` — Carcasa Metálica de Aluminio con Ventilador Activo para Raspberry Pi 4B (Sin Placa)

- **SKU Proveedor:** `60520146` | **SKU Humm:** `HUMM-KEY-60520146`
- **Nombre Comercial Humm:** **Carcasa Metálica de Aluminio con Ventilador Activo para Raspberry Pi 4B (Sin Placa)**
- **Categoría:** Raspberry Pi y accesorios
- **Precio Referencial Sugerido:** **$38,612 CLP** (Costo Base: $16.50 USD)
- **Nivel de Complejidad / Uso:** `INICIAL`
- **Compatibilidad Tecnológica Verificada:** `Raspberry Pi` *(respaldo fabricante)*
- **Compatibilidad Tecnológica Propuesta (Aula):** `Raspberry Pi` *(interpretación pedagógica Humm)*
- **Contenido Real del Pack / Empaque:** 1 carcasa de aleación de aluminio negro, 1 ventilador de enfriamiento de 5V, juego de disipadores térmicos y tornillos de fijación. NO incluye placa Raspberry Pi.
- **Unidad de Medida:** `unidad`
- **Apto Potencial para Kit:** **No**
- **Estado de Curaduría:** `VALIDADO`
- **Estado Especificación Técnica Neutra:** `NO_REVISADO` *(validación técnica documental progresiva)*
- **Descripción Educativa (Humm):** Caja protectora metálica de alta disipación térmica pasiva y activa mediante ventilador, diseñada a la medida para proteger placas Raspberry Pi 4B en laboratorios escolares de uso intensivo.
- **Posible Uso / Proyecto Escolar:** Protección física de computadoras escolares Raspberry Pi contra caídas accidentales, contactos electrostáticos y sobrecalentamiento térmico.
- **Observaciones y Trazabilidad:** Clasificación A. Compatible con Raspberry Pi 4B. Aclarar que es la carcasa protectora sin la placa.

#### [60] `67600041` — Soporte Acrílico Orientable para Cámara Raspberry Pi

- **SKU Proveedor:** `67600041` | **SKU Humm:** `HUMM-KEY-67600041`
- **Nombre Comercial Humm:** **Soporte Acrílico Orientable para Cámara Raspberry Pi**
- **Categoría:** Raspberry Pi y accesorios
- **Precio Referencial Sugerido:** **$11,701 CLP** (Costo Base: $5.00 USD)
- **Nivel de Complejidad / Uso:** `INICIAL`
- **Compatibilidad Tecnológica Verificada:** `Raspberry Pi` *(respaldo fabricante)*
- **Compatibilidad Tecnológica Propuesta (Aula):** `Raspberry Pi` *(interpretación pedagógica Humm)*
- **Contenido Real del Pack / Empaque:** 1 soporte acrílico negro con base y tornillos de ajuste para fijar el módulo de cámara.
- **Unidad de Medida:** `unidad`
- **Apto Potencial para Kit:** **No**
- **Estado de Curaduría:** `VALIDADO`
- **Estado Especificación Técnica Neutra:** `NO_REVISADO` *(validación técnica documental progresiva)*
- **Descripción Educativa (Humm):** Base articulada orientable para sujetar mecánicamente módulos de cámara de Raspberry Pi (como SMP0023 o cámara oficial V2), evitando que queden colgando del cable flexible.
- **Posible Uso / Proyecto Escolar:** Fijación estable de la cámara en proyectos de visión artificial, seguimiento de objetos y vigilancia en laboratorios.
- **Observaciones y Trazabilidad:** Clasificación A. Complemento de montaje para el módulo SMP0023.

---

### IoT y comunicación (6 productos)

#### [61] `KS0255` — Shield de Comunicación Bluetooth 4.0 BLE para Arduino Uno

- **SKU Proveedor:** `KS0255` | **SKU Humm:** `HUMM-KEY-KS0255`
- **Nombre Comercial Humm:** **Shield de Comunicación Bluetooth 4.0 BLE para Arduino Uno**
- **Categoría:** IoT y comunicación
- **Precio Referencial Sugerido:** **$25,719 CLP** (Costo Base: $10.99 USD)
- **Nivel de Complejidad / Uso:** `INTERMEDIO`
- **Compatibilidad Tecnológica Verificada:** `Arduino` *(respaldo fabricante)*
- **Compatibilidad Tecnológica Propuesta (Aula):** `Arduino` *(interpretación pedagógica Humm)*
- **Contenido Real del Pack / Empaque:** 1 shield de comunicación Bluetooth 4.0 BLE para acoplar sobre Arduino Uno.
- **Unidad de Medida:** `unidad`
- **Apto Potencial para Kit:** **Sí**
- **Estado de Curaduría:** `VALIDADO`
- **Estado Especificación Técnica Neutra:** `NO_REVISADO` *(validación técnica documental progresiva)*
- **Descripción Educativa (Humm):** Placa de expansión con tecnología Bluetooth de bajo consumo (BLE) que permite conectar de forma inalámbrica placas Arduino Uno con dispositivos móviles modernos (iOS, iPadOS y Android).
- **Posible Uso / Proyecto Escolar:** Telecontrol de robots desde aplicaciones en tabletas o celulares escolares, intercambio de datos de sensores y proyectos de domótica inalámbrica.
- **Observaciones y Trazabilidad:** Clasificación A. Formato shield sin cables sueltos.

#### [62] `MD0322` — Módulo Wi-Fi Serial ESP8266 para Arduino (Control por Comandos AT)

- **SKU Proveedor:** `MD0322` | **SKU Humm:** `HUMM-KEY-MD0322`
- **Nombre Comercial Humm:** **Módulo Wi-Fi Serial ESP8266 para Arduino (Control por Comandos AT)**
- **Categoría:** IoT y comunicación
- **Precio Referencial Sugerido:** **$5,850 CLP** (Costo Base: $2.50 USD)
- **Nivel de Complejidad / Uso:** `AVANZADO`
- **Compatibilidad Tecnológica Verificada:** `Arduino, ESP8266` *(respaldo fabricante)*
- **Compatibilidad Tecnológica Propuesta (Aula):** `Arduino, ESP8266` *(interpretación pedagógica Humm)*
- **Contenido Real del Pack / Empaque:** 1 módulo transceptor Wi-Fi ESP8266 en placa de 8 pines.
- **Unidad de Medida:** `unidad`
- **Apto Potencial para Kit:** **Sí**
- **Estado de Curaduría:** `VALIDADO`
- **Estado Especificación Técnica Neutra:** `NO_REVISADO` *(validación técnica documental progresiva)*
- **Descripción Educativa (Humm):** Módulo de bajo costo que añade conectividad Wi-Fi a microcontroladores mediante comunicación serial UART y comandos AT estándar.
- **Posible Uso / Proyecto Escolar:** Envío de datos de telemetría a servidores locales, solicitudes HTTP simples y aprendizaje de protocolos de red TCP/IP.
- **Observaciones y Trazabilidad:** Clasificación B. Corrección auditada: es módulo serial ESP8266 para Arduino (no ESP32). Opera con lógica de 3.3V.

#### [63] `KS0205` — Módulo Lector/Grabador RFID RC522 (13.56 MHz) con Tarjeta y Llavero

- **SKU Proveedor:** `KS0205` | **SKU Humm:** `HUMM-KEY-KS0205`
- **Nombre Comercial Humm:** **Módulo Lector/Grabador RFID RC522 (13.56 MHz) con Tarjeta y Llavero**
- **Categoría:** IoT y comunicación
- **Precio Referencial Sugerido:** **$10,766 CLP** (Costo Base: $4.60 USD)
- **Nivel de Complejidad / Uso:** `INTERMEDIO`
- **Compatibilidad Tecnológica Verificada:** `Arduino` *(respaldo fabricante)*
- **Compatibilidad Tecnológica Propuesta (Aula):** `Arduino, ESP32, Raspberry Pi` *(interpretación pedagógica Humm)*
- **Contenido Real del Pack / Empaque:** 1 módulo lector RFID RC522 con antena integrada + 1 tarjeta blanca Mifare + 1 llavero tag azul RFID.
- **Unidad de Medida:** `set (3 piezas)`
- **Apto Potencial para Kit:** **Sí**
- **Estado de Curaduría:** `VALIDADO`
- **Estado Especificación Técnica Neutra:** `NO_REVISADO` *(validación técnica documental progresiva)*
- **Descripción Educativa (Humm):** Sistema de identificación inalámbrica por radiofrecuencia (RFID a 13.56 MHz por interfaz SPI) capaz de leer y escribir información en tarjetas y llaveros de proximidad.
- **Posible Uso / Proyecto Escolar:** Sistemas de registro de asistencia escolar, cerraduras electrónicas para laboratorios y gestión digital de préstamos de libros en bibliotecas escolares.
- **Observaciones y Trazabilidad:** Clasificación A. Incluye tarjeta y llavero de prueba en el paquete.

#### [64] `MD0040` — Módulo Transceptor Inalámbrico por Radiofrecuencia NRF24L01+ 2.4 GHz

- **SKU Proveedor:** `MD0040` | **SKU Humm:** `HUMM-KEY-MD0040`
- **Nombre Comercial Humm:** **Módulo Transceptor Inalámbrico por Radiofrecuencia NRF24L01+ 2.4 GHz**
- **Categoría:** IoT y comunicación
- **Precio Referencial Sugerido:** **$9,361 CLP** (Costo Base: $4.00 USD)
- **Nivel de Complejidad / Uso:** `INTERMEDIO`
- **Compatibilidad Tecnológica Verificada:** `Arduino` *(respaldo fabricante)*
- **Compatibilidad Tecnológica Propuesta (Aula):** `Arduino, micro:bit, ESP32, Raspberry Pi` *(interpretación pedagógica Humm)*
- **Contenido Real del Pack / Empaque:** 1 módulo transceptor de radio NRF24L01+ con antena en PCB.
- **Unidad de Medida:** `unidad`
- **Apto Potencial para Kit:** **Sí**
- **Estado de Curaduría:** `VALIDADO`
- **Estado Especificación Técnica Neutra:** `NO_REVISADO` *(validación técnica documental progresiva)*
- **Descripción Educativa (Humm):** Módulo de comunicación digital inalámbrica en la banda ISM de 2.4 GHz mediante interfaz SPI. Permite intercambio bidireccional de paquetes de datos entre múltiples placas sin requerir red Wi-Fi.
- **Posible Uso / Proyecto Escolar:** Comunicación directa entre robots en competencias escolares, mandos a distancia para autos robóticos y redes de sensores en malla.
- **Observaciones y Trazabilidad:** Clasificación A. Comunicación por radio sin infraestructura de red.

#### [65] `KS0026` — Módulo Receptor Infrarrojo de 38 kHz para Control Remoto Keyestudio

- **SKU Proveedor:** `KS0026` | **SKU Humm:** `HUMM-KEY-KS0026`
- **Nombre Comercial Humm:** **Módulo Receptor Infrarrojo de 38 kHz para Control Remoto Keyestudio**
- **Categoría:** IoT y comunicación
- **Precio Referencial Sugerido:** **$8,894 CLP** (Costo Base: $3.80 USD)
- **Nivel de Complejidad / Uso:** `INICIAL`
- **Compatibilidad Tecnológica Verificada:** `Arduino` *(respaldo fabricante)*
- **Compatibilidad Tecnológica Propuesta (Aula):** `Arduino, micro:bit, ESP32` *(interpretación pedagógica Humm)*
- **Contenido Real del Pack / Empaque:** 1 módulo con receptor infrarrojo de 38 kHz (VS1838B) y conector de 3 pines.
- **Unidad de Medida:** `unidad`
- **Apto Potencial para Kit:** **Sí**
- **Estado de Curaduría:** `VALIDADO`
- **Estado Especificación Técnica Neutra:** `NO_REVISADO` *(validación técnica documental progresiva)*
- **Descripción Educativa (Humm):** Sensor que decodifica señales luminosas infrarrojas pulsadas a 38 kHz, permitiendo controlar microcontroladores con mandos a distancia comunes de televisión.
- **Posible Uso / Proyecto Escolar:** Control remoto de autos robóticos con controles de TV domésticos y sistemas interactivos de encendido/apagado a distancia.
- **Observaciones y Trazabilidad:** Clasificación A. Receptor óptico de 38 kHz.

#### [66] `KS0389` — Shield Wi-Fi ESP8266 para Arduino Uno con Conversor USB-Serial y Cable

- **SKU Proveedor:** `KS0389` | **SKU Humm:** `HUMM-KEY-KS0389`
- **Nombre Comercial Humm:** **Shield Wi-Fi ESP8266 para Arduino Uno con Conversor USB-Serial y Cable**
- **Categoría:** IoT y comunicación
- **Precio Referencial Sugerido:** **$23,378 CLP** (Costo Base: $9.99 USD)
- **Nivel de Complejidad / Uso:** `INTERMEDIO`
- **Compatibilidad Tecnológica Verificada:** `Arduino, ESP8266` *(respaldo fabricante)*
- **Compatibilidad Tecnológica Propuesta (Aula):** `Arduino, ESP8266` *(interpretación pedagógica Humm)*
- **Contenido Real del Pack / Empaque:** 1 shield Wi-Fi ESP8266 con chip CP2102 integrado + 1 cable micro-USB de 1 metro.
- **Unidad de Medida:** `set (2 piezas)`
- **Apto Potencial para Kit:** **Sí**
- **Estado de Curaduría:** `VALIDADO`
- **Estado Especificación Técnica Neutra:** `NO_REVISADO` *(validación técnica documental progresiva)*
- **Descripción Educativa (Humm):** Placa de expansión en formato shield para Arduino Uno que incorpora un módulo Wi-Fi ESP8266 con puerto micro-USB independiente para programarlo o depurarlo con facilidad.
- **Posible Uso / Proyecto Escolar:** Creación rápida de estaciones meteorológicas conectadas a internet, servidores web escolares y proyectos de domótica IoT con Arduino Uno.
- **Observaciones y Trazabilidad:** Clasificación A. Incorpora chip CP2102 y cable micro-USB.

---

### Kits educativos iniciales (3 productos)

#### [67] `KS0541` — Kit de Componentes para Arduino (20 Proyectos Guiados) — Sin Placa Controladora

- **SKU Proveedor:** `KS0541` | **SKU Humm:** `HUMM-KEY-KS0541`
- **Nombre Comercial Humm:** **Kit de Componentes para Arduino (20 Proyectos Guiados) — Sin Placa Controladora**
- **Categoría:** Kits educativos iniciales
- **Precio Referencial Sugerido:** **$45,633 CLP** (Costo Base: $19.50 USD)
- **Nivel de Complejidad / Uso:** `INICIAL`
- **Compatibilidad Tecnológica Verificada:** `Arduino` *(respaldo fabricante)*
- **Compatibilidad Tecnológica Propuesta (Aula):** `Arduino` *(interpretación pedagógica Humm)*
- **Contenido Real del Pack / Empaque:** Caja organizadora con sensores, actuadores, protoboard, LEDs, resistencias, cables y manual con 20 proyectos guiados. NO INCLUYE LA PLACA ARDUINO / PLUS.
- **Unidad de Medida:** `unidad`
- **Apto Potencial para Kit:** **Sí**
- **Estado de Curaduría:** `VALIDADO`
- **Estado Especificación Técnica Neutra:** `NO_REVISADO` *(validación técnica documental progresiva)*
- **Descripción Educativa (Humm):** Caja didáctica de iniciación a la electrónica que reúne los componentes necesarios para desarrollar 20 prácticas formativas guiadas, requiriendo una placa Arduino Uno o PLUS externa para programar.
- **Posible Uso / Proyecto Escolar:** Cursos escolares de electrónica básica donde el colegio ya dispone de placas Arduino y necesita paquetes individuales de componentes para cada estudiante.
- **Observaciones y Trazabilidad:** Clasificación B. Advertencia comercial obligatoria: no incluye placa controladora ('Without Plus Mainboard').

#### [68] `KS0487` — Maletín Multi-Sensor 37 en 1 Keyestudio V3.0 con Caja Organizadora

- **SKU Proveedor:** `KS0487` | **SKU Humm:** `HUMM-KEY-KS0487`
- **Nombre Comercial Humm:** **Maletín Multi-Sensor 37 en 1 Keyestudio V3.0 con Caja Organizadora**
- **Categoría:** Kits educativos iniciales
- **Precio Referencial Sugerido:** **$85,883 CLP** (Costo Base: $36.70 USD)
- **Nivel de Complejidad / Uso:** `INICIAL`
- **Compatibilidad Tecnológica Verificada:** `Arduino` *(respaldo fabricante)*
- **Compatibilidad Tecnológica Propuesta (Aula):** `Arduino, micro:bit, ESP32, Raspberry Pi` *(interpretación pedagógica Humm)*
- **Contenido Real del Pack / Empaque:** Maletín plástico compartimentado con 37 módulos de sensores y actuadores individuales + tutorial digital con 37 proyectos.
- **Unidad de Medida:** `unidad`
- **Apto Potencial para Kit:** **Sí**
- **Estado de Curaduría:** `VALIDADO`
- **Estado Especificación Técnica Neutra:** `NO_REVISADO` *(validación técnica documental progresiva)*
- **Descripción Educativa (Humm):** Colección completa de 37 módulos didácticos que abarcan sensores ambientales, ópticos, mecánicos, magnéticos y acústicos en un maletín ordenado.
- **Posible Uso / Proyecto Escolar:** Equipamiento de laboratorios escolares de ciencias y robótica para que estudiantes exploren el funcionamiento físico y la programación de múltiples transductores.
- **Observaciones y Trazabilidad:** Clasificación A. El maletín de sensores de referencia para colegios.

#### [69] `KS0567` — Kit Temático Granja Inteligente (Smart Farm) IoT con ESP32 Keyestudio

- **SKU Proveedor:** `KS0567` | **SKU Humm:** `HUMM-KEY-KS0567`
- **Nombre Comercial Humm:** **Kit Temático Granja Inteligente (Smart Farm) IoT con ESP32 Keyestudio**
- **Categoría:** Kits educativos iniciales
- **Precio Referencial Sugerido:** **$142,749 CLP** (Costo Base: $61.00 USD)
- **Nivel de Complejidad / Uso:** `INTERMEDIO`
- **Compatibilidad Tecnológica Verificada:** `ESP32, Arduino` *(respaldo fabricante)*
- **Compatibilidad Tecnológica Propuesta (Aula):** `ESP32, Arduino` *(interpretación pedagógica Humm)*
- **Contenido Real del Pack / Empaque:** Kit integral: estructura didáctica de madera ensamblable, tarjeta de control ESP32, sensor de humedad de suelo, fotocelda, servomotor, bomba de agua miniatura, pantalla y tutorial.
- **Unidad de Medida:** `unidad`
- **Apto Potencial para Kit:** **Sí**
- **Estado de Curaduría:** `VALIDADO`
- **Estado Especificación Técnica Neutra:** `NO_REVISADO` *(validación técnica documental progresiva)*
- **Descripción Educativa (Humm):** Sistema temático de agroecología automatizada que combina microcontrolador con conectividad Wi-Fi, sensores ambientales y actuadores de riego programable mediante bloques (Scratch) o C++.
- **Posible Uso / Proyecto Escolar:** Proyectos interdisciplinarios STEM de agricultura sustentable, optimización de riego hídrico, monitoreo en la nube y automatización escolar.
- **Observaciones y Trazabilidad:** Clasificación A. Proyecto integral de alto valor pedagógico.

---

### Herramientas y accesorios (3 productos)

#### [70] `49500005` — Multímetro Digital Portátil XL830L con Funda Protectora de Goma

- **SKU Proveedor:** `49500005` | **SKU Humm:** `HUMM-KEY-49500005`
- **Nombre Comercial Humm:** **Multímetro Digital Portátil XL830L con Funda Protectora de Goma**
- **Categoría:** Herramientas y accesorios
- **Precio Referencial Sugerido:** **$29,251 CLP** (Costo Base: $12.50 USD)
- **Nivel de Complejidad / Uso:** `INICIAL`
- **Compatibilidad Tecnológica Verificada:** `Otros` *(respaldo fabricante)*
- **Compatibilidad Tecnológica Propuesta (Aula):** `Otros` *(interpretación pedagógica Humm)*
- **Contenido Real del Pack / Empaque:** 1 multímetro digital XL830L con funda de goma antichoque + juego de 2 puntas de prueba (roja y negra).
- **Unidad de Medida:** `unidad`
- **Apto Potencial para Kit:** **Sí**
- **Estado de Curaduría:** `VALIDADO`
- **Estado Especificación Técnica Neutra:** `NO_REVISADO` *(validación técnica documental progresiva)*
- **Descripción Educativa (Humm):** Instrumento básico de medición eléctrica para comprobar voltaje continuo y alterno, corriente continua, resistencia y continuidad audible con zumbador.
- **Posible Uso / Proyecto Escolar:** Comprobación de conexiones en protoboards, detección de cortocircuitos, medición de voltaje de baterías y enseñanza de magnitudes eléctricas.
- **⚠️ Advertencia de Uso y Seguridad:** *Diseñado para medición de magnitudes eléctricas en bancos de trabajo escolares. Se recomienda orientar las actividades estudiantiles principalmente a circuitos educativos de baja tensión (hasta 24V).*
- **Observaciones y Trazabilidad:** Clasificación A. Puede no incluir la batería de 9V (6F22) por normativas de transporte aéreo.

#### [71] `49500004` — Multímetro Digital de Banco DT9205A con Pantalla Inclinable

- **SKU Proveedor:** `49500004` | **SKU Humm:** `HUMM-KEY-49500004`
- **Nombre Comercial Humm:** **Multímetro Digital de Banco DT9205A con Pantalla Inclinable**
- **Categoría:** Herramientas y accesorios
- **Precio Referencial Sugerido:** **$35,103 CLP** (Costo Base: $15.00 USD)
- **Nivel de Complejidad / Uso:** `INTERMEDIO`
- **Compatibilidad Tecnológica Verificada:** `Otros` *(respaldo fabricante)*
- **Compatibilidad Tecnológica Propuesta (Aula):** `Otros` *(interpretación pedagógica Humm)*
- **Contenido Real del Pack / Empaque:** 1 multímetro digital grande DT9205A con display abatible + juego de puntas de prueba.
- **Unidad de Medida:** `unidad`
- **Apto Potencial para Kit:** **No**
- **Estado de Curaduría:** `VALIDADO`
- **Estado Especificación Técnica Neutra:** `NO_REVISADO` *(validación técnica documental progresiva)*
- **Descripción Educativa (Humm):** Instrumento de medición de mayor tamaño y precisión con pantalla inclinable para mesa de trabajo, protección de sobrecarga y rangos extendidos de medición de resistencia y capacitancia.
- **Posible Uso / Proyecto Escolar:** Bancos de trabajo en talleres técnicos de especialidad electrónica y laboratorios avanzados de física.
- **⚠️ Advertencia de Uso y Seguridad:** *Instrumento de banco para medición eléctrica. Se recomienda orientar las actividades prácticas estudiantiles exclusivamente a circuitos formativos de baja tensión (hasta 24V).*
- **Observaciones y Trazabilidad:** Clasificación A. Formato de banco con pantalla abatible.

#### [72] `MD0118` — Módulo Conversor USB a Serial UART TTL CP2102 con Cable Dupont

- **SKU Proveedor:** `MD0118` | **SKU Humm:** `HUMM-KEY-MD0118`
- **Nombre Comercial Humm:** **Módulo Conversor USB a Serial UART TTL CP2102 con Cable Dupont**
- **Categoría:** Herramientas y accesorios
- **Precio Referencial Sugerido:** **$9,478 CLP** (Costo Base: $4.05 USD)
- **Nivel de Complejidad / Uso:** `INTERMEDIO`
- **Compatibilidad Tecnológica Verificada:** `Arduino, Otros` *(respaldo fabricante)*
- **Compatibilidad Tecnológica Propuesta (Aula):** `Otros, Arduino` *(interpretación pedagógica Humm)*
- **Contenido Real del Pack / Empaque:** 1 módulo convertidor USB-TTL con chip Silicon Labs CP2102 + 1 cable flexible de 4 pines hembra-hembra.
- **Unidad de Medida:** `set (2 piezas)`
- **Apto Potencial para Kit:** **Sí**
- **Estado de Curaduría:** `VALIDADO`
- **Estado Especificación Técnica Neutra:** `NO_REVISADO` *(validación técnica documental progresiva)*
- **Descripción Educativa (Humm):** Interfaz de comunicación que permite a una computadora conectarse mediante un puerto USB con dispositivos que se comunican por niveles seriales TTL (UART a 3.3V o 5V).
- **Posible Uso / Proyecto Escolar:** Herramienta indispensable para programar placas Pro Mini (como KS0247), depurar módulos Wi-Fi/Bluetooth y observar consolas de depuración.
- **Observaciones y Trazabilidad:** Clasificación A. Chip CP2102 confiable con drivers estándar.

---

## 5. Tabla Maestra de los 72 Productos Curados

| N° | SKU Proveedor | Nombre Comercial Humm | Categoría | Precio CLP | Nivel | Compat. Verificada | Compat. Propuesta | Advertencia Seguridad |
| :-: | :--- | :--- | :--- | :---: | :---: | :--- | :--- | :---: |
| 01 | `KS0486` | Placa Keyestudio PLUS con USB-C compatible co... | Arduino y controla | $26,912 | `INICIAL` | Arduino | Arduino | No |
| 02 | `KS0502` | Placa Keyestudio MEGA 2560 PRO compatible con... | Arduino y controla | $44,859 | `AVANZADO` | Arduino | Arduino | No |
| 03 | `KS0547` | Placa Keyestudio Nano Plus con USB-C compatib... | Arduino y controla | $21,062 | `INTERMEDIO` | Arduino | Arduino | No |
| 04 | `KS0503` | Placa Keyestudio Pro Micro 5V (ATmega32U4) co... | Arduino y controla | $25,742 | `INTERMEDIO` | Arduino | Arduino | No |
| 05 | `KS0247` | Placa Keyestudio Pro Mini 5V/16MHz (Requiere ... | Arduino y controla | $17,551 | `AVANZADO` | Arduino | Arduino | No |
| 06 | `KS0004` | Shield de Expansión de Sensores V5 para Ardui... | Arduino y controla | $15,446 | `INICIAL` | Arduino | Arduino | No |
| 07 | `KS0003` | Protoshield para Arduino Uno con Mini Protobo... | Arduino y controla | $14,510 | `INTERMEDIO` | Arduino | Arduino | No |
| 08 | `KS5013` | Placa Keyestudio 328 WIFI PLUS (Arduino Uno R... | Arduino y controla | $32,738 | `INTERMEDIO` | Arduino/ESP8266 | Arduino/ESP8266 | No |
| 09 | `KS0034` | Sensor Digital de Temperatura y Humedad DHT11... | Sensores y módulos | $10,063 | `INICIAL` | Arduino | Arduino/micro:bit/ESP32/Raspberry Pi | No |
| 10 | `KS0430` | Sensor Digital de Temperatura y Humedad DHT22... | Sensores y módulos | $19,423 | `INTERMEDIO` | Arduino | Arduino/ESP32/micro:bit/Raspberry Pi | No |
| 11 | `KS0049` | Sensor de Humedad de Suelo para Arduino y mic... | Sensores y módulos | $8,894 | `INICIAL` | Arduino | Arduino/micro:bit/ESP32 | No |
| 12 | `KS0052` | Sensor Infrarrojo Pasivo de Movimiento PIR Ke... | Sensores y módulos | $10,063 | `INICIAL` | Arduino | Arduino/micro:bit/ESP32/Raspberry Pi | No |
| 13 | `KS0040` | Sensor de Gas Combustible y Humo MQ-2 Keyestu... | Sensores y módulos | $10,999 | `INTERMEDIO` | Arduino | Arduino/ESP32 | ⚠️ Sí |
| 14 | `KS0028` | Módulo Sensor de Luz Fotorresistencia (LDR) K... | Sensores y módulos | $8,894 | `INICIAL` | Otros | Arduino/micro:bit/ESP32 | No |
| 15 | `KS0105` | Sensor de Sonido Analógico Keyestudio EASY Pl... | Sensores y módulos | $11,232 | `INICIAL` | Arduino | Arduino | No |
| 16 | `KS0116` | Sensor de Llama Keyestudio EASY Plug (Conecto... | Sensores y módulos | $11,232 | `INICIAL` | Arduino | Arduino | ⚠️ Sí |
| 17 | `KS0050` | Sensor Seguidor de Línea Infrarrojo Keyestudi... | Sensores y módulos | $8,894 | `INICIAL` | Arduino | Arduino/micro:bit/ESP32 | No |
| 18 | `KS0120` | Sensor de Obstáculos Infrarrojo Keyestudio EA... | Sensores y módulos | $11,701 | `INICIAL` | Arduino | Arduino | No |
| 19 | `19720010` | Sonda de Temperatura Sumergible en Acero Inox... | Sensores y módulos | $4,656 | `INTERMEDIO` | Arduino | Arduino/micro:bit/ESP32/Raspberry Pi | No |
| 20 | `KS6057` | Sensor Inercial IMU MPU6050 (Acelerómetro + G... | Sensores y módulos | $12,871 | `INTERMEDIO` | Arduino | Arduino/ESP32/micro:bit | No |
| 21 | `KS0031` | Módulo Sensor Táctil Capacitivo Digital Keyes... | Sensores y módulos | $8,894 | `INICIAL` | Arduino | Arduino/micro:bit/ESP32 | No |
| 22 | `KS0048` | Módulo Sensor de Nivel de Agua y Detección de... | Sensores y módulos | $8,894 | `INICIAL` | Arduino | Arduino/micro:bit/ESP32 | No |
| 23 | `KS0494` | Sensor de Color I2C TCS34725 Keyestudio Honey... | Sensores y módulos | $16,359 | `INTERMEDIO` | micro:bit | micro:bit/Arduino | No |
| 24 | `KS0492` | Sensor Magnético de Efecto Hall Keyestudio Ho... | Sensores y módulos | $9,829 | `INICIAL` | micro:bit | micro:bit/Arduino | No |
| 25 | `KS0272` | Sensor Piezoeléctrico Cerámico Analógico de V... | Sensores y módulos | $8,658 | `INICIAL` | Arduino | Arduino/micro:bit/ESP32 | No |
| 26 | `KS0171` | Sensor Óptico de Pulso Cardíaco XD-58C Keyest... | Sensores y módulos | $10,999 | `INTERMEDIO` | Otros | Arduino/micro:bit/ESP32 | ⚠️ Sí |
| 27 | `KS0047` | Sensor de Calidad de Aire MQ-135 Keyestudio... | Sensores y módulos | $10,999 | `INTERMEDIO` | Otros | Arduino/ESP32 | ⚠️ Sí |
| 28 | `KS0275` | Módulo Divisor de Tensión para Medición de Vo... | Sensores y módulos | $8,894 | `INICIAL` | Arduino | Arduino/ESP32/micro:bit | No |
| 29 | `CR0011` | Chasis de Robot Móvil 4WD con 4 Motores DC y ... | Robótica y vehícul | $39,783 | `INTERMEDIO` | Arduino | Arduino/ESP32/micro:bit/Raspberry Pi | ⚠️ Sí |
| 30 | `CR0019` | Chasis de Robot Móvil 2WD de Dos Niveles con ... | Robótica y vehícul | $35,080 | `INICIAL` | Arduino | Arduino/micro:bit/ESP32/Raspberry Pi | ⚠️ Sí |
| 31 | `CR0033 CR0034` | Chasis de Aluminio 4WD con Ruedas Mecanum par... | Robótica y vehícul | $50,546 | `AVANZADO` | Arduino/Raspberry Pi | Arduino/Raspberry Pi | ⚠️ Sí |
| 32 | `KS4039` | Brazo Robótico 4DOF para micro:bit — Sin Plac... | Robótica y vehícul | $98,286 | `INTERMEDIO` | micro:bit | micro:bit | No |
| 33 | `KS0326` | Pack de 3 Servomotores Micro SG90 9g Keyestud... | Motores y movimien | $21,039 | `INICIAL` | Arduino | Arduino/micro:bit/ESP32/Raspberry Pi | No |
| 34 | `OR0428` | Servomotor de Rotación Continua 360° en Bloqu... | Motores y movimien | $19,658 | `INICIAL` | Arduino | Arduino/micro:bit/ESP32 | No |
| 35 | `KS0140` | Motor Paso a Paso 28BYJ-48 (5V) con Módulo Co... | Motores y movimien | $14,041 | `INTERMEDIO` | Otros | Arduino/Raspberry Pi/ESP32 | No |
| 36 | `MD0140` | Módulo Controlador Dual de Motores DC Puente ... | Motores y movimien | $6,785 | `INICIAL` | Arduino | Arduino/micro:bit/ESP32/Raspberry Pi | No |
| 37 | `KS0057` | Módulo de 2 Relés con Optoacoplador (5V) Keye... | Motores y movimien | $15,913 | `INTERMEDIO` | Arduino/Otros | Arduino/ESP32/micro:bit/Raspberry Pi | ⚠️ Sí |
| 38 | `60320025` | Protoboard Transparente de 830 Puntos de Cont... | Electrónica y prot | $5,802 | `INICIAL` | Otros | Otros | No |
| 39 | `KS0331` | Pack de 3 Protoboards de 400 Puntos Keyestudi... | Electrónica y prot | $21,039 | `INICIAL` | Otros | Otros | No |
| 40 | `KT0072` | Set de 120 Cables de Conexión Dupont de 10 cm... | Electrónica y prot | $6,998 | `INICIAL` | Arduino/Otros | Otros/Arduino/micro:bit/Raspberry Pi/ESP32 | No |
| 41 | `KT0065` | Set de 120 Cables de Conexión Dupont Largos d... | Electrónica y prot | $8,894 | `INICIAL` | Arduino/Otros | Otros/Arduino/micro:bit/Raspberry Pi/ESP32 | No |
| 42 | `KS0014` | Módulo Potenciómetro Rotativo Analógico 10k K... | Electrónica y prot | $9,361 | `INICIAL` | Arduino | Arduino/Otros | No |
| 43 | `KS0029` | Módulo Pulsador Digital de Botón Momentáneo K... | Electrónica y prot | $8,894 | `INICIAL` | Arduino | Arduino/Otros | No |
| 44 | `KS0018` | Módulo Zumbador Activo (Buzzer) de Señal Acús... | Electrónica y prot | $8,894 | `INICIAL` | Arduino | Arduino/micro:bit/ESP32/Raspberry Pi | No |
| 45 | `KS0332` | Set de Prototipado 3 en 1: Fuente 3.3V/5V + P... | Electrónica y prot | $25,719 | `INICIAL` | Arduino/Otros | Otros/Arduino | ⚠️ Sí |
| 46 | `KS0061` | Pantalla LCD 1602 con Módulo I2C Integrado (F... | Pantallas e intera | $17,551 | `INICIAL` | Arduino | Arduino/ESP32/Raspberry Pi/micro:bit | No |
| 47 | `KS0271` | Pantalla Gráfica OLED 0.96 Pulgadas I2C (128x... | Pantallas e intera | $12,871 | `INTERMEDIO` | Arduino | Arduino/ESP32/Raspberry Pi/micro:bit | No |
| 48 | `KS0481` | Módulo Joystick Analógico de 2 Ejes Honeycomb... | Pantallas e intera | $9,829 | `INICIAL` | micro:bit | micro:bit/Arduino | No |
| 49 | `MD0089` | Pack de 3 Teclados Matriciales de Membrana 4x... | Pantallas e intera | $6,998 | `INTERMEDIO` | Arduino/Otros | Arduino/ESP32/Raspberry Pi | No |
| 50 | `KS0163` | Shield de 40 LEDs RGB Direccionables WS2812 p... | Pantallas e intera | $22,935 | `INTERMEDIO` | Arduino | Arduino | No |
| 51 | `KS0310` | Módulo Semáforo Escolar con LEDs Rojo, Amaril... | Pantallas e intera | $9,361 | `INICIAL` | Arduino | Arduino/micro:bit/ESP32/Raspberry Pi | No |
| 52 | `KS0434` | Placa de Expansión de Pines I/O para BBC micr... | Micro:bit y acceso | $11,701 | `INICIAL` | micro:bit | micro:bit | No |
| 53 | `MB0110` | Kit Oficial BBC micro:bit V2 Go (Tarjeta + Ca... | Micro:bit y acceso | $66,929 | `INICIAL` | micro:bit | micro:bit | No |
| 54 | `KS4038` | Brazo Robótico 4DOF para micro:bit — Con Plac... | Micro:bit y acceso | $150,705 | `INTERMEDIO` | micro:bit | micro:bit | No |
| 55 | `KS0802` | Kit Didáctico Creativo Crocodile con Pinzas C... | Micro:bit y acceso | $101,889 | `INICIAL` | micro:bit | micro:bit | No |
| 56 | `KT0284` | Pack de 4 Motores DC / Servos Continuos de Ej... | Micro:bit y acceso | $51,483 | `INICIAL` | micro:bit | micro:bit | No |
| 57 | `KS0219` | Adaptador GPIO en T con Cable de 40 Pines y P... | Raspberry Pi y acc | $21,529 | `INTERMEDIO` | Raspberry Pi | Raspberry Pi | No |
| 58 | `SMP0023` | Cámara 5MP 1080p con Cable Plano CSI para Ras... | Raspberry Pi y acc | $18,019 | `AVANZADO` | Raspberry Pi | Raspberry Pi | No |
| 59 | `60520146` | Carcasa Metálica de Aluminio con Ventilador A... | Raspberry Pi y acc | $38,612 | `INICIAL` | Raspberry Pi | Raspberry Pi | No |
| 60 | `67600041` | Soporte Acrílico Orientable para Cámara Raspb... | Raspberry Pi y acc | $11,701 | `INICIAL` | Raspberry Pi | Raspberry Pi | No |
| 61 | `KS0255` | Shield de Comunicación Bluetooth 4.0 BLE para... | IoT y comunicación | $25,719 | `INTERMEDIO` | Arduino | Arduino | No |
| 62 | `MD0322` | Módulo Wi-Fi Serial ESP8266 para Arduino (Con... | IoT y comunicación | $5,850 | `AVANZADO` | Arduino/ESP8266 | Arduino/ESP8266 | No |
| 63 | `KS0205` | Módulo Lector/Grabador RFID RC522 (13.56 MHz)... | IoT y comunicación | $10,766 | `INTERMEDIO` | Arduino | Arduino/ESP32/Raspberry Pi | No |
| 64 | `MD0040` | Módulo Transceptor Inalámbrico por Radiofrecu... | IoT y comunicación | $9,361 | `INTERMEDIO` | Arduino | Arduino/micro:bit/ESP32/Raspberry Pi | No |
| 65 | `KS0026` | Módulo Receptor Infrarrojo de 38 kHz para Con... | IoT y comunicación | $8,894 | `INICIAL` | Arduino | Arduino/micro:bit/ESP32 | No |
| 66 | `KS0389` | Shield Wi-Fi ESP8266 para Arduino Uno con Con... | IoT y comunicación | $23,378 | `INTERMEDIO` | Arduino/ESP8266 | Arduino/ESP8266 | No |
| 67 | `KS0541` | Kit de Componentes para Arduino (20 Proyectos... | Kits educativos in | $45,633 | `INICIAL` | Arduino | Arduino | No |
| 68 | `KS0487` | Maletín Multi-Sensor 37 en 1 Keyestudio V3.0 ... | Kits educativos in | $85,883 | `INICIAL` | Arduino | Arduino/micro:bit/ESP32/Raspberry Pi | No |
| 69 | `KS0567` | Kit Temático Granja Inteligente (Smart Farm) ... | Kits educativos in | $142,749 | `INTERMEDIO` | ESP32/Arduino | ESP32/Arduino | No |
| 70 | `49500005` | Multímetro Digital Portátil XL830L con Funda ... | Herramientas y acc | $29,251 | `INICIAL` | Otros | Otros | ⚠️ Sí |
| 71 | `49500004` | Multímetro Digital de Banco DT9205A con Panta... | Herramientas y acc | $35,103 | `INTERMEDIO` | Otros | Otros | ⚠️ Sí |
| 72 | `MD0118` | Módulo Conversor USB a Serial UART TTL CP2102... | Herramientas y acc | $9,478 | `INTERMEDIO` | Arduino/Otros | Otros/Arduino | No |

---

## 6. Estado del Sistema al Cierre de Fase 3

1. **Catálogo Maestro:** 929 productos conservados íntegramente.
2. **Catálogo Curado Aprobado:** 72 productos en `estado_curaduria = VALIDADO`.
3. **Catálogo Público:** 0 productos publicados (`publicado = False` en los 929 productos).
4. **Trazabilidad Implementada:** 5 campos de trazabilidad y campos de compatibilidad verificada/propuesta y advertencias de seguridad operativos en base de datos.
5. **Especificación Técnica Neutra:** Mantenida en `NO_REVISADO` para validación progresiva según demanda comercial, cumpliendo la regla de que solo `VALIDADO_HUMM` puede emitir cotización formal.
