import tempfile
from decimal import Decimal
from pathlib import Path
import openpyxl

from django.test import TestCase, override_settings
from django.core.management import call_command
from django.conf import settings

from apps.catalogo.models import Producto, Categoria, Proveedor, ProductoImagen
from apps.catalogo.management.commands.importar_catalogo_keyestudio import parse_precio_usd
from apps.core.models import ConfiguracionPricing


@override_settings(SECURE_SSL_REDIRECT=False)
class ImportadorKeyestudioTests(TestCase):
    def setUp(self):
        # Asegurar parámetros de pricing base
        self.pricing = ConfiguracionPricing.get_solo()
        self.pricing.tipo_cambio_usd_clp = Decimal("950.00")
        self.pricing.factor_internacion_flete_porcentaje = Decimal("15.00")
        self.pricing.recargo_general_porcentaje = Decimal("80.00")
        self.pricing.iva_porcentaje = Decimal("19.00")
        self.pricing.save()

    def test_parse_precio_usd(self):
        """Verifica la normalización de múltiples formatos de precio en texto a Decimal."""
        self.assertEqual(parse_precio_usd("11.99 USD"), Decimal("11.99"))
        self.assertEqual(parse_precio_usd("$ 11.99"), Decimal("11.99"))
        self.assertEqual(parse_precio_usd(" 11,99 USD "), Decimal("11.99"))
        self.assertEqual(parse_precio_usd("1,250.50 USD"), Decimal("1250.50"))
        self.assertEqual(parse_precio_usd(15.5), Decimal("15.50"))
        self.assertIsNone(parse_precio_usd(""))
        self.assertIsNone(parse_precio_usd(None))
        self.assertIsNone(parse_precio_usd("N/A"))

    def _crear_excel_prueba(self, filas):
        """Crea un archivo Excel temporal para pruebas con los 5 encabezados reales."""
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Productos"
        ws.append([
            "SKU o ID",
            "Descripción del producto",
            "Miniatura",
            "Precio (USD)",
            "Imagen alta resolución"
        ])
        for fila in filas:
            ws.append(fila)

        temp_dir = tempfile.mkdtemp()
        excel_path = Path(temp_dir) / "test_catalogo.xlsx"
        wb.save(excel_path)
        wb.close()
        return excel_path

    def test_dry_run_no_modifica_base_de_datos(self):
        """Verifica que el modo --dry-run clasifique duplicados y no escriba en BD."""
        filas = [
            ["KS0001", "Sensor de Humedad V1", "mini1.jpg", "10.00 USD", "hd1.jpg"],
            ["KS0002", "Placa Desarrollo Uno", "mini2.jpg", "15.00 USD", "hd2.jpg"],
            # Duplicado idéntico
            ["KS0002", "Placa Desarrollo Uno", "mini2.jpg", "15.00 USD", "hd2.jpg"],
            # Duplicado conflictivo (mismo SKU, precio y texto distinto)
            ["KS0003", "Kit Robótica Básico", "", "25.00 USD", ""],
            ["KS0003", "Kit Robótica Avanzado", "", "35.00 USD", ""],
            # Fila sin SKU
            ["", "Producto Fantasma", "", "5.00 USD", ""],
            # Fila sin precio
            ["KS0004", "Motor Servo", "", "", ""],
        ]
        excel_path = self._crear_excel_prueba(filas)
        reporte_path = excel_path.parent / "reporte_test.md"

        call_command(
            "importar_catalogo_keyestudio",
            excel=str(excel_path),
            dry_run=True,
            reporte=str(reporte_path),
        )

        # Cero productos en BD
        self.assertEqual(Producto.objects.count(), 0)

        # Verificar que el reporte se generó y contiene el análisis
        self.assertTrue(reporte_path.exists())
        contenido = reporte_path.read_text(encoding="utf-8")
        self.assertIn("Duplicados Idénticos", contenido)
        self.assertIn("KS0002", contenido)
        self.assertIn("Duplicados Conflictivos", contenido)
        self.assertIn("KS0003", contenido)
        self.assertIn("CONFLICTO — REQUIERE REVISIÓN", contenido)

    def test_importacion_real_y_upsert_no_destructivo(self):
        """
        Verifica que la importación real:
        1. Cree productos despublicados en 'Sin clasificar'.
        2. Aplique la fórmula de pricing con recargo comercial.
        3. Excluya los duplicados conflictivos.
        4. Al re-importar con nuevos costos, preserve los campos curados por Humm.
        """
        filas = [
            ["KS0010", "Sensor Temperatura", "mini.jpg", "5.00 USD", "hd.jpg"],
            # Duplicado idéntico consolidado
            ["KS0020", "Kit Arduino", "", "20.00 USD", ""],
            ["KS0020", "Kit Arduino", "", "20.00 USD", ""],
            # Conflictivo excluido
            ["KS0030", "Versión A", "", "10.00 USD", ""],
            ["KS0030", "Versión B", "", "12.00 USD", ""],
        ]
        excel_path = self._crear_excel_prueba(filas)

        # 1. Primera importación real
        call_command("importar_catalogo_keyestudio", excel=str(excel_path))

        # KS0010 y KS0020 creados; KS0030 excluido por conflicto
        self.assertEqual(Producto.objects.count(), 2)
        p1 = Producto.objects.get(sku_proveedor="KS0010")
        self.assertFalse(p1.publicado)
        self.assertEqual(p1.categoria.nombre, "Sin clasificar")
        self.assertEqual(p1.costo_proveedor_usd, Decimal("5.00"))

        # Validar cálculo de precio con recargo comercial de 80%
        # 5 USD * 950 * 1.15 * 1.80 * 1.19 = 11,701 CLP
        self.assertEqual(p1.precio_sugerido_total_clp, Decimal("11701.00"))

        # 2. Simular curaduría manual por parte de Humm en Fase 3
        cat_curada, _ = Categoria.objects.get_or_create(nombre="Sensores y Módulos", defaults={"slug": "sensores"})
        p1.nombre_comercial = "Sensor Digital de Temperatura de Precisión"
        p1.descripcion_educativa = "Ideal para proyectos de monitoreo ambiental escolar con microcontrolador."
        p1.categoria = cat_curada
        p1.especificacion_tecnica_neutral = "Sensor de temperatura digital con protocolo de comunicación 1-wire."
        p1.publicado = True
        p1.save()

        # 3. Segunda importación (fábrica sube el costo a 6.00 USD)
        filas_actualizadas = [
            ["KS0010", "Sensor Temperatura New Batch", "mini.jpg", "6.00 USD", "hd.jpg"],
            ["KS0020", "Kit Arduino", "", "20.00 USD", ""],
        ]
        excel_path_v2 = self._crear_excel_prueba(filas_actualizadas)
        call_command("importar_catalogo_keyestudio", excel=str(excel_path_v2), actualizar_costos=True)

        # Recargar producto desde BD
        p1.refresh_from_db()

        # Costo y precios actualizados
        self.assertEqual(p1.costo_proveedor_usd, Decimal("6.00"))
        # 6 USD * 950 * 1.15 * 1.80 * 1.19 = 14,041 CLP
        self.assertEqual(p1.precio_sugerido_total_clp, Decimal("14041.00"))

        # BLINDAJE CONFIRMADO: Los campos curados se mantuvieron intactos
        self.assertEqual(p1.nombre_comercial, "Sensor Digital de Temperatura de Precisión")
        self.assertEqual(p1.descripcion_educativa, "Ideal para proyectos de monitoreo ambiental escolar con microcontrolador.")
        self.assertEqual(p1.categoria.nombre, "Sensores y Módulos")
        self.assertEqual(p1.especificacion_tecnica_neutral, "Sensor de temperatura digital con protocolo de comunicación 1-wire.")
        self.assertTrue(p1.publicado)

    def test_asociacion_imagenes_y_placeholder(self):
        """Verifica la vinculación física de imágenes, optimización y fallback a placeholder."""
        from PIL import Image

        temp_dir = Path(tempfile.mkdtemp())
        img_dir = temp_dir / "imagenes"
        img_dir.mkdir()

        # Crear una imagen real de prueba para KS0050
        test_img_path = img_dir / "KS0050.jpg"
        img = Image.new("RGB", (200, 200), color="blue")
        img.save(test_img_path)

        filas = [
            ["KS0050", "Módulo Bluetooth con imagen", "", "8.00 USD", ""],
            ["KS0060", "Módulo WiFi sin imagen", "", "12.00 USD", ""],
        ]
        excel_path = self._crear_excel_prueba(filas)

        call_command(
            "importar_catalogo_keyestudio",
            excel=str(excel_path),
            imagenes=str(img_dir),
        )

        p_con_img = Producto.objects.get(sku_proveedor="KS0050")
        self.assertEqual(p_con_img.imagenes.count(), 1)
        img_record = p_con_img.imagenes.first()
        self.assertTrue(img_record.es_principal)
        self.assertIn("KS0050", img_record.archivo.name)
        self.assertIn("/media/productos/KS0050", p_con_img.imagen_principal_url)

        p_sin_img = Producto.objects.get(sku_proveedor="KS0060")
        self.assertEqual(p_sin_img.imagenes.count(), 0)
        self.assertEqual(p_sin_img.imagen_principal_url, "/static/img/placeholder_producto.svg")

