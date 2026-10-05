"""
Pruebas automatizadas de la eliminación controlada de solicitudes de prueba
y edición de contactos en /gestion/ (Mejora Operacional EduCompra Humm).
"""

from decimal import Decimal
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.core.management import call_command
from django.test import TestCase, Client
from django.urls import reverse

from apps.catalogo.models import Producto, Categoria, Proveedor
from apps.cotizaciones.models import (
    SolicitudCotizacion,
    SolicitudItem,
    CotizacionFormal,
    CotizacionItem,
    Establecimiento,
    Contacto,
)
from apps.gestion.models import RegistroActividad

User = get_user_model()


class LimpiezaPruebasYContactosTestCase(TestCase):
    """Suite de pruebas para eliminación segura de pruebas y edición de contactos."""

    def setUp(self):
        call_command("crear_roles_gestion")

        self.superuser = User.objects.create_superuser(
            username="admin_test",
            email="admin@humm.cl",
            password="TestPassword123!",
            first_name="Admin",
            last_name="Test"
        )
        self.client = Client()
        self.client.force_login(self.superuser)

        # Establecimiento y Contacto
        self.establecimiento = Establecimiento.objects.create(
            nombre="Colegio San Francisco de Asís",
            comuna="Providencia",
            region="Metropolitana de Santiago",
            rut="65.123.456-7",
            rbd="12345",
            activo=True
        )
        self.contacto = Contacto.objects.create(
            nombre="Prof. Roberto Morales",
            cargo="Coordinador de Robótica",
            email="roberto.morales@sanfrancisco.cl",
            telefono="+56 9 1111 2222",
            establecimiento_principal=self.establecimiento,
            activo=True
        )

        # Catálogo
        self.proveedor = Proveedor.objects.create(
            nombre="Keyestudio Oficial",
            codigo="KEY",
            moneda_origen="USD",
            activo=True
        )
        self.categoria = Categoria.objects.create(
            nombre="Robótica",
            slug="robotica",
            activa=True
        )
        self.producto = Producto.objects.create(
            sku_humm="HUMM-KEY-KS0001",
            sku_proveedor="KS0001",
            nombre_comercial="Kit de Inicio Micro:bit V2",
            costo_proveedor_usd=Decimal("25.00"),
            precio_sugerido_total_clp=Decimal("45000"),
            proveedor=self.proveedor,
            categoria=self.categoria,
            publicado=True,
            activo=True
        )

    def test_solicitud_real_no_puede_eliminarse(self):
        """Una solicitud comercial real (es_prueba=False) no puede eliminarse ni por GET ni por POST."""
        sol_real = SolicitudCotizacion.objects.create(
            nombre_solicitante="Docente Colegio Real",
            email="docente@colegioreal.cl",
            telefono="+56 9 8888 7777",
            establecimiento="Colegio Real de Prueba",
            comuna="Santiago",
            region="Metropolitana de Santiago",
            es_prueba=False
        )

        # Intento vía GET
        url = reverse("gestion:solicitud_eliminar", kwargs={"id": sol_real.id})
        response_get = self.client.get(url)
        self.assertEqual(response_get.status_code, 403)

        # Intento vía POST con manipulación manual
        response_post = self.client.post(url, {"confirmar": "1"})
        self.assertEqual(response_post.status_code, 403)

        # Verificar que la solicitud sigue intacta en la base de datos
        self.assertTrue(SolicitudCotizacion.objects.filter(id=sol_real.id).exists())

    def test_solicitud_prueba_si_puede_eliminarse(self):
        """Una solicitud de prueba (es_prueba=True) sí puede eliminarse mediante POST con confirmación."""
        sol_prueba = SolicitudCotizacion.objects.create(
            nombre_solicitante="PRUEBA INTERNA HUMM",
            email="prueba@humm.cl",
            telefono="+56 9 9999 9999",
            establecimiento="Colegio de Prueba",
            comuna="Santiago",
            region="Metropolitana de Santiago",
            es_prueba=True
        )

        url = reverse("gestion:solicitud_eliminar", kwargs={"id": sol_prueba.id})

        # GET muestra pantalla de confirmación
        response_get = self.client.get(url)
        self.assertEqual(response_get.status_code, 200)
        self.assertContains(response_get, "ELIMINAR SOLICITUD DE PRUEBA")
        self.assertContains(response_get, "Esta acción eliminará permanentemente esta solicitud de prueba")

        # POST con confirmar=1 elimina exitosamente
        response_post = self.client.post(url, {"confirmar": "1"})
        self.assertEqual(response_post.status_code, 302)
        self.assertIn(reverse("gestion:solicitudes_lista"), response_post.url)

        # Verificar eliminación
        self.assertFalse(SolicitudCotizacion.objects.filter(id=sol_prueba.id).exists())

    def test_eliminacion_mediante_get_rechazada(self):
        """La eliminación mediante GET no debe eliminar la solicitud."""
        sol_prueba = SolicitudCotizacion.objects.create(
            nombre_solicitante="PRUEBA TEST GET",
            email="testget@humm.cl",
            telefono="+56 9 9999 9999",
            establecimiento="Colegio Test GET",
            comuna="Santiago",
            region="Metropolitana de Santiago",
            es_prueba=True
        )

        url = reverse("gestion:solicitud_eliminar", kwargs={"id": sol_prueba.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # La solicitud aún debe existir
        self.assertTrue(SolicitudCotizacion.objects.filter(id=sol_prueba.id).exists())

        # En eliminación masiva, GET redirige sin eliminar
        response_masivo_get = self.client.get(reverse("gestion:solicitudes_eliminar_masivo"))
        self.assertEqual(response_masivo_get.status_code, 302)
        self.assertTrue(SolicitudCotizacion.objects.filter(id=sol_prueba.id).exists())

    def test_items_de_prueba_desaparecen(self):
        """Al eliminar una solicitud de prueba, sus SolicitudItem dependientes desaparecen en cascada."""
        sol_prueba = SolicitudCotizacion.objects.create(
            nombre_solicitante="PRUEBA ITEMS",
            email="pruebaitems@humm.cl",
            telefono="+56 9 9999 9999",
            establecimiento="Colegio Items",
            comuna="Santiago",
            region="Metropolitana de Santiago",
            es_prueba=True
        )
        item = SolicitudItem.objects.create(
            solicitud=sol_prueba,
            producto=self.producto,
            cantidad=3
        )

        item_id = item.id
        self.assertTrue(SolicitudItem.objects.filter(id=item_id).exists())

        # Eliminar solicitud
        url = reverse("gestion:solicitud_eliminar", kwargs={"id": sol_prueba.id})
        self.client.post(url, {"confirmar": "1"})

        # El ítem desapareció
        self.assertFalse(SolicitudItem.objects.filter(id=item_id).exists())

    def test_cotizacion_formal_de_prueba_desaparece(self):
        """Si la solicitud de prueba tiene cotización formal e ítems asociados, desaparecen en cascada."""
        sol_prueba = SolicitudCotizacion.objects.create(
            nombre_solicitante="PRUEBA COTIZACION",
            email="pruebacot@humm.cl",
            telefono="+56 9 9999 9999",
            establecimiento="Colegio Cotización",
            comuna="Santiago",
            region="Metropolitana de Santiago",
            es_prueba=True
        )
        cot_formal = CotizacionFormal.objects.create(
            solicitud=sol_prueba,
            numero_cotizacion="COT-PRUEBA-9999",
            subtotal_neto=Decimal("45000"),
            iva=Decimal("8550"),
            total=Decimal("53550")
        )
        cot_item = CotizacionItem.objects.create(
            cotizacion=cot_formal,
            producto=self.producto,
            descripcion_tecnica_neutra_utilizada="Kit de robótica educacional",
            cantidad=1,
            precio_unitario_neto_definitivo=Decimal("45000")
        )

        cot_id = cot_formal.id
        cot_item_id = cot_item.id

        # Eliminar solicitud
        url = reverse("gestion:solicitud_eliminar", kwargs={"id": sol_prueba.id})
        self.client.post(url, {"confirmar": "1"})

        self.assertFalse(CotizacionFormal.objects.filter(id=cot_id).exists())
        self.assertFalse(CotizacionItem.objects.filter(id=cot_item_id).exists())

    def test_productos_del_catalogo_permanecen_intactos(self):
        """Al eliminar una solicitud de prueba, los productos del catálogo permanecen 100% intactos."""
        sol_prueba = SolicitudCotizacion.objects.create(
            nombre_solicitante="PRUEBA CATALOGO",
            email="pruebacat@humm.cl",
            telefono="+56 9 9999 9999",
            establecimiento="Colegio Catálogo",
            comuna="Santiago",
            region="Metropolitana de Santiago",
            es_prueba=True
        )
        SolicitudItem.objects.create(
            solicitud=sol_prueba,
            producto=self.producto,
            cantidad=2
        )

        prod_id = self.producto.id
        url = reverse("gestion:solicitud_eliminar", kwargs={"id": sol_prueba.id})
        self.client.post(url, {"confirmar": "1"})

        self.assertTrue(Producto.objects.filter(id=prod_id).exists())
        prod = Producto.objects.get(id=prod_id)
        self.assertEqual(prod.sku_humm, "HUMM-KEY-KS0001")
        self.assertTrue(prod.publicado)

    def test_contacto_permanece_intacto(self):
        """Al eliminar una solicitud de prueba, el Contacto docente permanece intacto."""
        sol_prueba = SolicitudCotizacion.objects.create(
            nombre_solicitante="PRUEBA CONTACTO",
            email=self.contacto.email,
            telefono=self.contacto.telefono,
            establecimiento=self.establecimiento.nombre,
            comuna="Providencia",
            region="Metropolitana de Santiago",
            contacto_ref=self.contacto,
            establecimiento_ref=self.establecimiento,
            es_prueba=True
        )

        contacto_id = self.contacto.id
        url = reverse("gestion:solicitud_eliminar", kwargs={"id": sol_prueba.id})
        self.client.post(url, {"confirmar": "1"})

        self.assertTrue(Contacto.objects.filter(id=contacto_id).exists())

    def test_establecimiento_permanece_intacto(self):
        """Al eliminar una solicitud de prueba, el Establecimiento permanece intacto."""
        sol_prueba = SolicitudCotizacion.objects.create(
            nombre_solicitante="PRUEBA ESTABLECIMIENTO",
            email="test@humm.cl",
            telefono="+56 9 9999 9999",
            establecimiento=self.establecimiento.nombre,
            comuna="Providencia",
            region="Metropolitana de Santiago",
            establecimiento_ref=self.establecimiento,
            es_prueba=True
        )

        est_id = self.establecimiento.id
        url = reverse("gestion:solicitud_eliminar", kwargs={"id": sol_prueba.id})
        self.client.post(url, {"confirmar": "1"})

        self.assertTrue(Establecimiento.objects.filter(id=est_id).exists())

    def test_eliminacion_masiva_solo_afecta_es_prueba_true(self):
        """La eliminación masiva solo acepta registros con es_prueba=True y rechaza si hay reales."""
        sol_prueba_1 = SolicitudCotizacion.objects.create(
            nombre_solicitante="PRUEBA 1",
            email="p1@humm.cl",
            telefono="+56 9 9999 9999",
            establecimiento="Col 1",
            comuna="Santiago",
            region="Metropolitana de Santiago",
            es_prueba=True
        )
        sol_prueba_2 = SolicitudCotizacion.objects.create(
            nombre_solicitante="PRUEBA 2",
            email="p2@humm.cl",
            telefono="+56 9 9999 9999",
            establecimiento="Col 2",
            comuna="Santiago",
            region="Metropolitana de Santiago",
            es_prueba=True
        )
        sol_real = SolicitudCotizacion.objects.create(
            nombre_solicitante="REAL 1",
            email="r1@colegio.cl",
            telefono="+56 9 8888 8888",
            establecimiento="Col Real",
            comuna="Santiago",
            region="Metropolitana de Santiago",
            es_prueba=False
        )

        url_masivo = reverse("gestion:solicitudes_eliminar_masivo")

        # Intento de eliminación masiva incluyendo solicitud real -> RECHAZADO (403)
        response_bloqueo = self.client.post(url_masivo, {
            "selected_ids": [str(sol_prueba_1.id), str(sol_real.id)],
            "confirmar": "1"
        })
        self.assertEqual(response_bloqueo.status_code, 403)
        self.assertTrue(SolicitudCotizacion.objects.filter(id=sol_real.id).exists())
        self.assertTrue(SolicitudCotizacion.objects.filter(id=sol_prueba_1.id).exists())

        # Eliminación masiva válida: solo solicitudes de prueba
        response_valido = self.client.post(url_masivo, {
            "selected_ids": [str(sol_prueba_1.id), str(sol_prueba_2.id)],
            "confirmar": "1"
        })
        self.assertEqual(response_valido.status_code, 302)
        self.assertFalse(SolicitudCotizacion.objects.filter(id=sol_prueba_1.id).exists())
        self.assertFalse(SolicitudCotizacion.objects.filter(id=sol_prueba_2.id).exists())
        self.assertTrue(SolicitudCotizacion.objects.filter(id=sol_real.id).exists())

    def test_edicion_de_contacto_funciona(self):
        """Permite editar campos autorizados de un contacto docente."""
        url_editar = reverse("gestion:contacto_editar", kwargs={"id": self.contacto.id})

        # GET muestra formulario con datos actuales
        response_get = self.client.get(url_editar)
        self.assertEqual(response_get.status_code, 200)
        self.assertContains(response_get, self.contacto.nombre)

        # POST actualiza campos
        response_post = self.client.post(url_editar, {
            "nombre": "Prof. Roberto Morales Editado",
            "cargo": "Jefe de Departamento de Ciencias",
            "email": "roberto.editado@sanfrancisco.cl",
            "telefono": "+56 9 94199879",
            "establecimiento_principal": str(self.establecimiento.id),
            "es_encargado_compras": "on",
            "posible_duplicado": "",
            "activo": "on",
            "observaciones_internas": "Contacto verificado telefónicamente."
        })
        self.assertEqual(response_post.status_code, 302)
        self.assertIn(reverse("gestion:contactos_lista"), response_post.url)

        self.contacto.refresh_from_db()
        self.assertEqual(self.contacto.nombre, "Prof. Roberto Morales Editado")
        self.assertEqual(self.contacto.cargo, "Jefe de Departamento de Ciencias")
        self.assertEqual(self.contacto.email, "roberto.editado@sanfrancisco.cl")
        self.assertEqual(self.contacto.telefono, "+56 9 94199879")
        self.assertTrue(self.contacto.es_encargado_compras)
        self.assertFalse(self.contacto.posible_duplicado)
        self.assertTrue(self.contacto.activo)
        self.assertEqual(self.contacto.observaciones_internas, "Contacto verificado telefónicamente.")

    def test_telefono_admite_formato_especificado(self):
        """El campo de teléfono admite y muestra exactamente el formato '+56 9 94199879'."""
        self.contacto.telefono = "+56 9 94199879"
        self.contacto.save()

        self.contacto.refresh_from_db()
        self.assertEqual(self.contacto.telefono, "+56 9 94199879")

        # Verificar visualización en /gestion/contactos/
        response = self.client.get(reverse("gestion:contactos_lista"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "+56 9 94199879")

    def test_auditoria_registro_actividad_al_eliminar_prueba(self):
        """Antes de eliminar una solicitud de prueba se registra en RegistroActividad con los datos requeridos."""
        sol_prueba = SolicitudCotizacion.objects.create(
            nombre_solicitante="PRUEBA AUDITORIA",
            email="audit@humm.cl",
            telefono="+56 9 9999 9999",
            establecimiento="Colegio Audit",
            comuna="Santiago",
            region="Metropolitana de Santiago",
            es_prueba=True
        )
        codigo = sol_prueba.codigo_seguimiento
        sol_id = sol_prueba.id

        url = reverse("gestion:solicitud_eliminar", kwargs={"id": sol_id})
        self.client.post(url, {"confirmar": "1"})

        # Comprobar auditoría
        registro = RegistroActividad.objects.filter(
            descripcion="ELIMINACIÓN CONTROLADA DE SOLICITUD DE PRUEBA",
            objeto_id=str(sol_id)
        ).first()

        self.assertIsNotNone(registro)
        self.assertEqual(registro.modelo_afectado, "SolicitudCotizacion")
        self.assertEqual(registro.detalles.get("codigo_seguimiento"), codigo)
        self.assertEqual(registro.detalles.get("email"), "audit@humm.cl")
        self.assertEqual(registro.detalles.get("establecimiento"), "Colegio Audit")
        self.assertIn("existencia_cotizacion_asociada", registro.detalles)
