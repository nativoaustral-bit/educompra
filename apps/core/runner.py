from django.test.runner import DiscoverRunner

class EduCompraTestRunner(DiscoverRunner):
    """
    Test runner personalizado que ejecuta automáticamente la suite de todas las apps
    del proyecto si no se especifican etiquetas de prueba en la línea de comandos.
    """
    def build_suite(self, test_labels=None, extra_tests=None, **kwargs):
        if not test_labels:
            test_labels = ["apps.core.tests", "apps.catalogo.tests", "apps.cotizaciones.tests"]
        return super().build_suite(test_labels=test_labels, extra_tests=extra_tests, **kwargs)
