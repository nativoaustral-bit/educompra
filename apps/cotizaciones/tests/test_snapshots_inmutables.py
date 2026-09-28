from decimal import Decimal
from django.test import TestCase
from apps.catalogo.models import Proveedor, Categoria, Producto
from apps.cotizaciones.models import (
    SolicitudCotizacion,
    SolicitudItem,
    CotizacionFormal,
    CotizacionItem
)

class SnapshotsInmutablesTestCase(TestCase):
    def setUp(self):
        self.proveedor = Proveedor.objects.create(nombre="Keyestudio", codigo="KEY")
        self.categoria = Categoria.objects.create(nombre="Sensores", slug="sensores")

        self.producto = Producto.objects.create(
            sku_humm="HUMM-SEN-001",
            sku_proveedor="KS0011",
            proveedor=self.proveedor,
            categoria=self.categoria,
            marca="Keyestudio",
            modelo="KS0011",
            nombre_comercial="Sensor de Humedad de Suelo Keyestudio KS0011",
            titulo_especificacion_neutral="Módulo Sensor de Humedad para Suelo",
            especificacion_tecnica_neutral="Sensor higrométrico resistivo para suelo con salida analógica y digital...",
            criterios_equivalencia="O técnicamente equivalente compatible.",
            costo_proveedor_usd=Decimal("2.00")
        )
        self.producto.calcular_precios_sugeridos()
        self.producto.save()

    def test_snapshot_inmutable_al_crear_solicitud_item(self):
        """
        Verifica que al crear un SolicitudItem, los datos del producto se congelen
        en los campos *_snapshot y permanezcan inalterables incluso si el producto se modifica o elimina.
        """
        solicitud = SolicitudCotizacion.objects.create(
            nombre_solicitante="Profesor Juan Pérez",
            email="juan.perez@colegio.cl",
            telefono="+56912345678",
            establecimiento="Liceo Politécnico San José",
            comuna="Temuco",
            region="La Araucanía"
        )

        item = SolicitudItem.objects.create(
            solicitud=solicitud,
            producto=self.producto,
            cantidad=10
        )

        # 1. Comprobar que los campos de snapshot se poblaron automáticamente
        self.assertEqual(item.sku_humm_snapshot, "HUMM-SEN-001")
        self.assertEqual(item.marca_snapshot, "Keyestudio")
        self.assertEqual(item.modelo_snapshot, "KS0011")
        self.assertEqual(item.nombre_comercial_snapshot, "Sensor de Humedad de Suelo Keyestudio KS0011")
        self.assertEqual(item.especificacion_neutra_snapshot, self.producto.especificacion_tecnica_neutral)
        self.assertEqual(item.precio_referencial_unitario_snapshot, self.producto.precio_sugerido_total_clp)
        self.assertEqual(item.subtotal_referencial_snapshot, 10 * self.producto.precio_sugerido_total_clp)

        # 2. Modificar el producto original en el catálogo (cambiar marca, nombre y costo)
        self.producto.marca = "OtraMarca"
        self.producto.nombre_comercial = "Sensor Modificado 2027"
        self.producto.especificacion_tecnica_neutral = "Texto neutral completamente modificado."
        self.producto.costo_proveedor_usd = Decimal("5.00")
        self.producto.calcular_precios_sugeridos()
        self.producto.save()

        # 3. Recargar el item desde BD y comprobar que el snapshot NO cambió en absoluto
        item.refresh_from_db()
        self.assertEqual(item.sku_humm_snapshot, "HUMM-SEN-001")
        self.assertEqual(item.marca_snapshot, "Keyestudio")
        self.assertEqual(item.modelo_snapshot, "KS0011")
        self.assertEqual(item.nombre_comercial_snapshot, "Sensor de Humedad de Suelo Keyestudio KS0011")
        self.assertNotEqual(item.nombre_comercial_snapshot, self.producto.nombre_comercial)
        self.assertNotEqual(item.precio_referencial_unitario_snapshot, self.producto.precio_sugerido_total_clp)

        # 4. Eliminar el producto del catálogo (on_delete=models.SET_NULL)
        producto_id = self.producto.id
        self.producto.delete()

        item.refresh_from_db()
        self.assertIsNone(item.producto)
        # El snapshot sigue intacto y accesible para auditoría y cotizaciones
        self.assertEqual(item.sku_humm_snapshot, "HUMM-SEN-001")
        self.assertEqual(item.nombre_comercial_snapshot, "Sensor de Humedad de Suelo Keyestudio KS0011")

    def test_cotizacion_formal_con_descripcion_neutra_y_override_manual(self):
        """
        Verifica que CotizacionItem utilice obligatoriamente una descripción técnica neutra
        y permita que el administrador Humm fije un precio definitivo distinto al sugerido.
        """
        solicitud = SolicitudCotizacion.objects.create(
            nombre_solicitante="Profesora Andrea Soto",
            email="andrea.soto@colegio.cl",
            telefono="+56987654321",
            establecimiento="Colegio Bicentenario",
            comuna="Concepción",
            region="Biobío"
        )

        cotizacion = CotizacionFormal.objects.create(
            solicitud=solicitud,
            numero_cotizacion="COT-HUMM-2026-0001",
            validez_dias=30
        )

        # Precio sugerido neto del producto era aprox $3.933 CLP
        # El administrador Humm decide ajustar manualmente a $3.500 CLP por volumen
        precio_definitivo_ajustado = Decimal("3500.00")
        descripcion_neutra = (
            "Sensor higrométrico resistivo para suelo con salida analógica/digital, "
            "compatible con microcontroladores de 3.3V-5V o técnicamente equivalente."
        )

        item_cotizacion = CotizacionItem.objects.create(
            cotizacion=cotizacion,
            producto=self.producto,
            descripcion_tecnica_neutra_utilizada=descripcion_neutra,
            cantidad=20,
            unidad_medida="unidad",
            precio_unitario_neto_definitivo=precio_definitivo_ajustado
        )

        # Comprobar que subtotal se calculó con el precio definitivo ajustado
        self.assertEqual(item_cotizacion.subtotal_neto, Decimal("70000.00"))

        # REGLA OBLIGATORIA DE NEUTRALIDAD DOCUMENTAL:
        # La descripción formal no debe contener marcas ni SKUs comerciales de origen
        self.assertNotIn("Keyestudio", item_cotizacion.descripcion_tecnica_neutra_utilizada)
        self.assertNotIn("KS0011", item_cotizacion.descripcion_tecnica_neutra_utilizada)
