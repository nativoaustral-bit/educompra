"""
Comando de conciliación histórica no destructiva de Establecimientos y Contactos.
Cumple rigurosamente con los Ajustes Obligatorios #5, #6, #7, #8 y #28 de Humm.
- Idempotente.
- Soporta --dry-run (modo predeterminado por seguridad).
- Aplica jerarquía de 3 niveles sin mutilar términos institucionales.
- Conserva intactos los snapshots y textos históricos de SolicitudCotizacion.
- Registra verdaderas fechas históricas de primera y última interacción.
"""

from collections import defaultdict
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone
from apps.cotizaciones.models import SolicitudCotizacion, Establecimiento, Contacto
from apps.core.normalizacion import normalizar_texto_busqueda, normalizar_email, normalizar_rut


class Command(BaseCommand):
    help = (
        "Analiza solicitudes históricas y concilia/vincula entidades Establecimiento y Contacto. "
        "Por defecto ejecuta en modo simulación (--dry-run). Use --aplicar para escribir en BD."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--aplicar",
            action="store_true",
            help="Ejecuta la conciliación definitiva en la base de datos (por defecto es --dry-run).",
        )
        parser.add_argument(
            "--forzar-reconciliar",
            action="store_true",
            help="Reanaliza solicitudes que ya tengan establecimiento_ref o contacto_ref asignado.",
        )

    def handle(self, *args, **options):
        es_dry_run = not options["aplicar"]
        forzar = options["forzar_reconciliar"]

        self.stdout.write("=" * 70)
        self.stdout.write("EDUCOMPRA HUMM — CONCILIACIÓN HISTÓRICA DE ESTABLECIMIENTOS Y CONTACTOS")
        self.stdout.write(f"Modo: {'SIMULACIÓN (DRY-RUN) — CERO ESCRITURAS' if es_dry_run else 'APLICACIÓN PRODUCTIVA DEFINITIVA'}")
        self.stdout.write("=" * 70)

        # Consultar solicitudes en orden cronológico ascendente (más antiguas primero)
        qs = SolicitudCotizacion.objects.all().order_by("created_at")
        if not forzar:
            qs = qs.filter(establecimiento_ref__isnull=True)

        total_solicitudes = qs.count()
        self.stdout.write(f"Solicitudes históricas a procesar: {total_solicitudes}")

        if total_solicitudes == 0:
            self.stdout.write(self.style.SUCCESS("No hay solicitudes pendientes de conciliación."))
            return

        # Estadísticas
        stats = {
            "solicitudes_analizadas": 0,
            "matches_exactos_rut": 0,
            "matches_exactos_nombre_comuna": 0,
            "establecimientos_nuevos": 0,
            "contactos_nuevos": 0,
            "contactos_recurrentes": 0,
            "casos_ambiguos": 0,
            "posibles_duplicados_email": 0,
        }

        # Cache en memoria durante el procesamiento
        establecimientos_por_rut = {}
        establecimientos_por_nombre_comuna = {}
        contactos_por_email = {}

        # Cargar existentes en memoria
        for est in Establecimiento.objects.all():
            if est.rut:
                establecimientos_por_rut[normalizar_rut(est.rut)] = est
            clave = (est.nombre_normalizado, est.comuna.strip().lower())
            establecimientos_por_nombre_comuna[clave] = est

        for con in Contacto.objects.all():
            contactos_por_email[con.email] = con

        solicitudes_a_actualizar = []
        establecimientos_a_crear_o_actualizar = {}
        contactos_a_crear_o_actualizar = {}

        for sol in qs:
            stats["solicitudes_analizadas"] += 1
            nombre_est = sol.establecimiento.strip()
            nombre_norm = normalizar_texto_busqueda(nombre_est)
            comuna = sol.comuna.strip()
            comuna_norm = comuna.lower()
            region = sol.region.strip()
            rut_est = normalizar_rut(sol.rut_institucion)
            tipo_inst = sol.tipo_institucion.strip()
            fecha_solicitud = sol.created_at

            # --- JERARQUÍA DE CONCILIACIÓN DE ESTABLECIMIENTO (Ajuste #5) ---
            est_match = None
            estado_concil = "CONCILIADO"

            # Nivel 1 — Identificador fuerte (RUT institucional)
            if rut_est and rut_est in establecimientos_por_rut:
                est_match = establecimientos_por_rut[rut_est]
                stats["matches_exactos_rut"] += 1

            # Nivel 2 — Coincidencia segura (nombre completo normalizado + comuna) sin mutilar términos
            if not est_match and (nombre_norm, comuna_norm) in establecimientos_por_nombre_comuna:
                est_match = establecimientos_por_nombre_comuna[(nombre_norm, comuna_norm)]
                stats["matches_exactos_nombre_comuna"] += 1

            # Nivel 3 — Caso ambiguo o nuevo
            if not est_match:
                # Comprobar si existe el mismo nombre en distinta comuna (caso de atención)
                coincidencias_otro_lugar = [
                    e for (n, c), e in establecimientos_por_nombre_comuna.items()
                    if n == nombre_norm and c != comuna_norm
                ]
                if coincidencias_otro_lugar:
                    stats["casos_ambiguos"] += 1
                    estado_concil = "PENDIENTE_CONCILIACION"

                # Crear representación en memoria
                est_match = Establecimiento(
                    nombre=nombre_est,
                    nombre_normalizado=nombre_norm,
                    rut=rut_est,
                    tipo_institucion=tipo_inst,
                    comuna=comuna,
                    region=region,
                    estado_conciliacion=estado_concil,
                    primera_interaccion=fecha_solicitud,
                    ultima_interaccion=fecha_solicitud,
                )
                stats["establecimientos_nuevos"] += 1
                if rut_est:
                    establecimientos_por_rut[rut_est] = est_match
                establecimientos_por_nombre_comuna[(nombre_norm, comuna_norm)] = est_match
            else:
                # Actualizar fechas históricas verdaderas (Ajuste #7)
                if not est_match.primera_interaccion or fecha_solicitud < est_match.primera_interaccion:
                    est_match.primera_interaccion = fecha_solicitud
                if not est_match.ultima_interaccion or fecha_solicitud > est_match.ultima_interaccion:
                    est_match.ultima_interaccion = fecha_solicitud
                if rut_est and not est_match.rut:
                    est_match.rut = rut_est

            # --- CONCILIACIÓN DE CONTACTO (Ajustes #7 y #8) ---
            email_docente = normalizar_email(sol.email)
            contacto_match = contactos_por_email.get(email_docente)

            if contacto_match:
                stats["contactos_recurrentes"] += 1
                # Verificar si pertenece a otro colegio (Ajuste #8)
                if contacto_match.establecimiento_principal and contacto_match.establecimiento_principal != est_match:
                    contacto_match.posible_duplicado = True
                    stats["posibles_duplicados_email"] += 1

                if not contacto_match.primera_interaccion or fecha_solicitud < contacto_match.primera_interaccion:
                    contacto_match.primera_interaccion = fecha_solicitud
                if not contacto_match.ultima_interaccion or fecha_solicitud > contacto_match.ultima_interaccion:
                    contacto_match.ultima_interaccion = fecha_solicitud
            else:
                stats["contactos_nuevos"] += 1
                contacto_match = Contacto(
                    establecimiento_principal=est_match,
                    nombre=sol.nombre_solicitante.strip(),
                    cargo=sol.cargo_solicitante.strip(),
                    email=email_docente,
                    telefono=sol.telefono.strip(),
                    primera_interaccion=fecha_solicitud,
                    ultima_interaccion=fecha_solicitud,
                )
                contactos_por_email[email_docente] = contacto_match

            solicitudes_a_actualizar.append((sol, est_match, contacto_match))

        # --- REPORTE DETALLADO (Ajuste #6) ---
        self.stdout.write("\n" + "=" * 70)
        self.stdout.write("INFORME DE CONCILIACIÓN HISTÓRICA")
        self.stdout.write("=" * 70)
        self.stdout.write(f"Solicitudes analizadas:           {stats['solicitudes_analizadas']}")
        self.stdout.write(f"Matches exactos por RUT:         {stats['matches_exactos_rut']}")
        self.stdout.write(f"Matches seguros (Nombre+Comuna):  {stats['matches_exactos_nombre_comuna']}")
        self.stdout.write(f"Establecimientos nuevos a crear:  {stats['establecimientos_nuevos']}")
        self.stdout.write(f"Contactos nuevos a crear:         {stats['contactos_nuevos']}")
        self.stdout.write(f"Contactos recurrentes:            {stats['contactos_recurrentes']}")
        self.stdout.write(f"Posibles duplicados / multi-col:  {stats['posibles_duplicados_email']}")
        self.stdout.write(f"Casos ambiguos (revisión manual): {stats['casos_ambiguos']}")
        self.stdout.write("=" * 70)

        if es_dry_run:
            self.stdout.write(self.style.WARNING(
                "\n[AVISO] Ejecución en modo SIMULACIÓN. Ningún dato fue escrito en la base de datos."
            ))
            self.stdout.write("Para aplicar estos cambios en la base de datos ejecute:\n")
            self.stdout.write("  python manage.py conciliar_establecimientos_historicos --aplicar\n")
            return

        # Aplicación definitiva bajo transacción atómica
        self.stdout.write("\nAplicando conciliación definitiva en base de datos...")
        with transaction.atomic():
            # Guardar establecimientos
            guardados_est = {}
            for clave, est in establecimientos_por_nombre_comuna.items():
                if clave not in guardados_est:
                    est.save()
                    guardados_est[clave] = est

            # Guardar contactos
            guardados_con = {}
            for email, con in contactos_por_email.items():
                if email not in guardados_con:
                    con.save()
                    guardados_con[email] = con

            # Vincular solicitudes
            for sol, est, con in solicitudes_a_actualizar:
                sol.establecimiento_ref = est
                sol.contacto_ref = con
                sol.save(update_fields=["establecimiento_ref", "contacto_ref"])

        self.stdout.write(self.style.SUCCESS("✔ Conciliación histórica aplicada con éxito sin alterar snapshots."))
