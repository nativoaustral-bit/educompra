# EduCompra Humm — Plataforma de Soluciones Tecnológicas Educativas

[![Django Version](https://img.shields.io/badge/Django-5.1+-green.svg)](https://www.djangoproject.com/)
[![Python Version](https://img.shields.io/badge/Python-3.12%20%7C%203.14-blue.svg)](https://www.python.org/)
[![Test Suite](https://img.shields.io/badge/Tests-46%20passing-brightgreen.svg)]()
[![Production Status](https://img.shields.io/badge/Production-Fase%204%20Activa-success.svg)](https://educompra.humm.cl)

**EduCompra Humm** ([educompra.humm.cl](https://educompra.humm.cl)) es la plataforma digital de **Humm SpA** especializada en abastecimiento y equipamiento tecnológico para establecimientos educacionales de Chile (colegios, liceos técnicos y proyectos escolares).

A diferencia de un ecommerce tradicional B2C, EduCompra está optimizado para los procesos de compra escolar pública y privada en Chile:
* **Explorar y aprender:** Fichas con descripciones didácticas, advertencias de uso escolar y tecnologías compatibles (Arduino, BBC micro:bit, Raspberry Pi, ESP32).
* **Especificaciones técnicas neutras:** Preparadas para compras públicas (Ley 19.886), postulaciones a subvenciones (SEP, FAEP) y Mercado Público (Compra Ágil, Licitaciones y Convenio Marco).
* **Canasta "Mi Cotización":** Los docentes y encargados de compras arman su lista de insumos y solicitan una cotización formal sin necesidad de registro previo ni pasarelas de pago.

---

## 1. Arquitectura de Despliegue y Política de Entornos

El proyecto opera bajo el principio de **separación estricta entre código canónico y entorno de ejecución**:

```
                  ┌────────────────────────────────────────┐
                  │       GITHUB (Fuente Canónica)          │
                  │  • Código Django, Templates, Static    │
                  │  • Workflows CI/CD, Tests (46)         │
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
                  │  │   ├── secrets/  (.env productivo)   │
                  │  │   └── venv/     (Python env)        │
                  │  └── educompra.humm.cl/ (DocumentRoot) │
                  │      ├── passenger_wsgi.py             │
                  │      ├── static/                       │
                  │      └── tmp/restart.txt               │
                  └────────────────────────────────────────┘
```

### Reglas Críticas de Producción:
1. **Base de Datos Persistente Aislada:** La base SQLite de producción reside exclusivamente en `/home1/paulocis/apps/educompra/data/db.sqlite3`. **Nunca** debe ubicarse dentro del DocumentRoot ni versionarse en Git.
2. **Archivos Multimedia Persistentes:** Las fotos de los productos se almacenan en `/home1/paulocis/apps/educompra/media/` y persisten independientemente de los despliegues.
3. **Exclusión de Archivos Sensibles y Markdown:** Por seguridad, ningún archivo `.md`, `.git`, `.env` ni copias de base de datos se transfieren ni permiten dentro del DocumentRoot.
4. **Activación de Catálogo No Destructiva:** Los despliegues automáticos **nunca** auto-publican ni alteran el catálogo si ya existen productos públicos. La activación es una operación administrativa controlada.

---

## 2. Estructura Modular de la Aplicación

El proyecto está organizado en 3 aplicaciones Django cohesivas:

```
apps/
├── core/                  # Utilidades y configuración transversal
│   ├── templatetags/      # Filtros de plantilla: separador_miles, formato_clp
│   ├── regiones_chile.py  # 16 regiones y 346 comunas oficiales de Chile (100% local)
│   ├── models.py          # ParametrosPricing (TC USD, internación, recargo general)
│   └── views.py           # Home institucional y health-check (/health/)
│
├── catalogo/              # Gestión de productos y experiencia de navegación
│   ├── models.py          # Producto, Categoria, Tecnologia, Imagen, Especificación Neutra
│   ├── views.py           # Catálogo público, buscador, filtros por categoría y ficha técnica
│   ├── admin.py           # Panel administrativo con acciones de curaduría y recálculo de pricing
│   └── management/        # Comandos operativos de sincronización y activación
│
└── cotizaciones/          # Experiencia de cotización docente
    ├── models.py          # SolicitudCotizacion, ItemSolicitudCotizacion (Snapshots inmutables)
    ├── services.py        # CartService (sesión anónima) y SubmissionService (idempotencia)
    ├── forms.py           # Formulario docente con validaciones chilenas y honeypot anti-spam
    ├── views.py           # Mi Cotización, actualizar cantidades, confirmación pública higienizada
    └── emails.py          # Envío asíncrono seguro de correos transaccionales (guardar primero)
```

---

## 3. Catálogo Curado Oficial (72 Productos)

El catálogo inicial público está compuesto por **72 productos rigurosamente seleccionados y validados** en Fase 3 y 4:
* **929 productos totales** en catálogo maestro del proveedor.
* **72 productos aprobados** con estado de curaduría `VALIDADO` y `publicado=True`.
* **857 productos restantes** conservados en base maestra (`publicado=False`) para futuras etapas.
* **Precios Referenciales:** Calculados en base a fórmula institucional con IVA incluido, expresados con separador de miles oficial (`$XX.XXX CLP`).

---

## 4. Comandos de Gestión Operativos (`manage.py`)

Para operaciones administrativas en servidor o desarrollo local:

### Auditoría y Verificación de Estado
```bash
# Verifica los conteos de la base productiva y falla si no hay exactamente 72 publicados
python manage.py verificar_estado_catalogo_produccion --assert-72

# Inspección informativa sin abortar
python manage.py verificar_estado_catalogo_produccion
```

### Sincronización de Curaduría Canónica (Fase 3)
```bash
# Sincroniza en la base de datos los 72 productos canónicos aprobados en Fase 3
python manage.py sincronizar_curaduria_fase_3
```

### Activación y Publicación Controlada (Fase 4B)
```bash
# Simulación previa obligatoria (valida que exactamente 72 productos sean elegibles)
python manage.py activar_catalogo_publico_fase_4 --dry-run

# Activación definitiva (establece publicado=True sin tocar otros metadatos)
python manage.py activar_catalogo_publico_fase_4
```

### Auditoría de Integridad contra Documentación
```bash
# Compara campo por campo los 72 productos en BD contra CATALOGO_CURADO_FASE_3.md
python manage.py auditar_integridad_fase_4b
```

---

## 5. Instalación y Ejecución Local

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

# 4. Configurar variables de entorno locales (opcional para desarrollo)
cp config/.env.example .env 2>/dev/null || true

# 5. Aplicar migraciones
python manage.py migrate

# 6. Ejecutar suite de pruebas unitarias y de integración (46 tests)
python manage.py test

# 7. Iniciar servidor de desarrollo
python manage.py runserver
```

---

## 6. Pipeline CI/CD en GitHub Actions

El archivo `.github/workflows/deploy.yml` orquesta el despliegue automático ante cada `push` a la rama `main`:

1. **Gate de Calidad:** Configura Python 3.12 y ejecuta la suite completa de 46 pruebas. Si algún test falla, el despliegue se cancela inmediatamente.
2. **Empaquetado Selectivo:** Construye un bundle limpio excluyendo tests, Markdown, archivos `.git` y bases de datos.
3. **Despliegue Atómico SSH:** Transmite el paquete a HostGator y ejecuta el script remoto protegido con un **bucle de reintentos automáticos** para tolerar bloqueos temporales de red o de firewall (cPHulk).
4. **Sincronización Web:** Actualiza estáticos (`collectstatic`), migraciones (`migrate`), sincroniza `passenger_wsgi.py` con permisos `755` y reinicia Passenger tocando `tmp/restart.txt`.
5. **Smoke Test Remoto Estricto:** 
   * Comprueba que `/health/` y `/catalogo/` respondan HTTP 200.
   * Valida en el HTML que se reporten 72 productos y que no aparezca el aviso de validación.
   * Ejecuta en la base productiva `verificar_estado_catalogo_produccion --assert-72`. Si el catálogo público no tiene exactamente 72 ítems, el despliegue marca error.
6. **Auditoría de Seguridad:** Valida que ningún archivo `.md` ni el árbol `.git/` queden accesibles públicamente a través de HTTP.

---

## 7. Archivo Histórico de Fases y Documentación

Para auditar en profundidad las decisiones comerciales, pedagógicas y técnicas de etapas anteriores, consultar los informes de cada hito:

| Documento | Descripción / Alcance |
| :--- | :--- |
| [ARQUITECTURA_REPOSITORIO_Y_DESPLIEGUE.md](file:///Users/rmerinog/PLATAFORMAS/EDUCOMPRA/ARQUITECTURA_REPOSITORIO_Y_DESPLIEGUE.md) | Política de separación canónica GitHub vs HostGator |
| [CATALOGO_CURADO_FASE_3.md](file:///Users/rmerinog/PLATAFORMAS/EDUCOMPRA/CATALOGO_CURADO_FASE_3.md) | **Fuente canónica oficial** de los 72 productos aprobados |
| [AUDITORIA_CANDIDATOS_FASE_3.md](file:///Users/rmerinog/PLATAFORMAS/EDUCOMPRA/AUDITORIA_CANDIDATOS_FASE_3.md) | Auditoría de selección técnica y metodológica |
| [INFORME_IMPLEMENTACION_FASE_4.md](file:///Users/rmerinog/PLATAFORMAS/EDUCOMPRA/INFORME_IMPLEMENTACION_FASE_4.md) | Construcción de la interfaz pública y experiencia docente |
| [INFORME_ACTIVACION_FASE_4B.md](file:///Users/rmerinog/PLATAFORMAS/EDUCOMPRA/INFORME_ACTIVACION_FASE_4B.md) | Activación en producción y trazabilidad de los 72 productos |
| [INFORME_IMPLEMENTACION_FASE_1.md](file:///Users/rmerinog/PLATAFORMAS/EDUCOMPRA/INFORME_IMPLEMENTACION_FASE_1.md) | Modelado de datos y arquitectura base Django |
| [INFORME_IMPLEMENTACION_FASE_2.md](file:///Users/rmerinog/PLATAFORMAS/EDUCOMPRA/INFORME_IMPLEMENTACION_FASE_2.md) | Motor de importación del catálogo Keyestudio |

---

## 8. Licencia y Derechos

© 2026 **Humm SpA** — Todos los derechos reservados.  
Plataforma desarrollada exclusivamente para soluciones educativas y compras institucionales en Chile.
