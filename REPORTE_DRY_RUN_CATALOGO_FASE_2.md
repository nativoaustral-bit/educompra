# REPORTE DE AUDITORÍA Y SIMULACIÓN (DRY-RUN) — CATÁLOGO FASE 2
## Plataforma EduCompra Humm (`educompra.humm.cl`)

**Fecha de Ejecución:** America/Santiago  
**Archivo Analizado:** `keyestudio_productos_completo.xlsx`  
**Modo:** SIMULACIÓN OBLIGATORIA (DRY-RUN) — CERO ESCRITURAS EN BASE DE DATOS  
**Estado:** **PUNTO DE CONTROL — DETENIDO A LA ESPERA DE REVISIÓN Y APROBACIÓN DE HUMM**  

---

## 1. Tabla Resumen de Auditoría Requerida

Conforme a las instrucciones de Fase 2, se presenta la verificación punto por punto:

| Indicador Requerido | Valor Detectado | Observaciones y Regla Aplicada |
| :--- | :---: | :--- |
| **Filas totales leídas** | **966** | Total de filas leídas en la hoja `Productos Keyestudio`. |
| **Filas válidas** | **966** | Filas con datos íntegros procesables. |
| **SKU únicos** | **944** | Cantidad total de códigos de fabricante identificados. |
| **SKU duplicados** | **16** | SKUs que aparecen en 2 o más filas del archivo. |
| **Duplicados idénticos** | **1** | Mismo SKU, misma descripción y mismo precio (consolidados en 1). |
| **Duplicados conflictivos** | **15** | **EXCLUIDOS:** Mismo SKU con diferente precio o descripción. |
| **Filas sin SKU** | **0** | Ninguna fila carece de identificador de fabricante. |
| **Filas sin precio** | **0** | Todas las filas contienen valor en columna de precio. |
| **Precios que no pudieron interpretarse** | **0** | Todos los valores (ej: `11.99 USD`) fueron convertidos exitosamente a Decimal. |
| **Precio mínimo USD** | **$0.99 USD** | Producto de menor costo (candidatos válidos). |
| **Precio máximo USD** | **$368.00 USD** | Producto de mayor costo (candidatos válidos). |
| **Imágenes encontradas** | **943** | Total de archivos fotográficos válidos en el directorio local. |
| **Productos sin imagen** | **1** | 1 producto candidato carece de fotografía física. |
| **Imágenes sin producto correspondiente** | **0** | El 100% de las imágenes físicas en la carpeta corresponden a SKUs del Excel. |
| **Productos nuevos que serían creados** | **0** | Candidatos listos para ingresar con `publicado = False` y categoría `"Sin clasificar"`. |
| **Productos existentes que serían actualizados** | **929** | Base de datos vacía actualmente (primer ingreso maestro). |
| **Productos que serían ignorados** | **15** | Los 15 SKUs en conflicto quedan fuera de importación hasta su curaduría. |
| **Errores de importación** | **0** | Proceso completado limpiamente sin excepciones ni bloqueos. |

---

## 2. Manejo Obligatorio de Duplicados

### 2.1 Duplicados Conflictivos (`CONFLICTO — REQUIERE REVISIÓN`)
Los siguientes **15 SKUs** (que involucran 36 filas del Excel) presentan disparidades en precios o descripciones. Siguiendo la directriz de seguridad de Humm, **ninguno se elige de manera arbitraria**; han sido clasificados como conflictivos y **quedan estrictamente excluidos de la importación definitiva** hasta su resolución manual por Humm:


