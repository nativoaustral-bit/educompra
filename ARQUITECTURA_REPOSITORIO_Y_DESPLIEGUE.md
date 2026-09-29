# EDUCOMPRA HUMM — POLÍTICA Y ARQUITECTURA DE REPOSITORIO Y DESPLIEGUE

**Fecha:** 29 de septiembre de 2026  
**Aprobación Institucional:** Humm  
**Estado:** **VIGENTE Y APLICADA**

---

## 1. PRINCIPIO FUNDAMENTAL DE ARQUITECTURA

A partir de esta directriz, el ecosistema EduCompra Humm opera bajo una separación estricta de responsabilidades entre el versionamiento de software y el entorno de ejecución:

```
┌────────────────────────────────────────────────────────┐
│                        GITHUB                          │
│               FUENTE CANÓNICA DEL PROYECTO             │
│  (Código, Migraciones, Templates, Estáticos, Tests,    │
│   Workflows CI/CD, Documentación Técnica Versionable)  │
└───────────────────────────┬────────────────────────────┘
                            │
                            │ GitHub Actions
                            │ (Tests + Bundle Limpio vía SCP)
                            ▼
┌────────────────────────────────────────────────────────┐
│                       HOSTGATOR                        │
│             ENTORNO DE EJECUCIÓN PRODUCTIVO            │
│  (Runtime mínimo indispensable, Sin .git, Sin Docs,    │
│   Datos persistentes y Secretos aislados de código)    │
└────────────────────────────────────────────────────────┘
```

1. **GITHUB = FUENTE CANÓNICA:** Contiene todo lo necesario para reconstruir el software, auditar el historial de cambios, ejecutar baterías de pruebas automatizadas y gobernar los despliegues.
2. **HOSTGATOR = ENTORNO DE EJECUCIÓN:** Recibe exclusivamente los binarios y scripts indispensables para interpretar Django bajo Phusion Passenger. **No es una copia completa del repositorio Git ni un repositorio de desarrollo.**

---

## 2. POLÍTICA DE PRIVACIDAD Y SEGURIDAD EN GITHUB

Dado que el repositorio puede tener visibilidad compartida o externa, queda **estrictamente prohibido** versionar o registrar en commits:

| Tipo de Información | Ejemplos | Mitigación Técnica en `.gitignore` |
| :--- | :--- | :--- |
| **Secretos y Credenciales** | `.env`, contraseñas, API keys, tokens, credenciales SSH, claves SMTP, Django `SECRET_KEY`. | Exclusión de `.env`, `.env.*`, `secrets/`, `*.pem`, `*.key`. |
| **Bases de Datos Productivas** | `db.sqlite3`, journals, WALs, dumps SQL. | Exclusión de `*.sqlite3`, `*.sqlite3-journal`, `*.db`, `*.sql`, `data/`. |
| **Archivos Multimedia** | Imágenes subidas por usuarios o catálogo en runtime. | Exclusión de `media/`. |
| **Respaldos de Datos** | Snapshots generados antes o después de despliegues. | Exclusión de `backups/`. |
| **Datos Críticos / Leads** | Solicitudes reales de cotización docente, datos de colegios, RUTs de clientes. | Nunca se persisten en código fuente (exclusivos de BD productiva). |
| **Fuentes Maestras Proveedor** | Planillas Excel brutas con costos de importación y notas internas. | Exclusión de `*.xlsx`, `*.xls`, `*.csv`, `data_import/`. |
| **Archivos de Construcción** | Caches de compilación, bytecode, temporales. | Exclusión de `__pycache__/`, `*.pyc`, `*.tar.gz`, `deploy_dist/`, `tmp/`. |

---

## 3. SEPARACIÓN DE DOCUMENTACIÓN: GITHUB VS. PRODUCCIÓN

Los documentos técnicos de desarrollo, tales como:
- `implementation_plan*.md`
- `INFORME_*.md`
- `CATALOGO_CURADO_FASE_3.md`
- Auditorías semánticas y minutas de arquitectura

**Se mantienen versionados en GitHub** para efectos de trazabilidad histórica, auditoría y control de calidad institucional.

**Sin embargo, NUNCA se despliegan al servidor HostGator.**  
El servidor público no requiere archivos Markdown para servir páginas web y su exposición representaría una fuga innecesaria de información de ingeniería interna.

---

## 4. ESTRUCTURA DE AISLAMIENTO EN EL SERVIDOR HOSTGATOR

En el servidor HostGator (`/home1/paulocis/apps/educompra/`), se implementa una arquitectura modular de directorios con permisos restrictivos (`chmod 700`):

