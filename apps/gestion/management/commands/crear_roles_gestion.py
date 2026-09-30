"""
Comando para crear los grupos y asignar permisos nativos de Django (Ajuste Obligatorio #19 de Humm).
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from apps.gestion.models import RegistroActividad


class Command(BaseCommand):
    help = "Crea los grupos de usuarios y asigna los permisos nativos de Administración EduCompra."

    def handle(self, *args, **options):
        self.stdout.write("Configurando grupos y permisos nativos de Django para /gestion/...")

        # 1. Obtener los permisos del modelo RegistroActividad
        content_type = ContentType.objects.get_for_model(RegistroActividad)
        todos_permisos_gestion = Permission.objects.filter(content_type=content_type)
        permisos_map = {p.codename: p for p in todos_permisos_gestion}

        # 2. Grupo: Administradores EduCompra
        admin_group, created = Group.objects.get_or_create(name="Administradores EduCompra")
        permisos_admin = [
            "can_view_gestion",
            "can_manage_catalogo",
            "can_publish_producto",
            "can_run_importaciones",
            "can_manage_solicitudes",
            "can_manage_cotizaciones",
            "can_manage_establecimientos",
            "can_view_analitica",
            "can_manage_configuracion",
        ]
        admin_group.permissions.clear()
        for codename in permisos_admin:
            if codename in permisos_map:
                admin_group.permissions.add(permisos_map[codename])
        self.stdout.write(self.style.SUCCESS(f"✔ Grupo '{admin_group.name}' configurado ({len(permisos_admin)} permisos)."))

        # 3. Grupo: Comercial EduCompra
        comercial_group, created = Group.objects.get_or_create(name="Comercial EduCompra")
        permisos_comercial = [
            "can_view_gestion",
            "can_manage_solicitudes",
            "can_manage_cotizaciones",
            "can_manage_establecimientos",
        ]
        comercial_group.permissions.clear()
        for codename in permisos_comercial:
            if codename in permisos_map:
                comercial_group.permissions.add(permisos_map[codename])
        self.stdout.write(self.style.SUCCESS(f"✔ Grupo '{comercial_group.name}' configurado ({len(permisos_comercial)} permisos)."))

        self.stdout.write(self.style.SUCCESS("✔ Asignación de roles y permisos completada exitosamente."))
