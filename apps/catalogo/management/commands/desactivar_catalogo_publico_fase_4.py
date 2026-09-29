"""
Comando de rollback de emergencia para EduCompra Humm.
Desactiva públicamente (publicado=False) los productos de EduCompra,
restituyendo el estado de catálogo privado sin eliminar ni modificar datos de curaduría.
"""

from django.core.management.base import BaseCommand
from django.db import transaction
from apps.catalogo.models import Producto


class Command(BaseCommand):
    help = "Rollback de emergencia: desactiva públicamente el catálogo (publicado=False) protegiendo los datos."

    def handle(self, *args, **options):
        self.stdout.write("=" * 70)
        self.stdout.write("EDUCOMPRA HUMM — DESACTIVACIÓN DE EMERGENCIA (ROLLBACK CATÁLOGO)")
        self.stdout.write("=" * 70)

        with transaction.atomic():
            desactivados = Producto.objects.filter(publicado=True).update(publicado=False)

        total_maestro = Producto.objects.count()
        total_publicados = Producto.objects.filter(publicado=True).count()
        total_no_publicados = Producto.objects.filter(publicado=False).count()

        self.stdout.write(f"Productos desactivados: {desactivados}")
        self.stdout.write(f"Total publicados ahora: {total_publicados}")
        self.stdout.write(f"Total no publicados: {total_no_publicados}")
        self.stdout.write(f"Total en catálogo maestro: {total_maestro}")

        if total_publicados == 0 and total_no_publicados == 929:
            self.stdout.write(self.style.SUCCESS("\n✔ ROLLBACK EXITOSO: El catálogo público ha quedado completamente cerrado y protegido."))
        else:
            self.stdout.write(self.style.WARNING(f"\nAlerta: Se detectaron {total_publicados} productos aún publicados."))
