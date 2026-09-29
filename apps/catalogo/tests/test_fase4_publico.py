from decimal import Decimal
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from apps.catalogo.models import Proveedor, Categoria, Producto, TecnologiaCompatible


class CatalogoFase4PublicoTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.proveedor = Proveedor.objects.create(nombre="Keyestudio", codigo="KEY")
        self.categoria = Categoria.objects.create(nombre="Robótica", slug="robotica")
        self.tecnologia = TecnologiaCompatible.objects.create(nombre="Arduino", slug="arduino")

        # Producto 1: Publicado y Validado
        self.prod_publicado = Producto.objects.create(
            sku_humm="HUMM-ROB-001",
            sku_proveedor="KS0001",
            proveedor=self.proveedor,
            categoria=self.categoria,
            nombre_comercial="Kit de Inicio Arduino Básico KS0001",
            estado_curaduria="VALIDADO",
            publicado=True,
            activo=True,
            costo_proveedor_usd=Decimal("10.00"),
            slug="ks0001-kit-de-inicio-arduino-basico"
        )
        self.prod_publicado.tecnologias_compatibles.add(self.tecnologia)
        self.prod_publicado.calcular_precios_sugeridos()
        self.prod_publicado.save()

        # Producto 2: NO Publicado (publicado=False) pero VALIDADO (típico de Fase 4A)
        self.prod_no_publicado = Producto.objects.create(
            sku_humm="HUMM-ROB-002",
            sku_proveedor="KS0002",
            proveedor=self.proveedor,
            categoria=self.categoria,
            nombre_comercial="Servomotor SG90 KS0002",
            estado_curaduria="VALIDADO",
            publicado=False,
            activo=True,
            costo_proveedor_usd=Decimal("2.00"),
            slug="ks0002-servomotor-sg90"
        )
        self.prod_no_publicado.calcular_precios_sugeridos()
        self.prod_no_publicado.save()

        # Usuario Staff para pruebas de Modo Preview
        self.staff_user = User.objects.create_user(
            username="admin_humm",
            password="securepassword123",
            is_staff=True
        )

    def test_slug_no_publicado_devuelve_404_para_publico(self):
        """Un producto no publicado debe devolver 404 aunque se conozca su slug exacto."""
        url = reverse("catalogo:detalle", kwargs={"slug": self.prod_no_publicado.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_slug_no_publicado_accesible_para_staff_en_preview(self):
        """Un usuario staff autenticado puede previsualizar productos no publicados en Fase 4A."""
        self.client.login(username="admin_humm", password="securepassword123")
        url = reverse("catalogo:detalle", kwargs={"slug": self.prod_no_publicado.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Servomotor SG90 KS0002")

    def test_sitemap_solo_contiene_productos_publicados(self):
        """El sitemap.xml solo debe exponer productos con publicado=True, activo=True y VALIDADO."""
        url = reverse("sitemap")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/xml")
        
        # Debe contener el producto publicado
        self.assertContains(response, self.prod_publicado.slug)
        # NUNCA debe contener el producto no publicado
        self.assertNotContains(response, self.prod_no_publicado.slug)

    def test_catalogo_publico_oculta_no_publicados(self):
        """El listado público solo expone productos publicados."""
        url = reverse("catalogo:lista")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.prod_publicado.nombre_comercial)
        self.assertNotContains(response, self.prod_no_publicado.nombre_comercial)

    def test_precio_publico_no_muestra_desglose_interno(self):
        """La ficha pública debe mostrar solo precio referencial con IVA sin desglose neto/costo/recargo."""
        url = reverse("catalogo:detalle", kwargs={"slug": self.prod_publicado.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Precio referencial con IVA")
        self.assertNotContains(response, "costo_proveedor")
        self.assertNotContains(response, "recargo")
        self.assertNotContains(response, "internacion")

    def test_comando_activar_catalogo_dry_run_y_publicacion(self):
        """Verifica que el comando de activación respete dry-run, valide expected_count y publique."""
        from django.core.management import call_command, CommandError
        from io import StringIO
        from apps.catalogo.models import ProductoImagen

        # Darle descripción educativa e imagen a ambos productos para que sean elegibles
        self.prod_publicado.descripcion_educativa = "Kit Arduino para educación inicial."
        self.prod_publicado.save()
        ProductoImagen.objects.create(producto=self.prod_publicado, nombre_archivo_original="KS0001.jpg", orden=0)

        self.prod_no_publicado.descripcion_educativa = "Servomotor educativo para proyectos escolares."
        self.prod_no_publicado.save()
        ProductoImagen.objects.create(producto=self.prod_no_publicado, nombre_archivo_original="KS0002.jpg", orden=0)

        # 1. Comprobar que falla con CommandError si hay menos de 72 productos (comportamiento por defecto)
        with self.assertRaises(CommandError) as ctx:
            call_command("activar_catalogo_publico_fase_4", dry_run=True)
        self.assertIn("DETENCIÓN OBLIGATORIA", str(ctx.exception))

        # 2. Ejecutar dry-run indicando la cantidad esperada en este test case (2 productos)
        out = StringIO()
        call_command("activar_catalogo_publico_fase_4", dry_run=True, expected_count=2, stdout=out)
        output = out.getvalue()
        self.assertIn("[DRY-RUN]", output)
        self.prod_no_publicado.refresh_from_db()
        self.assertFalse(self.prod_no_publicado.publicado)

        # 3. Ejecutar publicación real con expected_count=2
        out_real = StringIO()
        call_command("activar_catalogo_publico_fase_4", expected_count=2, stdout=out_real)
        self.prod_no_publicado.refresh_from_db()
        self.assertTrue(self.prod_no_publicado.publicado)

        # 4. Probar rollback con desactivación
        out_rollback = StringIO()
        call_command("desactivar_catalogo_publico_fase_4", stdout=out_rollback)
        self.prod_no_publicado.refresh_from_db()
        self.assertFalse(self.prod_no_publicado.publicado)

    def test_desglose_unidades_comerciales(self):
        """Verifica el cálculo pedagógico de desglose para packs, sets y unidades."""
        from apps.cotizaciones.services import calcular_desglose_unidades

        self.assertEqual(calcular_desglose_unidades("pack (3 unidades)", 2), "2 packs — 6 unidades en total")
        self.assertEqual(calcular_desglose_unidades("pack (4 unidades)", 3), "3 packs — 12 unidades en total")
        self.assertEqual(calcular_desglose_unidades("set (120 cables)", 1), "1 set — 120 cables en total")
        self.assertEqual(calcular_desglose_unidades("unidad", 5), "5 unidades")
