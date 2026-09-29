from decimal import Decimal
from unittest.mock import patch
from django.test import TestCase, Client, override_settings
from django.urls import reverse
from apps.core.models import ConfiguracionPricing

@override_settings(SECURE_SSL_REDIRECT=False)
class HealthCheckAndPricingTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_health_check_returns_200_and_minimal_json(self):
        """Verifica que /health/ retorne 200 y sólo el payload mínimo requerido sin filtrar datos sensibles."""
        url = reverse("core:health")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data, {"status": "ok", "db": "ok"})
        # Asegurar que NO se expongan versiones, servidores ni paths
        self.assertNotIn("version", data)
        self.assertNotIn("server", data)
        self.assertNotIn("database_name", data)
        self.assertNotIn("django", data)

    def test_health_check_returns_503_on_db_failure(self):
        """Verifica que /health/ retorne 503 si la conexión a base de datos falla."""
        with patch("django.db.connection.cursor", side_effect=Exception("Database down")):
            url = reverse("core:health")
            response = self.client.get(url)
            self.assertEqual(response.status_code, 503)
            self.assertEqual(response.json(), {"status": "error", "db": "error"})

    def test_home_view_returns_200(self):
        """Verifica que la página de bienvenida responda 200."""
        url = reverse("core:home")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "EduCompra")

    def test_configuracion_pricing_singleton(self):
        """Verifica que solo exista una instancia de configuración (Singleton con pk=1)."""
        config1 = ConfiguracionPricing.get_solo()
        self.assertEqual(config1.pk, 1)

        config2 = ConfiguracionPricing.objects.create(
            tipo_cambio_usd_clp=Decimal("990.00"),
            recargo_general_porcentaje=Decimal("85.00")
        )
        self.assertEqual(config2.pk, 1)
        self.assertEqual(ConfiguracionPricing.objects.count(), 1)
        self.assertEqual(ConfiguracionPricing.get_solo().tipo_cambio_usd_clp, Decimal("990.00"))