| SKU en Conflicto | Repeticiones | Filas Excel | Variaciones de Precio (USD) | Descripciones Registradas |
| :--- | :---: | :---: | :--- | :--- |
| **`KS0077`** | 3 | 22, 674, 949 | $52.00 / $45.00 / $60.00 | • Fila 22: KEYESTUDIO Super Starter kit/Learning  Kit for Arduino  Education W/Gift Box+ 32 Projects. KEYESTUDIO Super Starter kit/Learning  Kit for Arduino  Education W/Gift Box+ 32 Projects<br>• Fila 674: Keyestudio Super Starter Learning Kit (NO UNOR3 Board) for Arduino Programming Education Kit + PDF. Keyestudio Super Starter Learning Kit (NO UNOR3 Board) for Arduino Programming Education Kit + PDF<br>• Fila 949: Keyestudio Super Starter Kit/Learning Kit With Mega 2560R3 For Arduino Education Project +PDF(online)+32Projects+Gift Box. Keyestudio Super Starter Kit/Learning Kit With Mega 2560R3 For Arduino Education Project +PDF(online)+32Projects+Gift Box |
| **`KS0078`** | 3 | 23, 675, 950 | $52.00 / $45.00 / $60.00 | • Fila 23: KEYESTUDIO Super Starter kit/Learning  Kit for Arduino  Education W/Gift Box+ 32 Projects. KEYESTUDIO Super Starter kit/Learning  Kit for Arduino  Education W/Gift Box+ 32 Projects<br>• Fila 675: Keyestudio Super Starter Learning Kit (NO UNOR3 Board) for Arduino Programming Education Kit + PDF. Keyestudio Super Starter Learning Kit (NO UNOR3 Board) for Arduino Programming Education Kit + PDF<br>• Fila 950: Keyestudio Super Starter Kit/Learning Kit With Mega 2560R3 For Arduino Education Project +PDF(online)+32Projects+Gift Box. Keyestudio Super Starter Kit/Learning Kit With Mega 2560R3 For Arduino Education Project +PDF(online)+32Projects+Gift Box |
| **`KS0079`** | 3 | 24, 676, 951 | $52.00 / $45.00 / $60.00 | • Fila 24: KEYESTUDIO Super Starter kit/Learning  Kit for Arduino  Education W/Gift Box+ 32 Projects. KEYESTUDIO Super Starter kit/Learning  Kit for Arduino  Education W/Gift Box+ 32 Projects<br>• Fila 676: Keyestudio Super Starter Learning Kit (NO UNOR3 Board) for Arduino Programming Education Kit + PDF. Keyestudio Super Starter Learning Kit (NO UNOR3 Board) for Arduino Programming Education Kit + PDF<br>• Fila 951: Keyestudio Super Starter Kit/Learning Kit With Mega 2560R3 For Arduino Education Project +PDF(online)+32Projects+Gift Box. Keyestudio Super Starter Kit/Learning Kit With Mega 2560R3 For Arduino Education Project +PDF(online)+32Projects+Gift Box |
| **`KS0240`** | 2 | 38, 585 | $19.00 / $7.20 | • Fila 38: Keyestudio RJ11 EASY Plug Main Control Upgrade Board V2.0 Controller +USB Cable for Arduino STEAM. Keyestudio RJ11 EASY Plug Main Control Upgrade Board V2.0 Controller +USB Cable for Arduino STEAM<br>• Fila 585: Keyestudio RJ11  RGB TCS34725 Color Sensor Module I2C interface for Arduino STEM. Keyestudio RJ11  RGB TCS34725 Color Sensor Module I2C interface for Arduino STEM |
| **`KS0080`** | 3 | 44, 626, 954 | $45.00 / $53.00 / $62.00 | • Fila 44: Keyestudio Maker Learning Kit/Starter Kit(NO UNOR3  Board) For Arduino  Starter W/Gift BOX+UNO Platform +1602 LCD+Servo+LEDs+PDF. Keyestudio Maker Learning Kit/Starter Kit(NO UNOR3  Board) For Arduino  Starter W/Gift BOX+UNO Platform +1602 LCD+Servo+LEDs+PDF<br>• Fila 626: Keyestudio Maker Learning kit /Starter kit For Arduino Project W/Gift Box+User Manual +1602LCD+Chassis+PDF(online). Keyestudio Maker Learning kit /Starter kit For Arduino Project W/Gift Box+User Manual +1602LCD+Chassis+PDF(online)<br>• Fila 954: Keyestudio Maker Starter Kit(MEGA 2560 R3)For Arduino Project W/Gift Box+User Manual+1602LCD+Chassis+PDF(online)+35Project+Video. Keyestudio Maker Starter Kit(MEGA 2560 R3)For Arduino Project W/Gift Box+User Manual+1602LCD+Chassis+PDF(online)+35Project+Video |
| **`KS0081`** | 3 | 45, 627, 955 | $45.00 / $53.00 / $62.00 | • Fila 45: Keyestudio Maker Learning Kit/Starter Kit(NO UNOR3  Board) For Arduino  Starter W/Gift BOX+UNO Platform +1602 LCD+Servo+LEDs+PDF. Keyestudio Maker Learning Kit/Starter Kit(NO UNOR3  Board) For Arduino  Starter W/Gift BOX+UNO Platform +1602 LCD+Servo+LEDs+PDF<br>• Fila 627: Keyestudio Maker Learning kit /Starter kit For Arduino Project W/Gift Box+User Manual +1602LCD+Chassis+PDF(online). Keyestudio Maker Learning kit /Starter kit For Arduino Project W/Gift Box+User Manual +1602LCD+Chassis+PDF(online)<br>• Fila 955: Keyestudio Maker Starter Kit(MEGA 2560 R3)For Arduino Project W/Gift Box+User Manual+1602LCD+Chassis+PDF(online)+35Project+Video. Keyestudio Maker Starter Kit(MEGA 2560 R3)For Arduino Project W/Gift Box+User Manual+1602LCD+Chassis+PDF(online)+35Project+Video |
| **`KS0082`** | 3 | 46, 628, 956 | $45.00 / $53.00 / $62.00 | • Fila 46: Keyestudio Maker Learning Kit/Starter Kit(NO UNOR3  Board) For Arduino  Starter W/Gift BOX+UNO Platform +1602 LCD+Servo+LEDs+PDF. Keyestudio Maker Learning Kit/Starter Kit(NO UNOR3  Board) For Arduino  Starter W/Gift BOX+UNO Platform +1602 LCD+Servo+LEDs+PDF<br>• Fila 628: Keyestudio Maker Learning kit /Starter kit For Arduino Project W/Gift Box+User Manual +1602LCD+Chassis+PDF(online). Keyestudio Maker Learning kit /Starter kit For Arduino Project W/Gift Box+User Manual +1602LCD+Chassis+PDF(online)<br>• Fila 956: Keyestudio Maker Starter Kit(MEGA 2560 R3)For Arduino Project W/Gift Box+User Manual+1602LCD+Chassis+PDF(online)+35Project+Video. Keyestudio Maker Starter Kit(MEGA 2560 R3)For Arduino Project W/Gift Box+User Manual+1602LCD+Chassis+PDF(online)+35Project+Video |
| **`KS0400`** | 2 | 60, 787 | $47.00 / $60.50 | • Fila 60: Keyestudio Sensor Starter V2.0 Kit 37 in 1 Box Sensor Kit for Arduino Sensor Kit (No Board). KS0399 kit with no board<br>• Fila 787: Keyestudio Sensor Starter V2.0 Kit 37 in 1 Box for Arduino UNO Starter Kit. KS0400 kit with V4.0 |
| **`KS0401`** | 2 | 61, 320 | $47.00 / $71.00 | • Fila 61: Keyestudio Sensor Starter V2.0 Kit 37 in 1 Box Sensor Kit for Arduino Sensor Kit (No Board). KS0399 kit with no board<br>• Fila 320: Keyestudio 37 in 1 Box Sensor Kit V2.0 Mega Controller Board Sensor Electronic Kit For Arduino. KS0401 kit with 2560 MEGA R3 |
| **`60720227`** | 2 | 237, 964 | $10.90 / $7.85 | • Fila 237: 8M Memory Voice Prompter 1W Active speaker Lighting/Button Control. 8M Memory Voice Prompter 1W Active speaker Lighting/Button Control<br>• Fila 964: DC 5V Active Speaker Buzzer D Digital Power Amplifier For DIY Electronic. DC 5V Active Speaker Buzzer D Digital Power Amplifier For DIY Electronic |
| **`KS0801`** | 2 | 481, 757 | $26.30 / $49.20 | • Fila 481: Keyestudio STEM Programming DIY Button Piano Learning Kit For Microbit Starter Kit Support Makcode/KidsBlock Without Board. Keyestudio STEM Programming DIY Button Piano Learning Kit For Microbit Starter Kit Support Makcode/KidsBlock Without Board<br>• Fila 757: Keyestudio STEM Programming DIY Button Piano Learning Kit For Microbit Starter Kit Support Makcode/KidsBlock With Microbit Board. Included micro:bit mainboard |
| **`KS4031`** | 2 | 551, 946 | $52.00 / $74.40 | • Fila 551: Keyestudio Micro Bit V2 4WD Mecanum Wheel Robot Car Kit STEM Toys Makecode &amp;Python Programming Without Microbit Board. It boasts multiply functions including ultrasonic sound following, line tracking, infrared control and Bluetooth control uses two 18650 lithium batteries<br>• Fila 946: Keyestudio Micro Bit V2 4WD Mecanum Wheel Robot Car Kit STEM Toys Makecode &amp;Python Programming With Microbit Board. It boasts multiply functions including ultrasonic sound following, line tracking, infrared control and Bluetooth control uses two 18650 lithium batteries |
| **`KS4032`** | 2 | 552, 947 | $52.00 / $74.40 | • Fila 552: Keyestudio Micro Bit V2 4WD Mecanum Wheel Robot Car Kit STEM Toys Makecode &amp;Python Programming Without Microbit Board. It boasts multiply functions including ultrasonic sound following, line tracking, infrared control and Bluetooth control uses two 18650 lithium batteries<br>• Fila 947: Keyestudio Micro Bit V2 4WD Mecanum Wheel Robot Car Kit STEM Toys Makecode &amp;Python Programming With Microbit Board. It boasts multiply functions including ultrasonic sound following, line tracking, infrared control and Bluetooth control uses two 18650 lithium batteries |
| **`KS0536`** | 2 | 899, 902 | $46.00 / $53.00 | • Fila 899: Keyestudio IoT Ultimate Starter Kit for Arduino Programming DIY Project Kit Without Plus Mainboard. KS0537 dose not includes Plus mainboard<br>• Fila 902: Keyestudio IoT Ultimate Starter Kit for Arduino Programming DIY Project Kit With Plus Mainboard. KS0536 includes Plus mainboard |
| **`KS0537`** | 2 | 900, 903 | $46.00 / $53.00 | • Fila 900: Keyestudio IoT Ultimate Starter Kit for Arduino Programming DIY Project Kit Without Plus Mainboard. KS0537 dose not includes Plus mainboard<br>• Fila 903: Keyestudio IoT Ultimate Starter Kit for Arduino Programming DIY Project Kit With Plus Mainboard. KS0536 includes Plus mainboard |


