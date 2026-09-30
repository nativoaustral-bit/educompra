"""
Pruebas automatizadas de la Plataforma de Administración EduCompra Humm (/gestion/)
Fase 5A — Verificación de los Ajustes Obligatorios de Humm.
"""

from decimal import Decimal
from io import StringIO
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management import call_command
from django.test import TestCase, Client
from django.urls import reverse

from apps.catalogo.models import Producto, Categoria, Proveedor, ProductoImagen
from apps.catalogo.services_publicacion import ProductoPublicationService
from apps.core.models import ConfiguracionPricing
from apps.core.normalizacion import (
    normalizar_texto_busqueda,
    normalizar_email,
    normalizar_rut,
    generar_session_hash,
)
from apps.cotizaciones.models import SolicitudCotizacion, SolicitudItem, Establecimiento, Contacto
from apps.gestion.models import EventoUso, RegistroActividad
from apps.gestion.services_telemetria import TelemetriaService


User = get_user_model()


class GestionFase5ABaseTestCase(TestCase):
    """Configuración base con usuarios, roles y modelos elementales."""

    def setUp(self):
        # Crear roles
        call_command("crear_roles_gestion")

        # Configuración de Pricing
        self.config_pricing = ConfiguracionPricing.get_solo()
        self.config_pricing.tipo_cambio_usd_clp = Decimal("950.00")
        self.config_pricing.recargo_general_porcentaje = Decimal("40.00")
        self.config_pricing.factor_internacion_flete_porcentaje = Decimal("15.00")
        self.config_pricing.iva_porcentaje = Decimal("19.00")
        self.config_pricing.save()

        # Superusuario
        self.superuser = User.objects.create_superuser(
            username="admin_super",
            email="super@humm.cl",
            password="SuperPassword123!",
            first_name="Super",
            last_name="Admin"
        )

        # Usuario Administrador EduCompra
        self.admin_user = User.objects.create_user(
            username="admin_educompra",
            email="admin@humm.cl",
            password="AdminPassword123!",
            first_name="Admin",
            last_name="Humm",
            is_staff=True
        )
        grupo_admin = Group.objects.get(name="Administradores EduCompra")
        self.admin_user.groups.add(grupo_admin)

        # Usuario Comercial EduCompra
        self.comercial_user = User.objects.create_user(
            username="comercial_educompra",
            email="comercial@humm.cl",
            password="ComercialPassword123!",
            first_name="Comercial",
            last_name="Humm",
            is_staff=True
        )
        grupo_comercial = Group.objects.get(name="Comercial EduCompra")
        self.comercial_user.groups.add(grupo_comercial)

        # Usuario sin permisos
        self.regular_user = User.objects.create_user(
            username="regular_user",
            email="regular@humm.cl",
            password="RegularPassword123!",
            first_name="Regular",
            last_name="User"
        )

        # Datos de prueba para Catálogo
        self.proveedor = Proveedor.objects.create(
            nombre="Keyestudio Oficial",
            codigo="KEY",
            moneda_origen="USD",
            activo=True
        )
        self.categoria = Categoria.objects.create(
            nombre="Robótica Educativa",
            slug="robotica-educativa",
            activa=True,
            orden=1
        )


class AutenticacionYPermisosTests(GestionFase5ABaseTestCase):
    """Verifica acceso y control de permisos nativos Django (Ajuste #19)."""

    def test_acceso_anonimo_redirige_a_login(self):
        client = Client()
        response = client.get(reverse("gestion:dashboard"))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("gestion:login"), response.url)

    def test_superuser_acceso_total(self):
        client = Client()
        client.force_login(self.superuser)
        response = client.get(reverse("gestion:dashboard"))
        self.assertEqual(response.status_code, 200)

        response_config = client.get(reverse("gestion:configuracion"))
        self.assertEqual(response_config.status_code, 200)

    def test_administrador_educompra_acceso_completo(self):
        client = Client()
        client.force_login(self.admin_user)
        response = client.get(reverse("gestion:dashboard"))
        self.assertEqual(response.status_code, 200)

        response_prod = client.get(reverse("gestion:productos_lista"))
        self.assertEqual(response_prod.status_code, 200)

    def test_comercial_restringido_de_configuracion_pricing(self):
        client = Client()
        client.force_login(self.comercial_user)

        # Puede ver solicitudes y dashboard
        resp_sol = client.get(reverse("gestion:solicitudes_lista"))
        self.assertEqual(resp_sol.status_code, 200)

        # No tiene permiso para configurar pricing (redirige con mensaje a dashboard)
        resp_conf = client.get(reverse("gestion:configuracion"))
        self.assertEqual(resp_conf.status_code, 302)
        self.assertEqual(resp_conf.url, reverse("gestion:dashboard"))


