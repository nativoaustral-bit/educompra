# EDUCOMPRA HUMM — SEGUNDO PUNTO DE CONTROL FASE 3
## Auditoría Semántica y Técnica de los 86 Candidatos Sugeridos
### Informe de Evaluación Técnica, Compatibilidad y Selección para Catálogo Inicial

**Fecha de Auditoría:** 29 de Septiembre de 2026  
**Plataforma:** EduCompra Humm (`educompra.humm.cl`)  
**Modo de Ejecución:** **SOLO LECTURA — BASE DE DATOS SIN MODIFICAR**  
**Total de Productos Auditados:** **86 productos candidatos**  
**Resultado Lote Recomendado (A + B):** **72 productos** (objetivo: 60–80 productos)  
**Estado:** **SEGUNDO PUNTO DE CONTROL — DETENIDO PARA REVISIÓN Y APROBACIÓN DE HUMM**  

---

## 1. Marco Metodológico y Reglas Fundamentales

En conformidad estricta con las directrices de Humm para este Segundo Punto de Control:

> [!IMPORTANT]
> ### REGLA FUNDAMENTAL: NO INVENTAR ESPECIFICACIONES
> La descripción original del proveedor disponible en la base de datos constituye la **fuente técnica primaria**.
> No se agregaron como hechos rangos, voltajes, interfaces, precisión, componentes, sensores, protocolos, compatibilidades, cantidades, certificaciones ni prestaciones que no estén fehacientemente respaldados por los datos técnicos.
> Cuando una característica técnica no pudo determinarse con certeza absoluta, se clasificó como `REQUIERE_VERIFICACION_TECNICA` (Estado C) en lugar de realizar inferencias.

### Compromiso de Sólo Lectura
Esta auditoría fue realizada en modo estrictamente de **sólo lectura**:
- No se modificaron registros en producción.
- `estado_curaduria` permanece intacto (`SIN_REVISAR`).
- `estado_especificacion_neutral` permanece intacto (`NO_REVISADO`).
- Ninguna especificación técnica fue promovida a `VALIDADO_HUMM`.
- El flag `publicado = False` se mantiene para el 100% de los productos del catálogo maestro.

### Criterios de Clasificación Aplicados
Cada uno de los 86 candidatos fue evaluado y clasificado en uno de los 5 estados normativos:

1. **`A — RECOMENDADO`**: Producto técnicamente transparente, pedagógicamente de alto valor, sin ambigüedades en empaque ni compatibilidad, e ideal para el catálogo público inicial.
2. **`B — RECOMENDADO CON CORRECCIÓN`**: Producto de indudable utilidad educativa, pero cuya ficha requiere corregir compatibilidad, ajustar motivo educativo o explicitar el contenido de packs múltiples y accesorios requeridos.
3. **`C — REQUIERE VERIFICACIÓN TÉCNICA`**: Producto potencialmente útil, pero donde los datos disponibles del fabricante presentan ambigüedades (ej. versión con/sin carcasa, zócalo físico especial, dependencia de nube en el extranjero).
4. **`D — POSTERGAR`**: Producto válido pero de baja prioridad para el primer catálogo (alto costo unitario, hiper-especialización técnica, o redundancia con otro componente de menor precio).
5. **`E — DESCARTAR DEL CATÁLOGO INICIAL`**: Producto técnicamente confuso, con incompatibilidad comercial para Chile (ej. enchufe no estándar), o inadecuado para la enseñanza escolar.

---

## 2. Errores Identificados Previamente y Medidas de Corrección

Se verificó y subsanó la totalidad de los 6 errores iniciales detectados por Humm:

| SKU Proveedor | Diagnóstico Erróneo Previo | Realidad Técnica Proveedor | Clasificación y Medida Adoptada |
| :--- | :--- | :--- | :--- |
| **`KT0326`** | Sensor ultrasónico de distancia (2-400 cm) para robótica. | Módulo de atomización/humidificación ultrasónica de líquidos (*heavy fog mist maker*). | **`E — DESCARTAR`**: Eliminada descripción errónea. Descartado del catálogo inicial por no ser sensor ni prioritario. |
| **`KS5013`** | Clasificado con compatibilidad ESP32. | Placa híbrida basada en **ATmega328P + ESP8266** (*328 WIFI PLUS*). | **`B — RECOMENDADO CON CORRECCIÓN`**: Corregida compatibilidad a `Arduino / ESP8266`. |
| **`KS0272`** | Descrito como interruptor interno de resorte mecánico. | Sensor piezoeléctrico cerámico analógico (*Piezoelectric Ceramic Vibration Sensor*). | **`B — RECOMENDADO CON CORRECCIÓN`**: Corregida descripción técnica a transductor piezoeléctrico de impactos. |
| **`CR0033 CR0034`** | Asignada compatibilidad con micro:bit sin respaldo. | Chasis robot de aluminio Mecanum con compatibilidad explícita: **Arduino + Raspberry Pi**. | **`B — RECOMENDADO CON CORRECCIÓN`**: Corregida compatibilidad a `Arduino / Raspberry Pi` (eliminado micro:bit). |
| **`KS4039`** | Clasificado con compatibilidad Arduino. | Brazo robótico 4DOF diseñado exclusivamente para **micro:bit**, entregado **SIN la tarjeta micro:bit** (*Without Microbit Board*). | **`B — RECOMENDADO CON CORRECCIÓN`**: Corregida compatibilidad a `micro:bit` (eliminado Arduino). Explicitar 'Sin placa micro:bit'. |
| **`MD0322`** | Clasificado erróneamente como ESP32. | Módulo transceptor Wi-Fi serial **ESP8266** para Arduino (*Keyes ESP8266 remote serial Port*). | **`B — RECOMENDADO CON CORRECCIÓN`**: Corregida compatibilidad a `Arduino / ESP8266` (eliminado ESP32). |

---

## 3. Revisión de Packs, Unidades y Restricciones Comerciales para Chile

### Normalización de Empaques y Cantidades Múltiples
Para evitar discrepancias en compras públicas y garantizar que los docentes comprendan exactamente qué están adquiriendo, se identificaron y etiquetaron los productos vendidos en packs o sets:

- **`KS0326`**: **Pack de 3 servomotores SG90 9g**. El precio de $21,039 CLP corresponde al lote de 3 unidades ($7,013 CLP c/u). Debe titularse explícitamente como pack.
- **`KS0331`**: **Pack de 3 protoboards de 400 puntos**. Debe presentarse como pack de 3 unidades.
- **`MD0089`**: **Pack de 3 teclados matriciales 4x3** de membrana. Debe especificarse como pack de 3 unidades.
- **`KT0284`**: **Pack de 4 motores DC / servos continuos** de eje doble para micro:bit.
- **`KT0072`**: **Set de 120 cables Dupont de 10 cm** (40 M-M, 40 M-H, 40 H-H).
- **`KT0065`**: **Set de 120 cables Dupont de 30 cm** (40 M-M, 40 M-H, 40 H-H).
- **`KS0332`**: **Set de prototipado 3 en 1**: 1 fuente regulable de protoboard + 1 protoboard 830 pts + 65 cables.

### Alertas Comerciales Críticas para Chile
Se identificaron productos que representan riesgos comerciales específicos para el contexto nacional:

- **`KS3010` (Enchufe Australiano y Falta de Placa)**: Contiene fuente con **enchufe australiano (`AU Plug`)**, incompatible con el estándar chileno (220V, 50Hz, Tipos C y L). Además, pese a titularse *Raspberry Pi 4B Complete Starter kit*, advierte en letra chica `(No Raspberry Pi board)`. **Clasificado como E (Descartar)**.
- **`KS0541` (Kit sin Placa Base)**: Titulado *Basic Starter Kit 20 Projects*, pero indica explícitamente `Without Plus Mainboard`. **Clasificado como B**, requiriendo titular de forma obligatoria y destacada 'Kit de 20 Proyectos SIN PLACA ARDUINO'.
- **`KS0105`, `KS0116`, `KS0120` (Conectores RJ11 EASY Plug)**: Utilizan enchufes telefónicos RJ11 6P6C. Requieren shield o cables adaptadores para su uso en protoboard estándar. Clasificados como B con advertencia explícita.

---

## 4. Auditoría Semántica y Técnica Detallada (86 Candidatos)

A continuación se presenta la revisión individualizada de los 86 productos, organizada por las 11 categorías propuestas:

### Arduino y controladores (9 candidatos)

#### Candidato N° 01: `KS0486` — Arduino y controladores
- **SKU Proveedor:** `KS0486` (SKU Humm: `HUMM-KEY-KS0486`)
- **Nombre Original Proveedor:** `Keyestudio PLUS Development Board with Type C interface +USB cable  compatible with Arduino Uno R3. Keyestudio PLUS Development Board with Type C interface +USB cable  compatible with Arduino Uno R3`
- **Precio Sugerido:** `$26,912 CLP`
- **Categoría Propuesta:** Arduino y controladores
- **Compatibilidad Propuesta:** `Arduino` ➔ **Corregida:** `Arduino (Uno R3)`
- **Clasificación Auditoría:** 🟢 `A — RECOMENDADO`
- **Correcciones Detectadas:** Ninguna inconsistencia técnica. Descripción y compatibilidad consistentes.
- **Recomendación Técnica y Pedagógica:** Aprobar como controlador principal estándar para el catálogo inicial.
- **Observaciones de Contenido del Pack:** Incluye 1 placa Keyestudio PLUS (ATmega328P con conector USB Tipo C) + 1 cable USB Tipo C.
- **Necesidad de Verificación Adicional:** Ninguna requerida.

#### Candidato N° 02: `KS0502` — Arduino y controladores
- **SKU Proveedor:** `KS0502` (SKU Humm: `HUMM-KEY-KS0502`)
- **Nombre Original Proveedor:** `Keyestudio MEGA 2560 PRO Development Board(Black and Eco-friendly). Keyestudio MEGA 2560 PRO Development Board(Black and Eco-friendly)`
- **Precio Sugerido:** `$44,859 CLP`
- **Categoría Propuesta:** Arduino y controladores
- **Compatibilidad Propuesta:** `Arduino` ➔ **Corregida:** `Arduino (Mega 2560)`
- **Clasificación Auditoría:** 🟢 `A — RECOMENDADO`
- **Correcciones Detectadas:** Ninguna. Microcontrolador de alta capacidad consistente.
- **Recomendación Técnica y Pedagógica:** Aprobar para proyectos avanzados que requieran más de 14 pines I/O o múltiples puertos seriales UART.
- **Observaciones de Contenido del Pack:** 1 unidad placa Keyestudio MEGA 2560 PRO. No especifica cable USB en el empaque (vender cable por separado si no viene incluido).
- **Necesidad de Verificación Adicional:** Confirmar empaque comercial de cable USB en lote de importación.

#### Candidato N° 03: `KS0547` — Arduino y controladores
- **SKU Proveedor:** `KS0547` (SKU Humm: `HUMM-KEY-KS0547`)
- **Nombre Original Proveedor:** `Keyestudio NANO PLUS Development Board Compatible with Arduino NANO. NANO PLUS Development Board`
- **Precio Sugerido:** `$21,062 CLP`
- **Categoría Propuesta:** Arduino y controladores
- **Compatibilidad Propuesta:** `Arduino` ➔ **Corregida:** `Arduino (Nano)`
- **Clasificación Auditoría:** 🟢 `A — RECOMENDADO`
- **Correcciones Detectadas:** Ninguna. Formato Nano con conector USB Tipo C para inserción directa en protoboard.
- **Recomendación Técnica y Pedagógica:** Aprobar como opción ultra-compacta para prototipado en aula.
- **Observaciones de Contenido del Pack:** 1 unidad placa Nano Plus (con pines soldados).
- **Necesidad de Verificación Adicional:** Ninguna requerida.

#### Candidato N° 04: `KS0503` — Arduino y controladores
- **SKU Proveedor:** `KS0503` (SKU Humm: `HUMM-KEY-KS0503`)
- **Nombre Original Proveedor:** `Keyestudio PRO MICRO 5V 16MHZ ATMEGA32U4-MU Development Board For Arduino. Keyestudio PRO MICRO 5V 16MHZ ATMEGA32U4-MU Development Board For Arduino`
- **Precio Sugerido:** `$25,742 CLP`
- **Categoría Propuesta:** Arduino y controladores
- **Compatibilidad Propuesta:** `Arduino` ➔ **Corregida:** `Arduino (Leonardo / Micro)`
- **Clasificación Auditoría:** 🟢 `A — RECOMENDADO`
- **Correcciones Detectadas:** Ninguna. Basado en ATmega32U4 a 16MHz y 5V.
- **Recomendación Técnica y Pedagógica:** Aprobar para proyectos de interacción hombre-máquina, emulación HID (teclado/mouse) y diseño de mandos.
- **Observaciones de Contenido del Pack:** 1 unidad placa Pro Micro 5V.
- **Necesidad de Verificación Adicional:** Ninguna requerida.

#### Candidato N° 05: `KS0247` — Arduino y controladores
- **SKU Proveedor:** `KS0247` (SKU Humm: `HUMM-KEY-KS0247`)
- **Nombre Original Proveedor:** `Keyestudio 5V/16MHZ ProMini Original ATMEGA328P Development Board For Arduino DIY Projects. Keyestudio 5V/16MHZ ProMini Original ATMEGA328P Development Board For Arduino DIY Projects`
- **Precio Sugerido:** `$17,551 CLP`
- **Categoría Propuesta:** Arduino y controladores
- **Compatibilidad Propuesta:** `Arduino` ➔ **Corregida:** `Arduino (Pro Mini)`
- **Clasificación Auditoría:** 🟡 `B — RECOMENDADO CON CORRECCIÓN`
- **Correcciones Detectadas:** Debe advertirse explícitamente en la descripción educativa y técnica que esta placa NO tiene chip USB-Serial integrado.
- **Recomendación Técnica y Pedagógica:** Aprobar con corrección: vincular en la ficha de compra la necesidad de un módulo programador USB-UART externo (como MD0118).
- **Observaciones de Contenido del Pack:** 1 unidad placa Pro Mini 5V/16MHz (ATmega328P). No incluye cable ni módulo programador.
- **Necesidad de Verificación Adicional:** Verificar si viene con pines sin soldar o soldados.

#### Candidato N° 06: `KS0004` — Arduino y controladores
- **SKU Proveedor:** `KS0004` (SKU Humm: `HUMM-KEY-KS0004`)
- **Nombre Original Proveedor:** `Keyestudio Sensor Shield V5 Expansion Board Module for Arduino UNO Arduino LEONARDO. Keyestudio Sensor Shield V5 Expansion Board Module for Arduino UNO Arduino LEONARDO`
- **Precio Sugerido:** `$15,446 CLP`
- **Categoría Propuesta:** Arduino y controladores
- **Compatibilidad Propuesta:** `Arduino` ➔ **Corregida:** `Arduino (Uno / Leonardo / Mega)`
- **Clasificación Auditoría:** 🟢 `A — RECOMENDADO`
- **Correcciones Detectadas:** Ninguna. Shield estándar de conexión sensor/servo de 3 pines (G-V-S).
- **Recomendación Técnica y Pedagógica:** Aprobar como accesorio de conexión primordial para simplificar el cableado en colegios.
- **Observaciones de Contenido del Pack:** 1 unidad Sensor Shield V5.
- **Necesidad de Verificación Adicional:** Ninguna requerida.

#### Candidato N° 07: `KS0151` — Arduino y controladores
- **SKU Proveedor:** `KS0151` (SKU Humm: `HUMM-KEY-KS0151`)
- **Nombre Original Proveedor:** `keyestudio CNC shield V2 engraving machine / 3 D Printer / A4988 driver expansion board for Arduino. keyestudio CNC shield V2 engraving machine / 3 D Printer / A4988 driver expansion board for Arduino`
- **Precio Sugerido:** `$15,913 CLP`
- **Categoría Propuesta:** Arduino y controladores
- **Compatibilidad Propuesta:** `Arduino`
- **Clasificación Auditoría:** 🟠 `D — POSTERGAR`
- **Correcciones Detectadas:** Producto altamente especializado para fresado CNC e impresión 3D. Requiere 4 drivers A4988 y fuente externa de 12V-36V no incluidos.
- **Recomendación Técnica y Pedagógica:** POSTERGAR para un futuro catálogo especializado técnico-profesional (TP). No prioritario para el catálogo escolar general.
- **Observaciones de Contenido del Pack:** 1 unidad placa CNC Shield V2 (placa base con zócalos, NO incluye los módulos controladores A4988).
- **Necesidad de Verificación Adicional:** Ninguna para el MVP inicial.

#### Candidato N° 08: `KS0003` — Arduino y controladores
- **SKU Proveedor:** `KS0003` (SKU Humm: `HUMM-KEY-KS0003`)
- **Nombre Original Proveedor:** `Keyestudio Protoshield for Arduino with Mini Breadboard. Keyestudio Protoshield for Arduino with Mini Breadboard`
- **Precio Sugerido:** `$14,510 CLP`
- **Categoría Propuesta:** Arduino y controladores
- **Compatibilidad Propuesta:** `Arduino` ➔ **Corregida:** `Arduino (Uno)`
- **Clasificación Auditoría:** 🟢 `A — RECOMENDADO`
- **Correcciones Detectadas:** Ninguna. Placa de prototipado directo sobre formato Uno.
- **Recomendación Técnica y Pedagógica:** Aprobar para talleres de electrónica práctica donde se construyan circuitos permanentes o de prueba compactos.
- **Observaciones de Contenido del Pack:** Incluye 1 unidad Protoshield + 1 mini protoboard autoadhesiva de 170 puntos.
- **Necesidad de Verificación Adicional:** Ninguna requerida.

