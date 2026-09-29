import re
from decimal import Decimal
from pathlib import Path
from django.test import TestCase
from django.core.management import call_command
from django.contrib.admin.sites import site
from django.conf import settings

from apps.catalogo.models import Proveedor, Categoria, TecnologiaCompatible, Producto
from apps.catalogo.admin import ProductoAdmin


class CuraduriaInfraestructuraTests(TestCase):
    """
    Pruebas unitarias de la infraestructura de curaduría educativa de Fase 3:
    - Modelos y relaciones (TecnologiaCompatible, Producto).
    - Regla obligatoria de neutralidad técnica (puede_generar_cotizacion_formal).
    - Ausencia de acciones masivas de validación neutral en Django Admin.
    - Idempotencia del sembrador de taxonomía y tecnologías.
    - Modo de solo lectura del algoritmo de sugerencia de candidatos.
    """

    def setUp(self):
        self.proveedor = Proveedor.objects.create(
            nombre="Keyestudio Test",
            codigo="KEY_TEST",
            moneda_origen="USD",
        )
        self.categoria = Categoria.objects.create(
            nombre="Arduino y controladores",
            slug="arduino-controladores",
            orden=10,
        )
        self.tec_arduino = TecnologiaCompatible.objects.create(
            nombre="Arduino",
            slug="arduino",
            orden=10,
        )
        self.tec_esp32 = TecnologiaCompatible.objects.create(
            nombre="ESP32",
            slug="esp32",
            orden=20,
        )
        self.producto = Producto.objects.create(
            sku_humm="HUMM-KEY-TEST01",
            sku_proveedor="TEST01",
            proveedor=self.proveedor,
            categoria=self.categoria,
            nombre_comercial="Placa de Desarrollo UNO R3 Test",
            nombre_original_proveedor="Keyestudio UNO R3 Development Board",
            costo_proveedor_usd=Decimal("10.00"),
            publicado=False,
            activo=True,
        )

    def test_modelo_tecnologia_compatible(self):
        """Verifica la creación y ManyToMany de TecnologiaCompatible."""
        self.assertEqual(str(self.tec_arduino), "Arduino")
        self.producto.tecnologias_compatibles.add(self.tec_arduino, self.tec_esp32)
        self.assertEqual(self.producto.tecnologias_compatibles.count(), 2)
        self.assertIn(self.tec_arduino, self.producto.tecnologias_compatibles.all())

    def test_valores_por_defecto_curaduria_y_especificacion(self):
        """Verifica que los nuevos productos nazcan con los estados iniciales correctos."""
        prod = Producto.objects.create(
            sku_humm="HUMM-KEY-TEST02",
            sku_proveedor="TEST02",
            proveedor=self.proveedor,
            nombre_comercial="Sensor Test",
            costo_proveedor_usd=Decimal("5.00"),
        )
        self.assertEqual(prod.estado_curaduria, "SIN_REVISAR")
        self.assertEqual(prod.estado_especificacion_neutral, "NO_REVISADO")
        self.assertEqual(prod.nivel_dificultad, "NO_DEFINIDO")
        self.assertFalse(prod.apto_para_kit)
        self.assertFalse(prod.publicado)

    def test_regla_neutralidad_puede_generar_cotizacion_formal(self):
        """
        Regla obligatoria de Humm:
        Solo productos con estado_especificacion_neutral == 'VALIDADO_HUMM'
        pueden emitir cotizaciones formales. NO_REVISADO y BORRADOR deben retornar False.
        """
        self.producto.estado_especificacion_neutral = "NO_REVISADO"
        self.assertFalse(self.producto.puede_generar_cotizacion_formal())

        self.producto.estado_especificacion_neutral = "BORRADOR"
        self.assertFalse(self.producto.puede_generar_cotizacion_formal())

        self.producto.estado_especificacion_neutral = "VALIDADO_HUMM"
        self.assertTrue(self.producto.puede_generar_cotizacion_formal())

    def test_admin_sin_accion_masiva_de_validacion_neutral(self):
        """
        Verifica que la acción masiva validar_especificacion_neutra_humm NO esté disponible
        en ProductoAdmin (la validación técnica requiere revisión humana individual obligatoria).
        """
        model_admin = ProductoAdmin(Producto, site)
        self.assertNotIn("validar_especificacion_neutra_humm", model_admin.actions)

    def test_admin_acciones_masivas_seguras_presentes(self):
        """Verifica que las acciones masivas seguras autorizadas sí estén disponibles."""
        model_admin = ProductoAdmin(Producto, site)
        self.assertIn("marcar_como_candidatos", model_admin.actions)
        self.assertIn("descartar_de_catalogo_publico", model_admin.actions)
        self.assertIn("iniciar_curaduria", model_admin.actions)
        self.assertIn("marcar_apto_kit", model_admin.actions)
        self.assertIn("desmarcar_apto_kit", model_admin.actions)

    def test_poblar_taxonomia_educativa_idempotente(self):
        """
        Verifica que el comando poblar_taxonomia_educativa cree las 11 categorías
        aprobadas más 'Sin clasificar' y las 5 tecnologías controladas, y sea 100% idempotente.
        """
        call_command("poblar_taxonomia_educativa")
        # 11 categorías docentes + 1 'Sin clasificar' = 12 categorías
        self.assertEqual(Categoria.objects.count(), 12)
        # 5 tecnologías controladas: Arduino, ESP32, micro:bit, Raspberry Pi, Otros
        self.assertEqual(TecnologiaCompatible.objects.count(), 5)

        # Ejecutar por segunda vez para verificar idempotencia
        call_command("poblar_taxonomia_educativa")
        self.assertEqual(Categoria.objects.count(), 12)
        self.assertEqual(TecnologiaCompatible.objects.count(), 5)

    def test_sugerir_candidatos_curaduria_solo_lectura(self):
        """
        Verifica que el comando sugerir_candidatos_curaduria no modifique
        ningún registro en la base de datos (modo SOLO LECTURA estricto).
        """
        call_command("poblar_taxonomia_educativa")
        estado_inicial = self.producto.estado_curaduria
        publicado_inicial = self.producto.publicado

        # Ejecutar sugerencia
        test_reporte = Path(settings.BASE_DIR) / "test_candidatos_reporte.md"
        try:
            call_command("sugerir_candidatos_curaduria", reporte=str(test_reporte))
            self.producto.refresh_from_db()

            # Comprobar que no hubo modificaciones en los campos de producto
            self.assertEqual(self.producto.estado_curaduria, estado_inicial)
            self.assertEqual(self.producto.publicado, publicado_inicial)
            self.assertTrue(test_reporte.exists())

            contenido = test_reporte.read_text(encoding="utf-8")
            self.assertIn("CANDIDATOS SUGERIDOS PARA FASE 3", contenido)
            self.assertIn("SOLO LECTURA", contenido)
            self.assertIn("PRIMER PUNTO DE CONTROL", contenido)
        finally:
            if test_reporte.exists():
                test_reporte.unlink()
