import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = "Crea un superusuario administrador de forma idempotente a partir de variables de entorno."

    def handle(self, *args, **options):
        User = get_user_model()
        username = os.getenv("ADMIN_USER", "admin")
        email = os.getenv("ADMIN_EMAIL", "contacto@humm.cl")
        password = os.getenv("ADMIN_PASSWORD")

        if not password:
            self.stdout.write(self.style.WARNING("ADMIN_PASSWORD no está definida. Omitiendo creación de superusuario."))
            return

        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.SUCCESS(f"El usuario '{username}' ya existe. No se realizaron cambios."))
        else:
            User.objects.create_superuser(username=username, email=email, password=password)
            self.stdout.write(self.style.SUCCESS(f"Superusuario '{username}' creado exitosamente."))