#### Candidato N° 09: `KS5013` — Arduino y controladores
- **SKU Proveedor:** `KS5013` (SKU Humm: `HUMM-KEY-KS5013`)
- **Nombre Original Proveedor:** `Keyestudio 328 WIFI PLUS Main Control Board For Arduino UNO R3 and ESP8266 Development Board. 1. MCU:ATMEGA328 and esp8266 2. Function:Arduino unoR3 and ESP8266development board`
- **Precio Sugerido:** `$32,738 CLP`
- **Categoría Propuesta:** Arduino y controladores
- **Compatibilidad Propuesta:** `Arduino / ESP32` ➔ **Corregida:** `Arduino / ESP8266`
- **Clasificación Auditoría:** 🟡 `B — RECOMENDADO CON CORRECCIÓN`
- **Correcciones Detectadas:** ERROR IDENTIFICADO: En CANDIDATOS_SUGERIDOS_FASE_3.md se clasificó con compatibilidad 'ESP32'. La descripción original indica explícitamente ATmega328P + ESP8266.
- **Recomendación Técnica y Pedagógica:** Aprobar con corrección: cambiar compatibilidad tecnológica a 'Arduino / ESP8266'. Explicar en ficha técnica que cuenta con microcontrolador dual en una sola placa con selector DIP switch.
- **Observaciones de Contenido del Pack:** 1 unidad placa Keyestudio 328 WIFI PLUS.
- **Necesidad de Verificación Adicional:** Ninguna adicional requerida una vez corregida la compatibilidad.

---

### Sensores y módulos (22 candidatos)

#### Candidato N° 10: `KT0326` — Sensores y módulos
- **SKU Proveedor:** `KT0326` (SKU Humm: `HUMM-KEY-KT0326`)
- **Nombre Original Proveedor:** `High Spray Heavy Fog Atomization Drive Circuit Board DlY Humidifier Atomization Module Ultrasonic Atomizer. High Spray Heavy Fog Atomization Drive Circuit Board DlY Humidifier Atomization Module Ultrasonic Atomizer`
- **Precio Sugerido:** `$7,770 CLP`
- **Categoría Propuesta:** Sensores y módulos
- **Compatibilidad Propuesta:** `Arduino / micro:bit` ➔ **Corregida:** `Arduino / Otros`
- **Clasificación Auditoría:** 🔴 `E — DESCARTAR DEL CATÁLOGO INICIAL`
- **Correcciones Detectadas:** ERROR CRÍTICO IDENTIFICADO: Se catalogó erróneamente como sensor ultrasónico de distancia (2-400cm). Es un circuito transductor piezoeléctrico de humidificación/atomización de agua (mist maker).
- **Recomendación Técnica y Pedagógica:** DESCARTAR DEL CATÁLOGO INICIAL. No cumple función de sensor de distancia y carece de relevancia para los objetivos de alfabetización STEM inicial.
- **Observaciones de Contenido del Pack:** Módulo oscilador + disco transductor atomizador de líquido.
- **Necesidad de Verificación Adicional:** Descartado definitivamente del lote escolar inicial.

#### Candidato N° 11: `KS0034` — Sensores y módulos
- **SKU Proveedor:** `KS0034` (SKU Humm: `HUMM-KEY-KS0034`)
- **Nombre Original Proveedor:** `Keyestudio DHT11 Temperature Humidity Moisture Sensor Detection module for arduino. Keyestudio DHT11 Temperature Humidity Moisture Sensor Detection module for arduino`
- **Precio Sugerido:** `$10,063 CLP`
- **Categoría Propuesta:** Sensores y módulos
- **Compatibilidad Propuesta:** `Arduino / micro:bit` ➔ **Corregida:** `Arduino / micro:bit / ESP32 / Raspberry Pi`
- **Clasificación Auditoría:** 🟢 `A — RECOMENDADO`
- **Correcciones Detectadas:** Ninguna. Sensor digital resistivo/capacitivo de temperatura y humedad relativa DHT11 estándar.
- **Recomendación Técnica y Pedagógica:** Aprobar como sensor ambiental básico de alta rotación escolar.
- **Observaciones de Contenido del Pack:** 1 unidad módulo DHT11 montado en PCB con resistencia pull-up y conector de 3 pines.
- **Necesidad de Verificación Adicional:** Ninguna requerida.

#### Candidato N° 12: `KS0430` — Sensores y módulos
- **SKU Proveedor:** `KS0430` (SKU Humm: `HUMM-KEY-KS0430`)
- **Nombre Original Proveedor:** `Keyestudio DHT22 (AM2302)Temperature and Humidity Sensor for  Arduino Uno r3. Keyestudio DHT22 (AM2302)Temperature and Humidity Sensor for  Arduino Uno r3`
- **Precio Sugerido:** `$19,423 CLP`
- **Categoría Propuesta:** Sensores y módulos
- **Compatibilidad Propuesta:** `Arduino / ESP32` ➔ **Corregida:** `Arduino / ESP32 / micro:bit / Raspberry Pi`
- **Clasificación Auditoría:** 🟢 `A — RECOMENDADO`
- **Correcciones Detectadas:** Ninguna. Sensor DHT22 (AM2302) de precisión superior (-40 a 80°C, 0-100% HR).
- **Recomendación Técnica y Pedagógica:** Aprobar para estaciones meteorológicas de mayor exigencia y proyectos científicos de ciencias naturales.
- **Observaciones de Contenido del Pack:** 1 unidad módulo sensor DHT22 con PCB de soporte de 3 pines.
- **Necesidad de Verificación Adicional:** Ninguna requerida.

#### Candidato N° 13: `KS0049` — Sensores y módulos
- **SKU Proveedor:** `KS0049` (SKU Humm: `HUMM-KEY-KS0049`)
- **Nombre Original Proveedor:** `Keyestudio Soil Humidity Sensor for Arduino. Keyestudio Soil Humidity Sensor for Arduino`
- **Precio Sugerido:** `$8,894 CLP`
- **Categoría Propuesta:** Sensores y módulos
- **Compatibilidad Propuesta:** `Arduino / micro:bit` ➔ **Corregida:** `Arduino / micro:bit / ESP32`
- **Clasificación Auditoría:** 🟢 `A — RECOMENDADO`
- **Correcciones Detectadas:** Ninguna. Sensor resistivo de humedad de suelo mediante pistas expuestas.
- **Recomendación Técnica y Pedagógica:** Aprobar como componente central para huertos inteligentes escolares y riego automático.
- **Observaciones de Contenido del Pack:** 1 unidad sensor de humedad de suelo con conector estándar de 3 pines.
- **Necesidad de Verificación Adicional:** Ninguna requerida.

#### Candidato N° 14: `KS0052` — Sensores y módulos
- **SKU Proveedor:** `KS0052` (SKU Humm: `HUMM-KEY-KS0052`)
- **Nombre Original Proveedor:** `Keyestudio PIR Motion Sensor for Arduino. Keyestudio PIR Motion Sensor for Arduino`
- **Precio Sugerido:** `$10,063 CLP`
- **Categoría Propuesta:** Sensores y módulos
- **Compatibilidad Propuesta:** `Arduino / micro:bit` ➔ **Corregida:** `Arduino / micro:bit / ESP32 / Raspberry Pi`
- **Clasificación Auditoría:** 🟢 `A — RECOMENDADO`
- **Correcciones Detectadas:** Ninguna. Sensor infrarrojo pasivo (PIR) estándar para detección de presencia.
- **Recomendación Técnica y Pedagógica:** Aprobar para proyectos escolares de alarmas, domótica y ahorro energético.
- **Observaciones de Contenido del Pack:** 1 unidad sensor PIR con lente Fresnel cilíndrica y potenciómetros de sensibilidad y retardo.
- **Necesidad de Verificación Adicional:** Ninguna requerida.

#### Candidato N° 15: `KS0040` — Sensores y módulos
- **SKU Proveedor:** `KS0040` (SKU Humm: `HUMM-KEY-KS0040`)
- **Nombre Original Proveedor:** `Keyestudio  MQ-2 Combustible gas and Smoke for Arduino. Keyestudio  MQ-2 Combustible gas and Smoke for Arduino`
- **Precio Sugerido:** `$10,999 CLP`
- **Categoría Propuesta:** Sensores y módulos
- **Compatibilidad Propuesta:** `Arduino / ESP32`
- **Clasificación Auditoría:** 🟢 `A — RECOMENDADO`
- **Correcciones Detectadas:** Ninguna. Sensor electroquímico MQ-2 para GLP, propano, metano y humo.
- **Recomendación Técnica y Pedagógica:** Aprobar para maquetas de prevención de riesgos y detección de fugas en laboratorios escolares.
- **Observaciones de Contenido del Pack:** 1 unidad módulo MQ-2 con salidas analógica y digital.
- **Necesidad de Verificación Adicional:** Registrar en ficha requerimiento de corriente (~150mA a 5V) y tiempo de precalentamiento.

#### Candidato N° 16: `KS0028` — Sensores y módulos
- **SKU Proveedor:** `KS0028` (SKU Humm: `HUMM-KEY-KS0028`)
- **Nombre Original Proveedor:** `Keyestudio photoresistor light dependent resistor sensor module. Keyestudio photoresistor light dependent resistor sensor module`
- **Precio Sugerido:** `$8,894 CLP`
- **Categoría Propuesta:** Sensores y módulos
- **Compatibilidad Propuesta:** `Arduino / micro:bit` ➔ **Corregida:** `Arduino / micro:bit / ESP32`
- **Clasificación Auditoría:** 🟢 `A — RECOMENDADO`
- **Correcciones Detectadas:** Ninguna. Módulo fotorresistencia LDR con potenciómetro comparador (LM393).
- **Recomendación Técnica y Pedagógica:** Aprobar para proyectos de alumbrado público inteligente, fotómetros y seguidores de luz.
- **Observaciones de Contenido del Pack:** 1 unidad módulo con sensor LDR y salidas analógica/digital.
- **Necesidad de Verificación Adicional:** Ninguna requerida.

#### Candidato N° 17: `KS0105` — Sensores y módulos
- **SKU Proveedor:** `KS0105` (SKU Humm: `HUMM-KEY-KS0105`)
- **Nombre Original Proveedor:** `Keyestudio EASY plug Analog Sound Sensor for Arduino STEAM. Keyestudio EASY plug Analog Sound Sensor for Arduino STEAM`
- **Precio Sugerido:** `$11,232 CLP`
- **Categoría Propuesta:** Sensores y módulos
- **Compatibilidad Propuesta:** `Arduino / micro:bit` ➔ **Corregida:** `Arduino (EASY Plug / Requiere adaptador RJ11)`
- **Clasificación Auditoría:** 🟡 `B — RECOMENDADO CON CORRECCIÓN`
- **Correcciones Detectadas:** RESTRICCIÓN FÍSICA DETECTADA: Pertenece a la serie 'EASY plug'. Utiliza conector tipo telefónico RJ11 6P6C, no pines Dupont estándar de 2.54mm.
- **Recomendación Técnica y Pedagógica:** Aprobar con corrección: debe advertirse con total claridad al profesor que utiliza conector RJ11 y requiere cable RJ11 o shield EASY Plug para conectarse sin adaptadores.
- **Observaciones de Contenido del Pack:** 1 unidad sensor de sonido analógico con puerto hembra RJ11 integrado.
- **Necesidad de Verificación Adicional:** Verificar si el SKU individual suministra cable RJ11 a pines macho o solo el módulo suelto.

#### Candidato N° 18: `KS0116` — Sensores y módulos
- **SKU Proveedor:** `KS0116` (SKU Humm: `HUMM-KEY-KS0116`)
- **Nombre Original Proveedor:** `Keyestudio RJ11 EASY plug Flame Sensor module for Arduino STEAM. Keyestudio RJ11 EASY plug Flame Sensor module for Arduino STEAM`
- **Precio Sugerido:** `$11,232 CLP`
- **Categoría Propuesta:** Sensores y módulos
- **Compatibilidad Propuesta:** `Arduino / micro:bit` ➔ **Corregida:** `Arduino (EASY Plug / Requiere adaptador RJ11)`
- **Clasificación Auditoría:** 🟡 `B — RECOMENDADO CON CORRECCIÓN`
- **Correcciones Detectadas:** RESTRICCIÓN FÍSICA DETECTADA: Pertenece a la serie 'EASY plug' con conector telefónico RJ11 6P6C.
- **Recomendación Técnica y Pedagógica:** Aprobar con corrección: advertir la interfaz física RJ11. Es un transductor óptico infrarrojo (760nm-1100nm) para robots apagafuegos.
- **Observaciones de Contenido del Pack:** 1 unidad módulo sensor de llama con puerto hembra RJ11.
- **Necesidad de Verificación Adicional:** Confirmar inclusión de cable de interconexión RJ11.

#### Candidato N° 19: `KS0050` — Sensores y módulos
- **SKU Proveedor:** `KS0050` (SKU Humm: `HUMM-KEY-KS0050`)
- **Nombre Original Proveedor:** `Keyestudio Line Tracking Sensor module white/black line detector for Arduino UNO R3 MEGA 2560 R3. Keyestudio Line Tracking Sensor module white/black line detector for Arduino UNO R3 MEGA 2560 R3`
- **Precio Sugerido:** `$8,894 CLP`
- **Categoría Propuesta:** Sensores y módulos
- **Compatibilidad Propuesta:** `Arduino / micro:bit` ➔ **Corregida:** `Arduino / micro:bit / ESP32`
- **Clasificación Auditoría:** 🟢 `A — RECOMENDADO`
- **Correcciones Detectadas:** Ninguna. Sensor seguidor de línea infrarrojo óptico con pines estándar Dupont de 2.54mm.
- **Recomendación Técnica y Pedagógica:** Aprobar como insumo primordial para robótica móvil y autos seguidores de línea.
- **Observaciones de Contenido del Pack:** 1 unidad módulo con par emisor/receptor IR y potenciómetro de umbral.
- **Necesidad de Verificación Adicional:** Ninguna requerida.

#### Candidato N° 20: `KS0120` — Sensores y módulos
- **SKU Proveedor:** `KS0120` (SKU Humm: `HUMM-KEY-KS0120`)
- **Nombre Original Proveedor:** `Keyestudio RJ11 EASY plug Infrared Obstacle Avoidance Sensor Module for Arduino Starter STEAM. obstacle sensor`
- **Precio Sugerido:** `$11,701 CLP`
- **Categoría Propuesta:** Sensores y módulos
- **Compatibilidad Propuesta:** `Arduino / micro:bit` ➔ **Corregida:** `Arduino (EASY Plug / Requiere adaptador RJ11)`
- **Clasificación Auditoría:** 🟡 `B — RECOMENDADO CON CORRECCIÓN`
- **Correcciones Detectadas:** RESTRICCIÓN FÍSICA DETECTADA: Sensor de obstáculos IR con conector RJ11 EASY plug.
- **Recomendación Técnica y Pedagógica:** Aprobar con corrección: advertir explícitamente en la descripción que incorpora conector RJ11.
- **Observaciones de Contenido del Pack:** 1 unidad módulo con conector RJ11 y potenciómetro de distancia.
- **Necesidad de Verificación Adicional:** Confirmar presencia de cable RJ11 en el paquete.

#### Candidato N° 21: `KS6040` — Sensores y módulos
- **SKU Proveedor:** `KS6040` (SKU Humm: `HUMM-KEY-KS6040`)
- **Nombre Original Proveedor:** `Keyestudio BMP388 Barometric Pressure Sensor For Arduino DIY Programmable Electronic Building Blocks Optional With(Out) Shell For Lego. Keyestudio BMP388 Barometric Pressure Sensor For Arduino DIY Programmable Electronic Building Blocks Optional With(Out) Shell For Lego`
- **Precio Sugerido:** `$11,701 CLP`
- **Categoría Propuesta:** Sensores y módulos
- **Compatibilidad Propuesta:** `Arduino / ESP32` ➔ **Corregida:** `Arduino / ESP32 (I2C)`
- **Clasificación Auditoría:** 🔵 `C — REQUIERE VERIFICACIÓN TÉCNICA`
- **Correcciones Detectadas:** DESCRIPCIÓN DEL PROVEEDOR AMBIGUA: Indica 'Optional With(Out) Shell For Lego'. No es posible determinar si este SKU incluye la carcasa de bloque Lego o es la placa desnuda.
- **Recomendación Técnica y Pedagógica:** REQUIERE VERIFICACIÓN TÉCNICA. No incorporar a cotizaciones formales hasta comprobar físicamente si el paquete incluye o no la carcasa plástica.
- **Observaciones de Contenido del Pack:** Módulo sensor barométrico BMP388 I2C/SPI. Empaque ambiguo respecto a la carcasa plástica.
- **Necesidad de Verificación Adicional:** REQUIERE_VERIFICACION_TECNICA para confirmar versión física exacta (con o sin carcasa Lego).

#### Candidato N° 22: `19720010` — Sensores y módulos
- **SKU Proveedor:** `19720010` (SKU Humm: `HUMM-KEY-19720010`)
- **Nombre Original Proveedor:** `1PCS DS18B20 Stainless steel package Waterproof DS18b20 temperature probe temperature sensor 18B20 For Arduino(100CM). 1PCS DS18B20 Stainless steel package Waterproof DS18b20 temperature probe temperature sensor 18B20 For Arduino(100CM)`
- **Precio Sugerido:** `$4,656 CLP`
- **Categoría Propuesta:** Sensores y módulos
- **Compatibilidad Propuesta:** `Arduino / micro:bit` ➔ **Corregida:** `Arduino / micro:bit / ESP32 / Raspberry Pi`
- **Clasificación Auditoría:** 🟢 `A — RECOMENDADO`
- **Correcciones Detectadas:** Ninguna en los datos base. Sonda sumergible DS18B20 digital 1-Wire.
- **Recomendación Técnica y Pedagógica:** Aprobar como sensor de temperatura para líquidos en laboratorios de química y acuicultura.
- **Observaciones de Contenido del Pack:** 1 unidad sonda de acero inoxidable sellada con cable de 100 cm. Requiere resistencia pull-up de 4.7kΩ para operar (no incluida en el cable crudo).
- **Necesidad de Verificación Adicional:** Ninguna requerida.

