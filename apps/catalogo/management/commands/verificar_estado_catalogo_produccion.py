"""
Comando de verificación de estado y métricas del catálogo de productos en base de datos.
Permite inspeccionar conteos clave y auditar que exactamente 72 productos curados
estén en estado VALIDADO y publicados.
"""

from django.core.management.base import BaseCommand, CommandError
from apps.catalogo.models import Producto


class Command(BaseCommand):
    help = "Verifica y reporta los conteos y estados del catálogo en la base de datos."

    def add_arguments(self, parser):
        parser.add_argument(
            "--assert-72",
            action="store_true",
            help="Valida que la base contenga exactamente 929 productos, 72 publicados y 72 validados.",
        )

    def handle(self, *args, **options):
        assert_72 = options.get("assert_72", False)

        self.stdout.write("=" * 70)
        self.stdout.write("EDUCOMPRA HUMM — ESTADO DE BASE DE DATOS Y CATÁLOGO")
        self.stdout.write("=" * 70)

        total = Producto.objects.count()
        activos = Producto.objects.filter(activo=True).count()
        validados = Producto.objects.filter(estado_curaduria="VALIDADO").count()
        publicados = Producto.objects.filter(publicado=True).count()
        no_publicados = Producto.objects.filter(publicado=False).count()
        validados_humm = Producto.objects.filter(estado_especificacion_neutral="VALIDADO_HUMM").count()

        self.stdout.write(f"• Total Productos:                          {total}")
        self.stdout.write(f"• Productos Activos:                        {activos}")
        self.stdout.write(f"• Curaduría Pedagógica 'VALIDADO':          {validados}")
        self.stdout.write(f"• Publicados (Catálogo Abierto):            {publicados}")
        self.stdout.write(f"• No Publicados (En Espera/Descartados):    {no_publicados}")
        self.stdout.write(f"• Especificación Neutral 'VALIDADO_HUMM':   {validados_humm}")
        self.stdout.write("=" * 70)

        if assert_72:
            errores = []
            if total != 929:
                errores.append(f"Total productos esperado 929, detectado {total}")
            if validados != 72:
                errores.append(f"Productos en estado VALIDADO esperado 72, detectado {validados}")
            if publicados != 72:
                errores.append(f"Productos publicados esperado 72, detectado {publicados}")
            if no_publicados != 857:
                errores.append(f"Productos no publicados esperado 857, detectado {no_publicados}")
            if validados_humm != 0:
                errores.append(f"Especificaciones VALIDADO_HUMM esperado 0, detectado {validados_humm}")

            if errores:
                for err in errores:
                    self.stdout.write(self.style.ERROR(f"❌ {err}"))
                raise CommandError("La auditoría de estado del catálogo productivo no cumplió los requisitos.")

            self.stdout.write(self.style.SUCCESS("✔ AUDITORÍA EXITOSA: Exactamente 72 productos curados y publicados."))
