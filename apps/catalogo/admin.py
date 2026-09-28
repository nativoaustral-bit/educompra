from django.contrib import admin
from .models import Proveedor, Categoria, Producto, ProductoImagen

class ProductoImagenInline(admin.TabularInline):
    model = ProductoImagen
    extra = 1
    fields = ("archivo", "nombre_archivo_original", "es_principal", "orden")

@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ("nombre", "codigo", "moneda_origen", "activo", "updated_at")
    list_filter = ("activo", "moneda_origen")
    search_fields = ("nombre", "codigo")

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "slug", "orden", "activa")
    list_filter = ("activa",)
    search_fields = ("nombre",)
    prepopulated_fields = {"slug": ("nombre",)}

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = (
        "sku_humm",
        "sku_proveedor",
        "nombre_comercial",
        "categoria",
        "costo_proveedor_usd",
        "precio_sugerido_total_clp",
        "publicado",
        "activo",
    )
    list_filter = ("publicado", "activo", "categoria", "proveedor", "estado_stock")
    search_fields = (
        "sku_humm",
        "sku_proveedor",
        "nombre_comercial",
        "titulo_especificacion_neutral",
    )
    list_editable = ("publicado",)
    inlines = [ProductoImagenInline]

    fieldsets = (
        ("Identificación de Abastecimiento", {
            "fields": (
                "sku_humm",
                "sku_proveedor",
                "proveedor",
                "categoria",
            )
        }),
        ("Vista Profesor (Comercial y Pedagógica)", {
            "fields": (
                "marca",
                "modelo",
                "nombre_comercial",
                "descripcion_corta",
                "descripcion_educativa",
                "unidad_compra",
            ),
            "description": "Información presentada al docente en el catálogo público."
        }),
        ("Vista Compra Pública (Especificación Técnica Neutra)", {
            "fields": (
                "titulo_especificacion_neutral",
                "especificacion_tecnica_neutral",
                "criterios_equivalencia",
            ),
            "description": "REGLA OBLIGATORIA: Sin marcas ni SKUs. Utilizada para cotizaciones institucionales y Mercado Público."
        }),
        ("Costos y Precios Sugeridos", {
            "fields": (
                "costo_proveedor_usd",
                "costo_puesto_chile_clp",
                "porcentaje_recargo",
                "precio_sugerido_neto_clp",
                "precio_sugerido_total_clp",
            ),
            "description": "Precios calculados dinámicamente como sugerencia referencial."
        }),
        ("Gestión y Disponibilidad", {
            "fields": (
                "publicado",
                "activo",
                "destacado",
                "estado_stock",
                "dias_entrega_estimados",
                "observaciones_internas",
            )
        }),
    )

    actions = ["publicar_seleccionados", "despublicar_seleccionados", "recalcular_precios"]

    @admin.action(description="Publicar productos seleccionados en EduCompra")
    def publicar_seleccionados(self, request, queryset):
        filas = queryset.update(publicado=True)
        self.message_user(request, f"{filas} productos han sido publicados exitosamente.")

    @admin.action(description="Despublicar productos seleccionados")
    def despublicar_seleccionados(self, request, queryset):
        filas = queryset.update(publicado=False)
        self.message_user(request, f"{filas} productos han sido despublicados.")

    @admin.action(description="Recalcular precios sugeridos con parámetros vigentes")
    def recalcular_precios(self, request, queryset):
        for prod in queryset:
            prod.calcular_precios_sugeridos()
            prod.save()
        self.message_user(request, f"Precios sugeridos recalculados para {queryset.count()} productos.")
