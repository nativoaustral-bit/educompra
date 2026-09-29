from django.contrib import admin
from django.utils.html import format_html
from .models import SolicitudCotizacion, SolicitudItem, CotizacionFormal, CotizacionItem


class SolicitudItemInline(admin.TabularInline):
    model = SolicitudItem
    extra = 0
    readonly_fields = (
        "sku_humm_snapshot",
        "sku_proveedor_snapshot",
        "nombre_comercial_snapshot",
        "unidad_comercial_snapshot",
        "cantidad",
        "precio_referencial_unitario_snapshot",
        "subtotal_referencial_snapshot",
        "estado_validacion_tecnica",
    )
    fields = (
        "sku_humm_snapshot",
        "sku_proveedor_snapshot",
        "nombre_comercial_snapshot",
        "unidad_comercial_snapshot",
        "cantidad",
        "precio_referencial_unitario_snapshot",
        "subtotal_referencial_snapshot",
        "estado_validacion_tecnica",
    )
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False

    def estado_validacion_tecnica(self, obj):
        if not obj.producto:
            return format_html('<span style="color:#64748b;">(Sin producto vinculado)</span>')
        estado = obj.producto.estado_especificacion_neutral
        if estado == "VALIDADO_HUMM":
            return format_html('<span style="color:#15803d; font-weight:600;">✅ VALIDADO HUMM (Apto Licitación)</span>')
        elif estado == "BORRADOR":
            return format_html('<span style="color:#b45309; font-weight:600;">🟡 En Redacción Técnica</span>')
        else:
            return format_html('<span style="color:#dc2626; font-weight:600;">⚠️ Borrador No Validado</span>')
    estado_validacion_tecnica.short_description = "Validación Compra Pública"


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
        "region",
        "estado",
        "alerta_validacion",
        "total_referencial_estimado",
        "created_at",
    )
    list_filter = ("estado", "region", "tipo_institucion", "created_at")
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
                "token",
                "estado",
                "total_referencial_estimado",
                "created_at",
                "updated_at",
            )
        }),
        ("Datos del Profesor / Solicitante", {
            "fields": (
                "nombre_solicitante",
                "cargo_solicitante",
                "email",
                "telefono",
                "establecimiento",
                "tipo_institucion",
                "comuna",
                "region",
                "observaciones",
            )
        }),
        ("Contexto del Proyecto Educativo", {
            "fields": (
                "proyecto_educativo",
                "fecha_requerida_aproximada",
            )
        }),
        ("Datos Institucionales para Compra", {
            "fields": (
                "institucion_responsable_compra",
                "rut_institucion",
                "nombre_encargado_compras",
                "email_encargado_compras",
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
    readonly_fields = ("codigo_seguimiento", "token", "created_at", "updated_at")

    def alerta_validacion(self, obj):
        if obj.requiere_validacion_tecnica:
            return format_html(
                '<span style="background:#fee2e2; color:#b91c1c; padding:3px 8px; border-radius:4px; font-weight:600;">'
                '⚠️ Requiere Validación'
                '</span>'
            )
        return format_html(
            '<span style="background:#dcfce7; color:#15803d; padding:3px 8px; border-radius:4px; font-weight:600;">'
            '✅ Especificaciones Validadas'
            '</span>'
        )
    alerta_validacion.short_description = "Estado Compra Pública"


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
