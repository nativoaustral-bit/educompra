"""
Comando de activación pública controlada del catálogo inicial de EduCompra Humm (Fase 4B).
Publica exclusivamente los 72 productos curados y validados pedagógicamente.
Soporta --dry-run para validación previa obligatoria sin escrituras.
"""

from decimal import Decimal
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from apps.catalogo.models import Producto


class Command(BaseCommand):
    help = "Activa públicamente (publicado=True) los 72 productos curados y validados de EduCompra."

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Simula el proceso de activación y verifica los 7 criterios sin modificar la base de datos.",
        )
        parser.add_argument(
            "--expected-count",
            type=int,
            default=72,
            help="Cantidad exacta esperada de productos elegibles (por defecto: 72).",
        )

    def handle(self, *args, **options):
        dry_run = options.get("dry_run", False)
        expected_count = options.get("expected_count", 72)

        self.stdout.write("=" * 70)
        self.stdout.write("EDUCOMPRA HUMM — ACTIVACIÓN PÚBLICA CONTROLADA (FASE 4B)")
        self.stdout.write(f"Modo: {'SIMULACIÓN (--dry-run)' if dry_run else 'ACTIVACIÓN PRODUCTIVA REAL'}")
        self.stdout.write("=" * 70)

        # 1. Recuperar candidatos con curaduría validada
        candidatos = Producto.objects.filter(
            activo=True,
            estado_curaduria="VALIDADO"
        ).select_related("categoria").prefetch_related("imagenes").order_by("categoria__orden", "nombre_comercial")

        total_candidatos = candidatos.count()
        self.stdout.write(f"Total productos en estado VALIDADO y activo: {total_candidatos}")

        elegibles = []
        inconsistencias = []

        # 2. Comprobar los 7 requisitos para cada producto
        for p in candidatos:
            fallos = []

            if not p.activo:
                fallos.append("activo != True")
            if p.estado_curaduria != "VALIDADO":
                fallos.append("estado_curaduria != VALIDADO")
            if not p.nombre_comercial or not p.nombre_comercial.strip():
                fallos.append("nombre_comercial vacío")
            if not p.categoria or not p.categoria.activa or p.categoria.slug == "sin-clasificar":
                fallos.append(f"categoría inválida ({p.categoria.nombre if p.categoria else 'None'})")
            desc_educativa = (p.descripcion_educativa or p.descripcion_corta or "").strip()
            if not desc_educativa:
                fallos.append("descripcion_educativa pedagógica vacía")
            if not p.imagenes.exists():
                fallos.append("sin imagen asociada")
            if not p.precio_sugerido_total_clp or p.precio_sugerido_total_clp <= Decimal("0"):
                fallos.append(f"precio referencial no calculable ({p.precio_sugerido_total_clp})")

            if fallos:
                inconsistencias.append((p.sku_proveedor, p.nombre_comercial, fallos))
            else:
                elegibles.append(p)

        cant_elegibles = len(elegibles)
        self.stdout.write(f"Productos que cumplen los 7 criterios de publicación: {cant_elegibles}")

        if inconsistencias:
            self.stdout.write(self.style.ERROR(f"\nSe encontraron {len(inconsistencias)} productos con inconsistencias:"))
            for sku, nom, fallos in inconsistencias:
                self.stdout.write(f"  • [{sku}] {nom}: {', '.join(fallos)}")

        # 3. Validación estricta del total esperado (exactamente 72 por defecto)
        if cant_elegibles != expected_count:
            mensaje_error = (
                f"DETENCIÓN OBLIGATORIA: Se esperaban exactamente {expected_count} productos elegibles, "
                f"pero se detectaron {cant_elegibles}. Operación cancelada para proteger producción."
            )
            self.stdout.write(self.style.ERROR(f"\n{mensaje_error}"))
            raise CommandError(mensaje_error)

        self.stdout.write(self.style.SUCCESS(f"\n✔ Verificación exitosa: Exactamente {expected_count} productos elegibles validados."))

        if dry_run:
            self.stdout.write(self.style.WARNING("\n[DRY-RUN] Simulación completada con éxito. Ningún cambio aplicado a la base de datos."))
            self.stdout.write("Para activar formalmente en producción ejecute sin --dry-run:")
            self.stdout.write("  python manage.py activar_catalogo_publico_fase_4\n")
            return

        # 4. Activación real bajo transacción atómica
        self.stdout.write("\nIniciando activación de los 72 productos en base de datos...")
        with transaction.atomic():
            ids_elegibles = [p.id for p in elegibles]
            actualizados = Producto.objects.filter(id__in=ids_elegibles).update(publicado=True)

        # 5. Auditoría post-activación
        total_maestro = Producto.objects.count()
        total_publicados = Producto.objects.filter(publicado=True).count()
        total_no_publicados = Producto.objects.filter(publicado=False).count()
        total_validado_humm = Producto.objects.filter(estado_especificacion_neutral="VALIDADO_HUMM").count()

        self.stdout.write("=" * 70)
        self.stdout.write("RESULTADO DE LA ACTIVACIÓN PÚBLICA (FASE 4B):")
        self.stdout.write(f"  • Productos activados en este proceso: {actualizados}")
        self.stdout.write(f"  • Total productos publicados en EduCompra: {total_publicados}")
        self.stdout.write(f"  • Total productos ocultos (no publicados): {total_no_publicados}")
        self.stdout.write(f"  • Total productos en catálogo maestro: {total_maestro}")
        self.stdout.write(f"  • Especificaciones 'VALIDADO_HUMM': {total_validado_humm} (invariable)")
        self.stdout.write("=" * 70)

        # Comprobar invariantes exigidas en producción (esperados 72)
        if expected_count == 72:
            if total_publicados != 72 or total_no_publicados != 857 or total_maestro != 929:
                raise CommandError("ALERTA CRÍTICA: Los recuentos post-activación difieren de lo esperado (72 / 857 / 929).")
        elif total_publicados != expected_count:
            raise CommandError(f"ALERTA: Se esperaban {expected_count} publicados, hay {total_publicados}.")

        self.stdout.write(self.style.SUCCESS("\n✔ FASE 4B ACTIVADA: El catálogo de 72 productos está disponible públicamente."))
