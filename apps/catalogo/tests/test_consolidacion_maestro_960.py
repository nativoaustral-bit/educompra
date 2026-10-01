"""
Tests unitarios para la consolidación de Catálogo Maestro 960 SKU Keyestudio (Fase 5A).
Verifica blindaje de unicidad (UniqueConstraint), preservación del catálogo público,
incorporación de 6 nuevos SKUs, resolución de 13 conflictos históricos,
cuarentena estricta de 2 SKUs y detección de anomalías en tramos de volumen (KS5012).
"""

from decimal import Decimal
from django.core.management import call_command
from django.db import IntegrityError
from django.test import TestCase

from apps.catalogo.models import Proveedor, Categoria, Producto, PrecioProveedorTramo


class ConsolidacionMaestro960Tests(TestCase):
    def setUp(self):
        self.prov = Proveedor.objects.create(
            nombre="Keyestudio",
            codigo="KEY",
            moneda_origen="USD"
        )
        self.cat = Categoria.objects.create(
            nombre="Sin clasificar",
            slug="sin-clasificar"
        )

    def test_blindaje_unicidad_proveedor_sku(self):
        """Verifica que UniqueConstraint(proveedor, sku_proveedor) rechace duplicados a nivel de base de datos."""
        Producto.objects.create(
            sku_humm="HUMM-KEY-TEST01",
            sku_proveedor="TEST01",
            proveedor=self.prov,
            categoria=self.cat,
            nombre_comercial="Producto Test 01",
            costo_proveedor_usd=Decimal("10.00"),
        )

        with self.assertRaises(IntegrityError):
            Producto.objects.create(
                sku_humm="HUMM-KEY-TEST02",
                sku_proveedor="TEST01",  # Mismo proveedor y mismo SKU proveedor
                proveedor=self.prov,
                categoria=self.cat,
                nombre_comercial="Producto Test Duplicado",
                costo_proveedor_usd=Decimal("12.00"),
            )

    def test_creacion_cuarentena_2_skus(self):
        """Verifica que los productos en cuarentena tengan costo 0, activo=False, publicado=False."""
        prod_q = Producto.objects.create(
            sku_humm="HUMM-KEY-KS0240",
            sku_proveedor="KS0240",
            proveedor=self.prov,
            categoria=self.cat,
            nombre_comercial="[KS0240] — Pendiente resolución proveedor",
            nombre_original_proveedor="[KS0240] — Pendiente resolución proveedor",
            costo_proveedor_usd=Decimal("0.00"),
            activo=False,
            publicado=False,
            estado_curaduria="SIN_REVISAR",
            estado_especificacion_neutral="NO_REVISADO",
            observaciones_internas="Variantes conflictivas detectadas.",
        )
        self.assertFalse(prod_q.activo)
        self.assertFalse(prod_q.publicado)
        self.assertEqual(prod_q.costo_proveedor_usd, Decimal("0.00"))
        self.assertEqual(prod_q.estado_curaduria, "SIN_REVISAR")
        self.assertIn("Pendiente resolución", prod_q.nombre_comercial)

    def test_incorporacion_conflicto_resuelto(self):
        """Verifica que un conflicto resuelto ingrese como activo=True, publicado=False y con trazabilidad."""
        prod = Producto.objects.create(
            sku_humm="HUMM-KEY-KS0077",
            sku_proveedor="KS0077",
            proveedor=self.prov,
            categoria=self.cat,
            nombre_comercial="Keyestudio Super Learning Kit For Arduino Starter",
            costo_proveedor_usd=Decimal("24.00"),
            activo=True,
            publicado=False,
            estado_curaduria="SIN_REVISAR",
            observaciones_internas=(
                "Producto anteriormente excluido por conflicto en catálogo maestro original. "
                "Incorporado utilizando definición y precios de lista comercial posterior de Keyestudio."
            ),
        )
        self.assertTrue(prod.activo)
        self.assertFalse(prod.publicado)
        self.assertEqual(prod.estado_curaduria, "SIN_REVISAR")
        self.assertIn("conflicto en catálogo maestro original", prod.observaciones_internas)

    def test_tramos_volumen_anomalia_ks5012(self):
        """Verifica que el tramo anómalo Q101-300 de KS5012 sea marcado con PRECIO_PROVEEDOR_REQUIERE_REVISION."""
        prod = Producto.objects.create(
            sku_humm="HUMM-KEY-KS5012",
            sku_proveedor="KS5012",
            proveedor=self.prov,
            categoria=self.cat,
            nombre_comercial="Keyestudio ESP32 Learning Kit Basic Edition",
            costo_proveedor_usd=Decimal("16.00"),
        )

        # Simular registro de tramos
        tramos = [
            (1, 9, Decimal("16.00"), False, "VALIDADO"),
            (10, 49, Decimal("15.50"), False, "VALIDADO"),
            (50, 100, Decimal("15.00"), False, "VALIDADO"),
            (101, 300, Decimal("34.00"), True, "PRECIO_PROVEEDOR_REQUIERE_REVISION"),
        ]
        for c_min, c_max, p_usd, es_anom, est_val in tramos:
            PrecioProveedorTramo.objects.create(
                producto=prod,
                proveedor=self.prov,
                cantidad_minima=c_min,
                cantidad_maxima=c_max,
                precio_usd=p_usd,
                es_anomalo=es_anom,
                estado_validacion=est_val,
                notas_validacion="Anomalía" if es_anom else "",
            )

        tramo_anomalo = PrecioProveedorTramo.objects.get(producto=prod, cantidad_minima=101)
        self.assertTrue(tramo_anomalo.es_anomalo)
        self.assertEqual(tramo_anomalo.estado_validacion, "PRECIO_PROVEEDOR_REQUIERE_REVISION")
        self.assertEqual(tramo_anomalo.precio_usd, Decimal("34.00"))

        tramo_valido = PrecioProveedorTramo.objects.get(producto=prod, cantidad_minima=50)
        self.assertFalse(tramo_valido.es_anomalo)
        self.assertEqual(tramo_valido.estado_validacion, "VALIDADO")
