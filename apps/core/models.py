import os
from decimal import Decimal
from django.db import models
from django.core.validators import MinValueValidator

class ConfiguracionPricing(models.Model):
    """
    Configuración global y administrable de parámetros de precios para EduCompra Humm.
    Implementa un patrón Singleton para asegurar una única instancia de parámetros.
    """
    tipo_cambio_usd_clp = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal(os.getenv("TIPO_CAMBIO_DEFAULT", "950.00")),
        validators=[MinValueValidator(Decimal("1.00"))],
        verbose_name="Tipo de Cambio (USD a CLP)",
        help_text="Valor referencial del dólar para calcular costos en pesos chilenos."
    )
    recargo_general_porcentaje = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=Decimal(os.getenv("RECARGO_GENERAL_DEFAULT", "80.00")),
        validators=[MinValueValidator(Decimal("0.00"))],
        verbose_name="Recargo Comercial Sugerido (%)",
        help_text="Porcentaje de margen sugerido sobre el costo internado (ej: 80.00%). Administrable, no codificado rígidamente."
    )
    factor_internacion_flete_porcentaje = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=Decimal(os.getenv("FACTOR_INTERNACION_DEFAULT", "15.00")),
        validators=[MinValueValidator(Decimal("0.00"))],
        verbose_name="Factor Estimado de Flete e Internación (%)",
        help_text="Porcentaje estimado de costos de aduana y transporte internacional."
    )
    iva_porcentaje = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=Decimal(os.getenv("IVA_DEFAULT", "19.00")),
        validators=[MinValueValidator(Decimal("0.00"))],
        verbose_name="IVA (%)",
        help_text="Porcentaje de Impuesto al Valor Agregado en Chile (19%)."
    )
    email_notificaciones_humm = models.EmailField(
        default=os.getenv("EMAIL_NOTIFICACIONES_DEFAULT", "contacto@humm.cl"),
        verbose_name="Email Notificaciones Humm",
        help_text="Dirección de correo que recibe avisos cuando un profesor solicita cotización."
    )
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Última Actualización")

    class Meta:
        verbose_name = "Parámetros de Pricing y Configuración"
        verbose_name_plural = "Parámetros de Pricing y Configuración"

    def __str__(self):
        return f"Configuración Pricing (TC: ${self.tipo_cambio_usd_clp} | Recargo: {self.recargo_general_porcentaje}%)"

    def save(self, *args, **kwargs):
        # Garantizar que siempre se use id=1 (patrón Singleton)
        self.pk = 1
        if kwargs.get("force_insert"):
            if ConfiguracionPricing.objects.filter(pk=1).exists():
                kwargs.pop("force_insert", None)
        super().save(*args, **kwargs)

    @classmethod
    def get_solo(cls):
        """Obtiene la instancia única de configuración o la crea con valores por defecto."""
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj
