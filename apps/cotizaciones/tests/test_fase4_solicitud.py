from decimal import Decimal
from unittest.mock import patch
from django.test import TestCase, Client
from django.urls import reverse
from django.core.exceptions import ValidationError
from apps.catalogo.models import Proveedor, Categoria, Producto
from apps.cotizaciones.models import SolicitudCotizacion, SolicitudItem
from apps.cotizaciones.services import CartService, SubmissionService, SESSION_CART_KEY


class SolicitudCotizacionFase4TestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.proveedor = Proveedor.objects.create(nombre="Keyestudio", codigo="KEY")
        self.categoria = Categoria.objects.create(nombre="Sensores", slug="sensores")

        self.producto = Producto.objects.create(
            sku_humm="HUMM-SEN-001",
            sku_proveedor="KS0011",
            proveedor=self.proveedor,
            categoria=self.categoria,
            nombre_comercial="Sensor de Humedad KS0011",
            unidad_compra="pack (3 unidades)",
            estado_curaduria="VALIDADO",
            publicado=True,
            activo=True,
            costo_proveedor_usd=Decimal("5.00"),
            slug="ks0011-sensor-humedad"
        )
        self.producto.calcular_precios_sugeridos()
        self.producto.save()
        self.precio_real = self.producto.precio_sugerido_total_clp

    def test_sesion_no_guarda_precios_como_fuente_de_verdad(self):
        """Verifica que la sesión guarde únicamente producto_id y cantidad."""
        session = self.client.session
        session[SESSION_CART_KEY] = {
            str(self.producto.id): {"cantidad": 2}
        }
        session.save()

        # Enviar petición a la vista de canasta
        response = self.client.get(reverse("mi_cotizacion"))
        self.assertEqual(response.status_code, 200)

        # El subtotal debe ser exactamente 2 * precio_real desde BD
        subtotal_esperado = 2 * self.precio_real
        self.assertEqual(response.context["total_referencial"], subtotal_esperado)

    def test_manipulacion_de_precio_desde_navegador(self):
        """
        Intentar inyectar un precio falso en la petición no tiene efecto:
        el servidor calcula siempre a partir del precio vigente en BD.
        """
        # Se agrega a la canasta con precio real en BD
        self.client.post(reverse("canasta_agregar"), {
            "producto_id": self.producto.id,
            "cantidad": 3,
            "precio": "100.00",  # Precio manipulado maliciosamente
            "subtotal": "300.00",
        })

        session = self.client.session
        # La estructura en sesión no almacena precio
        self.assertEqual(session[SESSION_CART_KEY][str(self.producto.id)]["cantidad"], 3)
        self.assertNotIn("precio", session[SESSION_CART_KEY][str(self.producto.id)])

    def test_producto_despublicado_despues_de_agregarse(self):
        """
        Si un producto fue agregado y luego se despublica o inactiva,
        no debe poder enviarse silenciosamente; se retira y se alerta al profesor.
        """
        # 1. Agregar a sesión
        session = self.client.session
        session[SESSION_CART_KEY] = {str(self.producto.id): {"cantidad": 2}}
        session.save()

        # 2. Despublicar producto
        self.producto.publicado = False
        self.producto.save()

        # 3. Consultar canasta revalidada
        response = self.client.get(reverse("mi_cotizacion"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["items"]), 0)
        self.assertIn(self.producto.id, response.context["items_retirados"])

    def test_rechazo_cantidades_invalidas(self):
        """Rechaza cantidades negativas, cero o excesivas."""
        # 0
        response = self.client.post(reverse("canasta_agregar"), {
            "producto_id": self.producto.id,
            "cantidad": 0
        })
        session = self.client.session
        self.assertNotIn(str(self.producto.id), session.get(SESSION_CART_KEY, {}))

        # Negativo
        response = self.client.post(reverse("canasta_agregar"), {
            "producto_id": self.producto.id,
            "cantidad": -5
        })
        session = self.client.session
        self.assertNotIn(str(self.producto.id), session.get(SESSION_CART_KEY, {}))

        # Cantidad absurdamente alta (mayor a 500) es rechazada
        self.client.post(reverse("canasta_agregar"), {
            "producto_id": self.producto.id,
            "cantidad": 9999
        })
        session = self.client.session
        self.assertNotIn(str(self.producto.id), session.get(SESSION_CART_KEY, {}))

        # Cantidad válida (ej: 5) es aceptada
        self.client.post(reverse("canasta_agregar"), {
            "producto_id": self.producto.id,
            "cantidad": 5
        })
        session = self.client.session
        cant = session[SESSION_CART_KEY][str(self.producto.id)]["cantidad"]
        self.assertEqual(cant, 5)

    def test_idempotencia_previene_doble_envio(self):
        """El mismo token de envío no puede generar dos solicitudes de cotización."""
        # Preparar canasta
        session = self.client.session
        session[SESSION_CART_KEY] = {str(self.producto.id): {"cantidad": 2}}
        token = "test-unique-idempotency-token"
        session["form_idempotency_token"] = token
        session.save()

        form_data = {
            "idempotency_token": token,
            "sitio_web_docente": "",  # Honeypot vacío
            "nombre_solicitante": "Profesor Carlos Mendoza",
            "email": "carlos.mendoza@colegio.cl",
            "telefono": "+56911223344",
            "establecimiento": "Colegio San Francisco",
            "region": "Metropolitana de Santiago",
            "comuna": "Santiago",
        }

        # 1. Primer envío: debe ser exitoso
        resp1 = self.client.post(reverse("solicitar_cotizacion"), form_data)
        self.assertEqual(resp1.status_code, 302)
        self.assertEqual(SolicitudCotizacion.objects.count(), 1)

        # 2. Reenvío con el mismo token (simulando doble clic o refresh)
        resp2 = self.client.post(reverse("solicitar_cotizacion"), form_data)
        # No debe crear una segunda solicitud
        self.assertEqual(SolicitudCotizacion.objects.count(), 1)

    def test_honeypot_rechaza_spam_bots(self):
        """Si un bot rellena el campo trampa sitio_web_docente, la solicitud se rechaza."""
        session = self.client.session
        session[SESSION_CART_KEY] = {str(self.producto.id): {"cantidad": 1}}
        token = "bot-token-123"
        session["form_idempotency_token"] = token
        session.save()

        form_data = {
            "idempotency_token": token,
            "sitio_web_docente": "http://spambot-link.com",  # Bot completó campo oculto
            "nombre_solicitante": "Spam Bot",
            "email": "spam@bot.com",
            "telefono": "123456",
            "establecimiento": "Fake School",
            "region": "Valparaíso",
            "comuna": "Valparaíso",
        }

        resp = self.client.post(reverse("solicitar_cotizacion"), form_data)
        self.assertEqual(SolicitudCotizacion.objects.count(), 0)

    def test_snapshots_congelados_en_solicitud_item(self):
        """Verifica que SolicitudItem congele los datos y preserve inalterabilidad."""
        session = self.client.session
        session[SESSION_CART_KEY] = {str(self.producto.id): {"cantidad": 4}}
        token = "token-snapshot-test"
        session["form_idempotency_token"] = token
        session.save()

        form_data = {
            "idempotency_token": token,
            "sitio_web_docente": "",
            "nombre_solicitante": "Profesora María González",
            "email": "maria@colegio.cl",
            "telefono": "+56987654321",
            "establecimiento": "Liceo Experimental",
            "region": "Biobío",
            "comuna": "Concepción",
        }

        resp = self.client.post(reverse("solicitar_cotizacion"), form_data)
        solicitud = SolicitudCotizacion.objects.first()
        self.assertIsNotNone(solicitud)

        item = solicitud.items.first()
        self.assertEqual(item.sku_humm_snapshot, self.producto.sku_humm)
        self.assertEqual(item.sku_proveedor_snapshot, self.producto.sku_proveedor)
        self.assertEqual(item.nombre_comercial_snapshot, self.producto.nombre_comercial)
        self.assertEqual(item.unidad_comercial_snapshot, "pack (3 unidades)")
        self.assertEqual(item.cantidad, 4)
        self.assertEqual(item.precio_referencial_unitario_snapshot, self.precio_real)
        self.assertEqual(item.subtotal_referencial_snapshot, 4 * self.precio_real)

        # Modificar producto original en catálogo
        self.producto.costo_proveedor_usd = Decimal("50.00")
        self.producto.nombre_comercial = "Nombre Cambiado Posteriormente"
        self.producto.calcular_precios_sugeridos()
        self.producto.save()

        # Recargar item y verificar que snapshot no cambió
        item.refresh_from_db()
        self.assertEqual(item.nombre_comercial_snapshot, "Sensor de Humedad KS0011")
        self.assertEqual(item.precio_referencial_unitario_snapshot, self.precio_real)

    def test_confirmacion_publica_no_expone_datos_sensibles(self):
        """
        La vista /solicitud-recibida/<token>/ NO debe exhibir email completo,
        teléfono, RUT ni notas internas.
        """
        solicitud = SolicitudCotizacion.objects.create(
            nombre_solicitante="Profesor Privado",
            email="profesor.secreto@colegio.cl",
            telefono="+56999887766",
            rut_institucion="76.123.456-K",
            establecimiento="Liceo Comunal San Bernardo",
            comuna="San Bernardo",
            region="Metropolitana de Santiago",
            observaciones="Requerimiento interno confidencial",
            total_referencial_estimado=Decimal("50000.00")
        )

        url = reverse("solicitud_recibida", kwargs={"token": solicitud.token})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

        # Debe mostrar código y establecimiento
        self.assertContains(resp, solicitud.codigo_seguimiento)
        self.assertContains(resp, "Liceo Comunal San Bernardo")

        # NUNCA debe mostrar datos sensibles
        self.assertNotContains(resp, "profesor.secreto@colegio.cl")
        self.assertNotContains(resp, "+56999887766")
        self.assertNotContains(resp, "76.123.456-K")
        self.assertNotContains(resp, "Requerimiento interno confidencial")

    @patch("apps.cotizaciones.services.enviar_correos_solicitud")
    def test_resiliencia_fallo_correo_no_aborta_solicitud(self, mock_enviar_correos):
        """
        Si el envío de correos falla (ej: caída SMTP), la solicitud se guarda
        exitosamente y el profesor es redirigido a confirmación.
        """
        mock_enviar_correos.side_effect = Exception("Conexión SMTP rechazada")

        session = self.client.session
        session[SESSION_CART_KEY] = {str(self.producto.id): {"cantidad": 1}}
        token = "token-smtp-fail"
        session["form_idempotency_token"] = token
        session.save()

        form_data = {
            "idempotency_token": token,
            "sitio_web_docente": "",
            "nombre_solicitante": "Docente Test",
            "email": "docente@test.cl",
            "telefono": "+56900000000",
            "establecimiento": "Colegio Resiliente",
            "region": "Maule",
            "comuna": "Talca",
        }

        resp = self.client.post(reverse("solicitar_cotizacion"), form_data)
        # Debe redirigir a confirmación con éxito a pesar del fallo de correo
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(SolicitudCotizacion.objects.count(), 1)
