import os
import sqlite3
from datetime import datetime
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Genera un respaldo atómico y en caliente del archivo SQLite de producción."

    def add_arguments(self, parser):
        parser.add_argument(
            "--dest",
            type=str,
            default=os.getenv("BACKUP_DIR", ""),
            help="Directorio de destino para los respaldos.",
        )
        parser.add_argument(
            "--filename",
            type=str,
            default="",
            help="Nombre específico del archivo de respaldo (opcional).",
        )
        parser.add_argument(
            "--keep",
            type=int,
            default=14,
            help="Número de respaldos históricos a conservar (rotación automática).",
        )

    def handle(self, *args, **options):
        db_conf = settings.DATABASES.get("default", {})
        if db_conf.get("ENGINE") != "django.db.backends.sqlite3":
            raise CommandError("El comando de respaldo está diseñado exclusivamente para SQLite.")

        source_path = Path(db_conf.get("NAME"))
        if not source_path.exists():
            raise CommandError(f"El archivo de base de datos no existe: {source_path}")

        # Determinar directorio de respaldo seguro
        dest_arg = options.get("dest")
        if dest_arg:
            dest_dir = Path(dest_arg)
        elif source_path.parent.name == "data":
            # Si la db está en /apps/educompra/data/db.sqlite3, respaldar en /apps/educompra/backups/
            dest_dir = source_path.parent.parent / "backups"
        else:
            dest_dir = settings.BASE_DIR / "backups"

        dest_dir.mkdir(parents=True, exist_ok=True)
        os.chmod(dest_dir, 0o700)

        custom_name = options.get("filename")
        if custom_name:
            backup_filename = custom_name if custom_name.endswith(".sqlite3") else f"{custom_name}.sqlite3"
        else:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_filename = f"educompra_{timestamp}.sqlite3"
        dest_path = dest_dir / backup_filename

        self.stdout.write(f"Iniciando respaldo en caliente de {source_path.name}...")

        # Utilizar API de Backup Online de SQLite (no bloquea lectores ni escritores en modo WAL)
        try:
            source_conn = sqlite3.connect(str(source_path))
            dest_conn = sqlite3.connect(str(dest_path))
            with dest_conn:
                source_conn.backup(dest_conn, pages=100)
            dest_conn.close()
            source_conn.close()

            # Verificar apertura e integridad del respaldo generado
            check_conn = sqlite3.connect(str(dest_path))
            cur = check_conn.cursor()
            cur.execute("PRAGMA integrity_check;")
            integrity_result = cur.fetchone()[0]
            check_conn.close()
            if integrity_result != "ok":
                dest_path.unlink()
                raise CommandError(f"Fallo en la prueba de integridad del respaldo: {integrity_result}")

            # Permisos restrictivos sobre el archivo de respaldo
            os.chmod(dest_path, 0o600)

            size_kb = dest_path.stat().st_size / 1024
            self.stdout.write(
                self.style.SUCCESS(
                    f"✔ Respaldo completado e integridad verificada: {dest_path.name} ({size_kb:.1f} KB)"
                )
            )
        except Exception as e:
            if dest_path.exists():
                dest_path.unlink()
            raise CommandError(f"Error generando respaldo SQLite: {e}")

        # Rotación automática de respaldos
        keep_count = options.get("keep", 14)
        if keep_count > 0:
            existing_backups = sorted(
                dest_dir.glob("educompra_*.sqlite3"),
                key=lambda p: p.stat().st_mtime,
                reverse=True,
            )
            if len(existing_backups) > keep_count:
                to_remove = existing_backups[keep_count:]
                for old_backup in to_remove:
                    try:
                        old_backup.unlink()
                        self.stdout.write(f"Rotación: eliminado respaldo antiguo {old_backup.name}")
                    except OSError:
                        pass
