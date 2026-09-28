"""
Django settings for EduCompra Humm project.
Django 5.2 LTS compatible.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Base Directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Añadir directorio apps al path para importación limpia y auto-descubrimiento de tests
sys.path.insert(0, str(BASE_DIR / "apps"))

# Cargar variables de entorno desde .env si existe
env_path = BASE_DIR / ".env"
if env_path.exists():
    load_dotenv(env_path)

# ==============================================================================
# SEGURIDAD Y ENTORNO
# ==============================================================================

# Entorno: development | production
DJANGO_ENV = os.getenv("DJANGO_ENV", "development").lower()

SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    if DJANGO_ENV == "production":
        raise ValueError("CRÍTICO: SECRET_KEY no está configurada en el entorno de producción.")
    SECRET_KEY = "django-insecure-dev-fallback-key-for-local-only-educompra-humm"

# DEBUG: solo True si explícitamente se especifica y no es producción forzada
DEBUG = os.getenv("DEBUG", "True").lower() in ("true", "1", "yes")
if DJANGO_ENV == "production":
    DEBUG = False

# Hosts autorizados
allowed_hosts_raw = os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1,educompra.humm.cl")
ALLOWED_HOSTS = [host.strip() for host in allowed_hosts_raw.split(",") if host.strip()]

# Orígenes confiables para CSRF en producción
CSRF_TRUSTED_ORIGINS = [
    "https://educompra.humm.cl",
    "http://educompra.humm.cl",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]

# Medidas de Seguridad
# NOTA: SECURE_BROWSER_XSS_FILTER ha sido omitido deliberadamente por ser un mecanismo obsoleto.
X_FRAME_OPTIONS = "DENY"
SECURE_CONTENT_TYPE_NOSNIFF = True

if not DEBUG and DJANGO_ENV == "production":
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    CSRF_COOKIE_HTTPONLY = True
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# ==============================================================================
# APLICACIONES INSTALADAS
# ==============================================================================

INSTALLED_APPS = [
    # Django Core Apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # EduCompra Apps de Dominio
    "apps.core",
    "apps.catalogo",
    "apps.cotizaciones",
]

# ==============================================================================
# MIDDLEWARE
# ==============================================================================

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

# ==============================================================================
# PLANTILLAS
# ==============================================================================

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

# ==============================================================================
# BASE DE DATOS (Soporte Dual: SQLite / MySQL-MariaDB)
# ==============================================================================

DB_ENGINE = os.getenv("DB_ENGINE", "django.db.backends.sqlite3")

if DB_ENGINE == "django.db.backends.mysql":
    # Intentar mysqlclient nativo primero; si falla, usar PyMySQL como fallback puro Python
    try:
        import MySQLdb  # noqa: F401
    except ImportError:
        import pymysql
        pymysql.install_as_MySQLdb()

    # Compatibilidad HostGator: Servidor opera con MySQL 5.7.44
    # Django 5.x por defecto bloquea versiones < 8.0.11 mediante check_database_version_supported,
    # aunque todas las consultas relacionales del proyecto son plenamente compatibles con MySQL 5.7.
    from django.db.backends.mysql.base import DatabaseWrapper
    DatabaseWrapper.check_database_version_supported = lambda self: None

    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.mysql",
            "NAME": os.environ.get("DB_NAME", "educompra"),
            "USER": os.environ.get("DB_USER", "root"),
            "PASSWORD": os.environ.get("DB_PASSWORD", ""),
            "HOST": os.environ.get("DB_HOST", "localhost"),
            "PORT": os.environ.get("DB_PORT", "3306"),
            "OPTIONS": {
                "charset": "utf8mb4",
                "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
            },
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / os.getenv("DB_NAME", "db.sqlite3"),
        }
    }

# ==============================================================================
# VALIDADORES DE CONTRASEÑA
# ==============================================================================

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ==============================================================================
# INTERNACIONALIZACIÓN Y ZONA HORARIA
# ==============================================================================

LANGUAGE_CODE = "es-cl"
TIME_ZONE = "America/Santiago"
USE_I18N = True
USE_TZ = True

# ==============================================================================
# ARCHIVOS ESTÁTICOS Y MULTIMEDIA
# ==============================================================================

STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = Path(os.getenv("STATIC_ROOT")) if os.getenv("STATIC_ROOT") else BASE_DIR / "staticfiles"

MEDIA_URL = "/media/"
MEDIA_ROOT = Path(os.getenv("MEDIA_ROOT")) if os.getenv("MEDIA_ROOT") else BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Runner de pruebas personalizado para descubrimiento automático de apps
TEST_RUNNER = "apps.core.runner.EduCompraTestRunner"

# Permisos seguros para archivos multimedia creados por Django
FILE_UPLOAD_PERMISSIONS = 0o644
FILE_UPLOAD_DIRECTORY_PERMISSIONS = 0o755