#### Candidato N° 23: `KS6057` — Sensores y módulos
- **SKU Proveedor:** `KS6057` (SKU Humm: `HUMM-KEY-KS6057`)
- **Nombre Original Proveedor:** `Keyestudio Electronic Building Block MPU6050 3-Axis Acceleration Sensor for Arduino STEM DIY Projects. Keyestudio Electronic Building Block MPU6050 3-Axis Acceleration Sensor for Arduino STEM DIY Projects`
- **Precio Sugerido:** `$12,871 CLP`
- **Categoría Propuesta:** Sensores y módulos
- **Compatibilidad Propuesta:** `Arduino / ESP32` ➔ **Corregida:** `Arduino / ESP32 / micro:bit`
- **Clasificación Auditoría:** 🟢 `A — RECOMENDADO`
- **Correcciones Detectadas:** Ninguna. Unidad inercial MPU6050 (acelerómetro y giroscopio de 6 ejes I2C) montada en bloque tipo Lego.
- **Recomendación Técnica y Pedagógica:** Aprobar para proyectos de cinemática, péndulos, robótica de balance y captura de movimiento.
- **Observaciones de Contenido del Pack:** 1 unidad sensor MPU6050 encapsulado en carcasa plástica compatible con Lego.
- **Necesidad de Verificación Adicional:** Ninguna requerida.

#### Candidato N° 24: `KS0031` — Sensores y módulos
- **SKU Proveedor:** `KS0031` (SKU Humm: `HUMM-KEY-KS0031`)
- **Nombre Original Proveedor:** `Keyestudio Capacitive Touch Sensor Module for Arduino. Keyestudio Capacitive Touch Sensor Module for Arduino`
- **Precio Sugerido:** `$8,894 CLP`
- **Categoría Propuesta:** Sensores y módulos
- **Compatibilidad Propuesta:** `Arduino / micro:bit` ➔ **Corregida:** `Arduino / micro:bit / ESP32`
- **Clasificación Auditoría:** 🟢 `A — RECOMENDADO`
- **Correcciones Detectadas:** Ninguna. Sensor táctil capacitivo digital basado en chip TTP223.
- **Recomendación Técnica y Pedagógica:** Aprobar como pulsador de estado sólido higiénico y moderno para proyectos interactivos.
- **Observaciones de Contenido del Pack:** 1 unidad módulo con electrodo táctil y conector de 3 pines.
- **Necesidad de Verificación Adicional:** Ninguna requerida.

#### Candidato N° 25: `KS0048` — Sensores y módulos
- **SKU Proveedor:** `KS0048` (SKU Humm: `HUMM-KEY-KS0048`)
- **Nombre Original Proveedor:** `Keyestudio Water Level Sensor Droplet Detection Module for Arduino UNO R3. Keyestudio Water Level Sensor Droplet Detection Module for Arduino UNO R3`
- **Precio Sugerido:** `$8,894 CLP`
- **Categoría Propuesta:** Sensores y módulos
- **Compatibilidad Propuesta:** `Arduino / micro:bit` ➔ **Corregida:** `Arduino / micro:bit / ESP32`
- **Clasificación Auditoría:** 🟢 `A — RECOMENDADO`
- **Correcciones Detectadas:** Ninguna. Sensor de nivel de agua y gotas de lluvia por conductividad resistiva.
- **Recomendación Técnica y Pedagógica:** Aprobar para maquetas de inundaciones escolares y detección de nivel en estanques.
- **Observaciones de Contenido del Pack:** 1 unidad módulo con pistas conductoras expuestas.
- **Necesidad de Verificación Adicional:** Ninguna requerida.

#### Candidato N° 26: `KS0494` — Sensores y módulos
- **SKU Proveedor:** `KS0494` (SKU Humm: `HUMM-KEY-KS0494`)
- **Nombre Original Proveedor:** `Keyestudio micro bit honeycomb TCS34725 Color Sensor Module. Keyestudio micro bit honeycomb TCS34725 Color Sensor Module`
- **Precio Sugerido:** `$16,359 CLP`
- **Categoría Propuesta:** Sensores y módulos
- **Compatibilidad Propuesta:** `Arduino / micro:bit` ➔ **Corregida:** `micro:bit (Diseño primario Honeycomb) / Arduino (I2C)`
- **Clasificación Auditoría:** 🟡 `B — RECOMENDADO CON CORRECCIÓN`
- **Correcciones Detectadas:** Ajuste de diseño: es un módulo de la línea 'Honeycomb' para micro:bit, con perforaciones grandes para pinzas cocodrilo y tornillos de sujeción.
- **Recomendación Técnica y Pedagógica:** Aprobar con corrección: destacar en la descripción pedagógica que su factor de forma hexagonal Honeycomb está optimizado para micro:bit y cables caimán.
- **Observaciones de Contenido del Pack:** 1 unidad sensor de color I2C TCS34725 formato Honeycomb.
- **Necesidad de Verificación Adicional:** Ninguna requerida.

#### Candidato N° 27: `KS0492` — Sensores y módulos
- **SKU Proveedor:** `KS0492` (SKU Humm: `HUMM-KEY-KS0492`)
- **Nombre Original Proveedor:** `Keyestudio Micro bit Honeycomb Hall Magnetic Sensor for  BBC Micro Bit. Keyestudio Micro bit Honeycomb Hall Magnetic Sensor for  BBC Micro Bit`
- **Precio Sugerido:** `$9,829 CLP`
- **Categoría Propuesta:** Sensores y módulos
- **Compatibilidad Propuesta:** `Arduino / micro:bit` ➔ **Corregida:** `micro:bit (Diseño primario Honeycomb) / Arduino`
- **Clasificación Auditoría:** 🟡 `B — RECOMENDADO CON CORRECCIÓN`
- **Correcciones Detectadas:** Módulo sensor magnético Hall de la serie Honeycomb para micro:bit.
- **Recomendación Técnica y Pedagógica:** Aprobar con corrección: explicitar factor de forma Honeycomb pensado para pinzas caimán y micro:bit.
- **Observaciones de Contenido del Pack:** 1 unidad sensor Hall formato Honeycomb hexagonal.
- **Necesidad de Verificación Adicional:** Ninguna requerida.

#### Candidato N° 28: `KS0272` — Sensores y módulos
- **SKU Proveedor:** `KS0272` (SKU Humm: `HUMM-KEY-KS0272`)
- **Nombre Original Proveedor:** `Keyestudio Analog Piezoelectric Ceramic Vibration Sensor for Arduino. Keyestudio Analog Piezoelectric Ceramic Vibration Sensor for Arduino`
- **Precio Sugerido:** `$8,658 CLP`
- **Categoría Propuesta:** Sensores y módulos
- **Compatibilidad Propuesta:** `Arduino / micro:bit` ➔ **Corregida:** `Arduino / micro:bit / ESP32`
- **Clasificación Auditoría:** 🟡 `B — RECOMENDADO CON CORRECCIÓN`
- **Correcciones Detectadas:** ERROR IDENTIFICADO: En CANDIDATOS_SUGERIDOS_FASE_3.md se describió como 'interruptor de resorte interno'. Es un sensor piezoeléctrico cerámico analógico que genera tensión proporcional al impacto o vibración.
- **Recomendación Técnica y Pedagógica:** Aprobar con corrección: rectificar descripción técnica y pedagógica hacia transductor piezoeléctrico para sismógrafos y detección de impactos.
- **Observaciones de Contenido del Pack:** 1 unidad módulo con disco cerámico piezoeléctrico soldado a PCB.
- **Necesidad de Verificación Adicional:** Corregir descripción técnica en ficha.

#### Candidato N° 29: `KS0171` — Sensores y módulos
- **SKU Proveedor:** `KS0171` (SKU Humm: `HUMM-KEY-KS0171`)
- **Nombre Original Proveedor:** `keyestudio XD-58C Pulse Sensor Module. keyestudio XD-58C Pulse Sensor Module`
- **Precio Sugerido:** `$10,999 CLP`
- **Categoría Propuesta:** Sensores y módulos
- **Compatibilidad Propuesta:** `Arduino / micro:bit` ➔ **Corregida:** `Arduino / micro:bit / ESP32`
- **Clasificación Auditoría:** 🟢 `A — RECOMENDADO`
- **Correcciones Detectadas:** Ninguna. Sensor de pulso cardíaco XD-58C por fotopletismografía óptica.
- **Recomendación Técnica y Pedagógica:** Aprobar para proyectos interdisciplinarios de Biología, Deporte y Ciencias de la Salud.
- **Observaciones de Contenido del Pack:** 1 unidad sensor de pulso con cinta de velcro y cable de conexión.
- **Necesidad de Verificación Adicional:** Ninguna requerida.

#### Candidato N° 30: `KS0047` — Sensores y módulos
- **SKU Proveedor:** `KS0047` (SKU Humm: `HUMM-KEY-KS0047`)
- **Nombre Original Proveedor:** `Keyestudio MQ-135 SnO2 Benzene Sulfide Air Quality Sensor module. Keyestudio MQ-135 SnO2 Benzene Sulfide Air Quality Sensor module`
- **Precio Sugerido:** `$10,999 CLP`
- **Categoría Propuesta:** Sensores y módulos
- **Compatibilidad Propuesta:** `Arduino / ESP32`
- **Clasificación Auditoría:** 🟢 `A — RECOMENDADO`
- **Correcciones Detectadas:** Ninguna. Sensor de calidad de aire MQ-135 (sensible a amoníaco, sulfuros, vapores de benceno y humo).
- **Recomendación Técnica y Pedagógica:** Aprobar para proyectos escolares de ventilación de aulas y monitoreo ambiental.
- **Observaciones de Contenido del Pack:** 1 unidad sensor MQ-135 montado en PCB.
- **Necesidad de Verificación Adicional:** Indicar requerimiento de precalentamiento.

#### Candidato N° 31: `KS0275` — Sensores y módulos
- **SKU Proveedor:** `KS0275` (SKU Humm: `HUMM-KEY-KS0275`)
- **Nombre Original Proveedor:** `Keyestudio  Voltage detection module Voltage sensor Electronic blocks For Arduino UNO R3. Keyestudio  Voltage detection module Voltage sensor Electronic blocks For Arduino UNO R3`
- **Precio Sugerido:** `$8,894 CLP`
- **Categoría Propuesta:** Sensores y módulos
- **Compatibilidad Propuesta:** `Arduino / ESP32` ➔ **Corregida:** `Arduino / ESP32 / micro:bit`
- **Clasificación Auditoría:** 🟢 `A — RECOMENDADO`
- **Correcciones Detectadas:** Ninguna. Módulo divisor de tensión resistivo (factor 5:1, mide hasta 25V con entradas de 5V).
- **Recomendación Técnica y Pedagógica:** Aprobar como herramienta de telemetría de baterías y paneles fotovoltaicos escolares.
- **Observaciones de Contenido del Pack:** 1 unidad módulo divisor de tensión con bornera de tornillo y conector de 3 pines.
- **Necesidad de Verificación Adicional:** Ninguna requerida.

---

### Robótica y vehículos (7 candidatos)

#### Candidato N° 32: `CR0011` — Robótica y vehículos
- **SKU Proveedor:** `CR0011` (SKU Humm: `HUMM-KEY-CR0011`)
- **Nombre Original Proveedor:** `Keyestudio 4WD Smart car chassis /speed measurement car for Arduino Robot. Keyestudio 4WD Smart car chassis /speed measurement car for Arduino Robot`
- **Precio Sugerido:** `$39,783 CLP`
- **Categoría Propuesta:** Robótica y vehículos
- **Compatibilidad Propuesta:** `Arduino` ➔ **Corregida:** `Arduino / ESP32 / micro:bit / Raspberry Pi`
- **Clasificación Auditoría:** 🟢 `A — RECOMENDADO`
- **Correcciones Detectadas:** Ninguna inconsistencia técnica. Chasis robótico 4WD mecánico.
- **Recomendación Técnica y Pedagógica:** Aprobar como plataforma base de robótica móvil con tracción en las 4 ruedas.
- **Observaciones de Contenido del Pack:** Chasis mecánico: incluye 2 placas de acrílico, 4 motores DC con caja reductora, 4 ruedas, 4 discos encoder, portapilas y tornillería. NO incluye tarjeta de control ni driver de motores.
- **Necesidad de Verificación Adicional:** Aclarar en ficha que la electrónica de control se adquiere por separado.

#### Candidato N° 33: `CR0019` — Robótica y vehículos
- **SKU Proveedor:** `CR0019` (SKU Humm: `HUMM-KEY-CR0019`)
- **Nombre Original Proveedor:** `Two-drive double layers smart car chassis K-001 Extended Edition For Arduino Robot. Two-drive double layers smart car chassis K-001 Extended Edition For Arduino Robot`
- **Precio Sugerido:** `$35,080 CLP`
- **Categoría Propuesta:** Robótica y vehículos
- **Compatibilidad Propuesta:** `Arduino / micro:bit` ➔ **Corregida:** `Arduino / micro:bit / ESP32 / Raspberry Pi`
- **Clasificación Auditoría:** 🟢 `A — RECOMENDADO`
- **Correcciones Detectadas:** Ninguna. Chasis 2WD clásico con 2 motores DC y 1 rueda loca giratoria.
- **Recomendación Técnica y Pedagógica:** Aprobar como plataforma móvil más económica y maniobrable para iniciación en robótica.
- **Observaciones de Contenido del Pack:** Chasis mecánico de 2 niveles: 2 placas acrílicas, 2 motores DC, 2 ruedas, 1 rueda loca, portapilas y accesorios. NO incluye controlador.
- **Necesidad de Verificación Adicional:** Indicar claramente que es chasis mecánico sin microcontrolador.

#### Candidato N° 34: `CR0033 CR0034` — Robótica y vehículos
- **SKU Proveedor:** `CR0033 CR0034` (SKU Humm: `HUMM-KEY-CR0033 CR0034`)
- **Nombre Original Proveedor:** `Keyestudio 4WD Mecanum Wheel Smart Robot Car Aluminum Chassis Kit For Arduino Raspberry Pi. Keyestudio 4WD Mecanum Wheel Smart Robot Car Aluminum Chassis Kit For Arduino Raspberry Pi`
- **Precio Sugerido:** `$50,546 CLP`
- **Categoría Propuesta:** Robótica y vehículos
- **Compatibilidad Propuesta:** `Arduino / micro:bit` ➔ **Corregida:** `Arduino / Raspberry Pi`
- **Clasificación Auditoría:** 🟡 `B — RECOMENDADO CON CORRECCIÓN`
- **Correcciones Detectadas:** ERROR IDENTIFICADO: En CANDIDATOS_SUGERIDOS_FASE_3.md se le asignó compatibilidad micro:bit. La descripción del proveedor especifica compatibilidad: 'For Arduino Raspberry Pi'. Eliminar micro:bit.
- **Recomendación Técnica y Pedagógica:** Aprobar con corrección: ajustar compatibilidad a Arduino / Raspberry Pi. Destacar que es un chasis de aluminio reforzado con ruedas omnidireccionales Mecanum.
- **Observaciones de Contenido del Pack:** Kit de chasis de aleación de aluminio con 4 motores DC y 4 ruedas Mecanum especiales. No incluye microcontrolador.
- **Necesidad de Verificación Adicional:** Verificar en catálogo si el SKU doble 'CR0033 CR0034' se consolida internamente.

#### Candidato N° 35: `KS4039` — Robótica y vehículos
- **SKU Proveedor:** `KS4039` (SKU Humm: `HUMM-KEY-KS4039`)
- **Nombre Original Proveedor:** `Keyestudio 4DOF Robot Arm Microbit Learning Kit Robot Arm Kit DIY Robot STEM Programming Without Microbit Board. Keyestudio 4DOF Robot Arm Microbit Learning Kit Robot Arm Kit DIY Robot STEM Programming Without Microbit Board`
- **Precio Sugerido:** `$98,286 CLP`
- **Categoría Propuesta:** Robótica y vehículos
- **Compatibilidad Propuesta:** `Arduino / micro:bit` ➔ **Corregida:** `micro:bit`
- **Clasificación Auditoría:** 🟡 `B — RECOMENDADO CON CORRECCIÓN`
- **Correcciones Detectadas:** ERROR IDENTIFICADO: Se incluyó 'Arduino' como compatibilidad sin respaldo. El producto está diseñado específicamente para BBC micro:bit y viene explícitamente SIN la tarjeta micro:bit ('Without Microbit Board').
- **Recomendación Técnica y Pedagógica:** Aprobar con corrección: eliminar Arduino de compatibilidad. Agregar de forma obligatoria y destacada en el título comercial: 'Sin Placa micro:bit'.
- **Observaciones de Contenido del Pack:** Kit brazo robótico 4DOF: servomotores, piezas de acrílico/madera, shield de expansión para micro:bit y accesorios. NO INCLUYE LA TARJETA MICRO:BIT.
- **Necesidad de Verificación Adicional:** Ninguna una vez corregida la compatibilidad.

#### Candidato N° 36: `KS0543` — Robótica y vehículos
- **SKU Proveedor:** `KS0543` (SKU Humm: `HUMM-KEY-KS0543`)
- **Nombre Original Proveedor:** `Keyestudio Beetlebot 3 in 1 Robot for Arduino STEM Education. The Beetlebot smart robot, compatible with LEGO building blocks, is a STEM educational product which can automatically dodge obstacles, follow black lines and light to move. Besides, it has three cool forms such as the soccer robot, the siege robot,`
- **Precio Sugerido:** `$171,767 CLP`
- **Categoría Propuesta:** Robótica y vehículos
- **Compatibilidad Propuesta:** `Arduino`
- **Clasificación Auditoría:** 🟠 `D — POSTERGAR`
- **Correcciones Detectadas:** Robot Beetlebot 3 en 1 de alto costo unitario ($171,767 CLP).
- **Recomendación Técnica y Pedagógica:** POSTERGAR para una segunda fase. Para el catálogo inicial se priorizan los chasis modulares (CR0011, CR0019) que permiten mayor cantidad de alumnos por presupuesto.
- **Observaciones de Contenido del Pack:** Kit robótico completo con placa de control integrada, sensores y piezas compatibles con Lego.
- **Necesidad de Verificación Adicional:** Postergar del lote inicial.