class PublicacionControladaTests(GestionFase5ABaseTestCase):
    """Verifica publicación centralizada y despublicación (Ajustes #13 y #14)."""

    def test_producto_nuevo_creado_en_borrador_no_publicado(self):
        prod = Producto.objects.create(
            sku_humm="HUMM-TEST-001",
            sku_proveedor="KS0001",
            nombre_comercial="Placa de Prueba",
            proveedor=self.proveedor,
            categoria=self.categoria,
            costo_proveedor_usd=Decimal("10.00"),
            publicado=False,
            estado_curaduria="SIN_REVISAR"
        )
        self.assertFalse(prod.publicado)
        self.assertEqual(prod.estado_curaduria, "SIN_REVISAR")

    def test_publicacion_falla_si_no_cumple_8_criterios(self):
        prod = Producto.objects.create(
            sku_humm="HUMM-TEST-002",
            sku_proveedor="KS0002",
            nombre_comercial="Robot Incompleto",
            proveedor=self.proveedor,
            categoria=self.categoria,
            costo_proveedor_usd=Decimal("15.00"),
            publicado=False,
            estado_curaduria="SIN_REVISAR"  # No validado
        )

        errores = ProductoPublicationService.validar_para_publicacion(prod)
        self.assertTrue(len(errores) > 0)

        with self.assertRaises(ValidationError):
            ProductoPublicationService.publicar(prod, usuario=self.admin_user)

    def test_publicacion_exitosa_cuando_cumple_criterios_y_registra_auditoria(self):
        prod = Producto.objects.create(
            sku_humm="HUMM-TEST-003",
            sku_proveedor="KS0003",
            nombre_comercial="Kit de Sensores Completo",
            proveedor=self.proveedor,
            categoria=self.categoria,
            costo_proveedor_usd=Decimal("20.00"),
            descripcion_educativa="Excelente kit para aprender electrónica.",
            unidad_compra="kit",
            activo=True,
            estado_curaduria="VALIDADO",
            publicado=False
        )

        # Añadir imagen principal válida
        dummy_img = SimpleUploadedFile("sensor.jpg", b"dummy image content", content_type="image/jpeg")
        ProductoImagen.objects.create(producto=prod, archivo=dummy_img, es_principal=True)

        # Publicar
        exito = ProductoPublicationService.publicar(prod, usuario=self.admin_user)
        self.assertTrue(exito)
        prod.refresh_from_db()
        self.assertTrue(prod.publicado)

        # Verificar auditoría
        actividad = RegistroActividad.objects.filter(objeto_id=str(prod.id), accion="PUBLICAR_PRODUCTO").first()
        self.assertIsNotNone(actividad)
        self.assertEqual(actividad.usuario, self.admin_user)

    def test_despublicar_no_elimina_producto_y_registra_auditoria(self):
        prod = Producto.objects.create(
            sku_humm="HUMM-TEST-004",
            sku_proveedor="KS0004",
            nombre_comercial="Kit Despublicable",
            proveedor=self.proveedor,
            categoria=self.categoria,
            costo_proveedor_usd=Decimal("25.00"),
            publicado=True
        )

        ProductoPublicationService.despublicar(prod, usuario=self.admin_user)
        prod.refresh_from_db()
        self.assertFalse(prod.publicado)
        self.assertTrue(Producto.objects.filter(id=prod.id).exists())

        # Verificar auditoría
        actividad = RegistroActividad.objects.filter(objeto_id=str(prod.id), accion="DESPUBLICAR_PRODUCTO").first()
        self.assertIsNotNone(actividad)


