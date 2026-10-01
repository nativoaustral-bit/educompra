# EduCompra Humm — Plataforma de Soluciones Tecnológicas Educativas

[![Django Version](https://img.shields.io/badge/Django-5.1+-green.svg)](https://www.djangoproject.com/)
[![Python Version](https://img.shields.io/badge/Python-3.12%20%7C%203.14-blue.svg)](https://www.python.org/)
[![Test Suite](https://img.shields.io/badge/Tests-75%20passing-brightgreen.svg)]()
[![Production Status](https://img.shields.io/badge/Production-Fase%205A%20Activa%20(77%20Kits%20y%20Componentes)-success.svg)](https://educompra.humm.cl)

**EduCompra Humm** ([educompra.humm.cl](https://educompra.humm.cl)) es la plataforma digital de **Humm SpA** especializada en abastecimiento y equipamiento tecnológico para establecimientos educacionales de Chile (colegios, liceos técnicos, SLEP y proyectos escolares).

A diferencia de un ecommerce tradicional B2C, EduCompra está optimizado para los procesos de adquisición escolar pública y privada en Chile:
* **Explorar y aprender:** Fichas con descripciones pedagógicas, advertencias didácticas y tecnologías compatibles (Arduino, BBC micro:bit, Raspberry Pi, ESP32).
* **Especificaciones técnicas neutras:** Preparadas para compras públicas (Ley 19.886), postulaciones a subvenciones (SEP, FAEP) y Mercado Público (Compra Ágil, Licitaciones y Convenio Marco).
* **Canasta "Mi Cotización":** Los docentes y encargados de compras arman su selección de insumos y solicitan una cotización formal sin barreras de entrada ni pasarelas de pago.
* **Plataforma de Administración `/gestion/`:** Portal operacional propio para la gestión comercial, seguimiento en Kanban de solicitudes, administración de catálogo, conciliación de colegios y telemetría de demanda no cubierta.

---

## 1. Arquitectura de Despliegue y Política de Entornos

El proyecto opera bajo el principio de **separación estricta entre código canónico y entorno de persistencia**:

```
                  ┌────────────────────────────────────────┐
                  │       GITHUB (Fuente Canónica)          │
                  │  • Código Django, Templates, Static    │
                  │  • Workflows CI/CD, Tests (75 passing) │
                  │  • Informes y Memoria Técnica (.md)    │
                  └───────────────────┬────────────────────┘
                                      │ GitHub Actions (Push a main)
                                      ▼
                  ┌────────────────────────────────────────┐
                  │      HOSTGATOR (Runtime Mínimo)        │
                  │  /home1/paulocis/                      │
                  │  ├── apps/educompra/                   │
                  │  │   ├── app/      (Código desplegado) │
                  │  │   ├── data/     (db.sqlite3 pers.)  │
                  │  │   ├── media/    (Imágenes productos)│
                  │  │   ├── backups/  (Snapshots SQLite)  │
                  │  │   ├── secrets/  (.env productivo)   │
                  │  │   └── venv/     (Python 3.12 env)   │
                  │  └── educompra.humm.cl/ (DocumentRoot) │
                  │      ├── passenger_wsgi.py             │
                  │      ├── static/                       │
                  │      ├── media/    (Symlink o público) │
                  │      └── tmp/restart.txt               │
                  └────────────────────────────────────────┘
```

### Reglas Críticas de Producción:
1. **Base de Datos Persistente Aislada:** La base SQLite de producción reside en `/home1/paulocis/apps/educompra/data/db.sqlite3`. **Nunca** debe ubicarse dentro del DocumentRoot público ni versionarse en Git.
2. **Archivos Multimedia Persistentes:** Las fotos de los productos se almacenan en `/home1/paulocis/apps/educompra/media/` y en el DocumentRoot `/home1/paulocis/educompra.humm.cl/media/productos/`, persistiendo independientemente de los despliegues de código.
3. **Exclusión de Archivos Sensibles y Markdown:** Por seguridad, ningún archivo `.md`, `.git`, `.env` ni copias de base de datos se transfieren ni permiten dentro del DocumentRoot.
4. **Activación y Publicación Controlada:** Los despliegues automáticos **nunca** auto-publican ni alteran el catálogo de manera indiscriminada. Toda publicación requiere validación del Gate de Calidad mediante `ProductoPublicationService`.

---

## 2. Estructura Modular de la Aplicación

El proyecto está organizado en 4 aplicaciones Django cohesivas:

```
apps/
├── core/                  # Utilidades y configuración transversal
│   ├── templatetags/      # Filtros de plantilla: separador_miles, formato_clp
│   ├── regiones_chile.py  # 16 regiones y 346 comunas oficiales de Chile (100% local)
│   ├── models.py          # ParametrosPricing (TC USD, internación, recargo general)
│   └── views.py           # Home institucional y health-check (/health/)
│
├── catalogo/              # Gestión de productos y experiencia de navegación
│   ├── models.py          # Producto, Categoria, Tecnologia, ProductoImagen, PreciosVolumen
│   ├── views.py           # Catálogo público, buscador, filtros por categoría y ficha técnica
│   ├── services_importacion.py # Motor de importación de listas, tramos por volumen y fotos
│   ├── services_publicacion.py # Quality Gate con 8 criterios obligatorios de publicación
│   └── management/        # Comandos de auditoría, sincronización y verificación
│
├── cotizaciones/          # Experiencia de cotización docente
│   ├── models.py          # SolicitudCotizacion, ItemSolicitudCotizacion (Snapshots inmutables)
│   ├── services.py        # CartService (sesión anónima) y SubmissionService (idempotencia)
│   ├── forms.py           # Formulario docente con validaciones chilenas y honeypot anti-spam
│   ├── views.py           # Mi Cotización, actualizar cantidades, confirmación pública higienizada
│   └── emails.py          # Envío asíncrono seguro de correos transaccionales (guardar primero)
│
└── gestion/               # Plataforma administrativa y analítica (/gestion/)
    ├── models.py          # Establecimiento, Contacto, EventoUso, RegistroActividad
    ├── services_telemetria.py # Captura de eventos con anonimización irreversible (HMAC-SHA256)
    ├── services_auditoria.py  # Registro estructurado de actividad con sanitización de secretos
    ├── decorators.py      # Control de acceso por roles (gestion_required, permiso_requerido)
    └── views/             # Dashboard, Kanban, Productos, Establecimientos, Pricing, Analítica
```

---

## 3. Estado del Catálogo y Métricas Actuales

A partir de la incorporación de listas de proveedor con tramos por volumen y la curaduría institucional de kits educativos:

| Métrica | Valor Actual | Estado |
| :--- | :---: | :--- |
| **Productos en Catálogo Maestro** | **939** | Inventario consolidado de componentes y kits |
| **Curaduría Pedagógica 'VALIDADO'** | **88** | Fichas técnicas con curaduría y uso educativo formal |
| **Productos Públicos en Tienda** | **77** | Expuestos en [educompra.humm.cl/catalogo/](https://educompra.humm.cl/catalogo/) |
| **Productos en Resguardo (No Públicos)** | **862** | Preservados en base de datos (`publicado=False`) |
| **Kits Educativos Publicados** | **9** | Arduino (con y sin placa), micro:bit, ESP32, IoT, Didácticos |
| **Kits en Espera de Fotografía** | **6** | Lote 2 resguardado por gate de calidad (`SIN_IMAGEN`) |

### Fórmulas de Pricing Institucional:
* **Costo Puesto en Chile:** $\text{USD} \times \text{TC} \times (1 + \text{Arancel} + \text{Internación})$
* **Precio Sugerido Total:** $\text{Costo Chile} \times (1 + \text{Margen}) \times 1.19$ (IVA incluido).
* **Escalas por Volumen:** Registro de tramos diferenciados (1–9, 10–49, 50–100, 101–300+ unidades).

---

## 4. Plataforma de Administración Operativa (`/gestion/`)

Acceso seguro para el equipo de Humm en: **`https://educompra.humm.cl/gestion/`**

### Módulos Principales:
1. **Dashboard Operacional:** Resumen de solicitudes activas, cotizaciones en trámite, establecimientos atendidos y métricas de navegación.
2. **Embudo y Kanban de Solicitudes:** Seguimiento de estados comerciales: `NUEVA` $\rightarrow$ `EN_REVISION` $\rightarrow$ `CONTACTADO` $\rightarrow$ `COTIZADA` $\rightarrow$ `CERRADA_GANADA` / `CERRADA_PERDIDA`.
3. **Catálogo y Publicación:** Edición pedagógica, carga controlada de fotografías y publicación auditada.
4. **Directorio Escolar y Conciliación:** Gestión de colegios y contactos con jerarquía en 3 niveles (RUT exacto $\rightarrow$ Nombre+Comuna normalizado $\rightarrow$ Pendiente).
5. **Configuración de Pricing:** Simulación y recálculo masivo de tipo de cambio y márgenes con confirmación explícita.
6. **Analítica de Demanda y Búsquedas:** Identificación de términos buscados con 0 resultados para guiar futuras compras institucionales.

---

## 5. Comandos de Gestión Operativos (`manage.py`)

Para operaciones administrativas en servidor o desarrollo local:

### Auditoría y Verificación de Estado
```bash
# Verifica que el catálogo productivo contenga exactamente 77 productos publicados
python manage.py verificar_estado_catalogo_produccion --assert-77

# Verificación configurable por cantidad arbitraria
python manage.py verificar_estado_catalogo_produccion --assert-publicados 77

# Inspección informativa general sin abortar
python manage.py verificar_estado_catalogo_produccion
```

### Configuración de Roles y Permisos de Gestión
```bash
# Crea y actualiza los grupos 'Administradores EduCompra' y 'Comercial EduCompra'
python manage.py crear_roles_gestion
```

### Conciliación Histórica de Colegios
```bash
# Simulación no destructiva (dry-run)
python manage.py conciliar_establecimientos_historicos

# Aplicación definitiva en base de datos
python manage.py conciliar_establecimientos_historicos --aplicar
```

### Sincronización y Curaduría Canónica
```bash
# Sincroniza en la base de datos la curaduría pedagógica validada
python manage.py sincronizar_curaduria_fase_3
```

---

## 6. Instalación y Ejecución Local

### Prerrequisitos
* Python 3.12 o 3.14
* Git

### Paso a Paso
```bash
# 1. Clonar el repositorio
git clone https://github.com/nativoaustral-bit/educompra.git
cd educompra

# 2. Crear y activar entorno virtual
python3 -m venv .venv
source .venv/bin/activate

# 3. Instalar dependencias
pip install --upgrade pip
pip install -r requirements.txt

# 4. Configurar variables de entorno locales
cp config/.env.example .env 2>/dev/null || true

# 5. Aplicar migraciones
python manage.py migrate

# 6. Configurar grupos y permisos administrativos
python manage.py crear_roles_gestion

# 7. Ejecutar suite completa de pruebas automatizadas (75 tests)
python manage.py test

# 8. Iniciar servidor de desarrollo
python manage.py runserver
```

---

## 7. Pipeline CI/CD en GitHub Actions

El archivo `.github/workflows/deploy.yml` orquesta el despliegue automático ante cada `push` a la rama `main`:

1. **Gate de Calidad:** Configura Python 3.12 y ejecuta la suite completa de **75 pruebas automatizadas**. Si algún test falla, el despliegue se cancela inmediatamente.
2. **Empaquetado Selectivo:** Construye un bundle limpio excluyendo tests, Markdown, archivos `.git` y bases de datos (`tar -czf`).
3. **Despliegue Atómico SSH:** Transmite el paquete a HostGator con reintentos automáticos para tolerar restricciones temporales de red o cPHulk.
4. **Sincronización Web y Base de Datos:** Ejecuta migraciones, `crear_roles_gestion`, `collectstatic`, valida la integridad SQLite (`PRAGMA integrity_check`) y crea un snapshot de respaldo antes y después del despliegue.
5. **Auditoría de Estado de Catálogo (Solo Lectura):** Comprueba que la base productiva contenga exactamente los **77 productos esperados** (`--assert-77`). Si la cantidad no coincide, el despliegue se detiene para prevenir inconsistencias.
6. **Reinicio de Passenger y Smoke Test:** Recarga Phusion Passenger (`tmp/restart.txt`) y verifica que `/health/` y `/catalogo/` respondan HTTP 200 con 77 productos visibles en HTML.

---

## 8. Archivo Histórico de Fases y Documentación Técnica

Para auditar en profundidad las decisiones comerciales, pedagógicas y técnicas de cada etapa:

| Documento | Hito / Descripción |
| :--- | :--- |
| [INFORME_IMPLEMENTACION_FASE_5A.md](file:///Users/rmerinog/PLATAFORMAS/EDUCOMPRA/INFORME_IMPLEMENTACION_FASE_5A.md) | **Fase 5A:** Plataforma de Administración, Gestión Comercial y Telemetría Base |
| [INFORME_PUBLICACION_10_KITS_20260930.md](file:///Users/rmerinog/PLATAFORMAS/EDUCOMPRA/INFORME_PUBLICACION_10_KITS_20260930.md) | Publicación controlada de nuevos kits Keyestudio con tramos por volumen |
| [ARQUITECTURA_REPOSITORIO_Y_DESPLIEGUE.md](file:///Users/rmerinog/PLATAFORMAS/EDUCOMPRA/ARQUITECTURA_REPOSITORIO_Y_DESPLIEGUE.md) | Política de separación canónica GitHub vs persistencia HostGator |
| [INFORME_ACTIVACION_FASE_4B.md](file:///Users/rmerinog/PLATAFORMAS/EDUCOMPRA/INFORME_ACTIVACION_FASE_4B.md) | **Fase 4B:** Activación pública del catálogo escolar y smoke test inicial |
| [INFORME_IMPLEMENTACION_FASE_4.md](file:///Users/rmerinog/PLATAFORMAS/EDUCOMPRA/INFORME_IMPLEMENTACION_FASE_4.md) | **Fase 4A:** Construcción de la interfaz pública y experiencia docente |
| [CATALOGO_CURADO_FASE_3.md](file:///Users/rmerinog/PLATAFORMAS/EDUCOMPRA/CATALOGO_CURADO_FASE_3.md) | **Fase 3:** Catálogo canónico original de los 72 productos aprobados |
| [AUDITORIA_CANDIDATOS_FASE_3.md](file:///Users/rmerinog/PLATAFORMAS/EDUCOMPRA/AUDITORIA_CANDIDATOS_FASE_3.md) | Auditoría de selección técnica y metodológica de productos |
| [INFORME_IMPLEMENTACION_FASE_2.md](file:///Users/rmerinog/PLATAFORMAS/EDUCOMPRA/INFORME_IMPLEMENTACION_FASE_2.md) | **Fase 2:** Motor de importación del catálogo maestro Keyestudio |
| [INFORME_IMPLEMENTACION_FASE_1.md](file:///Users/rmerinog/PLATAFORMAS/EDUCOMPRA/INFORME_IMPLEMENTACION_FASE_1.md) | **Fase 1:** Modelado de datos y arquitectura base Django |

---

## 9. Licencia y Derechos

© 2026 **Humm SpA** — Todos los derechos reservados.  
Plataforma desarrollada exclusivamente para soluciones educativas y compras institucionales en Chile.
