from django.apps import AppConfig
from django.db.backends.signals import connection_created


def configure_sqlite_pragmas(sender, connection, **kwargs):
    """
    Configuración de alto rendimiento y concurrencia segura para SQLite en producción:
    - WAL (Write-Ahead Logging): Permite múltiples lectores simultáneos sin bloquear al escritor.
    - synchronous=NORMAL: Rendimiento óptimo manteniendo durabilidad e integridad en caso de fallos.
    - busy_timeout=20000: Espera activa de hasta 20s antes de arrojar un error de bloqueo.
    - foreign_keys=ON: Asegura la integridad referencial de claves foráneas.
    """
    if connection.vendor == "sqlite":
        with connection.cursor() as cursor:
            cursor.execute("PRAGMA journal_mode=WAL;")
            cursor.execute("PRAGMA synchronous=NORMAL;")
            cursor.execute("PRAGMA busy_timeout=20000;")
            cursor.execute("PRAGMA foreign_keys=ON;")


class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.core"
    verbose_name = "Núcleo y Configuración"

    def ready(self):
        connection_created.connect(configure_sqlite_pragmas)