class PreciosDerivadosYPricingTests(GestionFase5ABaseTestCase):
    """Verifica precios derivados inalterables y recálculo con previsualización (Ajustes #15 y #16)."""

    def test_precios_sugeridos_son_estrictamente_derivados(self):
        prod = Producto(
            sku_humm="HUMM-PRICE-01",
            sku_proveedor="KS010",
            nombre_comercial="Sensor Ultrasónico",
            proveedor=self.proveedor,
            categoria=self.categoria,
            costo_proveedor_usd=Decimal("10.00")
        )
        prod.save()

        # TC=950, Flete=15% -> Costo Chile = 10 * 950 * 1.15 = 10,925
        # Recargo=40% -> Neto = 10,925 * 1.40 = 15,295
        # IVA=19% -> Total = 15,295 * 1.19 = 18,201.05 -> redondeado
        self.assertEqual(prod.costo_puesto_chile_clp, Decimal("10925"))
        self.assertEqual(prod.precio_sugerido_neto_clp, Decimal("15295"))
        self.assertAlmostEqual(float(prod.precio_sugerido_total_clp), 18201, delta=2)

    def test_previsualizacion_de_impacto_no_modifica_base_de_datos(self):
        prod = Producto.objects.create(
            sku_humm="HUMM-SIM-01",
            sku_proveedor="KSSIM",
            nombre_comercial="Producto Simulación",
            proveedor=self.proveedor,
            categoria=self.categoria,
            costo_proveedor_usd=Decimal("10.00"),
            publicado=True,
            activo=True
        )
        precio_original = prod.precio_sugerido_total_clp

        # Modificamos config en memoria para simular
        self.config_pricing.tipo_cambio_usd_clp = Decimal("1000.00")
        self.config_pricing.save()

        client = Client()
        client.force_login(self.admin_user)
        response = client.post(
            reverse("gestion:configuracion"),
            {"accion": "previsualizar_impacto", "alcance": "publicos"}
        )
        self.assertEqual(response.status_code, 200)

        # El producto en la BD NO debe haber cambiado todavía
        prod.refresh_from_db()
        self.assertEqual(prod.precio_sugerido_total_clp, precio_original)

    def test_confirmar_recalculo_actualiza_precios_y_registra_auditoria(self):
        prod = Producto.objects.create(
            sku_humm="HUMM-REC-01",
            sku_proveedor="KSREC",
            nombre_comercial="Producto a Recalcular",
            proveedor=self.proveedor,
            categoria=self.categoria,
            costo_proveedor_usd=Decimal("10.00"),
            publicado=True,
            activo=True
        )

        # Aumentamos tipo de cambio a $1000
        self.config_pricing.tipo_cambio_usd_clp = Decimal("1000.00")
        self.config_pricing.save()

        client = Client()
        client.force_login(self.admin_user)
        response = client.post(
            reverse("gestion:configuracion"),
            {"accion": "confirmar_recalculo", "alcance": "publicos"}
        )
        self.assertEqual(response.status_code, 302)

        prod.refresh_from_db()
        # Nuevo costo Chile: 10 * 1000 * 1.15 = 11,500
        self.assertEqual(prod.costo_puesto_chile_clp, Decimal("11500"))

        # Registro en auditoría
        actividad = RegistroActividad.objects.filter(accion="RECALCULAR_PRECIOS_MASIVO").first()
        self.assertIsNotNone(actividad)