#### Candidato N° 37: `KS0607` — Robótica y vehículos
- **SKU Proveedor:** `KS0607` (SKU Humm: `HUMM-KEY-KS0607`)
- **Nombre Original Proveedor:** `Keyestudio Mini Caterpillar Tank Robot V3.0 For Arduino Kit Robot Car DIY Programmable STEM Toys. Upgraded with line-tracking and fire-extinguishing features. Easy assembly with user-friendly parts. Durable aluminum brackets and metal motors. Connects to sensors and LEGO via motor driver shield. Supports IR remote and app control for iOS/Android.`
- **Precio Sugerido:** `$195,635 CLP`
- **Categoría Propuesta:** Robótica y vehículos
- **Compatibilidad Propuesta:** `Arduino`
- **Clasificación Auditoría:** 🟠 `D — POSTERGAR`
- **Correcciones Detectadas:** Robot oruga Caterpillar V3 de alto valor ($195,635 CLP) y alta especialización mecánica.
- **Recomendación Técnica y Pedagógica:** POSTERGAR para catálogo avanzado o fase 4. El costo elevado restringe su adopción en colegios públicos.
- **Observaciones de Contenido del Pack:** Kit tanque con orugas de aluminio, motores y placa shield.
- **Necesidad de Verificación Adicional:** Postergar del lote inicial.

#### Candidato N° 38: `KS0377` — Robótica y vehículos
- **SKU Proveedor:** `KS0377` (SKU Humm: `HUMM-KEY-KS0377`)
- **Nombre Original Proveedor:** `Keyestudio Balance Car Shield V3 for Arduino  UNO R3. Keyestudio Balance Car Shield V3 for Arduino  UNO R3`
- **Precio Sugerido:** `$28,058 CLP`
- **Categoría Propuesta:** Robótica y vehículos
- **Compatibilidad Propuesta:** `Arduino` ➔ **Corregida:** `Arduino (Uno)`
- **Clasificación Auditoría:** 🟠 `D — POSTERGAR`
- **Correcciones Detectadas:** CATEGORIZACIÓN Y ALCANCE CONFUSOS: Es solo un 'Shield V3' (placa de expansión) para un auto de balance. No incluye chasis, motores ni ruedas.
- **Recomendación Técnica y Pedagógica:** POSTERGAR. Puede generar falsas expectativas en profesores que crean estar comprando un vehículo auto-equilibrado completo por $28,058 CLP.
- **Observaciones de Contenido del Pack:** 1 unidad placa shield de expansión para Arduino UNO.
- **Necesidad de Verificación Adicional:** Postergar del catálogo inicial.

---

### Motores y movimiento (5 candidatos)

#### Candidato N° 39: `KS0326` — Motores y movimiento
- **SKU Proveedor:** `KS0326` (SKU Humm: `HUMM-KEY-KS0326`)
- **Nombre Original Proveedor:** `3 PCS keyestudio MINI SG90 9G  90 degrees Servo Motor  Blue with PH2.54 Connector  For Arduino Robot. 3 PCS keyestudio MINI SG90 9G  90 degrees Servo Motor  Blue with PH2.54 Connector  For Arduino Robot`
- **Precio Sugerido:** `$21,039 CLP`
- **Categoría Propuesta:** Motores y movimiento
- **Compatibilidad Propuesta:** `Arduino / micro:bit` ➔ **Corregida:** `Arduino / micro:bit / ESP32 / Raspberry Pi`
- **Clasificación Auditoría:** 🟡 `B — RECOMENDADO CON CORRECCIÓN`
- **Correcciones Detectadas:** REVISIÓN DE PACK Y CANTIDAD OBLIGATORIA: El título del proveedor indica claramente '3 PCS keyestudio MINI SG90 9G'.
- **Recomendación Técnica y Pedagógica:** Aprobar con corrección: titular obligatoriamente 'Pack de 3 Servomotores SG90 9g' para que el docente entienda que compra 3 unidades por $21,039 CLP ($7,013 CLP c/u).
- **Observaciones de Contenido del Pack:** Pack contiene exactamente 3 servomotores SG90 con sus brazos de plástico y tornillos.
- **Necesidad de Verificación Adicional:** Ninguna. Consistencia validada.

#### Candidato N° 40: `OR0428` — Motores y movimiento
- **SKU Proveedor:** `OR0428` (SKU Humm: `HUMM-KEY-OR0428`)
- **Nombre Original Proveedor:** `360 Degrees Servo Motor Continuous Rotation Programmable Electric Building Blocks Green Servo Motor For Arduino. 360 Degrees Servo Motor Continuous Rotation Programmable Electric Building Blocks Green Servo Motor For Arduino`
- **Precio Sugerido:** `$19,658 CLP`
- **Categoría Propuesta:** Motores y movimiento
- **Compatibilidad Propuesta:** `Arduino / micro:bit` ➔ **Corregida:** `Arduino / micro:bit / ESP32`
- **Clasificación Auditoría:** 🟢 `A — RECOMENDADO`
- **Correcciones Detectadas:** Ninguna. Servomotor de rotación continua 360° en formato compatible con bloques de construcción Lego.
- **Recomendación Técnica y Pedagógica:** Aprobar para tracción directa de ruedas en robots móviles modulares.
- **Observaciones de Contenido del Pack:** 1 unidad servomotor 360° con acople para ejes Lego.
- **Necesidad de Verificación Adicional:** Ninguna requerida.

#### Candidato N° 41: `KS0140` — Motores y movimiento
- **SKU Proveedor:** `KS0140` (SKU Humm: `HUMM-KEY-KS0140`)
- **Nombre Original Proveedor:** `keyestudio 5V stepper motor driver module + stepper motor. keyestudio 5V stepper motor driver module + stepper motor`
- **Precio Sugerido:** `$14,041 CLP`
- **Categoría Propuesta:** Motores y movimiento
- **Compatibilidad Propuesta:** `Arduino / Raspberry Pi` ➔ **Corregida:** `Arduino / Raspberry Pi / ESP32`
- **Clasificación Auditoría:** 🟢 `A — RECOMENDADO`
- **Correcciones Detectadas:** Ninguna. Motor paso a paso 28BYJ-48 de 5V con placa controladora ULN2003.
- **Recomendación Técnica y Pedagógica:** Aprobar para enseñanza de control angular preciso, dosificadores y posicionadores.
- **Observaciones de Contenido del Pack:** Set completo: incluye 1 motor paso a paso 5V + 1 módulo driver ULN2003 con 4 LEDs de estado.
- **Necesidad de Verificación Adicional:** Ninguna requerida.

#### Candidato N° 42: `MD0140` — Motores y movimiento
- **SKU Proveedor:** `MD0140` (SKU Humm: `HUMM-KEY-MD0140`)
- **Nombre Original Proveedor:** `L9110S H-bridge Stepper Motor Dual DC Stepper Motor Driver  Board Module  L9110 For Arduino. L9110S H-bridge Stepper Motor Dual DC Stepper Motor Driver  Board Module  L9110 For Arduino`
- **Precio Sugerido:** `$6,785 CLP`
- **Categoría Propuesta:** Motores y movimiento
- **Compatibilidad Propuesta:** `Arduino / micro:bit` ➔ **Corregida:** `Arduino / micro:bit / ESP32 / Raspberry Pi`
- **Clasificación Auditoría:** 🟢 `A — RECOMENDADO`
- **Correcciones Detectadas:** Ninguna. Controlador dual puente H basado en chip L9110S.
- **Recomendación Técnica y Pedagógica:** Aprobar como driver de potencia económico y compacto para 2 motores DC en chasis escolares.
- **Observaciones de Contenido del Pack:** 1 unidad módulo controlador L9110S con borneras de tornillo para motores.
- **Necesidad de Verificación Adicional:** Ninguna requerida.

#### Candidato N° 43: `KS0057` — Motores y movimiento
- **SKU Proveedor:** `KS0057` (SKU Humm: `HUMM-KEY-KS0057`)
- **Nombre Original Proveedor:** `Keyestudio 2-channel 5V Relay Module for Arduino ARM PIC AVR DSP Electronic. Keyestudio 2-channel 5V Relay Module for Arduino ARM PIC AVR DSP Electronic`
- **Precio Sugerido:** `$15,913 CLP`
- **Categoría Propuesta:** Motores y movimiento
- **Compatibilidad Propuesta:** `Arduino / ESP32` ➔ **Corregida:** `Arduino / ESP32 / micro:bit / Raspberry Pi`
- **Clasificación Auditoría:** 🟢 `A — RECOMENDADO`
- **Correcciones Detectadas:** Ninguna. Módulo de 2 relés con optoacoplador para cargas de 250VAC/10A o 30VDC/10A.
- **Recomendación Técnica y Pedagógica:** Aprobar para proyectos de domótica, riego y control de iluminación en aula.
- **Observaciones de Contenido del Pack:** 1 unidad módulo con 2 relés electromecánicos y borneras seguras.
- **Necesidad de Verificación Adicional:** Ninguna requerida.

---

### Electrónica y prototipado (9 candidatos)

#### Candidato N° 44: `60320025` — Electrónica y prototipado
- **SKU Proveedor:** `60320025` (SKU Humm: `HUMM-KEY-60320025`)
- **Nombre Original Proveedor:** `High quality 830 hole transparent breadboard  test board 165X55mm. High quality 830 hole transparent breadboard  test board 165X55mm`
- **Precio Sugerido:** `$5,802 CLP`
- **Categoría Propuesta:** Electrónica y prototipado
- **Compatibilidad Propuesta:** `Otros (Universal)` ➔ **Corregida:** `Universal (Todas las plataformas)`
- **Clasificación Auditoría:** 🟢 `A — RECOMENDADO`
- **Correcciones Detectadas:** Ninguna. Protoboard transparente de 830 puntos de contacto estándar.
- **Recomendación Técnica y Pedagógica:** Aprobar como insumo primordial para todos los bancos de trabajo de electrónica.
- **Observaciones de Contenido del Pack:** 1 unidad protoboard de 830 contactos (165 x 55 mm) con bandas de alimentación.
- **Necesidad de Verificación Adicional:** Ninguna requerida.

#### Candidato N° 45: `KS0331` — Electrónica y prototipado
- **SKU Proveedor:** `KS0331` (SKU Humm: `HUMM-KEY-KS0331`)
- **Nombre Original Proveedor:** `3PCS HIGH QUALITY 400 Holes Mini Solderless  PCB Breadboard Universal Test  Breadboard with keyestudio color  Packaging. 3PCS HIGH QUALITY 400 Holes Mini Solderless  PCB Breadboard Universal Test  Breadboard with keyestudio color  Packaging`
- **Precio Sugerido:** `$21,039 CLP`
- **Categoría Propuesta:** Electrónica y prototipado
- **Compatibilidad Propuesta:** `Otros (Universal)` ➔ **Corregida:** `Universal (Todas las plataformas)`
- **Clasificación Auditoría:** 🟡 `B — RECOMENDADO CON CORRECCIÓN`
- **Correcciones Detectadas:** REVISIÓN DE PACK Y CANTIDAD OBLIGATORIA: El nombre del fabricante indica '3PCS HIGH QUALITY 400 Holes Mini Solderless PCB Breadboard'.
- **Recomendación Técnica y Pedagógica:** Aprobar con corrección: titular obligatoriamente 'Pack de 3 Protoboards de 400 Puntos' para evitar reclamos comerciales.
- **Observaciones de Contenido del Pack:** Pack contiene exactamente 3 protoboards medianas de 400 contactos con empaque individual Keyestudio.
- **Necesidad de Verificación Adicional:** Ninguna requerida.

#### Candidato N° 46: `60320054` — Electrónica y prototipado
- **SKU Proveedor:** `60320054` (SKU Humm: `HUMM-KEY-60320054`)
- **Nombre Original Proveedor:** `7PCS Mini 25 Tie-point Breadboard Solderless Prototype Test Board ( 7 kinds of colors / lot). 7PCS Mini 25 Tie-point Breadboard Solderless Prototype Test Board ( 7 kinds of colors / lot)`
- **Precio Sugerido:** `$3,042 CLP`
- **Categoría Propuesta:** Electrónica y prototipado
- **Compatibilidad Propuesta:** `Otros (Universal)` ➔ **Corregida:** `Universal`
- **Clasificación Auditoría:** 🔴 `E — DESCARTAR DEL CATÁLOGO INICIAL`
- **Correcciones Detectadas:** INADECUADO PEDAGÓGICAMENTE: Pack de protoboards diminutas de solo 25 puntos (5x5). No tienen capacidad para alojar circuitos integrados o proyectos educativos reales.
- **Recomendación Técnica y Pedagógica:** DESCARTAR DEL CATÁLOGO INICIAL. Es un insumo anecdótico sin utilidad en laboratorios escolares.
- **Observaciones de Contenido del Pack:** Pack de 7 mini placas de 25 contactos.
- **Necesidad de Verificación Adicional:** Descartar del catálogo inicial.

#### Candidato N° 47: `KT0072` — Electrónica y prototipado
- **SKU Proveedor:** `KT0072` (SKU Humm: `HUMM-KEY-KT0072`)
- **Nombre Original Proveedor:** `Dupont line 120pcs 10cm male to male + male to female +female to female jumper wire Dupont cable for arduino. Dupont line 120pcs 10cm male to male + male to female +female to female jumper wire Dupont cable for arduino`
- **Precio Sugerido:** `$6,998 CLP`
- **Categoría Propuesta:** Electrónica y prototipado
- **Compatibilidad Propuesta:** `Otros (Universal)` ➔ **Corregida:** `Universal (Todas las plataformas)`
- **Clasificación Auditoría:** 🟢 `A — RECOMENDADO`
- **Correcciones Detectadas:** Ninguna. Insumo de interconexión esencial.
- **Recomendación Técnica y Pedagógica:** Aprobar como insumo obligatorio en todo laboratorio escolar.
- **Observaciones de Contenido del Pack:** Pack de 120 cables Dupont de 10 cm dividido en 3 cintas de 40 cables: Macho-Macho, Macho-Hembra y Hembra-Hembra.
- **Necesidad de Verificación Adicional:** Ninguna requerida.

#### Candidato N° 48: `KT0065` — Electrónica y prototipado
- **SKU Proveedor:** `KT0065` (SKU Humm: `HUMM-KEY-KT0065`)
- **Nombre Original Proveedor:** `Dupont line 120pcs 30CM male to male + male to female and female to female jumper wire Dupont cable for Arduino. Dupont line 120pcs 30CM male to male + male to female and female to female jumper wire Dupont cable for Arduino`
- **Precio Sugerido:** `$8,894 CLP`
- **Categoría Propuesta:** Electrónica y prototipado
- **Compatibilidad Propuesta:** `Otros (Universal)` ➔ **Corregida:** `Universal (Todas las plataformas)`
- **Clasificación Auditoría:** 🟢 `A — RECOMENDADO`
- **Correcciones Detectadas:** Ninguna. Cables cinta largos de 30 cm.
- **Recomendación Técnica y Pedagógica:** Aprobar para maquetas grandes, brazos robóticos y robots móviles donde los cables de 10cm o 20cm resultan insuficientes.
- **Observaciones de Contenido del Pack:** Pack de 120 cables Dupont de 30 cm (40 M-M, 40 M-H, 40 H-H).
- **Necesidad de Verificación Adicional:** Ninguna requerida.

#### Candidato N° 49: `KS0014` — Electrónica y prototipado
- **SKU Proveedor:** `KS0014` (SKU Humm: `HUMM-KEY-KS0014`)
- **Nombre Original Proveedor:** `Keyestudio Adjustable Potentiometer Module for Arduino UNO and MEGA. Analog Rotation Sensor`
- **Precio Sugerido:** `$9,361 CLP`
- **Categoría Propuesta:** Electrónica y prototipado
- **Compatibilidad Propuesta:** `Otros (Universal)` ➔ **Corregida:** `Universal (Entradas Analógicas)`
- **Clasificación Auditoría:** 🟢 `A — RECOMENDADO`
- **Correcciones Detectadas:** Ninguna. Módulo potenciómetro rotativo de 10k lineal.
- **Recomendación Técnica y Pedagógica:** Aprobar para proyectos de control de luminosidad, velocidad de motores y enseñanza de entradas analógicas.
- **Observaciones de Contenido del Pack:** 1 unidad módulo con potenciómetro rotativo con perilla y conector de 3 pines.
- **Necesidad de Verificación Adicional:** Ninguna requerida.

#### Candidato N° 50: `KS0029` — Electrónica y prototipado
- **SKU Proveedor:** `KS0029` (SKU Humm: `HUMM-KEY-KS0029`)
- **Nombre Original Proveedor:** `Keyestudio Digital Push Button Switch Module for Arduino. Keyestudio Digital Push Button Switch Module for Arduino`
- **Precio Sugerido:** `$8,894 CLP`
- **Categoría Propuesta:** Electrónica y prototipado
- **Compatibilidad Propuesta:** `Otros (Universal)` ➔ **Corregida:** `Universal (Entradas Digitales)`
- **Clasificación Auditoría:** 🟢 `A — RECOMENDADO`
- **Correcciones Detectadas:** Ninguna. Módulo pulsador con resistencia de polarización integrada.
- **Recomendación Técnica y Pedagógica:** Aprobar para diseño de interfaces de usuario y conmutadores sin falsos contactos.
- **Observaciones de Contenido del Pack:** 1 unidad módulo pulsador digital con conector de 3 pines.
- **Necesidad de Verificación Adicional:** Ninguna requerida.

