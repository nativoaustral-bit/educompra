from django.contrib import admin
from .models import SolicitudCotizacion, SolicitudItem, CotizacionFormal, CotizacionItem

class SolicitudItemInline(admin.TabularInline):
    model = SolicitudItem
    extra = 0
    readonly_fields = (
        "sku_humm_snapshot",
        "marca_snapshot",
        "modelo_snapshot",
        "nombre_comercial_snapshot",
        "especificacion_neutra_snapshot",
        "cantidad",
        "precio_referencial_unitario_snapshot",
        "subtotal_referencial_snapshot",
    )
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False


class CotizacionItemInline(admin.TabularInline):
    model = CotizacionItem
    extra = 1
    fields = (
        "descripcion_tecnica_neutra_utilizada",
        "cantidad",
        "unidad_medida",
        "precio_unitario_neto_definitivo",
        "subtotal_neto",
        "producto",
    )
    readonly_fields = ("subtotal_neto",)


@admin.register(SolicitudCotizacion)
class SolicitudCotizacionAdmin(admin.ModelAdmin):
    list_display = (
        "codigo_seguimiento",
        "establecimiento",
        "nombre_solicitante",
        "comuna",
        "region",
        "estado",
        "total_referencial_estimado",
        "created_at",
    )
    list_filter = ("estado", "region", "created_at")
    search_fields = (
        "codigo_seguimiento",
        "nombre_solicitante",
        "establecimiento",
        "email",
        "telefono",
    )
    inlines = [SolicitudItemInline]

    fieldsets = (
        ("Identificación de la Solicitud", {
            "fields": (
                "codigo_seguimiento",
                "estado",
                "total_referencial_estimado",
                "created_at",
                "updated_at",
            )
        }),
        ("Datos del Profesor / Solicitante", {
            "fields": (
                "nombre_solicitante",
                "email",
                "telefono",
                "establecimiento",
                "comuna",
                "region",
                "observaciones",
            )
        }),
        ("Datos Institucionales para Compra", {
            "fields": (
                "institucion_responsable_compra",
                "contacto_adquisiciones_nombre",
                "contacto_adquisiciones_email",
            )
        }),
        ("Seguimiento Mercado Público", {
            "fields": (
                "id_licitacion_mp",
                "id_compra_agil_mp",
                "id_orden_compra_mp",
            ),
            "classes": ("collapse",)
        }),
        ("Gestión Interna Humm", {
            "fields": (
                "notas_internas_humm",
            )
        }),
    )
    readonly_fields = ("codigo_seguimiento", "created_at", "updated_at")


@admin.register(CotizacionFormal)
class CotizacionFormalAdmin(admin.ModelAdmin):
    list_display = (
        "numero_cotizacion",
        "solicitud",
        "fecha_emision",
        "validez_dias",
        "subtotal_neto",
        "iva",
        "total",
    )
    list_filter = ("fecha_emision",)
    search_fields = ("numero_cotizacion", "solicitud__establecimiento")
    inlines = [CotizacionItemInline]
