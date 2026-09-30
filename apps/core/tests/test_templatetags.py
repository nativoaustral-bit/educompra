"""
Pruebas unitarias para filtros de plantillas en apps/core/templatetags/core_tags.py.
Verifica el correcto funcionamiento del formateo de precios con separador de miles chileno.
"""

from decimal import Decimal
from django.test import TestCase
from django.template import Template, Context
from apps.core.templatetags.core_tags import separador_miles, formato_precio, formato_clp


class CoreTemplateTagsTest(TestCase):
    """Test suite para filtros personalizados de precios y separador de miles."""

    def test_separador_miles_con_decimales_y_enteros(self):
        """Comprueba el separador de miles con punto para valores numéricos."""
        self.assertEqual(separador_miles(Decimal("26912.00")), "26.912")
        self.assertEqual(separador_miles(Decimal("14041.00")), "14.041")
        self.assertEqual(separador_miles(Decimal("4680.00")), "4.680")
        self.assertEqual(separador_miles(Decimal("1234567.89")), "1.234.568")
        self.assertEqual(separador_miles(500), "500")
        self.assertEqual(separador_miles(0), "0")
        self.assertEqual(separador_miles(Decimal("0.00")), "0")

    def test_separador_miles_con_strings_y_vacios(self):
        """Comprueba el manejo robusto de valores en texto y nulos."""
        self.assertEqual(separador_miles("26912"), "26.912")
        self.assertEqual(separador_miles("  14990  "), "14.990")
        self.assertEqual(separador_miles(""), "")
        self.assertEqual(separador_miles(None), "")
        self.assertEqual(separador_miles("texto_invalido"), "texto_invalido")

    def test_formato_precio_alias(self):
        """Verifica que formato_precio sea un alias funcional de separador_miles."""
        self.assertEqual(formato_precio(Decimal("15990.00")), "15.990")
        self.assertEqual(formato_precio(3000), "3.000")

    def test_formato_clp(self):
        """Verifica que formato_clp incluya el prefijo de signo peso y separador de miles."""
        self.assertEqual(formato_clp(Decimal("26912.00")), "$26.912")
        self.assertEqual(formato_clp(500), "$500")
        self.assertEqual(formato_clp(""), "")
        self.assertEqual(formato_clp(None), "")

    def test_render_en_plantilla_django(self):
        """Comprueba que el filtro esté disponible globalmente vía builtins en plantillas."""
        template = Template("Precio: ${{ precio|separador_miles }}")
        rendered = template.render(Context({"precio": Decimal("44859.00")}))
        self.assertEqual(rendered, "Precio: $44.859")

    def test_render_en_plantilla_con_formato_clp(self):
        """Comprueba renderizado directo con formato_clp."""
        template = Template("Valor: {{ precio|formato_clp }}")
        rendered = template.render(Context({"precio": Decimal("99990.00")}))
        self.assertEqual(rendered, "Valor: $99.990")