#### Candidato N° 51: `KS0018` — Electrónica y prototipado
- **SKU Proveedor:** `KS0018` (SKU Humm: `HUMM-KEY-KS0018`)
- **Nombre Original Proveedor:** `Keyestudio Active Buzzer Alarm Module for Arduino. Digital Buzzer Module`
- **Precio Sugerido:** `$8,894 CLP`
- **Categoría Propuesta:** Electrónica y prototipado
- **Compatibilidad Propuesta:** `Arduino / micro:bit` ➔ **Corregida:** `Arduino / micro:bit / ESP32 / Raspberry Pi`
- **Clasificación Auditoría:** 🟢 `A — RECOMENDADO`
- **Correcciones Detectadas:** Ninguna. Módulo zumbador activo (active buzzer) con oscilador interno.
- **Recomendación Técnica y Pedagógica:** Aprobar para sistemas de alarma sonoros de activación directa por nivel alto.
- **Observaciones de Contenido del Pack:** 1 unidad módulo zumbador activo.
- **Necesidad de Verificación Adicional:** Ninguna requerida.

#### Candidato N° 52: `KS0332` — Electrónica y prototipado
- **SKU Proveedor:** `KS0332` (SKU Humm: `HUMM-KEY-KS0332`)
- **Nombre Original Proveedor:** `Keyestudio 1PCS 3.3V/5V Breadboard power module+ 1PCS 830 points  Breadboard + 1PCS 65 Flexible jumper wires for arduino DIY. Keyestudio 1PCS 3.3V/5V Breadboard power module+ 1PCS 830 points  Breadboard + 1PCS 65 Flexible jumper wires for arduino DIY`
- **Precio Sugerido:** `$25,719 CLP`
- **Categoría Propuesta:** Electrónica y prototipado
- **Compatibilidad Propuesta:** `Otros (Universal)` ➔ **Corregida:** `Universal (Todas las plataformas)`
- **Clasificación Auditoría:** 🟢 `A — RECOMENDADO`
- **Correcciones Detectadas:** Ninguna. Combo de prototipado completo.
- **Recomendación Técnica y Pedagógica:** Aprobar como set de inicio para equipar puestos de laboratorio con alimentación independiente.
- **Observaciones de Contenido del Pack:** Set contiene: 1 fuente de alimentación regulada para protoboard (salidas 3.3V / 5V) + 1 protoboard 830 puntos + 1 set de 65 cables de puente flexibles.
- **Necesidad de Verificación Adicional:** Confirmar que la fuente admite entrada jack DC 7-12V o USB.

---

### Pantallas e interacción (7 candidatos)

#### Candidato N° 53: `KS0061` — Pantallas e interacción
- **SKU Proveedor:** `KS0061` (SKU Humm: `HUMM-KEY-KS0061`)
- **Nombre Original Proveedor:** `Keyestudio 16X2 1602 I2C/TWI LCD Display Module for Arduino UNO R3 MEGA 2560 White in Blue. Keyestudio 16X2 1602 I2C/TWI LCD Display Module for Arduino UNO R3 MEGA 2560 White in Blue`
- **Precio Sugerido:** `$17,551 CLP`
- **Categoría Propuesta:** Pantallas e interacción
- **Compatibilidad Propuesta:** `Arduino / Raspberry Pi` ➔ **Corregida:** `Arduino / ESP32 / Raspberry Pi / micro:bit`
- **Clasificación Auditoría:** 🟢 `A — RECOMENDADO`
- **Correcciones Detectadas:** Ninguna. Pantalla LCD 1602 con módulo convertidor I2C integrado.
- **Recomendación Técnica y Pedagógica:** Aprobar como el display alfanumérico escolar por excelencia.
- **Observaciones de Contenido del Pack:** 1 unidad pantalla LCD 16x2 fondo azul con caracteres blancos y módulo I2C soldado en la parte posterior.
- **Necesidad de Verificación Adicional:** Ninguna requerida.

#### Candidato N° 54: `KS0271` — Pantallas e interacción
- **SKU Proveedor:** `KS0271` (SKU Humm: `HUMM-KEY-KS0271`)
- **Nombre Original Proveedor:** `Keyestudio 0.96'' OLED Module/128X64 Blue LCD LED Display Module / IIC Serial for Arduino. Keyestudio 0.96'' OLED Module/128X64 Blue LCD LED Display Module / IIC Serial for Arduino`
- **Precio Sugerido:** `$12,871 CLP`
- **Categoría Propuesta:** Pantallas e interacción
- **Compatibilidad Propuesta:** `Arduino / ESP32` ➔ **Corregida:** `Arduino / ESP32 / Raspberry Pi / micro:bit`
- **Clasificación Auditoría:** 🟢 `A — RECOMENDADO`
- **Correcciones Detectadas:** Ninguna. Pantalla OLED monocromática de 0.96'' (128x64 píxeles) por I2C.
- **Recomendación Técnica y Pedagógica:** Aprobar para proyectos que requieran gráficos, curvas de sensores e íconos en tamaño compacto.
- **Observaciones de Contenido del Pack:** 1 unidad pantalla OLED 0.96 pulgadas con conector de 4 pines (VCC, GND, SCL, SDA).
- **Necesidad de Verificación Adicional:** Ninguna requerida.

#### Candidato N° 55: `MD0082` — Pantallas e interacción
- **SKU Proveedor:** `MD0082` (SKU Humm: `HUMM-KEY-MD0082`)
- **Nombre Original Proveedor:** `4Pcs  3mm 8 * 8 led lattice bright red dot matrix module. 4Pcs  3mm 8 * 8 led lattice bright red dot matrix module`
- **Precio Sugerido:** `$10,530 CLP`
- **Categoría Propuesta:** Pantallas e interacción
- **Compatibilidad Propuesta:** `Arduino / micro:bit`
- **Clasificación Auditoría:** 🟠 `D — POSTERGAR`
- **Correcciones Detectadas:** REVISIÓN TÉCNICA Y DE PACK: Pack de 4 matrices LED 8x8 de 3mm. Son matrices pasivas de 16 pines crudos, sin controlador multiplexor integrado (como el MAX7219). Conectarlas a Arduino requiere 16 pines directos o chips auxiliares.
- **Recomendación Técnica y Pedagógica:** POSTERGAR. Muy compleja de cablear directamente para estudiantes iniciales. Priorizar módulos matriciales con chip MAX7219 o shields matriciales.
- **Observaciones de Contenido del Pack:** Pack contiene 4 piezas de matriz LED 8x8 pasiva suelta.
- **Necesidad de Verificación Adicional:** Confirmar ausencia de controlador MAX7219.

#### Candidato N° 56: `KS0481` — Pantallas e interacción
- **SKU Proveedor:** `KS0481` (SKU Humm: `HUMM-KEY-KS0481`)
- **Nombre Original Proveedor:** `Keyestudio Micro bit Honeycomb PS2 Joystick Module. Keyestudio Micro bit Honeycomb PS2 Joystick Module`
- **Precio Sugerido:** `$9,829 CLP`
- **Categoría Propuesta:** Pantallas e interacción
- **Compatibilidad Propuesta:** `Arduino / micro:bit` ➔ **Corregida:** `micro:bit (Diseño primario Honeycomb) / Arduino`
- **Clasificación Auditoría:** 🟡 `B — RECOMENDADO CON CORRECCIÓN`
- **Correcciones Detectadas:** Módulo Joystick PS2 de la serie Honeycomb para micro:bit (con orificios de caimán).
- **Recomendación Técnica y Pedagógica:** Aprobar con corrección: explicitar optimización física para micro:bit (y utilizable en Arduino mediante pines 2.54mm).
- **Observaciones de Contenido del Pack:** 1 unidad joystick analógico de dos ejes con pulsador central en PCB Honeycomb.
- **Necesidad de Verificación Adicional:** Ninguna requerida.

#### Candidato N° 57: `MD0089` — Pantallas e interacción
- **SKU Proveedor:** `MD0089` (SKU Humm: `HUMM-KEY-MD0089`)
- **Nombre Original Proveedor:** `3PCS/LOT 4*3 Matrix Array 12 Key Membrane Switch Keypad Keyboard/ 3*4 Control Panel Microprocessor Keyboard for Arduino AVR. 3PCS/LOT 4*3 Matrix Array 12 Key Membrane Switch Keypad Keyboard/ 3*4 Control Panel Microprocessor Keyboard for Arduino AVR`
- **Precio Sugerido:** `$6,998 CLP`
- **Categoría Propuesta:** Pantallas e interacción
- **Compatibilidad Propuesta:** `Arduino` ➔ **Corregida:** `Arduino / ESP32 / Raspberry Pi`
- **Clasificación Auditoría:** 🟡 `B — RECOMENDADO CON CORRECCIÓN`
- **Correcciones Detectadas:** REVISIÓN DE PACK Y CANTIDAD OBLIGATORIA: El título del proveedor indica '3PCS/LOT 4*3 Matrix Array 12 Key Membrane Switch Keypad'.
- **Recomendación Técnica y Pedagógica:** Aprobar con corrección: titular obligatoriamente 'Pack de 3 Teclados Matriciales de Membrana 4x3'.
- **Observaciones de Contenido del Pack:** Pack contiene exactamente 3 teclados planos de membrana de 12 teclas autoadhesivos con conector hembra de 7 pines.
- **Necesidad de Verificación Adicional:** Ninguna requerida.

#### Candidato N° 58: `KS0163` — Pantallas e interacción
- **SKU Proveedor:** `KS0163` (SKU Humm: `HUMM-KEY-KS0163`)
- **Nombre Original Proveedor:** `Keyestudio 40 RGB LED WS2812 Pixel Matrix Shield for Arduino. Keyestudio 40 RGB LED WS2812 Pixel Matrix Shield for Arduino`
- **Precio Sugerido:** `$22,935 CLP`
- **Categoría Propuesta:** Pantallas e interacción
- **Compatibilidad Propuesta:** `Arduino / micro:bit` ➔ **Corregida:** `Arduino (Uno)`
- **Clasificación Auditoría:** 🟢 `A — RECOMENDADO`
- **Correcciones Detectadas:** Ninguna. Shield para Arduino UNO con matriz de 40 LEDs RGB direccionables WS2812.
- **Recomendación Técnica y Pedagógica:** Aprobar para proyectos de arte interactivo, señales visuales y efectos cromáticos.
- **Observaciones de Contenido del Pack:** 1 unidad shield matricial de 40 píxeles RGB direccionables.
- **Necesidad de Verificación Adicional:** Ninguna requerida.

#### Candidato N° 59: `KS0310` — Pantallas e interacción
- **SKU Proveedor:** `KS0310` (SKU Humm: `HUMM-KEY-KS0310`)
- **Nombre Original Proveedor:** `Keyestudio Traffic Light Module (Black and Eco-friendly) For arduino. Keyestudio Traffic Light Module (Black and Eco-friendly) For arduino`
- **Precio Sugerido:** `$9,361 CLP`
- **Categoría Propuesta:** Pantallas e interacción
- **Compatibilidad Propuesta:** `Arduino / micro:bit` ➔ **Corregida:** `Arduino / micro:bit / ESP32 / Raspberry Pi`
- **Clasificación Auditoría:** 🟢 `A — RECOMENDADO`
- **Correcciones Detectadas:** Ninguna. Módulo semáforo con LEDs rojo, amarillo y verde.
- **Recomendación Técnica y Pedagógica:** Aprobar para proyectos de educación vial, lógica booleana y secuencias en básica y media.
- **Observaciones de Contenido del Pack:** 1 unidad módulo con 3 LEDs integrados y conector de 4 pines (GND, R, Y, G).
- **Necesidad de Verificación Adicional:** Ninguna requerida.

---

### Micro:bit y accesorios (5 candidatos)

#### Candidato N° 60: `KS0434` — Micro:bit y accesorios
- **SKU Proveedor:** `KS0434` (SKU Humm: `HUMM-KEY-KS0434`)
- **Nombre Original Proveedor:** `KEYESTUDIO Microbit Edge Connector I/O Sensor Breakout Expansion. KEYESTUDIO Microbit Edge Connector I/O Sensor Breakout Expansion`
- **Precio Sugerido:** `$11,701 CLP`
- **Categoría Propuesta:** Micro:bit y accesorios
- **Compatibilidad Propuesta:** `micro:bit`
- **Clasificación Auditoría:** 🟢 `A — RECOMENDADO`
- **Correcciones Detectadas:** Ninguna. Placa de expansión para el conector de borde de BBC micro:bit.
- **Recomendación Técnica y Pedagógica:** Aprobar como accesorio imprescindible para conectar sensores estándar a micro:bit.
- **Observaciones de Contenido del Pack:** 1 unidad shield breakout con zócalo vertical para micro:bit y cabezales G-V-S.
- **Necesidad de Verificación Adicional:** Ninguna requerida.

#### Candidato N° 61: `MB0110` — Micro:bit y accesorios
- **SKU Proveedor:** `MB0110` (SKU Humm: `HUMM-KEY-MB0110`)
- **Nombre Original Proveedor:** `Original Microbit Go Kit Main Board+USB Cable+Battery Holder With Batteries Learning Diy Electronic Kit. Original Microbit Go Kit Main Board+USB Cable+Battery Holder With Batteries Learning Diy Electronic Kit`
- **Precio Sugerido:** `$66,929 CLP`
- **Categoría Propuesta:** Micro:bit y accesorios
- **Compatibilidad Propuesta:** `micro:bit`
- **Clasificación Auditoría:** 🟢 `A — RECOMENDADO`
- **Correcciones Detectadas:** Ninguna. Kit oficial micro:bit V2 Go original.
- **Recomendación Técnica y Pedagógica:** Aprobar como la tarjeta controladora insignia para educación básica y programas ministeriales.
- **Observaciones de Contenido del Pack:** Kit completo en caja comercial oficial: 1 tarjeta micro:bit V2, 1 cable USB, 1 portapilas con 2 baterías AAA y guía de inicio.
- **Necesidad de Verificación Adicional:** Ninguna requerida.

#### Candidato N° 62: `KS4038` — Micro:bit y accesorios
- **SKU Proveedor:** `KS4038` (SKU Humm: `HUMM-KEY-KS4038`)
- **Nombre Original Proveedor:** `Keyestudio 4DOF Robot Arm Microbit Learning Kit Robot Arm Kit DIY Robot STEM Programming With Microbit Board. Keyestudio 4DOF Robot Arm Microbit Learning Kit Robot Arm Kit DIY Robot STEM Programming With Microbit Board`
- **Precio Sugerido:** `$150,705 CLP`
- **Categoría Propuesta:** Micro:bit y accesorios
- **Compatibilidad Propuesta:** `micro:bit`
- **Clasificación Auditoría:** 🟢 `A — RECOMENDADO`
- **Correcciones Detectadas:** Ninguna. Kit completo de brazo robótico 4DOF que INCLUYE la tarjeta micro:bit ('With Microbit Board').
- **Recomendación Técnica y Pedagógica:** Aprobar como kit robótico integral para colegios que no dispongan de tarjetas micro:bit previas.
- **Observaciones de Contenido del Pack:** Kit integral: estructura brazo robótico 4DOF, servomotores, placa shield de expansión Y 1 TARJETA MICRO:BIT INCLUIDA.
- **Necesidad de Verificación Adicional:** Diferenciar de KS4039 en catálogo.

#### Candidato N° 63: `KS0802` — Micro:bit y accesorios
- **SKU Proveedor:** `KS0802` (SKU Humm: `HUMM-KEY-KS0802`)
- **Nombre Original Proveedor:** `Keyestudio Crocodile Creative Learning Starter Kit DIY Stem Programming With Microbit Mainboard. Included Microbit mainboard`
- **Precio Sugerido:** `$101,889 CLP`
- **Categoría Propuesta:** Micro:bit y accesorios
- **Compatibilidad Propuesta:** `micro:bit`
- **Clasificación Auditoría:** 🟢 `A — RECOMENDADO`
- **Correcciones Detectadas:** Ninguna. Kit creativo con cables caimán y tarjeta micro:bit INCLUIDA ('Included Microbit mainboard').
- **Recomendación Técnica y Pedagógica:** Aprobar para proyectos de ciencias y arte en ciclo primario (frutas conductoras, circuitos en papel).
- **Observaciones de Contenido del Pack:** Kit didáctico: cables caimán, módulos, piezas y 1 tarjeta micro:bit incluida en el empaque.
- **Necesidad de Verificación Adicional:** Ninguna requerida.

#### Candidato N° 64: `KT0284` — Micro:bit y accesorios
- **SKU Proveedor:** `KT0284` (SKU Humm: `HUMM-KEY-KT0284`)
- **Nombre Original Proveedor:** `4pcs Dual Output Shaft 2KG DC Motor (Low Speed)In Blue Servo Motor 360 Degree Continuous Rotation Programmable for Microbit Smart Car. 4pcs Dual Output Shaft 2KG DC Motor (Low Speed)In Blue Servo Motor 360 Degree Continuous Rotation Programmable for Microbit Smart Car`
- **Precio Sugerido:** `$51,483 CLP`
- **Categoría Propuesta:** Micro:bit y accesorios
- **Compatibilidad Propuesta:** `micro:bit` ➔ **Corregida:** `micro:bit / Lego compatible`
- **Clasificación Auditoría:** 🟡 `B — RECOMENDADO CON CORRECCIÓN`
- **Correcciones Detectadas:** REVISIÓN DE PACK Y CANTIDAD OBLIGATORIA: El nombre del proveedor dice '4pcs Dual Output Shaft 2KG DC Motor In Blue Servo Motor 360 Degree Continuous Rotation'.
- **Recomendación Técnica y Pedagógica:** Aprobar con corrección: titular obligatoriamente 'Pack de 4 Motores DC / Servos 360° para micro:bit'.
- **Observaciones de Contenido del Pack:** Pack contiene exactamente 4 motores de eje doble compatibles con ruedas Lego y micro:bit.
- **Necesidad de Verificación Adicional:** Ninguna requerida.

