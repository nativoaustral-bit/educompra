from decimal import Decimal
from django.test import TestCase
from apps.core.models import ConfiguracionPricing
from apps.catalogo.models import Proveedor, Categoria, Producto, ProductoImagen

class CatalogoModelsTestCase(TestCase):
    def setUp(self):
        self.config = ConfiguracionPricing.get_solo()
        self.config.tipo_cambio_usd_clp = Decimal("950.00")
        self.config.factor_internacion_flete_porcentaje = Decimal("15.00")
        self.config.recargo_general_porcentaje = Decimal("80.00")
        self.config.iva_porcentaje = Decimal("19.00")
        self.config.save()

        self.proveedor = Proveedor.objects.create(
            nombre="Keyestudio",
            codigo="KEY",
            moneda_origen="USD"
        )
        self.categoria = Categoria.objects.create(
            nombre="Sensores y Módulos",
            slug="sensores-y-modulos"
        )

    def test_creacion_producto_y_calculo_precios_sugeridos(self):
        """
        Verifica el cálculo del precio referencial sugerido:
        Costo USD: $2.00
        Tipo de Cambio: $950 CLP -> $1.900 CLP
        Factor Internación: +15% -> $1.900 * 1.15 = $2.185 CLP (Costo puesto Chile)
        Recargo Humm (80%): $2.185 * 1.80 = $3.933 CLP (Precio Sugerido Neto)
        IVA (19%): $3.933 * 1.19 = $4.680 CLP (Precio Sugerido Total con IVA)
        """
        producto = Producto.objects.create(
            sku_humm="HUMM-SEN-001",
            sku_proveedor="KS0011",
            proveedor=self.proveedor,
            categoria=self.categoria,
            marca="Keyestudio",
            modelo="KS0011",
            nombre_comercial="Sensor de Humedad de Suelo Keyestudio KS0011",
            titulo_especificacion_neutral="Módulo Sensor de Humedad para Suelo",
            especificacion_tecnica_neutral="Sensor higrométrico resistivo para suelo con salida analógica y digital...",
            costo_proveedor_usd=Decimal("2.00"),
            publicado=True
        )

        self.assertEqual(producto.costo_puesto_chile_clp, Decimal("2185.00"))
        self.assertEqual(producto.precio_sugerido_neto_clp, Decimal("3933.00"))
        self.assertEqual(producto.precio_sugerido_total_clp, Decimal("4680.00"))

    def test_recargo_especifico_sobrescribe_general(self):
        """Verifica que un recargo específico en el producto tenga prioridad sobre el general."""
        producto = Producto.objects.create(
            sku_humm="HUMM-ARD-001",
            sku_proveedor="KS0001",
            proveedor=self.proveedor,
            categoria=self.categoria,
            marca="Keyestudio",
            nombre_comercial="Placa de Desarrollo UNO R3",
            costo_proveedor_usd=Decimal("10.00"),
            porcentaje_recargo=Decimal("50.00"),  # 50% en vez del 80% general
        )

        # Costo base: 10 * 950 * 1.15 = 10.925
        # Neto sugerido con 50%: 10.925 * 1.50 = 16.388 (redondeado)
        self.assertEqual(producto.costo_puesto_chile_clp, Decimal("10925.00"))
        self.assertEqual(producto.precio_sugerido_neto_clp, Decimal("16388.00"))

    def test_separacion_comercial_vs_especificacion_neutral(self):
        """Valida que los campos comerciales y neutros coexistan claramente en el modelo."""
        producto = Producto.objects.create(
            sku_humm="HUMM-ROB-001",
            sku_proveedor="KS0420",
            proveedor=self.proveedor,
            marca="Keyestudio",
            modelo="KS0420",
            nombre_comercial="Kit de Robot Tanque Keyestudio V2",
            descripcion_educativa="Permite a los estudiantes aprender cinemática diferencial y programación de motores...",
            titulo_especificacion_neutral="Kit de Robótica Móvil Educativa con Chasis de Oruga",
            especificacion_tecnica_neutral="Plataforma robótica sobre orugas con control microcontrolado, sensores de ultrasonido y línea...",
            criterios_equivalencia="O plataforma técnica equivalente compatible con IDE Arduino."
        )

        # La vista comercial contiene la marca
        self.assertIn("Keyestudio", producto.nombre_comercial)
        self.assertEqual(producto.marca, "Keyestudio")

        # La especificación neutra no debe exigir la marca en su definición
        self.assertNotIn("Keyestudio", producto.titulo_especificacion_neutral)
        self.assertIn("equivalente", producto.criterios_equivalencia.lower())
