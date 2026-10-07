import sys
import io
from decimal import Decimal
from unittest.mock import patch
from django.test import TestCase, Client, override_settings
from django.urls import reverse
from apps.catalogo.models import Proveedor, Categoria, Producto
from apps.cotizaciones.models import SolicitudCotizacion, SolicitudItem, Contacto, Establecimiento
from apps.cotizaciones.services import SESSION_CART_KEY


class RegresionEnvioSolicitudTestCase(TestCase):
    """
    Tests de regresión end-to-end para el flujo de envío de solicitud de cotización:
    POST /solicitar-cotizacion/
    
    Cubre:
    1. contacto nuevo
    2. contacto ya existente
    3. establecimiento nuevo
    4. establecimiento ya existente
    5. RUT vacío
    6. RUT informado
    7. campos opcionales vacíos
    8. campos opcionales completos
    9. envío de email fallido (resiliencia: commit BD intacto, sin 500)
    10. redirect y render de confirmación (HTTP 302 -> HTTP 200)
    """

    def setUp(self):
        self.client = Client()
        self.proveedor = Proveedor.objects.create(nombre="Keyestudio", codigo="KEY")
        self.categoria = Categoria.objects.create(nombre="Robótica", slug="robotica")

        self.producto = Producto.objects.create(
            sku_humm="HUMM-KEY-001",
            sku_proveedor="KS0001",
            proveedor=self.proveedor,
            categoria=self.categoria,
            nombre_comercial="Kit de Inicio Robot",
            unidad_compra="unidad",
            estado_curaduria="VALIDADO",
            publicado=True,
            activo=True,
            costo_proveedor_usd=Decimal("20.00"),
            slug="ks0001-kit-inicio-robot",
        )
        self.producto.calcular_precios_sugeridos()
        self.producto.save()

    def _preparar_canasta_y_token(self, token="token-test-123"):
        session = self.client.session
        session[SESSION_CART_KEY] = {str(self.producto.id): {"cantidad": 2}}
        session["form_idempotency_token"] = token
        session.save()

    def test_solicitud_contacto_nuevo_establecimiento_nuevo_rut_vacio_opcionales_vacios(self):
        """
        Escenario 1: Contacto nuevo, establecimiento nuevo, RUT vacío,
        campos opcionales vacíos.
        Comprueba: POST -> 302, Solicitud guardada, Items guardados,
        Contacto creado, Establecimiento creado, GET confirmación -> 200.
        """
        token = "token-nuevo-1"
        self._preparar_canasta_y_token(token)

        form_data = {
            "idempotency_token": token,
            "sitio_web_docente": "",  # honeypot vacío
            "nombre_solicitante": "Profesor Nuevo",
            "email": "profesor.nuevo@escuelanueva.cl",
            "telefono": "+56 9 1111 2222",
            "establecimiento": "Escuela Básica Rural Los Coihues",
            "tipo_institucion": "",  # opcional vacío
            "cargo_solicitante": "",  # opcional vacío
            "region": "Los Lagos",
            "comuna": "Frutillar",
            "institucion_responsable_compra": "",  # opcional vacío
            "rut_institucion": "",  # RUT vacío
            "nombre_encargado_compras": "",  # opcional vacío
            "email_encargado_compras": "",  # opcional vacío
            "proyecto_educativo": "",  # opcional vacío
            "fecha_requerida_aproximada": "",  # opcional vacío
            "observaciones": "",  # opcional vacío
        }

        resp = self.client.post(reverse("solicitar_cotizacion"), form_data)
        self.assertEqual(resp.status_code, 302)

        # 1. Solicitud creada
        self.assertEqual(SolicitudCotizacion.objects.count(), 1)
        solicitud = SolicitudCotizacion.objects.first()
        self.assertEqual(solicitud.nombre_solicitante, "Profesor Nuevo")
        self.assertEqual(solicitud.email, "profesor.nuevo@escuelanueva.cl")
        self.assertEqual(solicitud.rut_institucion, "")

        # 2. SolicitudItem creados con snapshots
        self.assertEqual(solicitud.items.count(), 1)
        item = solicitud.items.first()
        self.assertEqual(item.producto, self.producto)
        self.assertEqual(item.cantidad, 2)
        self.assertEqual(item.nombre_comercial_snapshot, "Kit de Inicio Robot")
        self.assertGreater(solicitud.total_referencial_estimado, Decimal("0"))

        # 3. Establecimiento nuevo creado y vinculado
        self.assertIsNotNone(solicitud.establecimiento_ref)
        est = solicitud.establecimiento_ref
        self.assertEqual(est.nombre, "Escuela Básica Rural Los Coihues")
        self.assertEqual(est.comuna, "Frutillar")
        self.assertEqual(est.region, "Los Lagos")

        # 4. Contacto nuevo creado y vinculado
        self.assertIsNotNone(solicitud.contacto_ref)
        contacto = solicitud.contacto_ref
        self.assertEqual(contacto.email, "profesor.nuevo@escuelanueva.cl")
        self.assertEqual(contacto.nombre, "Profesor Nuevo")
        self.assertEqual(contacto.establecimiento_principal, est)

        # 5. GET confirmación -> 200
        confirm_url = reverse("solicitud_recibida", kwargs={"token": solicitud.token})
        confirm_resp = self.client.get(confirm_url)
        self.assertEqual(confirm_resp.status_code, 200)
        self.assertContains(confirm_resp, solicitud.codigo_seguimiento)
        self.assertContains(confirm_resp, "Kit de Inicio Robot")

    def test_solicitud_contacto_existente_establecimiento_existente_rut_informado_opcionales_llenos(self):
        """
        Escenario 2: Contacto ya existente, establecimiento ya existente,
        RUT informado, campos opcionales completamente llenos.
        Comprueba reutilización y actualización correcta de entidades.
        """
        # Precrear establecimiento con RUT
        est_existente = Establecimiento.objects.create(
            nombre="Colegio San Francisco",
            comuna="Santiago",
            region="Metropolitana de Santiago",
            rut="76.543.210-K",
            tipo_institucion="PARTICULAR_SUBVENCIONADO",
        )
        # Precrear contacto
        contacto_existente = Contacto.objects.create(
            nombre="María Docente",
            email="maria.docente@sanfrancisco.cl",
            telefono="+56 9 8888 7777",
            cargo="Jefa UTP",
            establecimiento_principal=est_existente,
        )

        token = "token-existente-2"
        self._preparar_canasta_y_token(token)

        form_data = {
            "idempotency_token": token,
            "sitio_web_docente": "",
            "nombre_solicitante": "María Docente",
            "email": "maria.docente@sanfrancisco.cl",
            "telefono": "+56 9 8888 7777",
            "establecimiento": "Colegio San Francisco",
            "tipo_institucion": "PARTICULAR_SUBVENCIONADO",
            "cargo_solicitante": "Jefa UTP",
            "region": "Metropolitana de Santiago",
            "comuna": "Santiago",
            "institucion_responsable_compra": "Fundación Educacional San Francisco",
            "rut_institucion": "76.543.210-K",
            "nombre_encargado_compras": "Pedro Adquisiciones",
            "email_encargado_compras": "adquisiciones@sanfrancisco.cl",
            "proyecto_educativo": "Taller Robótica Escolar 2026",
            "fecha_requerida_aproximada": "Marzo 2026",
            "observaciones": "Requerimos factura institucional y despacho a colegio.",
        }

        resp = self.client.post(reverse("solicitar_cotizacion"), form_data)
        self.assertEqual(resp.status_code, 302)

        # Verificar que no se duplicaron entidades
        self.assertEqual(Establecimiento.objects.filter(nombre="Colegio San Francisco").count(), 1)
        self.assertEqual(Contacto.objects.filter(email="maria.docente@sanfrancisco.cl").count(), 1)

        solicitud = SolicitudCotizacion.objects.first()
        self.assertEqual(solicitud.establecimiento_ref, est_existente)
        self.assertEqual(solicitud.contacto_ref, contacto_existente)
        self.assertEqual(solicitud.rut_institucion, "76.543.210-K")
        self.assertEqual(est_existente.rut, "76543210-K")
        self.assertEqual(solicitud.institucion_responsable_compra, "Fundación Educacional San Francisco")
        self.assertEqual(solicitud.contacto_adquisiciones_nombre, "Pedro Adquisiciones")

        # GET confirmación -> 200
        confirm_resp = self.client.get(reverse("solicitud_recibida", kwargs={"token": solicitud.token}))
        self.assertEqual(confirm_resp.status_code, 200)

    @patch("apps.cotizaciones.emails.send_mail")
    def test_solicitud_fallo_envio_email_no_aborta_y_confirma_200(self, mock_send_mail):
        """
        Escenario 3: Si send_mail lanza una excepción (fallo de red, SMTP caído),
        la solicitud DEBE guardarse, la transacción confirmarse, y el usuario
        redirigido a la confirmación exitosa con HTTP 200 (sin 500).
        """
        mock_send_mail.side_effect = Exception("SMTP server unavailable / Connection refused")

        token = "token-fail-email-3"
        self._preparar_canasta_y_token(token)

        form_data = {
            "idempotency_token": token,
            "sitio_web_docente": "",
            "nombre_solicitante": "Docente Resiliente",
            "email": "docente.resiliente@colegio.cl",
            "telefono": "+56 9 9999 0000",
            "establecimiento": "Liceo Bicentenario Resiliencia",
            "region": "Biobío",
            "comuna": "Concepción",
        }

        resp = self.client.post(reverse("solicitar_cotizacion"), form_data)
        # No debe haber 500
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(SolicitudCotizacion.objects.count(), 1)

        solicitud = SolicitudCotizacion.objects.first()
        confirm_resp = self.client.get(reverse("solicitud_recibida", kwargs={"token": solicitud.token}))
        self.assertEqual(confirm_resp.status_code, 200)
        self.assertContains(confirm_resp, solicitud.codigo_seguimiento)

    def test_solicitud_no_emite_salida_en_stdout_con_backend_smtp(self):
        """
        Escenario 4: Verificar que durante el flujo de solicitud no se escriba
        nada a sys.stdout (lo cual provocaría 'malformed header' en CGI/Apache).
        """
        token = "token-stdout-check"
        self._preparar_canasta_y_token(token)

        form_data = {
            "idempotency_token": token,
            "sitio_web_docente": "",
            "nombre_solicitante": "Docente Test Stdout",
            "email": "docente.stdout@test.cl",
            "telefono": "+56 9 4444 5555",
            "establecimiento": "Colegio Stdout Limpio",
            "region": "Aysén del General Carlos Ibáñez del Campo",
            "comuna": "Coyhaique",
        }

        stdout_capture = io.StringIO()
        real_stdout = sys.stdout
        sys.stdout = stdout_capture
        try:
            resp = self.client.post(reverse("solicitar_cotizacion"), form_data)
        finally:
            sys.stdout = real_stdout

        self.assertEqual(resp.status_code, 302)
        self.assertEqual(stdout_capture.getvalue(), "", "sys.stdout no debe recibir ninguna salida durante el envío de solicitud.")
