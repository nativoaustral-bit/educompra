# INFORME DE IMPLEMENTACIÓN — FASE 5A
## Plataforma de Administración Operacional, Gestión Comercial y Telemetría Base
**EduCompra Humm — `https://educompra.humm.cl/gestion/`**
*Fecha de Cierre: 30 de Septiembre de 2026*  
*Estado: IMPLEMENTADA Y VERIFICADA (65/65 Pruebas Exitosas — 100% OK)*

---

### Resumen Ejecutivo

Conforme a la aprobación con ajustes obligatorios emitida por Humm sobre el documento `implementation_plan_fase_5_administracion.md`, se ha completado la implementación de **Fase 5A (Administración Operacional)**, incorporando desde el inicio la captura de telemetría de eventos de uso seudónimos (Ajuste #1) y todos los candados de seguridad y calidad exigidos.

El acceso administrativo se encuentra operativo en:
- **URL Base:** `https://educompra.humm.cl/gestion/`
- **Herramienta técnica de respaldo:** `/admin/` (Django Admin estándar preservado intacto)
- **Catálogo Público Escolar:** `/` (Catálogo interactivo con captura de eventos integrada)

---

### 1. Modelos Creados y Modificados

#### Nuevos Modelos en `apps/cotizaciones/models.py`:
1. **`Establecimiento`**:
   - `nombre`, `nombre_normalizado` (sin diacríticos), `rbd`, `rut`, `tipo_institucion`, `comuna`, `region`, `dependencia_slep`, `estado_conciliacion` (`CONCILIADO_AUTOMATICO`, `CONCILIADO_MANUAL`, `PENDIENTE_CONCILIACION`).
   - Fechas históricas reales: `primera_interaccion` y `ultima_interaccion` (campos `DateTimeField` administrables programáticamente, sin `auto_now_add` para preservar veracidad histórica, cumpliendo el **Ajuste #7**).
2. **`Contacto`**:
   - `nombre`, `email` (normalizado en minúsculas), `telefono`, `cargo`, `establecimiento_principal` (FK opcional, **Ajuste #9**), `posible_duplicado` (booleano para multi-colegios o correos compartidos, **Ajuste #8**), `primera_interaccion`, `ultima_interaccion`.

#### Campos Agregados a `SolicitudCotizacion`:
- `establecimiento_ref`: FK opcional a `Establecimiento` (preserva 100% el texto histórico original `establecimiento` y snapshot de precios, **Ajustes #6 y #9**).
- `contacto_ref`: FK opcional a `Contacto`.
- `responsable`: FK a `auth.User` para asignación de ejecutivos Humm.
- `fuente_origen`, `utm_source`, `utm_medium`, `utm_campaign`, `utm_term`, `utm_content`: Atribución de tráfico.
- `monto_final_vendido`: Decimal independiente (**Ajuste #18**).
- `subestado_cierre`, `fecha_cierre`: Motivo o canal de cierre comercial.
- `es_prueba`: Booleano (**Ajuste #29**) para aislar pruebas internas de las métricas comerciales oficiales.

#### Nuevos Modelos en `apps/gestion/models.py`:
1. **`EventoUso`**:
   - `session_hash`: Hash HMAC-SHA256 irreversible de 64 caracteres. **Nunca almacena la `session_key` Django real** (**Ajuste #2**).
   - `tipo_evento`: `VISITA`, `BUSQUEDA`, `VER_PRODUCTO`, `AGREGAR_COTIZACION`, `QUITAR_COTIZACION`, `VER_MI_COTIZACION`, `INICIAR_SOLICITUD`, `ENVIAR_SOLICITUD` (**Ajuste #1**).
   - `metadata`: Filtrada estrictamente por `METADATA_WHITELIST`. **Prohíbe datos personales, RUT, contraseñas o tokens** (**Ajuste #3**).
   - `termino_busqueda_normalizado`, `resultados_busqueda`: Base para la detección de **Demanda No Cubierta** (**Ajuste #24**).
2. **`RegistroActividad`**:
   - Auditoría operacional estructurada (`PUBLICAR_PRODUCTO`, `DESPUBLICAR_PRODUCTO`, `MODIFICAR_PRICING`, `RECALCULAR_PRECIOS_MASIVO`, etc.).
   - Función `sanitizar_detalles()` que redacta recursivamente contraseñas, secretos y tokens (**Ajuste #30**).
3. **`LoteImportacion`**:
   - Archivos Excel y ZIP almacenados en `PRIVATE_STORAGE_ROOT` fuera del DocumentRoot público (**Ajuste #10**).
   - Trazabilidad de simulación DRY-RUN, errores, conflictos, productos nuevos y costos actualizados.

---

### 2. Migraciones Ejecutadas

Las migraciones fueron creadas en desarrollo y probadas bajo transacción segura sin generar archivos en caliente en el entorno de despliegue (**Ajuste #26**):
1. `apps/cotizaciones/migrations/0005_contacto_establecimiento_and_more.py`
2. `apps/gestion/migrations/0001_initial.py`

Verificación de integridad física SQLite:
```sql
PRAGMA integrity_check;
-- Resultado: ok
```

---

### 3. Matriz de Rutas Administrativas (`/gestion/`)

| Ruta URL | Nombre de Vista | Rol / Permiso Requerido | Descripción |
|---|---|---|---|
| `/gestion/login/` | `gestion:login` | Público | Autenticación administrativa con interfaz sobria Humm |
| `/gestion/logout/` | `gestion:logout` | Autenticado | Cierre seguro de sesión |
| `/gestion/` | `gestion:dashboard` | `can_view_gestion` | Dashboard con 10 KPIs, Funnel de conversión y alertas |
| `/gestion/productos/` | `gestion:productos_lista` | `can_manage_catalogo` | Catálogo maestro con filtros multidimensionales y switches |
| `/gestion/productos/nuevo/` | `gestion:producto_crear` | `can_manage_catalogo` | Alta manual en borrador (`publicado=False`) |
| `/gestion/productos/<id>/` | `gestion:producto_detalle` | `can_manage_catalogo` | Ficha modular en 6 bloques temáticos con demanda |
| `/gestion/productos/<id>/editar/` | `gestion:producto_editar` | `can_manage_catalogo` | Edición pedagógica/técnica (precios derivados no editables) |
| `/gestion/productos/<id>/toggle-publicado/` | `gestion:producto_toggle_publicado` | `can_publish_producto` | Switch controlado por `ProductoPublicationService` |
| `/gestion/importaciones/` | `gestion:importaciones` | `can_run_importaciones` | Subida a almacenamiento privado y lista de lotes |
| `/gestion/importaciones/subir/` | `gestion:importaciones_subir` | `can_run_importaciones` | Paso 1 y 2: Validación anti-ZIP-bomb y DRY-RUN |
| `/gestion/importaciones/<id>/` | `gestion:importacion_detalle` | `can_run_importaciones` | Paso 3 y 4: Informe de simulación y conflictos |
| `/gestion/importaciones/<id>/aprobar/` | `gestion:importacion_aprobar` | `can_run_importaciones` | Paso 5 y 6: Aprobación explícita e impacto en BD |
| `/gestion/solicitudes/` | `gestion:solicitudes_lista` | `can_manage_solicitudes` | Listado tabular con filtros avanzados |
| `/gestion/solicitudes/kanban/` | `gestion:solicitudes_kanban` | `can_manage_solicitudes` | Tablero Kanban con 8 columnas del ciclo escolar |
| `/gestion/solicitudes/<id>/` | `gestion:solicitud_detalle` | `can_manage_solicitudes` | Ficha 360° de solicitud, bitácora y validación técnica |
| `/gestion/solicitudes/<id>/estado/` | `gestion:solicitud_cambiar_estado` | `can_manage_solicitudes` | Actualización de estado, asignación de responsable y notas |
| `/gestion/establecimientos/` | `gestion:establecimientos_lista` | `can_manage_establecimientos` | Directorio de colegios con estado de conciliación |
| `/gestion/establecimientos/<id>/` | `gestion:establecimiento_detalle` | `can_manage_establecimientos` | Ficha 360° del colegio, ranking de compras y contactos |
| `/gestion/contactos/` | `gestion:contactos_lista` | `can_manage_establecimientos` | Directorio de docentes con alerta de duplicados |
| `/gestion/cotizaciones/` | `gestion:cotizaciones_lista` | `can_manage_cotizaciones` | Cotizaciones formales emitidas |
| `/gestion/analitica/` | `gestion:analitica_uso` | `can_view_analitica` | Telemetría global por `session_hash` y UTMs |
| `/gestion/analitica/productos/` | `gestion:analitica_productos` | `can_view_analitica` | Demanda: más vistos, agregados, solicitados y cerrados |
| `/gestion/analitica/busquedas/` | `gestion:analitica_busquedas` | `can_view_analitica` | Demanda no cubierta (búsquedas con 0 resultados) |
| `/gestion/configuracion/` | `gestion:configuracion` | `can_manage_configuracion` | Pricing, previsualización de impacto y recálculo |
| `/gestion/exportar/<recurso>/` | `gestion:exportar_csv` | Permiso según recurso | Descarga de CSV en UTF-8 con BOM |

---

### 4. Roles y Permisos Nativos de Django (Ajuste #19)

Se implementó el comando `python manage.py crear_roles_gestion`, estableciendo que los grupos son paquetes de permisos nativos Django y no simples comparaciones de cadenas de texto:
1. **Superadministrador**:
   - `is_superuser=True`. Acceso irrestricto a todas las funciones y Django Admin.
2. **Administradores EduCompra**:
   - Permisos: `can_view_gestion`, `can_manage_catalogo`, `can_publish_producto`, `can_run_importaciones`, `can_manage_solicitudes`, `can_manage_cotizaciones`, `can_manage_establecimientos`, `can_view_analitica`, `can_manage_configuracion`.
3. **Comercial EduCompra**:
   - Permisos: `can_view_gestion`, `can_manage_solicitudes`, `can_manage_cotizaciones`, `can_manage_establecimientos`.
   - Restringido de modificación de pricing y publicación de productos.

---

### 5. Conciliación Histórica de Establecimientos (Ajustes #5, #6, #7, #8 y #9)

Se creó el comando idempotente:
```bash
python manage.py conciliar_establecimientos_historicos --dry-run
python manage.py conciliar_establecimientos_historicos --aplicar
```

#### Jerarquía de 3 Niveles Implementada:
- **Nivel 1 (Identificador Fuerte):** Coincidencia exacta por RUT institucional o RBD normalizado.
- **Nivel 2 (Coincidencia Segura):** `nombre_normalizado + comuna` sin mutilar palabras institucionales significativas (se conservan términos como "Colegio", "Liceo", "Escuela" para evitar falsos positivos).
- **Nivel 3 (Ambiguo):** Mismo nombre en distinta comuna o coincidencia parcial no concluyente. **No se fusiona automáticamente**; se marca como `PENDIENTE_CONCILIACION` para arbitraje manual desde `/gestion/establecimientos/`.
- **Contactos Docentes:** Emails normalizados en minúsculas. Si un correo se detecta con nombres distintos o en múltiples instituciones, se marca `posible_duplicado=True` sin destruir datos históricos.

---

### 6. Telemetría de Uso Seudónima y Demanda No Cubierta (Ajustes #1, #2, #3, #4 y #24)

- **Captura activa en Fase 5A:** Instrumentada en `apps/core/views.py`, `apps/catalogo/views.py`, `apps/cotizaciones/views.py` y `apps/cotizaciones/services.py`.
- **`session_hash`:** Generado con HMAC-SHA256 utilizando la `SECRET_KEY` del servidor. La `session_key` real de Django jamás toca la base de datos.
- **Whitelist estricta de metadatos:** Se descartan de manera forzosa correos, RUTs, nombres, cookies y contraseñas.
- **Métricas:** En los dashboards se diferencia explícitamente:
  - *Sesiones Anónimas* ≠ *Contactos Identificados* ≠ *Establecimientos*.
  - Si no hay eventos acumulados, se despliega *"Sin datos todavía"*.
- **Demanda No Cubierta:** Panel destacado en `/gestion/analitica/busquedas/` que consolida búsquedas con 0 resultados devueltos, orientando decisiones comerciales de inventario sin generar productos automáticos.

---

### 7. Motor de Importación Asistida y Seguridad (Ajustes #10, #11, #12, #20 y #21)

- **Servicio Unificado:** `ImportacionCatalogoService` en `apps/catalogo/services_importacion.py`. Es consumido exactamente por la interfaz web `/gestion/importaciones/` y el comando de consola `importar_catalogo_keyestudio`.
- **Almacenamiento Privado:** Configurado en `settings.PRIVATE_STORAGE_ROOT` (`private/importaciones/`), inaccesible vía HTTP público.
- **Seguridad en Descompresión ZIP:**
  - Inspección previa de cada archivo en el archivo comprimido.
  - Rechazo de rutas absolutas (`/`) y secuencias de escape de directorio (`../`).
  - Protección anti-ZIP bomb (límite de archivos: 1.000, tamaño descomprimido máximo: 250 MB).
  - Admisión exclusiva de extensiones de imagen (`.jpg`, `.jpeg`, `.png`, `.webp`).
- **Flujo en 2 Fases (DRY-RUN + Aprobación):** La subida ejecuta obligatoriamente una simulación. Solo tras la confirmación con checkbox explícito se persisten los registros en base de datos. Los productos nuevos ingresan en borrador (`publicado=False`).

---

### 8. Publicación Controlada y Precios Derivados (Ajustes #13, #14, #15 y #16)

- **`ProductoPublicationService`:** Valida 8 requisitos de calidad antes de permitir `publicado=True`:
  1. Producto activo en sistema.
  2. Curaduría en estado `VALIDADO`.
  3. Nombre comercial no vacío.
  4. Categoría válida asignada.
  5. Descripción pedagógica/educativa redactada.
  6. Imagen principal asignada.
  7. Precio sugerido mayor a $0 CLP.
  8. Unidad de compra definida.
- **Despublicar:** Acción directa y segura que no altera solicitudes, cotizaciones ni snapshots existentes.
- **Precios Derivados:** Los campos `costo_puesto_chile_clp`, `precio_sugerido_neto_clp` y `precio_sugerido_total_clp` son derivados automáticos del costo USD y los factores financieros.
- **Previsualización de Impacto en Pricing:** En `/gestion/configuracion/`, modificar tipo de cambio o recargos no altera la base de datos de inmediato. Exige previsualizar una muestra del impacto y confirmar explícitamente el alcance deseado (*Públicos*, *Activos* o *Todos*).

---

### 9. Distinción Comercial Rigurosa (Ajustes #17, #18 y #29)

- **Monto Solicitado vs Cotizado vs Vendido:**
  - `SolicitudCotizacion.total_referencial_estimado`: Monto referencial solicitado por el profesor.
  - `CotizacionFormal.total`: Monto cotizado formalmente por Humm.
  - `SolicitudCotizacion.monto_final_vendido`: Monto efectivamente facturado tras el cierre.
  - No se infieren unos de otros.
- **Demanda vs Venta:** Se eliminó la etiqueta errónea *"Más vendidos"* para solicitudes cerradas. Se utiliza *"Productos en solicitudes cerradas"* de forma provisional hasta que en Fase 5C se registre la venta detallada por ítem.
- **Aislamiento de Pruebas:** Cualquier solicitud marcada con `es_prueba=True` se excluye de forma automática de los KPIs del Dashboard y reportes analíticos.

---

### 10. Respaldo, Verificación de Pruebas e Integridad

#### Batería de Pruebas Automatizadas:
```bash
.venv/bin/python manage.py test apps.catalogo apps.cotizaciones apps.core apps.gestion
```
**Resultado:**
```
Ran 65 tests in 11.761s
OK
```
- **19 pruebas unitarias y de integración de Fase 5A** (`apps/gestion/tests/test_fase5a_gestion.py`):
  - Control de accesos y redirecciones a login.
  - Restricciones por roles y permisos nativos.
  - Bloqueo y autorización por `ProductoPublicationService`.
  - Inalterabilidad manual de precios derivados.
  - Previsualización y confirmación de recálculo masivo de pricing.
  - Hash HMAC irreversible de sesiones anónimas.
  - Filtrado estricto por whitelist de metadata en telemetría.
  - Conciliación de establecimientos por RUT (Nivel 1) y Nombre+Comuna (Nivel 2).
  - Exclusión de solicitudes de prueba en el Dashboard.
  - Exportación de productos y solicitudes a CSV con codificación UTF-8 con BOM.
- **46 pruebas existentes** (Catálogo, Cotizaciones, Correos, Servicios): 100% aprobadas sin regresiones.

#### Verificación de Base de Datos SQLite:
```bash
python manage.py shell -c "from django.db import connection; cursor = connection.cursor(); cursor.execute('PRAGMA integrity_check;'); print(cursor.fetchone())"
# ('ok',)
```

---

### 11. Protocolo de Despliegue en Producción (Ajustes #25, #26, #27 y #28)

1. **GitHub = Fuente Canónica:** Los cambios se empaquetan y despliegan a través del workflow de GitHub Actions existente. **No se ejecuta `git pull` en HostGator** (**Ajuste #25**).
2. **Migraciones:** Se aplican exclusivamente con:
   ```bash
   python manage.py migrate --noinput
   ```
   **No se ejecuta `makemigrations` en el servidor de producción** (**Ajuste #26**).
3. **Respaldo Pre-Despliegue:** Respaldar `db.sqlite3` y verificar `PRAGMA integrity_check;` previo y posterior a la migración (**Ajuste #27**).
4. **Conciliación Histórica:** El comando `conciliar_establecimientos_historicos` **NO** se incluye en el script automático de deploy. Se ejecutará una única vez de forma controlada tras verificar su `--dry-run` (**Ajuste #28**).
5. **Roles:** Ejecutar en producción `python manage.py crear_roles_gestion`.

---

### 12. Punto de Control (Ajuste #33)

Con la entrega de este informe técnico:
- **Fase 5A se encuentra 100% completada y verificada.**
- Conforme a la instrucción expresa de Humm, **se detiene el avance aquí**.
- **NO se iniciará la Fase 5B completa (Dashboards analíticos avanzados) ni Fase 5C sin la revisión y autorización formal de Humm.**
