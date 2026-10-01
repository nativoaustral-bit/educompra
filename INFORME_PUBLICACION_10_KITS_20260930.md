# INFORME DE PUBLICACIÓN CONTROLADA — LOTE DE 10 KITS KEYESTUDIO
## Plataforma EduCompra Humm (`educompra.humm.cl`)
**Fecha:** 30 de Septiembre de 2026  
**Operación:** Publicación Controlada mediante `ProductoPublicationService`  
**Resultado Global:** **4 PRODUCTOS PUBLICADOS (APROBADOS POR GATE)** | **6 PRODUCTOS BLOQUEADOS (SIN IMAGEN)**  
**Catálogo Público:** **72 → 76 PRODUCTOS PÚBLICOS** (Delta: **+4**)

---

## 1. Resumen Ejecutivo de la Operación

En estricto cumplimiento de la autorización de Humm y del principio de calidad y rigor institucional:
1. **Publicación Controlada:** No se realizó actualización masiva ni bypass de reglas; se evaluó cada uno de los 10 productos individualmente a través de [`ProductoPublicationService.validar_para_publicacion()`](file:///Users/rmerinog/PLATAFORMAS/EDUCOMPRA/apps/catalogo/services_publicacion.py).
2. **Resultados del Gate de Calidad (8 Criterios):**
   * **4 productos superaron el 100% de los requisitos** (`KS4050`, `FKS0003`, `KS4049`, `KS0474`) disponiendo de imagen fotográfica real vinculada en `/media/productos/`, curaduría pedagógica validada, precio referencial y unidad de compra. Fueron publicados formalmente con `publicado=True` y registro de auditoría en `RegistroActividad`.
   * **6 productos fueron bloqueados** (`FKS0004`, `FKS0005`, `KS4036F`, `KS0562F`, `KT0193F`, `KS0403`) por el criterio obligatorio de carecer de fotografía en el banco de imágenes (`"No cuenta con ninguna fotografía o imagen asociada."`). Permanecen en el catálogo maestro protegidos con `publicado=False`.
3. **Catálogo Público en Tienda:** Pasó de **72 a 76 productos públicos** (Delta exacto de **+4**).
4. **Verificación Especial de `KS0540`:** Se evaluó el kit prioritario `KS0540`. Aunque superó el gate de calidad pedagógica y fotográfica, **se mantuvo estrictamente con `publicado=False`**, conforme a la instrucción expresa de no publicarlo sin autorización adicional.
5. **Especificación Técnica Neutra:** Los 10 kits mantienen inalterado su estado `estado_especificacion_neutral='NO_REVISADO'`, sin asignación automática de `VALIDADO_HUMM`.
6. **Smoke Test de Cotización:** Se verificó exitosamente en la tienda la adición de kits Arduino, micro:bit y ESP32, la actualización de cantidades, el cálculo de subtotales y la disponibilidad del formulario de solicitud.

---

## 2. Matriz Exhaustiva Fila por Fila (10 SKUs Evaluados)

| SKU Humm / ID | SKU Prov. | Gate Calidad | Criterio Faltante | Precio CLP (IVA inc.) | Categoría | Estado Antes | Estado Después | URL Ficha Pública | Imagen Vinculada |
| :--- | :---: | :---: | :--- | :---: | :--- | :---: | :---: | :--- | :--- |
| **`HUMM-KEY-KS4050`**<br>(ID 932) | `KS4050` | **APROBADO** | *Ninguno (100% cumplido)* | **$93.325** | Micro:bit y accesorios | No publicado | **PUBLICADO** | [`/catalogo/ks4050-environment-monitoring-learning-kit-for-microbit/`](https://educompra.humm.cl/catalogo/ks4050-environment-monitoring-learning-kit-for-microbit/) | `/media/productos/KS4050_01.png` |
| **`HUMM-KEY-FKS0003`**<br>(ID 930) | `FKS0003` | **APROBADO** | *Ninguno (100% cumplido)* | **$69.995** | Robótica y vehículos | No publicado | **PUBLICADO** | [`/catalogo/fks0003-esp32-smart-robot-arm/`](https://educompra.humm.cl/catalogo/fks0003-esp32-smart-robot-arm/) | `/media/productos/FKS0003_01.png` |
| **`HUMM-KEY-KS4049`**<br>(ID 931) | `KS4049` | **APROBADO** | *Ninguno (100% cumplido)* | **$102.147** | Micro:bit y accesorios | No publicado | **PUBLICADO** | [`/catalogo/ks4049-micro-bit-smart-homewith-microbit-board/`](https://educompra.humm.cl/catalogo/ks4049-micro-bit-smart-homewith-microbit-board/) | `/media/productos/KS4049_01.png` |
| **`HUMM-KEY-KS0474`**<br>(ID 933) | `KS0474` | **APROBADO** | *Ninguno (100% cumplido)* | **$39.783** | Pantallas e interacción | No publicado | **PUBLICADO** | [`/catalogo/ks0474-keyestudio-gamepi-atmega32u4-diy-kit/`](https://educompra.humm.cl/catalogo/ks0474-keyestudio-gamepi-atmega32u4-diy-kit/) | `/media/productos/KS0474_01.jpg` |
| **`HUMM-KEY-FKS0004`**<br>(ID 934) | `FKS0004` | **RECHAZADO** | Falta fotografía asociada | $74.675 | Micro:bit y accesorios | No publicado | **NO PUBLICADO** | *No expuesto* (Bloqueado) | Placeholder (`SIN_IMAGEN`) |
| **`HUMM-KEY-FKS0005`**<br>(ID 936) | `FKS0005` | **RECHAZADO** | Falta fotografía asociada | $20.735 | Pantallas e interacción | No publicado | **NO PUBLICADO** | *No expuesto* (Bloqueado) | Placeholder (`SIN_IMAGEN`) |
| **`HUMM-KEY-KS4036F`**<br>(ID 935) | `KS4036F` | **RECHAZADO** | Falta fotografía asociada | $36.296 | Robótica y vehículos | No publicado | **NO PUBLICADO** | *No expuesto* (Bloqueado) | Placeholder (`SIN_IMAGEN`) |
| **`HUMM-KEY-KS0562F`**<br>(ID 937) | `KS0562F` | **RECHAZADO** | Falta fotografía asociada | $46.803 | Kits educativos iniciales | No publicado | **NO PUBLICADO** | *No expuesto* (Bloqueado) | Placeholder (`SIN_IMAGEN`) |
| **`HUMM-KEY-KT0193F`**<br>(ID 938) | `KT0193F` | **RECHAZADO** | Falta fotografía asociada | $56.000 | Sensores y módulos | No publicado | **NO PUBLICADO** | *No expuesto* (Bloqueado) | Placeholder (`SIN_IMAGEN`) |
| **`HUMM-KEY-KS0403`**<br>(ID 939) | `KS0403` | **RECHAZADO** | Falta fotografía asociada | $50.313 | Kits educativos iniciales | No publicado | **NO PUBLICADO** | *No expuesto* (Bloqueado) | Placeholder (`SIN_IMAGEN`) |

---

## 3. Estado del Catálogo y Métricas de Publicación

| Métrica | Antes de Publicar | Después de Publicar | Variación (Delta) | Observación |
| :--- | :---: | :---: | :---: | :--- |
| **Productos Públicos en Tienda** | **72** | **76** | **+4** | 4 productos aprobados formalmente |
| **Productos en Catálogo Maestro** | 939 | 939 | 0 | Sin alteraciones de inventario |
| **Productos con Imagen Real** | 78 | **82** | +4 | 4 nuevas fotos vinculadas en `/media/productos/` |
| **Kits de esta Lista Publicados** | 0 | **4** | +4 | Lote 1 completamente publicado |
| **Kits de esta Lista Pendientes de Foto** | 6 | **6** | 0 | Lote 2 resguardado hasta recibir fotografías |

---

## 4. Verificación de `KS0540` (Caso Prioritario)

* **SKU:** `KS0540` (ID 584)
* **Nombre Comercial:** Kit Inicial Arduino con Placa Controladora — 20 Proyectos Guiados
* **Evaluación del Gate:** **APROBADO** (Cumple los 8 criterios: activo, curaduría validada, categoría válida, descripción pedagógica, imagen `/media/productos/KS0540_01.jpg`, precio referencial positivo, unidad de compra).
* **Estado de Publicación:** **`publicado = False`** *(Preservado sin cambios)*.
* **Motivo:** En estricta conformidad con la instrucción de Humm, no se publicó por requerir autorización explícita e independiente.

---

## 5. Auditoría Operacional en `/gestion/`

Se registraron en `RegistroActividad` las 4 publicaciones con usuario superadministrador `rmerinog`:

1. `2026-10-01 01:06:44` | **PUBLICAR_PRODUCTO** | `HUMM-KEY-KS4050` | *Publicó 'Kit de Monitoreo Ambiental con micro:bit' en catálogo escolar.*
2. `2026-10-01 01:06:44` | **PUBLICAR_PRODUCTO** | `HUMM-KEY-FKS0003` | *Publicó 'Brazo Robótico Inteligente con ESP32' en catálogo escolar.*
3. `2026-10-01 01:06:44` | **PUBLICAR_PRODUCTO** | `HUMM-KEY-KS4049` | *Publicó 'Kit Smart Home con micro:bit y Placa Incluida' en catálogo escolar.*
4. `2026-10-01 01:06:44` | **PUBLICAR_PRODUCTO** | `HUMM-KEY-KS0474` | *Publicó 'Kit GamePi DIY Programable' en catálogo escolar.*

---

## 6. Resultados del Smoke Test de Cotización

Se ejecutó una prueba de integración punta a punta simulando una sesión docente:

1. **Navegación al Catálogo (`GET /catalogo/`):**
   * Código HTTP: `200 OK`.
   * Contador visible en storefront: **76 productos encontrados**.
   * Sin errores 500, sin duplicados y con renderizado fotográfico íntegro.

2. **Acceso a Fichas de Detalle (`GET /catalogo/<slug>/`):**
   * `/catalogo/ks4050-environment-monitoring-learning-kit-for-microbit/` $\rightarrow$ `200 OK` (Imagen real renderizada).
   * `/catalogo/fks0003-esp32-smart-robot-arm/` $\rightarrow$ `200 OK` (Imagen real renderizada).
   * `/catalogo/ks4049-micro-bit-smart-homewith-microbit-board/` $\rightarrow$ `200 OK` (Imagen real renderizada).
   * `/catalogo/ks0474-keyestudio-gamepi-atmega32u4-diy-kit/` $\rightarrow$ `200 OK` (Imagen real renderizada).

3. **Canasta de Cotización Docente:**
   * **Ítem 1 (Arduino):** `CR0033 CR0034` (Chasis 4WD Mecanum) $\times$ 1 un. = $50.546 CLP.
   * **Ítem 2 (micro:bit):** `KS4049` (Smart Home micro:bit) $\times$ 2 un. = $204.294 CLP.
   * **Ítem 3 (ESP32 / Robótica):** `FKS0003` (Brazo Robótico ESP32) $\times$ 1 un. = $69.995 CLP.
   * **Subtotal Inicial:** $324.835 CLP (3 ítems, 4 artículos) $\rightarrow$ `302 Redirect` a `/mi-cotizacion/`.
   * **Modificación de Cantidad:** Se actualizó `FKS0003` de 1 a 3 unidades vía `POST /mi-cotizacion/actualizar/`.
   * **Subtotal Revalidado:** $464.825 CLP (3 ítems, 6 artículos en total) calculado con precisión.
   * **Formulario Institucional (`GET /solicitar-cotizacion/`):** `200 OK`, formulario con campos docentes, datos de colegio y token de idempotencia operativo.

---

## 7. Integridad, Pruebas y Despliegue

1. **Respaldo Previo:**
   * Archivo: `backups/db_backup_pre_publicacion_10kits_20260930.sqlite3`.
   * Verificación SQLite: `PRAGMA integrity_check = ok`.
2. **Integridad Post-Operación:**
   * `sqlite3 db.sqlite3 "PRAGMA integrity_check;"` $\rightarrow$ **`ok`**.
3. **Suite Completa de Pruebas Automatizadas:**
   * Comando: `.venv/bin/python manage.py test`
   * **Resultado:** **75 tests ejecutados, 75 aprobados (0 fallos, 0 errores)** en 12.0s.

---

# 🛑 8. PUNTO DE CONTROL FINAL (DETENCIÓN TOTAL)

- **CATÁLOGO PÚBLICO EN TIENDA:** **76 PRODUCTOS PÚBLICOS.**
- **4 KITS PUBLICADOS** (`KS4050`, `FKS0003`, `KS4049`, `KS0474`).
- **6 KITS BLOQUEADOS POR AUSENCIA DE FOTOGRAFÍA** (`FKS0004`, `FKS0005`, `KS4036F`, `KS0562F`, `KT0193F`, `KS0403`), preservados con `publicado=False`.
- **`KS0540` PRESERVADO CON `publicado=False`** a la espera de autorización independiente.
- **NO SE HA INICIADO FASE 5B.**
- **SE DETIENE LA EJECUCIÓN CONFORMIDAD CON LAS INSTRUCCIONES.**