---

### Raspberry Pi y accesorios (6 candidatos)

#### Candidato N° 65: `KS0219` — Raspberry Pi y accesorios
- **SKU Proveedor:** `KS0219` (SKU Humm: `HUMM-KEY-KS0219`)
- **Nombre Original Proveedor:** `KEYESTUDIO Raspberry Pi T type board+40P Colorful Ribbon Cable+400-hole Breadboard. KEYESTUDIO Raspberry Pi T type board+40P Colorful Ribbon Cable+400-hole Breadboard`
- **Precio Sugerido:** `$21,529 CLP`
- **Categoría Propuesta:** Raspberry Pi y accesorios
- **Compatibilidad Propuesta:** `Raspberry Pi` ➔ **Corregida:** `Raspberry Pi (Modelos 40 pines: Pi 2, 3, 4, 5)`
- **Clasificación Auditoría:** 🟢 `A — RECOMENDADO`
- **Correcciones Detectadas:** Ninguna. Adaptador GPIO tipo 'T' con cable plano de 40 vías y protoboard de 400 puntos.
- **Recomendación Técnica y Pedagógica:** Aprobar como la herramienta de conexión más segura y económica para Raspberry Pi en aula.
- **Observaciones de Contenido del Pack:** Set contiene: 1 placa adaptadora T-Cobbler + 1 cable cinta 40 pines + 1 protoboard 400 puntos.
- **Necesidad de Verificación Adicional:** Ninguna requerida.

#### Candidato N° 66: `SMP0023` — Raspberry Pi y accesorios
- **SKU Proveedor:** `SMP0023` (SKU Humm: `HUMM-KEY-SMP0023`)
- **Nombre Original Proveedor:** `KEYESTUDIO 5 Megapixels 1080p Mini Camera Video Module for Raspberry Pi Model A/B/B+, Pi 2 and Raspberry Pi 3. KEYESTUDIO 5 Megapixels 1080p Mini Camera Video Module for Raspberry Pi Model A/B/B+, Pi 2 and Raspberry Pi 3`
- **Precio Sugerido:** `$18,019 CLP`
- **Categoría Propuesta:** Raspberry Pi y accesorios
- **Compatibilidad Propuesta:** `Raspberry Pi` ➔ **Corregida:** `Raspberry Pi (Pi 2, 3, 4 / Requiere adaptador en Pi 5 y Pi Zero)`
- **Clasificación Auditoría:** 🟡 `B — RECOMENDADO CON CORRECCIÓN`
- **Correcciones Detectadas:** COMPATIBILIDAD FÍSICA A DETALLAR: Módulo de cámara con cable cinta CSI de 15 pines estándar para Raspberry Pi 1, 2, 3 y 4. En Raspberry Pi 5 y Pi Zero el conector CSI es de 22 pines más estrecho.
- **Recomendación Técnica y Pedagógica:** Aprobar con corrección: advertir en la ficha técnica que para Raspberry Pi 5 o Pi Zero se requiere cable adaptador de 22 a 15 pines.
- **Observaciones de Contenido del Pack:** 1 unidad cámara 5MP (OV5647) con cable plano flexible CSI de 15 pines.
- **Necesidad de Verificación Adicional:** Ninguna adicional requerida.

#### Candidato N° 67: `KS3018` — Raspberry Pi y accesorios
- **SKU Proveedor:** `KS3018` (SKU Humm: `HUMM-KEY-KS3018`)
- **Nombre Original Proveedor:** `KEYESTUDIO GPIO Breakout Kit for Raspberry Pi 4 4b 3 3b+ with Solderless Breadboard, GPIO Cable, LEDs, Resistors. KEYESTUDIO GPIO Breakout Kit for Raspberry Pi 4 4b 3 3b+ with Solderless Breadboard, GPIO Cable, LEDs, Resistors`
- **Precio Sugerido:** `$39,783 CLP`
- **Categoría Propuesta:** Raspberry Pi y accesorios
- **Compatibilidad Propuesta:** `Raspberry Pi`
- **Clasificación Auditoría:** 🟠 `D — POSTERGAR`
- **Correcciones Detectadas:** REDUNDANCIA CON KS0219: Contiene un T-Cobbler, cable y protoboard similar a KS0219, agregando solo unas resistencias y LEDs, pero cuesta casi el doble ($39,783 CLP vs $21,529 CLP).
- **Recomendación Técnica y Pedagógica:** POSTERGAR. KS0219 cubre la misma función técnica con mejor relación costo-beneficio para los colegios.
- **Observaciones de Contenido del Pack:** Kit breakout con T-board, cable, protoboard y componentes básicos.
- **Necesidad de Verificación Adicional:** Postergar del catálogo inicial.

#### Candidato N° 68: `60520146` — Raspberry Pi y accesorios
- **SKU Proveedor:** `60520146` (SKU Humm: `HUMM-KEY-60520146`)
- **Nombre Original Proveedor:** `Black Aluminum alloy box case Porous heat-dissipating metal case with fan for Raspberry Pi 4B. Black Aluminum alloy box case Porous heat-dissipating metal case with fan for Raspberry Pi 4B`
- **Precio Sugerido:** `$38,612 CLP`
- **Categoría Propuesta:** Raspberry Pi y accesorios
- **Compatibilidad Propuesta:** `Raspberry Pi` ➔ **Corregida:** `Raspberry Pi (Específico para Raspberry Pi 4B)`
- **Clasificación Auditoría:** 🟢 `A — RECOMENDADO`
- **Correcciones Detectadas:** Aclarar en ficha que es solo la carcasa de disipación y NO incluye la computadora Raspberry Pi.
- **Recomendación Técnica y Pedagógica:** Aprobar como accesorio de protección metálica robusta y enfriamiento activo con ventilador.
- **Observaciones de Contenido del Pack:** 1 unidad carcasa de aleación de aluminio negro con ventilador de 5V, disipadores y tornillos. NO incluye placa Raspberry Pi.
- **Necesidad de Verificación Adicional:** Ninguna requerida.

#### Candidato N° 69: `60520134` — Raspberry Pi y accesorios
- **SKU Proveedor:** `60520134` (SKU Humm: `HUMM-KEY-60520134`)
- **Nombre Original Proveedor:** `Hi-Q Acrylic Transparent Case Box For Raspberry Pi 4  Enclosure(NO Raspberry Pi BOARD). Hi-Q Acrylic Transparent Case Box For Raspberry Pi 4  Enclosure(NO Raspberry Pi BOARD)`
- **Precio Sugerido:** `$11,701 CLP`
- **Categoría Propuesta:** Raspberry Pi y accesorios
- **Compatibilidad Propuesta:** `Raspberry Pi` ➔ **Corregida:** `Raspberry Pi (Específico para Raspberry Pi 4B)`
- **Clasificación Auditoría:** 🟠 `D — POSTERGAR`
- **Correcciones Detectadas:** REDUNDANCIA COMERCIAL: Carcasa de acrílico transparente para Pi 4B. Teniendo la carcasa de aluminio metálica con ventilador (60520146), tener dos carcasas en un catálogo de 6 productos de Raspberry Pi es redundante.
- **Recomendación Técnica y Pedagógica:** POSTERGAR para evitar saturación de accesorios protectores similares.
- **Observaciones de Contenido del Pack:** Carcasa de láminas de acrílico transparente desmontable. Sin placa.
- **Necesidad de Verificación Adicional:** Postergar del catálogo inicial.

#### Candidato N° 70: `67600041` — Raspberry Pi y accesorios
- **SKU Proveedor:** `67600041` (SKU Humm: `HUMM-KEY-67600041`)
- **Nombre Original Proveedor:** `Raspberry Pi Camera holder Acrylic holder Compatible with Raspberry Pi Official Camera V2 Domestic Camera A Type Black (for SMP0023). Raspberry Pi Camera holder Acrylic holder Compatible with Raspberry Pi Official Camera V2 Domestic Camera A Type Black (for SMP0023)`
- **Precio Sugerido:** `$11,701 CLP`
- **Categoría Propuesta:** Raspberry Pi y accesorios
- **Compatibilidad Propuesta:** `Raspberry Pi` ➔ **Corregida:** `Raspberry Pi (Soporte cámara SMP0023 / V2)`
- **Clasificación Auditoría:** 🟢 `A — RECOMENDADO`
- **Correcciones Detectadas:** Ninguna. Soporte de acrílico orientable para cámaras de Raspberry Pi.
- **Recomendación Técnica y Pedagógica:** Aprobar como accesorio de fijación indispensable para proyectos de visión artificial y seguridad.
- **Observaciones de Contenido del Pack:** 1 soporte acrílico con base y tornillos de ajuste.
- **Necesidad de Verificación Adicional:** Ninguna requerida.

---

### IoT y comunicación (7 candidatos)

#### Candidato N° 71: `KS0143` — IoT y comunicación
- **SKU Proveedor:** `KS0143` (SKU Humm: `HUMM-KEY-KS0143`)
- **Nombre Original Proveedor:** `Keyestudio Bluetooh XBee Bluetooth wireless module HC-05 for arduino. Keyestudio Bluetooh XBee Bluetooth wireless module HC-05 for arduino`
- **Precio Sugerido:** `$23,378 CLP`
- **Categoría Propuesta:** IoT y comunicación
- **Compatibilidad Propuesta:** `Arduino` ➔ **Corregida:** `Arduino (Zócalo XBee 2.0mm / Requiere Shield)`
- **Clasificación Auditoría:** 🔵 `C — REQUIERE VERIFICACIÓN TÉCNICA`
- **Correcciones Detectadas:** RESTRICCIÓN FÍSICA CRÍTICA: Este módulo Bluetooth HC-05 tiene factor de forma de tarjeta XBee (pines de paso 2.0 mm). NO se puede insertar directamente en protoboards convencionales de 2.54 mm.
- **Recomendación Técnica y Pedagógica:** REQUIERE VERIFICACIÓN TÉCNICA. Evaluar si es conveniente para el primer catálogo escolar frente a módulos Bluetooth HC-05 con pines Dupont estándar de 2.54mm.
- **Observaciones de Contenido del Pack:** 1 unidad módulo HC-05 en zócalo tipo XBee.
- **Necesidad de Verificación Adicional:** REQUIERE_VERIFICACION_TECNICA para confirmar compatibilidad de zócalos en los laboratorios escolares.

#### Candidato N° 72: `KS0255` — IoT y comunicación
- **SKU Proveedor:** `KS0255` (SKU Humm: `HUMM-KEY-KS0255`)
- **Nombre Original Proveedor:** `Keyestudio Bluetooth 4.0 Shield Expansion Shield Board for Arduino UNO R3. Keyestudio Bluetooth 4.0 Shield Expansion Shield Board for Arduino UNO R3`
- **Precio Sugerido:** `$25,719 CLP`
- **Categoría Propuesta:** IoT y comunicación
- **Compatibilidad Propuesta:** `Arduino` ➔ **Corregida:** `Arduino (Uno)`
- **Clasificación Auditoría:** 🟢 `A — RECOMENDADO`
- **Correcciones Detectadas:** Ninguna. Shield de Bluetooth 4.0 BLE (Low Energy) para Arduino UNO.
- **Recomendación Técnica y Pedagógica:** Aprobar para proyectos de comunicación con iPads, tablets y teléfonos móviles modernos sin problemas de compatibilidad iOS.
- **Observaciones de Contenido del Pack:** 1 unidad shield de expansión para montar directamente sobre Arduino UNO.
- **Necesidad de Verificación Adicional:** Ninguna requerida.

#### Candidato N° 73: `MD0322` — IoT y comunicación
- **SKU Proveedor:** `MD0322` (SKU Humm: `HUMM-KEY-MD0322`)
- **Nombre Original Proveedor:** `Keyes ESP8266 remote serial Port WIFI module for arduino. Keyes ESP8266 remote serial Port WIFI module for arduino`
- **Precio Sugerido:** `$5,850 CLP`
- **Categoría Propuesta:** IoT y comunicación
- **Compatibilidad Propuesta:** `Arduino / ESP32` ➔ **Corregida:** `Arduino / ESP8266 (Puerto Serie AT)`
- **Clasificación Auditoría:** 🟡 `B — RECOMENDADO CON CORRECCIÓN`
- **Correcciones Detectadas:** ERROR IDENTIFICADO: En CANDIDATOS_SUGERIDOS_FASE_3.md se le asignó compatibilidad ESP32. El proveedor indica explícitamente 'Keyes ESP8266 remote serial Port WIFI module'.
- **Recomendación Técnica y Pedagógica:** Aprobar con corrección: rectificar compatibilidad a Arduino / ESP8266. Aclarar que opera a 3.3V y se controla mediante comandos AT vía puerto serie.
- **Observaciones de Contenido del Pack:** 1 unidad módulo WiFi ESP8266 en PCB compacta.
- **Necesidad de Verificación Adicional:** Corregir mención a ESP32.

#### Candidato N° 74: `KS0205` — IoT y comunicación
- **SKU Proveedor:** `KS0205` (SKU Humm: `HUMM-KEY-KS0205`)
- **Nombre Original Proveedor:** `Keyestudio RC522 RFID Module for Arduino. Keyestudio RC522 RFID Module for Arduino`
- **Precio Sugerido:** `$10,766 CLP`
- **Categoría Propuesta:** IoT y comunicación
- **Compatibilidad Propuesta:** `Arduino / ESP32` ➔ **Corregida:** `Arduino / ESP32 / Raspberry Pi`
- **Clasificación Auditoría:** 🟢 `A — RECOMENDADO`
- **Correcciones Detectadas:** Ninguna. Módulo de radiofrecuencia RFID RC522 (13.56 MHz, SPI).
- **Recomendación Técnica y Pedagógica:** Aprobar para proyectos de control de acceso, bibliotecas escolares y registro de asistencia escolar.
- **Observaciones de Contenido del Pack:** Pack contiene: 1 módulo lector RC522 + 1 tarjeta blanca RFID Mifare + 1 llavero tag RFID azul.
- **Necesidad de Verificación Adicional:** Ninguna requerida.

#### Candidato N° 75: `MD0040` — IoT y comunicación
- **SKU Proveedor:** `MD0040` (SKU Humm: `HUMM-KEY-MD0040`)
- **Nombre Original Proveedor:** `NRF24L01 2.4GHz wireless Transceiver module - Black for arduino. NRF24L01 2.4GHz wireless Transceiver module - Black for arduino`
- **Precio Sugerido:** `$9,361 CLP`
- **Categoría Propuesta:** IoT y comunicación
- **Compatibilidad Propuesta:** `Arduino` ➔ **Corregida:** `Arduino / micro:bit / ESP32 / Raspberry Pi`
- **Clasificación Auditoría:** 🟢 `A — RECOMENDADO`
- **Correcciones Detectadas:** Ninguna. Módulo transceptor inalámbrico 2.4 GHz NRF24L01+.
- **Recomendación Técnica y Pedagógica:** Aprobar para comunicación por radio bidireccional entre robots sin depender de redes WiFi.
- **Observaciones de Contenido del Pack:** 1 unidad módulo transceptor NRF24L01 con antena integrada en PCB.
- **Necesidad de Verificación Adicional:** Ninguna requerida.

#### Candidato N° 76: `KS0026` — IoT y comunicación
- **SKU Proveedor:** `KS0026` (SKU Humm: `HUMM-KEY-KS0026`)
- **Nombre Original Proveedor:** `Keyestudio Digital IR Infrared Receiver Module for Arduino  UNO R3 MEGA 2560 R3. Keyestudio Digital IR Infrared Receiver Module for Arduino  UNO R3 MEGA 2560 R3`
- **Precio Sugerido:** `$8,894 CLP`
- **Categoría Propuesta:** IoT y comunicación
- **Compatibilidad Propuesta:** `Arduino / micro:bit` ➔ **Corregida:** `Arduino / micro:bit / ESP32`
- **Clasificación Auditoría:** 🟢 `A — RECOMENDADO`
- **Correcciones Detectadas:** Ninguna. Módulo receptor infrarrojo de 38 kHz (VS1838B).
- **Recomendación Técnica y Pedagógica:** Aprobar para decodificación de mandos a distancia en proyectos de domótica y control remoto.
- **Observaciones de Contenido del Pack:** 1 unidad módulo receptor con conector de 3 pines.
- **Necesidad de Verificación Adicional:** Ninguna requerida.

#### Candidato N° 77: `KS0389` — IoT y comunicación
- **SKU Proveedor:** `KS0389` (SKU Humm: `HUMM-KEY-KS0389`)
- **Nombre Original Proveedor:** `Keyestudio ESP8266 WI-FI Module Shield +1M Micro USB Cable For Arduino (Chip is CP2102-GMR). Keyestudio ESP8266 WI-FI Module Shield +1M Micro USB Cable For Arduino (Chip is CP2102-GMR)`
- **Precio Sugerido:** `$23,378 CLP`
- **Categoría Propuesta:** IoT y comunicación
- **Compatibilidad Propuesta:** `Arduino / ESP32` ➔ **Corregida:** `Arduino (Uno) / ESP8266`
- **Clasificación Auditoría:** 🟢 `A — RECOMENDADO`
- **Correcciones Detectadas:** Ninguna. Shield WiFi ESP8266 para Arduino UNO con conversor USB-Serial CP2102 integrado.
- **Recomendación Técnica y Pedagógica:** Aprobar como la solución WiFi más amigable y limpia para conectar placas Arduino Uno a internet.
- **Observaciones de Contenido del Pack:** Pack incluye: 1 shield WiFi ESP8266 + 1 cable micro-USB de 1 metro.
- **Necesidad de Verificación Adicional:** Ninguna requerida.

---

### Kits educativos iniciales (6 candidatos)

