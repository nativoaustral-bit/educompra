from django.contrib import admin
from .models import ConfiguracionPricing

@admin.register(ConfiguracionPricing)
class ConfiguracionPricingAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "tipo_cambio_usd_clp",
        "recargo_general_porcentaje",
        "factor_internacion_flete_porcentaje",
        "iva_porcentaje",
        "email_notificaciones_humm",
        "updated_at",
    )
    fieldsets = (
        ("Parámetros Cambiarios y Costos", {
            "fields": (
                "tipo_cambio_usd_clp",
                "factor_internacion_flete_porcentaje",
            ),
            "description": "Valores para calcular el costo estimado de los productos puestos en Chile."
        }),
        ("Política de Precios Sugeridos (Humm)", {
            "fields": (
                "recargo_general_porcentaje",
                "iva_porcentaje",
            ),
            "description": "El recargo general genera el precio referencial sugerido. En cada cotización el administrador puede ajustar los precios definitivos."
        }),
        ("Notificaciones Operacionales", {
            "fields": (
                "email_notificaciones_humm",
            ),
        }),
    )

    def has_add_permission(self, request):
        # Impedir agregar más de una instancia si ya existe (Singleton)
        return not ConfiguracionPricing.objects.exists()

    def has_delete_permission(self, request, obj=None):
        # Impedir borrar la configuración base
        return False