class TelemetriaYPrivacidadTests(GestionFase5ABaseTestCase):
    """Verifica sesión seudónima, whitelist de metadatos y demanda no cubierta (Ajustes #1, #2, #3, #4 y #24)."""

    def test_session_hash_irreversible_no_almacena_session_key_real(self):
        session_key_real = "fake_django_session_key_secret_12345"
        hash_1 = generar_session_hash(session_key_real)
        hash_2 = generar_session_hash(session_key_real)

        self.assertEqual(len(hash_1), 64)
        self.assertEqual(hash_1, hash_2)
        self.assertNotIn(session_key_real, hash_1)

    def test_analytics_hmac_key_independiente_y_ausencia_almacenamiento_session_key(self):
        """
        Demuestra conforme al Ajuste Final #1 de Humm:
        - mismo secret + misma session → mismo hash;
        - secret distinto → hash distinto;
        - session_key real nunca se almacena en BD ni en modelo.
        """
        session_key = "fake_django_session_key_secret_998877"
        secret_a = "analytics-independent-key-AAAAA"
        secret_b = "analytics-independent-key-BBBBB"

        hash_a1 = generar_session_hash(session_key, hmac_key=secret_a)
        hash_a2 = generar_session_hash(session_key, hmac_key=secret_a)
        hash_b = generar_session_hash(session_key, hmac_key=secret_b)

        # 1. Mismo secret + misma session → mismo hash de 64 caracteres
        self.assertEqual(hash_a1, hash_a2)
        self.assertEqual(len(hash_a1), 64)

        # 2. Secret distinto → hash distinto
        self.assertNotEqual(hash_a1, hash_b)

        # 3. Independencia de SECRET_KEY mediante override de settings
        with self.settings(ANALYTICS_HMAC_KEY="custom-analytics-key", SECRET_KEY="django-core-secret"):
            hash_setting = generar_session_hash(session_key)
            self.assertEqual(len(hash_setting), 64)
            # Debe coincidir con la clave analítica independiente
            self.assertEqual(hash_setting, generar_session_hash(session_key, hmac_key="custom-analytics-key"))
            # No debe coincidir si se calculara con SECRET_KEY
            self.assertNotEqual(hash_setting, generar_session_hash(session_key, hmac_key="django-core-secret"))

        # 4. Verificar que session_key NO existe como campo en el modelo EventoUso ni se almacena
        campos = [f.name for f in EventoUso._meta.get_fields()]
        self.assertNotIn("session_key", campos)
        self.assertIn("session_hash", campos)

        evento = EventoUso.objects.create(
            tipo_evento="VISITA",
            session_hash=hash_a1,
            metadata={}
        )
        evento.refresh_from_db()
        self.assertNotIn(session_key, evento.session_hash)
        self.assertFalse(hasattr(evento, "session_key"))


    def test_metadatos_controlados_por_whitelist_excluyen_datos_sensibles(self):
        evento = EventoUso(
            tipo_evento="VISITA",
            session_hash=generar_session_hash("test_session"),
            metadata={
                "filter_category": "robotica-educativa",
                "product_sku": "HUMM-TEST",
                "email": "sensible@colegio.cl",  # NO PERMITIDO
                "rut": "12.345.678-9",            # NO PERMITIDO
                "contraseña": "secreto"           # NO PERMITIDO
            }
        )
        evento.save()

        self.assertIn("filter_category", evento.metadata)
        self.assertIn("product_sku", evento.metadata)
        self.assertNotIn("email", evento.metadata)
        self.assertNotIn("rut", evento.metadata)
        self.assertNotIn("contraseña", evento.metadata)

    def test_demanda_no_cubierta_captura_busquedas_con_cero_resultados(self):
        client = Client()
        # Generar búsqueda con término inexistente
        response = client.get(reverse("catalogo:lista"), {"q": "dron submarino con camara"})
        self.assertEqual(response.status_code, 200)

        # Debe existir un evento BUSQUEDA con 0 resultados
        termino_norm = normalizar_texto_busqueda("dron submarino con camara")
        evento = EventoUso.objects.filter(
            tipo_evento="BUSQUEDA",
            termino_busqueda_normalizado=termino_norm
        ).first()

        self.assertIsNotNone(evento)
        self.assertEqual(evento.resultados_busqueda, 0)