```
/home1/paulocis/
├── apps/
│   └── educompra/
│       ├── app/           ← CÓDIGO EJECUTABLE DESPLEGADO (Sin .git, sin tests, sin docs)
│       │   ├── apps/
│       │   ├── config/
│       │   ├── templates/
│       │   ├── static/
│       │   ├── manage.py
│       │   ├── requirements.txt
│       │   └── passenger_wsgi.py
│       │
│       ├── data/          ← BASE DE DATOS PERSISTENTE (sqlite3)
│       │   └── db.sqlite3 (Permisos 700 - Aislada de despliegues)
│       │
│       ├── media/         ← MULTIMEDIA PERSISTENTE
│       │   └── catalogo/ (Imágenes cargadas e inmutables)
│       │
│       ├── backups/       ← RESPALDOS ATÓMICOS
│       │   └── pre_deploy_YYYYMMDD_HHMMSS.sqlite3 (Rotación automática)
│       │
│       ├── secrets/       ← CREDENCIALES PRODUCTIVAS
│       │   └── .env (Configuración sensible no versionada)
│       │
│       └── venv/          ← ENTORNO VIRTUAL PYTHON
│           └── (Dependencias optimizadas administradas con uv)
│
└── educompra.humm.cl/     ← DOCUMENTROOT PÚBLICO (Apache / Phusion Passenger)
    ├── passenger_wsgi.py  ← Punto de entrada WSGI sincronizado (permisos 0755 requeridos por suEXEC)
    ├── static/            ← Archivos estáticos recolectados (collectstatic)
    └── tmp/
        └── restart.txt    ← Gatillador de reinicio de Passenger
```

### Reglas de Preservación de Datos
1. **La base de datos productiva (`data/db.sqlite3`) NUNCA se sobreescribe durante un despliegue.**
2. **Las imágenes en `media/` NUNCA se eliminan durante un despliegue.**
3. **Antes de cualquier cambio de código, el pipeline genera un snapshot de respaldo en `backups/`.**
4. **El código desplegado en `app/` se conecta a `data/db.sqlite3` y `media/` a través de variables de entorno explícitas (`DB_NAME` y `MEDIA_ROOT`).**

---

## 5. PIPELINE CI/CD DE DESPLIEGUE SELECTIVO

Se reemplazó el antiguo mecanismo de `git reset --hard` por un flujo automatizado de empaquetado selectivo en GitHub Actions (`.github/workflows/deploy.yml`):

### Fases del Workflow:
1. **Quality Gate (Runner Ubuntu):**
   - Configura Python 3.12 y descarga dependencias.
   - Ejecuta la suite de pruebas completa (`python manage.py test`).
   - **Regla:** Si cualquier prueba unitaria o de integración falla, el despliegue se detiene de inmediato.
2. **Construcción del Paquete Limpio (`deploy_dist`):**
   - Extrae exclusivamente: `apps/` (con migraciones), `config/`, `templates/`, `static/`, `manage.py`, `requirements.txt` y `passenger_wsgi.py`.
   - Purga directorios `tests/`, `__pycache__/` y archivos `.pyc`.
   - Empaqueta el artefacto en `educompra_deploy.tar.gz`.
   - Ejecuta una aserción interna: **0 archivos `.md`, 0 carpetas `.git`, 0 archivos `.env`, 0 bases SQLite**.
3. **Despliegue Atómico y Seguro en HostGator (SSH):**
   - Abre un canal SSH seguro y comprueba directorios persistentes (`data/`, `media/`, `backups/`, `secrets/`).
   - Genera snapshot de respaldo preventivo en `backups/`.
   - Transmite vía streaming el paquete limpio directamente a `tar -xzf - -C app/` sin guardar archivos intermedios.
   - Instala o actualiza paquetes con `/home1/paulocis/.local/bin/uv pip install`.
   - Aplica migraciones con `python manage.py migrate --noinput`.
   - Ejecuta `python manage.py collectstatic --noinput`.
   - Sincroniza `passenger_wsgi.py` con permisos `0755` en `educompra.humm.cl`.
   - Purga residuos no públicos de `educompra.humm.cl` (`.md`, `.git`, `.env`, `.sqlite3`).
   - Reinicia la aplicación tocando `tmp/restart.txt`.
   - Purga residuos no públicos de `educompra.humm.cl`.
   - Reinicia la aplicación tocando `tmp/restart.txt`.
5. **Auditoría Post-Despliegue (Smoke Test y No-Exposición):**
   - `GET /health/`: Verifica que el servidor responda HTTP 200.
   - `GET /INFORME_ACTIVACION_FASE_4B.md`: Verifica que retorne **HTTP 404/403** (no expuesto).
   - `GET /.git/HEAD`: Verifica que retorne **HTTP 404/403** (no expuesto).
   - `GET /.env`: Verifica que retorne **HTTP 404/403** (no expuesto).
   - `GET /db.sqlite3`: Verifica que retorne **HTTP 404/403** (no expuesto).

---

## 6. COMANDOS DE CONTROL LOCAL Y EN SERVIDOR

### En Entorno de Desarrollo (Local)
- Ejecución de pruebas:
  ```bash
  python manage.py test
  ```
- Auditoría de integridad canónica:
  ```bash
  python manage.py auditar_integridad_fase_4b
  ```
- Respaldo manual en caliente:
  ```bash
  python manage.py respaldar_sqlite
  ```

### En Servidor HostGator (Producción)
- Reinicio manual de aplicación:
  ```bash
  touch /home1/paulocis/educompra.humm.cl/tmp/restart.txt
  ```
- Generación de respaldo de base de datos persistente:
  ```bash
  /home1/paulocis/apps/educompra/venv/bin/python /home1/paulocis/apps/educompra/app/manage.py respaldar_sqlite
  ```

---

## 7. DICTAMEN DE CUMPLIMIENTO

La nueva arquitectura:
- Elimina la presencia de Git y reportes Markdown en el servidor productivo.
- Protege de forma definitiva e inviolable la base de datos `db.sqlite3` y las imágenes `media/`.
- Automatiza el control de calidad previo a cualquier liberación a producción.
- Establece a GitHub como la fuente única de verdad versionable de EduCompra Humm.