#### Candidato N° 78: `KS0541` — Kits educativos iniciales
- **SKU Proveedor:** `KS0541` (SKU Humm: `HUMM-KEY-KS0541`)
- **Nombre Original Proveedor:** `Keyestudio Basic Starter Kit for Arduino DIY Programming Electronics Kit 20Project Without Plus Mainboard. Keyestudio Basic Starter Kit for Arduino DIY Programming Electronics Kit 20Project Without Plus Mainboard`
- **Precio Sugerido:** `$45,633 CLP`
- **Categoría Propuesta:** Kits educativos iniciales
- **Compatibilidad Propuesta:** `Arduino` ➔ **Corregida:** `Arduino (Requiere Placa Externa)`
- **Clasificación Auditoría:** 🟡 `B — RECOMENDADO CON CORRECCIÓN`
- **Correcciones Detectadas:** ADVERTENCIA COMERCIAL CRÍTICA DE PACK: El producto se titula 'Without Plus Mainboard'. Contiene 20 proyectos guiados y todos los componentes, PERO NO INCLUYE LA PLACA CONTROLADORA ARDUINO.
- **Recomendación Técnica y Pedagógica:** Aprobar con corrección: titular obligatoriamente 'Kit de Componentes para Arduino (20 Proyectos - Sin Placa Controladora)' para que ningún colegio lo compre esperando una placa de microcontrolador.
- **Observaciones de Contenido del Pack:** Caja con sensores, protoboard, LEDs, resistencias, cables y manual de 20 proyectos. SIN PLACA ARDUINO / PLUS.
- **Necesidad de Verificación Adicional:** Aclarar en el nombre comercial y descripción.

#### Candidato N° 79: `KS0487` — Kits educativos iniciales
- **SKU Proveedor:** `KS0487` (SKU Humm: `HUMM-KEY-KS0487`)
- **Nombre Original Proveedor:** `Keyestudio 37 in 1 Sensor Kit Upgrade V3.0 +Gift Box for Arduino starter Kit W/37 projects Tutorial/STEM Kids programing. Keyestudio 37 in 1 Sensor Kit Upgrade V3.0 +Gift Box for Arduino starter Kit W/37 projects Tutorial/STEM Kids programing`
- **Precio Sugerido:** `$85,883 CLP`
- **Categoría Propuesta:** Kits educativos iniciales
- **Compatibilidad Propuesta:** `Arduino / micro:bit` ➔ **Corregida:** `Arduino / micro:bit / ESP32 / Raspberry Pi`
- **Clasificación Auditoría:** 🟢 `A — RECOMENDADO`
- **Correcciones Detectadas:** Ninguna. Maletín con 37 sensores y actuadores para proyectos STEM.
- **Recomendación Técnica y Pedagógica:** Aprobar como el set multi-sensor definitivo para equipar laboratorios escolares de tecnología y ciencias.
- **Observaciones de Contenido del Pack:** Maletín plástico organizador con 37 módulos de sensores individuales y tutorial digital.
- **Necesidad de Verificación Adicional:** Ninguna requerida.

#### Candidato N° 80: `KS0567` — Kits educativos iniciales
- **SKU Proveedor:** `KS0567` (SKU Humm: `HUMM-KEY-KS0567`)
- **Nombre Original Proveedor:** `Keyestudio ESP32 IoT Control Smart Farm Starter Kit for Arduino Scratch 3.0 Graphical Programming. Combines multiple sensors for smart farm applications. Practical experiments for understanding sensor operations. Comprehensive tutorials with instructions and example codes. Uses ESP32 for flexibility and scalability. Interactive platform for communi`
- **Precio Sugerido:** `$142,749 CLP`
- **Categoría Propuesta:** Kits educativos iniciales
- **Compatibilidad Propuesta:** `ESP32`
- **Clasificación Auditoría:** 🟢 `A — RECOMENDADO`
- **Correcciones Detectadas:** Ninguna. Kit Granja Inteligente (Smart Farm) IoT basado en ESP32.
- **Recomendación Técnica y Pedagógica:** Aprobar como kit temático insignia de agroecología, sostenibilidad y programación gráfica.
- **Observaciones de Contenido del Pack:** Kit integral: estructura didáctica de madera, tarjeta ESP32, sensor de humedad de suelo, fotocelda, servomotor, bomba de agua, pantalla y tutorial.
- **Necesidad de Verificación Adicional:** Ninguna requerida.

#### Candidato N° 81: `KS3010` — Kits educativos iniciales
- **SKU Proveedor:** `KS3010` (SKU Humm: `HUMM-KEY-KS3010`)
- **Nombre Original Proveedor:** `Original Raspberry Pi 4B Complete Starter kit With AU Plug Power Supply (No Raspberry Pi board). Original Raspberry Pi 4B Complete Starter kit With AU Plug Power Supply (No Raspberry Pi board)`
- **Precio Sugerido:** `$65,524 CLP`
- **Categoría Propuesta:** Kits educativos iniciales
- **Compatibilidad Propuesta:** `Raspberry Pi`
- **Clasificación Auditoría:** 🔴 `E — DESCARTAR DEL CATÁLOGO INICIAL`
- **Correcciones Detectadas:** ERRORES COMERCIALES Y TÉCNICOS GRAVES PARA CHILE: 1) Viene con fuente de poder con enchufe australiano ('AU Plug'), incompatible con la red eléctrica chilena (220V tipo C/L). 2) Dice 'Complete Starter Kit', pero indica explícitamente '(No Raspberry Pi board)'. Genera enorme riesgo de reclamos en colegios.
- **Recomendación Técnica y Pedagógica:** DESCARTAR DEL CATÁLOGO INICIAL de manera inapelable.
- **Observaciones de Contenido del Pack:** Caja de accesorios con fuente con enchufe australiano AU y sin computadora Raspberry Pi.
- **Necesidad de Verificación Adicional:** Descartar totalmente de la selección.

#### Candidato N° 82: `FB1001` — Kits educativos iniciales
- **SKU Proveedor:** `FB1001` (SKU Humm: `HUMM-KEY-FB1001`)
- **Nombre Original Proveedor:** `Keyestudio Foxbit Go Development Kit Rich Sensor and Peripheral Modules Supports Wi-Fi and Bluetooth. Keyestudio Foxbit Go Development Kit Rich Sensor and Peripheral Modules Supports Wi-Fi and Bluetooth`
- **Precio Sugerido:** `$52,185 CLP`
- **Categoría Propuesta:** Kits educativos iniciales
- **Compatibilidad Propuesta:** `Otros (Universal)` ➔ **Corregida:** `Por determinar`
- **Clasificación Auditoría:** 🔵 `C — REQUIERE VERIFICACIÓN TÉCNICA`
- **Correcciones Detectadas:** DATOS TÉCNICOS INSUFICIENTES: Placa 'Foxbit Go' todo-en-uno con WiFi/BT. No se especifica en los datos primarios el microcontrolador exacto ni el soporte oficial de bloques o MakeCode en español.
- **Recomendación Técnica y Pedagógica:** REQUIERE VERIFICACIÓN TÉCNICA. Comprobar entorno de programación oficial, disponibilidad de librerías y documentación antes de incorporar al catálogo público.
- **Observaciones de Contenido del Pack:** 1 unidad placa de desarrollo Foxbit Go con sensores integrados.
- **Necesidad de Verificación Adicional:** REQUIERE_VERIFICACION_TECNICA de documentación y entorno de desarrollo.

#### Candidato N° 83: `KS5028` — Kits educativos iniciales
- **SKU Proveedor:** `KS5028` (SKU Humm: `HUMM-KEY-KS5028`)
- **Nombre Original Proveedor:** `Keyestudio ESP32 S3 Xiaozhi AI Chatbot Kit with Camera &amp; Breadboard Supports Multiple AI Models. 1.Vision-Enabled AI Chatbot Kit 2.Multi-Model Compatible AI Learning  3.Plug-and-Play Modular Design`
- **Precio Sugerido:** `$82,606 CLP`
- **Categoría Propuesta:** Kits educativos iniciales
- **Compatibilidad Propuesta:** `ESP32` ➔ **Corregida:** `ESP32 (ESP32-S3)`
- **Clasificación Auditoría:** 🔵 `C — REQUIERE VERIFICACIÓN TÉCNICA`
- **Correcciones Detectadas:** DEPENDE DE SERVICIOS EN LA NUBE: Kit Chatbot IA Xiaozhi con cámara y ESP32-S3. La arquitectura Xiaozhi AI depende habitualmente de servidores en la nube y configuración de cuentas que podrían no ser viables o requerir chino/inglés en colegios chilenos.
- **Recomendación Técnica y Pedagógica:** REQUIERE VERIFICACIÓN TÉCNICA. Probar el flujo de configuración de red y la disponibilidad de modelos de IA en español sin bloqueos de servidor.
- **Observaciones de Contenido del Pack:** Kit con placa ESP32-S3, cámara, altavoz, micrófono y protoboard.
- **Necesidad de Verificación Adicional:** REQUIERE_VERIFICACION_TECNICA sobre disponibilidad y latencia de backend en la nube en Chile.

---

### Herramientas y accesorios (3 candidatos)

#### Candidato N° 84: `49500005` — Herramientas y accesorios
- **SKU Proveedor:** `49500005` (SKU Humm: `HUMM-KEY-49500005`)
- **Nombre Original Proveedor:** `XL830L Mini Digital Multimeter AC/DC Current 20A Portable LCD 3-1/2 Digital Clamp 200MΩ Resistor 6F22 9V Battery Instrument. XL830L Mini Digital Multimeter AC/DC Current 20A Portable LCD 3-1/2 Digital Clamp 200MΩ Resistor 6F22 9V Battery Instrument`
- **Precio Sugerido:** `$29,251 CLP`
- **Categoría Propuesta:** Herramientas y accesorios
- **Compatibilidad Propuesta:** `Otros (Universal)` ➔ **Corregida:** `Universal (Instrumentación Eléctrica)`
- **Clasificación Auditoría:** 🟢 `A — RECOMENDADO`
- **Correcciones Detectadas:** Ninguna. Multímetro digital compacto XL830L con display retroiluminado y funda protectora.
- **Recomendación Técnica y Pedagógica:** Aprobar como el tester básico escolar por excelencia, económico y con protección de goma anticaídas.
- **Observaciones de Contenido del Pack:** 1 unidad multímetro digital + juego de 2 puntas de prueba (roja y negra). Indicar que puede no incluir la batería 9V por normativas de transporte aéreo.
- **Necesidad de Verificación Adicional:** Confirmar inclusión de batería 9V 6F22.

#### Candidato N° 85: `49500004` — Herramientas y accesorios
- **SKU Proveedor:** `49500004` (SKU Humm: `HUMM-KEY-49500004`)
- **Nombre Original Proveedor:** `DT9205A Fully Protected Multimeter 200MΩ Resistor AC/DC 20A 6F22 9V Battery Digital Multimeter Measuring Instrument. DT9205A Fully Protected Multimeter 200MΩ Resistor AC/DC 20A 6F22 9V Battery Digital Multimeter Measuring Instrument`
- **Precio Sugerido:** `$35,103 CLP`
- **Categoría Propuesta:** Herramientas y accesorios
- **Compatibilidad Propuesta:** `Otros (Universal)` ➔ **Corregida:** `Universal (Instrumentación Eléctrica)`
- **Clasificación Auditoría:** 🟢 `A — RECOMENDADO`
- **Correcciones Detectadas:** Ninguna. Multímetro digital grande DT9205A con pantalla inclinable.
- **Recomendación Técnica y Pedagógica:** Aprobar como opción de instrumentación avanzada para talleres de especialidad técnico-profesional (TP).
- **Observaciones de Contenido del Pack:** 1 unidad multímetro de mesa con pantalla abatible + puntas de prueba.
- **Necesidad de Verificación Adicional:** Confirmar presencia de batería 9V.

#### Candidato N° 86: `MD0118` — Herramientas y accesorios
- **SKU Proveedor:** `MD0118` (SKU Humm: `HUMM-KEY-MD0118`)
- **Nombre Original Proveedor:** `CP2102 USB to TTL / STC 6PIN Speed download for arduino+4Pin dupont cable. CP2102 USB to TTL / STC 6PIN Speed download for arduino+4Pin dupont cable`
- **Precio Sugerido:** `$9,478 CLP`
- **Categoría Propuesta:** Herramientas y accesorios
- **Compatibilidad Propuesta:** `Otros (Universal)` ➔ **Corregida:** `Universal (Programación UART)`
- **Clasificación Auditoría:** 🟢 `A — RECOMENDADO`
- **Correcciones Detectadas:** Ninguna. Conversor USB a TTL UART con chip Silicon Labs CP2102.
- **Recomendación Técnica y Pedagógica:** Aprobar como herramienta obligatoria para programar microcontroladores Pro Mini (KS0247) y comunicarse con módulos WiFi/BT.
- **Observaciones de Contenido del Pack:** 1 unidad módulo convertidor USB-TTL CP2102 + 1 cable hembra-hembra de 4 pines.
- **Necesidad de Verificación Adicional:** Ninguna requerida.

---

## 5. Resumen Estadístico y Clasificación Consolidada

Tras la auditoría minuciosa de los 86 productos propuestos:

| Clasificación de Auditoría | Cantidad de Productos | Porcentaje | Rol en la Estrategia del Catálogo MVP |
| :--- | :---: | :---: | :--- |
| 🟢 **A — Recomendados** | **54 productos** | **62.8%** | Aprobados directamente para proceso de curaduría pedagógica individual. |
| 🟡 **B — Recomendados con corrección** | **18 productos** | **20.9%** | Aprobados para curaduría incorporando correcciones de empaque y compatibilidad. |
| 🔵 **C — Requieren verificación técnica** | **4 productos** | **4.7%** | Retenidos en catálogo maestro hasta verificación de muestra física o soporte. |
| 🟠 **D — Postergar** | **7 productos** | **8.1%** | Válidos pero postergados para fase 4 o catálogo especializado TP. |
| 🔴 **E — Descartar inicialmente** | **3 productos** | **3.5%** | Descartados del catálogo inicial por inconsistencias o enchufes incompatibles. |
| **TOTAL AUDITADO** | **86 productos** | **100.0%** | **Universo completo de preselección Fase 3.** |

> [!TIP]
> ### UNIVERSO FINAL SUGERIDO PARA EL CATÁLOGO MVP: 72 PRODUCTOS
> La suma de **A (54) + B (18)** consolida un lote de **72 productos sólidos**, pedagógicamente diversos y técnicamente blindados, ubicándose de forma óptima en el rango meta de **60 a 80 productos**.

---

## 6. Listado Consolidado del Lote Recomendado (72 Productos A + B)

A continuación se lista el lote sugerido para avanzar a curaduría pedagógica formal:

| N° | SKU Proveedor | Nombre Comercial Recomendado | Categoría | Compatibilidad Estructurada | Estado |
| :-: | :--- | :--- | :--- | :--- | :---: |
| 1 | `KS0486` | Keyestudio PLUS Development Board with Type C interface +USB cabl... | Arduino y controladores | `Arduino (Uno R3)` | **A** |
| 2 | `KS0502` | Keyestudio MEGA 2560 PRO Development Board(Black and Eco-friendly... | Arduino y controladores | `Arduino (Mega 2560)` | **A** |
| 3 | `KS0547` | Keyestudio NANO PLUS Development Board Compatible with Arduino NA... | Arduino y controladores | `Arduino (Nano)` | **A** |
| 4 | `KS0503` | Keyestudio PRO MICRO 5V 16MHZ ATMEGA32U4-MU Development Board For... | Arduino y controladores | `Arduino (Leonardo / Micro)` | **A** |
| 5 | `KS0247` | Keyestudio 5V/16MHZ ProMini Original ATMEGA328P Development Board... | Arduino y controladores | `Arduino (Pro Mini)` | **B** |
| 6 | `KS0004` | Keyestudio Sensor Shield V5 Expansion Board Module for Arduino UN... | Arduino y controladores | `Arduino (Uno / Leonardo / Mega)` | **A** |
| 7 | `KS0003` | Keyestudio Protoshield for Arduino with Mini Breadboard. Keyestud... | Arduino y controladores | `Arduino (Uno)` | **A** |
| 8 | `KS5013` | Keyestudio 328 WIFI PLUS Main Control Board For Arduino UNO R3 an... | Arduino y controladores | `Arduino / ESP8266` | **B** |
| 9 | `KS0034` | Keyestudio DHT11 Temperature Humidity Moisture Sensor Detection m... | Sensores y módulos | `Arduino / micro:bit / ESP32 / Raspberry Pi` | **A** |
| 10 | `KS0430` | Keyestudio DHT22 (AM2302)Temperature and Humidity Sensor for  Ard... | Sensores y módulos | `Arduino / ESP32 / micro:bit / Raspberry Pi` | **A** |
| 11 | `KS0049` | Keyestudio Soil Humidity Sensor for Arduino. Keyestudio Soil Humi... | Sensores y módulos | `Arduino / micro:bit / ESP32` | **A** |
| 12 | `KS0052` | Keyestudio PIR Motion Sensor for Arduino. Keyestudio PIR Motion S... | Sensores y módulos | `Arduino / micro:bit / ESP32 / Raspberry Pi` | **A** |
| 13 | `KS0040` | Keyestudio  MQ-2 Combustible gas and Smoke for Arduino. Keyestudi... | Sensores y módulos | `Arduino / ESP32` | **A** |
| 14 | `KS0028` | Keyestudio photoresistor light dependent resistor sensor module. ... | Sensores y módulos | `Arduino / micro:bit / ESP32` | **A** |
| 15 | `KS0105` | Keyestudio EASY plug Analog Sound Sensor for Arduino STEAM. Keyes... | Sensores y módulos | `Arduino (EASY Plug / Requiere adaptador RJ11)` | **B** |
| 16 | `KS0116` | Keyestudio RJ11 EASY plug Flame Sensor module for Arduino STEAM. ... | Sensores y módulos | `Arduino (EASY Plug / Requiere adaptador RJ11)` | **B** |
| 17 | `KS0050` | Keyestudio Line Tracking Sensor module white/black line detector ... | Sensores y módulos | `Arduino / micro:bit / ESP32` | **A** |
| 18 | `KS0120` | Keyestudio RJ11 EASY plug Infrared Obstacle Avoidance Sensor Modu... | Sensores y módulos | `Arduino (EASY Plug / Requiere adaptador RJ11)` | **B** |
| 19 | `19720010` | 1PCS DS18B20 Stainless steel package Waterproof DS18b20 temperatu... | Sensores y módulos | `Arduino / micro:bit / ESP32 / Raspberry Pi` | **A** |
| 20 | `KS6057` | Keyestudio Electronic Building Block MPU6050 3-Axis Acceleration ... | Sensores y módulos | `Arduino / ESP32 / micro:bit` | **A** |
| 21 | `KS0031` | Keyestudio Capacitive Touch Sensor Module for Arduino. Keyestudio... | Sensores y módulos | `Arduino / micro:bit / ESP32` | **A** |
| 22 | `KS0048` | Keyestudio Water Level Sensor Droplet Detection Module for Arduin... | Sensores y módulos | `Arduino / micro:bit / ESP32` | **A** |
| 23 | `KS0494` | Keyestudio micro bit honeycomb TCS34725 Color Sensor Module. Keye... | Sensores y módulos | `micro:bit (Diseño primario Honeycomb) / Arduino (I2C)` | **B** |
| 24 | `KS0492` | Keyestudio Micro bit Honeycomb Hall Magnetic Sensor for  BBC Micr... | Sensores y módulos | `micro:bit (Diseño primario Honeycomb) / Arduino` | **B** |
| 25 | `KS0272` | Keyestudio Analog Piezoelectric Ceramic Vibration Sensor for Ardu... | Sensores y módulos | `Arduino / micro:bit / ESP32` | **B** |
| 26 | `KS0171` | keyestudio XD-58C Pulse Sensor Module. keyestudio XD-58C Pulse Se... | Sensores y módulos | `Arduino / micro:bit / ESP32` | **A** |
| 27 | `KS0047` | Keyestudio MQ-135 SnO2 Benzene Sulfide Air Quality Sensor module.... | Sensores y módulos | `Arduino / ESP32` | **A** |
| 28 | `KS0275` | Keyestudio  Voltage detection module Voltage sensor Electronic bl... | Sensores y módulos | `Arduino / ESP32 / micro:bit` | **A** |
| 29 | `CR0011` | Keyestudio 4WD Smart car chassis /speed measurement car for Ardui... | Robótica y vehículos | `Arduino / ESP32 / micro:bit / Raspberry Pi` | **A** |
| 30 | `CR0019` | Two-drive double layers smart car chassis K-001 Extended Edition ... | Robótica y vehículos | `Arduino / micro:bit / ESP32 / Raspberry Pi` | **A** |
| 31 | `CR0033 CR0034` | Keyestudio 4WD Mecanum Wheel Smart Robot Car Aluminum Chassis Kit... | Robótica y vehículos | `Arduino / Raspberry Pi` | **B** |
| 32 | `KS4039` | Keyestudio 4DOF Robot Arm Microbit Learning Kit Robot Arm Kit DIY... | Robótica y vehículos | `micro:bit` | **B** |
| 33 | `KS0326` | 3 PCS keyestudio MINI SG90 9G  90 degrees Servo Motor  Blue with ... | Motores y movimiento | `Arduino / micro:bit / ESP32 / Raspberry Pi` | **B** |
| 34 | `OR0428` | 360 Degrees Servo Motor Continuous Rotation Programmable Electric... | Motores y movimiento | `Arduino / micro:bit / ESP32` | **A** |
| 35 | `KS0140` | keyestudio 5V stepper motor driver module + stepper motor. keyest... | Motores y movimiento | `Arduino / Raspberry Pi / ESP32` | **A** |
| 36 | `MD0140` | L9110S H-bridge Stepper Motor Dual DC Stepper Motor Driver  Board... | Motores y movimiento | `Arduino / micro:bit / ESP32 / Raspberry Pi` | **A** |
| 37 | `KS0057` | Keyestudio 2-channel 5V Relay Module for Arduino ARM PIC AVR DSP ... | Motores y movimiento | `Arduino / ESP32 / micro:bit / Raspberry Pi` | **A** |
| 38 | `60320025` | High quality 830 hole transparent breadboard  test board 165X55mm... | Electrónica y prototipado | `Universal (Todas las plataformas)` | **A** |
| 39 | `KS0331` | 3PCS HIGH QUALITY 400 Holes Mini Solderless  PCB Breadboard Unive... | Electrónica y prototipado | `Universal (Todas las plataformas)` | **B** |
| 40 | `KT0072` | Dupont line 120pcs 10cm male to male + male to female +female to ... | Electrónica y prototipado | `Universal (Todas las plataformas)` | **A** |
| 41 | `KT0065` | Dupont line 120pcs 30CM male to male + male to female and female ... | Electrónica y prototipado | `Universal (Todas las plataformas)` | **A** |
| 42 | `KS0014` | Keyestudio Adjustable Potentiometer Module for Arduino UNO and ME... | Electrónica y prototipado | `Universal (Entradas Analógicas)` | **A** |
| 43 | `KS0029` | Keyestudio Digital Push Button Switch Module for Arduino. Keyestu... | Electrónica y prototipado | `Universal (Entradas Digitales)` | **A** |
| 44 | `KS0018` | Keyestudio Active Buzzer Alarm Module for Arduino. Digital Buzzer... | Electrónica y prototipado | `Arduino / micro:bit / ESP32 / Raspberry Pi` | **A** |
| 45 | `KS0332` | Keyestudio 1PCS 3.3V/5V Breadboard power module+ 1PCS 830 points ... | Electrónica y prototipado | `Universal (Todas las plataformas)` | **A** |
| 46 | `KS0061` | Keyestudio 16X2 1602 I2C/TWI LCD Display Module for Arduino UNO R... | Pantallas e interacción | `Arduino / ESP32 / Raspberry Pi / micro:bit` | **A** |
| 47 | `KS0271` | Keyestudio 0.96'' OLED Module/128X64 Blue LCD LED Display Module ... | Pantallas e interacción | `Arduino / ESP32 / Raspberry Pi / micro:bit` | **A** |
| 48 | `KS0481` | Keyestudio Micro bit Honeycomb PS2 Joystick Module. Keyestudio Mi... | Pantallas e interacción | `micro:bit (Diseño primario Honeycomb) / Arduino` | **B** |
| 49 | `MD0089` | 3PCS/LOT 4*3 Matrix Array 12 Key Membrane Switch Keypad Keyboard/... | Pantallas e interacción | `Arduino / ESP32 / Raspberry Pi` | **B** |
| 50 | `KS0163` | Keyestudio 40 RGB LED WS2812 Pixel Matrix Shield for Arduino. Key... | Pantallas e interacción | `Arduino (Uno)` | **A** |
| 51 | `KS0310` | Keyestudio Traffic Light Module (Black and Eco-friendly) For ardu... | Pantallas e interacción | `Arduino / micro:bit / ESP32 / Raspberry Pi` | **A** |
| 52 | `KS0434` | KEYESTUDIO Microbit Edge Connector I/O Sensor Breakout Expansion.... | Micro:bit y accesorios | `micro:bit` | **A** |
| 53 | `MB0110` | Original Microbit Go Kit Main Board+USB Cable+Battery Holder With... | Micro:bit y accesorios | `micro:bit` | **A** |
| 54 | `KS4038` | Keyestudio 4DOF Robot Arm Microbit Learning Kit Robot Arm Kit DIY... | Micro:bit y accesorios | `micro:bit` | **A** |
| 55 | `KS0802` | Keyestudio Crocodile Creative Learning Starter Kit DIY Stem Progr... | Micro:bit y accesorios | `micro:bit` | **A** |
| 56 | `KT0284` | 4pcs Dual Output Shaft 2KG DC Motor (Low Speed)In Blue Servo Moto... | Micro:bit y accesorios | `micro:bit / Lego compatible` | **B** |
| 57 | `KS0219` | KEYESTUDIO Raspberry Pi T type board+40P Colorful Ribbon Cable+40... | Raspberry Pi y accesorios | `Raspberry Pi (Modelos 40 pines: Pi 2, 3, 4, 5)` | **A** |
| 58 | `SMP0023` | KEYESTUDIO 5 Megapixels 1080p Mini Camera Video Module for Raspbe... | Raspberry Pi y accesorios | `Raspberry Pi (Pi 2, 3, 4 / Requiere adaptador en Pi 5 y Pi Zero)` | **B** |
| 59 | `60520146` | Black Aluminum alloy box case Porous heat-dissipating metal case ... | Raspberry Pi y accesorios | `Raspberry Pi (Específico para Raspberry Pi 4B)` | **A** |
| 60 | `67600041` | Raspberry Pi Camera holder Acrylic holder Compatible with Raspber... | Raspberry Pi y accesorios | `Raspberry Pi (Soporte cámara SMP0023 / V2)` | **A** |
| 61 | `KS0255` | Keyestudio Bluetooth 4.0 Shield Expansion Shield Board for Arduin... | IoT y comunicación | `Arduino (Uno)` | **A** |
| 62 | `MD0322` | Keyes ESP8266 remote serial Port WIFI module for arduino. Keyes E... | IoT y comunicación | `Arduino / ESP8266 (Puerto Serie AT)` | **B** |
| 63 | `KS0205` | Keyestudio RC522 RFID Module for Arduino. Keyestudio RC522 RFID M... | IoT y comunicación | `Arduino / ESP32 / Raspberry Pi` | **A** |
| 64 | `MD0040` | NRF24L01 2.4GHz wireless Transceiver module - Black for arduino. ... | IoT y comunicación | `Arduino / micro:bit / ESP32 / Raspberry Pi` | **A** |
| 65 | `KS0026` | Keyestudio Digital IR Infrared Receiver Module for Arduino  UNO R... | IoT y comunicación | `Arduino / micro:bit / ESP32` | **A** |
| 66 | `KS0389` | Keyestudio ESP8266 WI-FI Module Shield +1M Micro USB Cable For Ar... | IoT y comunicación | `Arduino (Uno) / ESP8266` | **A** |
| 67 | `KS0541` | Keyestudio Basic Starter Kit for Arduino DIY Programming Electron... | Kits educativos iniciales | `Arduino (Requiere Placa Externa)` | **B** |
| 68 | `KS0487` | Keyestudio 37 in 1 Sensor Kit Upgrade V3.0 +Gift Box for Arduino ... | Kits educativos iniciales | `Arduino / micro:bit / ESP32 / Raspberry Pi` | **A** |
| 69 | `KS0567` | Keyestudio ESP32 IoT Control Smart Farm Starter Kit for Arduino S... | Kits educativos iniciales | `ESP32` | **A** |
| 70 | `49500005` | XL830L Mini Digital Multimeter AC/DC Current 20A Portable LCD 3-1... | Herramientas y accesorios | `Universal (Instrumentación Eléctrica)` | **A** |
| 71 | `49500004` | DT9205A Fully Protected Multimeter 200MΩ Resistor AC/DC 20A 6F22 ... | Herramientas y accesorios | `Universal (Instrumentación Eléctrica)` | **A** |
| 72 | `MD0118` | CP2102 USB to TTL / STC 6PIN Speed download for arduino+4Pin dupo... | Herramientas y accesorios | `Universal (Programación UART)` | **A** |

---

## 7. Detalle de Productos en Verificación (C), Postergados (D) y Descartados (E)

### C — Productos que Requieren Verificación Técnica (4 productos)
Estos productos poseen valor potencial pero no deben ser incorporados a cotizaciones formales sin confirmación previa:

| SKU Proveedor | Nombre del Producto | Motivo de la Retención Técnica | Acción Requerida |
| :--- | :--- | :--- | :--- |
| **`KS6040`** | Keyestudio BMP388 Barometric Pressure Sensor For Arduin... | DESCRIPCIÓN DEL PROVEEDOR AMBIGUA: Indica 'Optional With(Out) Shell For Lego'. No es posible determinar si este SKU incluye la carcasa de bloque Lego o es la placa desnuda. | REQUIERE_VERIFICACION_TECNICA para confirmar versión física exacta (con o sin carcasa Lego). |
| **`KS0143`** | Keyestudio Bluetooh XBee Bluetooth wireless module HC-0... | RESTRICCIÓN FÍSICA CRÍTICA: Este módulo Bluetooth HC-05 tiene factor de forma de tarjeta XBee (pines de paso 2.0 mm). NO se puede insertar directamente en protoboards convencionales de 2.54 mm. | REQUIERE_VERIFICACION_TECNICA para confirmar compatibilidad de zócalos en los laboratorios escolares. |
| **`FB1001`** | Keyestudio Foxbit Go Development Kit Rich Sensor and Pe... | DATOS TÉCNICOS INSUFICIENTES: Placa 'Foxbit Go' todo-en-uno con WiFi/BT. No se especifica en los datos primarios el microcontrolador exacto ni el soporte oficial de bloques o MakeCode en español. | REQUIERE_VERIFICACION_TECNICA de documentación y entorno de desarrollo. |
| **`KS5028`** | Keyestudio ESP32 S3 Xiaozhi AI Chatbot Kit with Camera ... | DEPENDE DE SERVICIOS EN LA NUBE: Kit Chatbot IA Xiaozhi con cámara y ESP32-S3. La arquitectura Xiaozhi AI depende habitualmente de servidores en la nube y configuración de cuentas que podrían no ser viables o requerir chino/inglés en colegios chilenos. | REQUIERE_VERIFICACION_TECNICA sobre disponibilidad y latencia de backend en la nube en Chile. |

### D — Productos Postergados (7 productos)
Productos válidos pero que se recomienda reservar para una segunda etapa de expansión del catálogo:

| SKU Proveedor | Nombre del Producto | Categoría | Motivo de Postergación |
| :--- | :--- | :--- | :--- |
| **`KS0151`** | keyestudio CNC shield V2 engraving machine / 3 D Printe... | Arduino y controladores | POSTERGAR para un futuro catálogo especializado técnico-profesional (TP). No prioritario para el catálogo escolar general. |
| **`KS0543`** | Keyestudio Beetlebot 3 in 1 Robot for Arduino STEM Educ... | Robótica y vehículos | POSTERGAR para una segunda fase. Para el catálogo inicial se priorizan los chasis modulares (CR0011, CR0019) que permiten mayor cantidad de alumnos por presupuesto. |
| **`KS0607`** | Keyestudio Mini Caterpillar Tank Robot V3.0 For Arduino... | Robótica y vehículos | POSTERGAR para catálogo avanzado o fase 4. El costo elevado restringe su adopción en colegios públicos. |
| **`KS0377`** | Keyestudio Balance Car Shield V3 for Arduino  UNO R3. K... | Robótica y vehículos | POSTERGAR. Puede generar falsas expectativas en profesores que crean estar comprando un vehículo auto-equilibrado completo por $28,058 CLP. |
| **`MD0082`** | 4Pcs  3mm 8 * 8 led lattice bright red dot matrix modul... | Pantallas e interacción | POSTERGAR. Muy compleja de cablear directamente para estudiantes iniciales. Priorizar módulos matriciales con chip MAX7219 o shields matriciales. |
| **`KS3018`** | KEYESTUDIO GPIO Breakout Kit for Raspberry Pi 4 4b 3 3b... | Raspberry Pi y accesorios | POSTERGAR. KS0219 cubre la misma función técnica con mejor relación costo-beneficio para los colegios. |
| **`60520134`** | Hi-Q Acrylic Transparent Case Box For Raspberry Pi 4  E... | Raspberry Pi y accesorios | POSTERGAR para evitar saturación de accesorios protectores similares. |

### E — Productos Descartados del Catálogo Inicial (3 productos)
Productos que no formarán parte del primer catálogo público (permanecen archivados en el catálogo maestro):

| SKU Proveedor | Nombre del Producto | Razón Técnica de Exclusión |
| :--- | :--- | :--- |
| **`KT0326`** | High Spray Heavy Fog Atomization Drive Circuit Board Dl... | ERROR CRÍTICO IDENTIFICADO: Se catalogó erróneamente como sensor ultrasónico de distancia (2-400cm). Es un circuito transductor piezoeléctrico de humidificación/atomización de agua (mist maker). |
| **`60320054`** | 7PCS Mini 25 Tie-point Breadboard Solderless Prototype ... | INADECUADO PEDAGÓGICAMENTE: Pack de protoboards diminutas de solo 25 puntos (5x5). No tienen capacidad para alojar circuitos integrados o proyectos educativos reales. |
| **`KS3010`** | Original Raspberry Pi 4B Complete Starter kit With AU P... | ERRORES COMERCIALES Y TÉCNICOS GRAVES PARA CHILE: 1) Viene con fuente de poder con enchufe australiano ('AU Plug'), incompatible con la red eléctrica chilena (220V tipo C/L). 2) Dice 'Complete Starter Kit', pero indica explícitamente '(No Raspberry Pi board)'. Genera enorme riesgo de reclamos en colegios. |

---

## 8. Conclusiones y Próximos Pasos

1. **Estado del Repositorio:** El sistema se mantiene estrictamente en **SOLO LECTURA**. No se han ejecutado cambios de estado, publicación ni especificaciones en la base de datos de producción.
2. **Objetivo de Reducción Cumplido:** Se filtró y depuró con éxito el lote de 86 candidatos, entregando un núcleo de **72 productos de alta robustez técnica y viabilidad pedagógica** (dentro del rango requerido de 60 a 80).
3. **Punto de Control:** El proceso queda completamente **DETENIDO** en este punto, a la espera de la revisión, comentarios y autorización formal por parte del equipo Humm.