class ConciliacionYDatosPruebaTests(GestionFase5ABaseTestCase):
    """Verifica jerarquía de conciliación de establecimientos y exclusión de datos de prueba (Ajustes #5, #6, #7, #8, #9 y #29)."""

    def test_conciliacion_nivel_1_identificador_fuerte_rut(self):
        # Establecimiento existente con RUT institucional
        est = Establecimiento.objects.create(
            nombre="Liceo Bicentenario San Jose",
            nombre_normalizado=normalizar_texto_busqueda("Liceo Bicentenario San Jose"),
            comuna="Temuco",
            region="Araucanía",
            rut="65.123.456-7",
            estado_conciliacion="CONCILIADO_AUTOMATICO"
        )

        # Nueva solicitud con diferente nombre informal pero mismo RUT
        sol = SolicitudCotizacion.objects.create(
            establecimiento="Liceo San Jose",
            comuna="Temuco",
            region="Araucanía",
            rut_institucion="65123456-7",
            nombre_solicitante="Prof. Pedro Gomez",
            email="pedro@sanjose.cl",
            total_referencial_estimado=Decimal("500000")
        )

        # Ejecutar conciliación
        call_command("conciliar_establecimientos_historicos", aplicar=True)
        sol.refresh_from_db()
        self.assertEqual(sol.establecimiento_ref, est)

    def test_conciliacion_nivel_2_nombre_completo_sin_eliminar_palabras_institucionales(self):
        # Establecimiento existente
        est = Establecimiento.objects.create(
            nombre="Colegio San Ignacio",
            nombre_normalizado=normalizar_texto_busqueda("Colegio San Ignacio"),
            comuna="Providencia",
            region="Metropolitana",
            estado_conciliacion="CONCILIADO_AUTOMATICO"
        )

        # Solicitud con match exacto de nombre normalizado + comuna
        sol = SolicitudCotizacion.objects.create(
            establecimiento="Colegio San Ignacio",
            comuna="Providencia",
            region="Metropolitana",
            nombre_solicitante="Juan Perez",
            email="jperez@sanignacio.cl",
            total_referencial_estimado=Decimal("150000")
        )

        call_command("conciliar_establecimientos_historicos", aplicar=True)
        sol.refresh_from_db()
        self.assertEqual(sol.establecimiento_ref, est)

    def test_solicitudes_de_prueba_excluidas_de_metricas_comerciales(self):
        # Solicitud real
        SolicitudCotizacion.objects.create(
            establecimiento="Colegio Real",
            nombre_solicitante="Maria Gonzalez",
            email="mgonzalez@real.cl",
            total_referencial_estimado=Decimal("1000000"),
            es_prueba=False
        )

        # Solicitud de prueba
        SolicitudCotizacion.objects.create(
            establecimiento="Colegio Test Humm",
            nombre_solicitante="Tester Humm",
            email="test@humm.cl",
            total_referencial_estimado=Decimal("9999999"),
            es_prueba=True
        )

        client = Client()
        client.force_login(self.admin_user)
        response = client.get(reverse("gestion:dashboard"))
        self.assertEqual(response.status_code, 200)

        # Las métricas del dashboard deben contabilizar solo la solicitud real
        self.assertEqual(response.context["solicitudes_recibidas"], 1)
        self.assertEqual(response.context["monto_solicitado"], Decimal("1000000"))


class ExportacionesCSVTests(GestionFase5ABaseTestCase):
    """Verifica exportación limpia en CSV para auditoría y backup administrativo (Ajuste #32)."""

    def test_exportar_productos_csv(self):
        Producto.objects.create(
            sku_humm="HUMM-CSV-01",
            sku_proveedor="KSCSV",
            nombre_comercial="Producto para CSV",
            proveedor=self.proveedor,
            categoria=self.categoria,
            costo_proveedor_usd=Decimal("12.50")
        )

        client = Client()
        client.force_login(self.admin_user)
        response = client.get(reverse("gestion:exportar_csv", kwargs={"recurso": "productos"}))
        self.assertEqual(response.status_code, 200)
        self.assertIn("text/csv", response["Content-Type"])
        self.assertIn("HUMM-CSV-01", response.content.decode("utf-8-sig"))
        self.assertIn("Producto para CSV", response.content.decode("utf-8-sig"))

    def test_exportar_solicitudes_csv(self):
        SolicitudCotizacion.objects.create(
            establecimiento="Liceo CSV Test",
            nombre_solicitante="Docente CSV",
            email="docente@csv.cl",
            total_referencial_estimado=Decimal("450000")
        )

        client = Client()
        client.force_login(self.admin_user)
        response = client.get(reverse("gestion:exportar_csv", kwargs={"recurso": "solicitudes"}))
        self.assertEqual(response.status_code, 200)
        self.assertIn("Liceo CSV Test", response.content.decode("utf-8-sig"))