### 2.2 Duplicados Idénticos (Consolidados)
Los siguientes **1 SKUs** corresponden a filas repetidas con exactamente los mismos valores de SKU, descripción y precio. Se consolidan de forma segura en un único producto para evitar duplicidad de fichas:


| SKU Duplicado Idéntico | Repeticiones | Filas Excel | Precio (USD) | Descripción | Acción Aplicada |
| :--- | :---: | :---: | :---: | :--- | :--- |
| **`KS4014`** | 2 | 689, 690 | $43.00 | Keyestudio Micro：bit Mini Smart Turtle Robot  Car for STEM  Micro Bit Robot Without Micro Bit. Keyestudio Micro：bit Mini Smart Turtle Robot  Car for STEM  Micro Bit Robot Without Micro Bit | Consolidado en 1 producto único |


---

## 3. Pricing y Parámetros Comerciales

* **Fórmula de internación y precios:**
  $$\text{Costo Puesto en Chile (CLP)} = \text{Costo USD} \times \text{TC (\$950.00)} \times (1 + \text{15.00\%})$$
  $$\text{Precio Sugerido Neto (CLP)} = \text{Costo Puesto en Chile} \times (1 + \text{Recargo Comercial 80.00\%})$$
  $$\text{Precio Sugerido Total con IVA (CLP)} = \text{Precio Sugerido Neto} \times (1 + \text{19.00\%})$$

* **Parámetros aplicados desde `ConfiguracionPricing`:**
  * Tipo de cambio referencial: **\$950.00 CLP/USD**
  * Factor de flete e internación: **15.00%**
  * **RECARGO COMERCIAL:** **80.00%**
  * Impuesto al Valor Agregado (IVA): **19.00%**
* **Estadísticas de Precios USD (Candidatos Válidos):**
  * Precio mínimo: **\$0.99 USD**
  * Precio promedio: **\$17.07 USD**
  * Precio máximo: **\$368.00 USD**

---

## 4. Análisis de Cobertura de Imágenes

* **Total de imágenes físicas analizadas:** 943 archivos (.jpg).
* **Productos candidatos con imagen vinculada:** 928 de 929 (**99.9% de cobertura**).
* **Imágenes huérfanas (sin SKU en Excel):** 0.
* **Detalle del producto sin imagen:**

| SKU sin Imagen | Motivo Detectado en Excel | Acción Sugerida |
| :--- | :--- | :--- |
| **`KS0006`** | En Excel figura explícitamente: `Imagen alta resolución: No disponible`. | Asignar imagen placeholder institucional o solicitar asset a Keyestudio. |


---

## 5. Criterios de Blindaje y Reglas de Negocio Confirmadas

1. **Estructura Real del Excel:** Se utilizaron exactamente las 5 columnas maestras del archivo (`SKU o ID`, `Descripción del producto`, `Miniatura`, `Precio (USD)`, `Imagen alta resolución`).
2. **Categorización:** El 100% de los productos ingresará a la categoría provisional `"Sin clasificar"`. No se realiza categorización automática forzada en esta fase.
3. **Estado de Publicación:** Todos los productos ingresarán con `publicado = False` (estrictamente invisibles para el público).
4. **Política de Upsert no destructivo:** Ante futuras sincronizaciones de costos, se preservarán siempre las descripciones educativas, nombres comerciales en español y categorías curadas por el equipo de Humm.
5. **Cero escrituras en producción:** La ejecución se realizó en modo `--dry-run`. No se modificó ningún registro en la base de datos de producción.

---

**ESTADO ACTUAL:** Listo para revisión de Humm. La escritura real de los 929 productos candidatos queda en pausa hasta autorización expresa.
