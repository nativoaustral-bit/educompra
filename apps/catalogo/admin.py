from django.contrib import admin
from django.utils.html import format_html
from .models import Proveedor, Categoria, TecnologiaCompatible, Producto, ProductoImagen


class TieneImagenFilter(admin.SimpleListFilter):
    title = "Tiene Fotografía"
    parameter_name = "tiene_imagen"

    def lookups(self, request, model_admin):
        return (
            ("si", "Con fotografía"),
            ("no", "Sin fotografía"),
        )

    def queryset(self, request, queryset):
        if self.value() == "si":
            return queryset.filter(imagenes__isnull=False).distinct()
        if self.value() == "no":
            return queryset.filter(imagenes__isnull=True)
        return queryset


class ProductoImagenInline(admin.TabularInline):
    model = ProductoImagen
    extra = 1
    fields = ("vista_previa", "archivo", "nombre_archivo_original", "es_principal", "orden")
    readonly_fields = ("vista_previa",)

    @admin.display(description="Vista Previa")
    def vista_previa(self, obj):
        if obj.archivo:
            return format_html(
                '<img src="{}" style="height: 60px; width: 60px; object-fit: contain; border-radius: 4px; border: 1px solid #ccc; background: #fff;" />',
                obj.archivo.url,
            )
        return format_html('<span style="color: #999;">Sin imagen</span>')


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


@admin.register(TecnologiaCompatible)
class TecnologiaCompatibleAdmin(admin.ModelAdmin):
    list_display = ("nombre", "slug", "orden", "activa")
    list_filter = ("activa",)
    search_fields = ("nombre",)
    prepopulated_fields = {"slug": ("nombre",)}


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = (
        "miniatura_admin",
        "sku_humm",
        "sku_proveedor",
        "nombre_comercial",
        "categoria",
        "badge_curaduria",
        "badge_especificacion_neutral",
        "nivel_dificultad",
        "apto_para_kit",
        "precio_sugerido_total_clp",
        "publicado",
        "activo",
    )
    list_filter = (
        "estado_curaduria",
        "estado_especificacion_neutral",
        "nivel_dificultad",
        "apto_para_kit",
        TieneImagenFilter,
        "categoria",
        "tecnologias_compatibles",
        "publicado",
        "activo",
        "proveedor",
        "estado_stock",
    )
    search_fields = (
        "sku_humm",
        "sku_proveedor",
        "nombre_comercial",
        "titulo_especificacion_neutral",
        "nombre_original_proveedor",
    )
    list_editable = ("publicado",)
    filter_horizontal = ("tecnologias_compatibles",)
    inlines = [ProductoImagenInline]

    @admin.display(description="Foto")
    def miniatura_admin(self, obj):
        img = obj.imagenes.filter(es_principal=True).first() or obj.imagenes.first()
        if img and img.archivo:
            return format_html(
                '<img src="{}" style="width: 42px; height: 42px; object-fit: contain; border-radius: 4px; border: 1px solid #ddd; background: #fafafa;" />',
                img.archivo.url,
            )
        return format_html('<span style="color: #aaa; font-size: 11px;">(Sin foto)</span>')

    @admin.display(description="Curaduría", ordering="estado_curaduria")
    def badge_curaduria(self, obj):
        colores = {
            "SIN_REVISAR": ("#64748b", "#f1f5f9"),
            "CANDIDATO": ("#0284c7", "#e0f2fe"),
            "DESCARTADO_CATALOGO_PUBLICO": ("#94a3b8", "#f8fafc"),
            "EN_CURADURIA": ("#d97706", "#fef3c7"),
            "VALIDADO": ("#059669", "#d1fae5"),
            "LISTO_PARA_PUBLICAR": ("#7c3aed", "#ede9fe"),
        }
        texto = obj.get_estado_curaduria_display()
        fg, bg = colores.get(obj.estado_curaduria, ("#475569", "#f1f5f9"))
        return format_html(
            '<span style="background-color: {}; color: {}; padding: 3px 8px; border-radius: 12px; font-size: 11px; font-weight: 600; white-space: nowrap;">{}</span>',
            bg, fg, texto
        )

    @admin.display(description="Espec. Neutra", ordering="estado_especificacion_neutral")
    def badge_especificacion_neutral(self, obj):
        colores = {
            "NO_REVISADO": ("#dc2626", "#fee2e2", "⏳ No revisado"),
            "BORRADOR": ("#ea580c", "#ffedd5", "📝 Borrador"),
            "VALIDADO_HUMM": ("#16a34a", "#dcfce7", "✔ Validado Humm"),
        }
        fg, bg, label = colores.get(obj.estado_especificacion_neutral, ("#64748b", "#f1f5f9", obj.estado_especificacion_neutral))
        return format_html(
            '<span style="background-color: {}; color: {}; padding: 3px 8px; border-radius: 12px; font-size: 11px; font-weight: 600; white-space: nowrap;">{}</span>',
            bg, fg, label
        )

    fieldsets = (
        ("Identificación y Trazabilidad de Abastecimiento", {
            "fields": (
                "sku_humm",
                "sku_proveedor",
                "proveedor",
                "marca",
                "modelo",
                "nombre_original_proveedor",
            )
        }),
        ("Curaduría Pedagógica y Calidad (Humm)", {
            "fields": (
                "estado_curaduria",
                "categoria",
                "nivel_dificultad",
                "tecnologias_compatibles",
                "apto_para_kit",
            ),
            "description": "Clasificación docente y selección para el catálogo público de EduCompra."
        }),
        ("Vista Profesor (Comercial y Aplicación en Aula)", {
            "fields": (
                "nombre_comercial",
                "descripcion_corta",
                "uso_educativo",
                "descripcion_educativa",
                "unidad_compra",
            ),
            "description": "Información presentada al docente en el catálogo público."
        }),
        ("Vista Compra Pública (Especificación Técnica Neutra)", {
            "fields": (
                "estado_especificacion_neutral",
                "titulo_especificacion_neutral",
                "especificacion_tecnica_neutral",
                "criterios_equivalencia",
            ),
            "description": "REGLA OBLIGATORIA: Sin marcas ni SKUs. Solo productos con estado VALIDADO_HUMM pueden emitir cotización formal."
        }),
        ("Costos y Precios Sugeridos", {
            "fields": (
                "costo_proveedor_usd",
                "costo_puesto_chile_clp",
                "porcentaje_recargo",
                "precio_sugerido_neto_clp",
                "precio_sugerido_total_clp",
            ),
            "description": "Precios calculados dinámicamente según parámetros oficiales de pricing."
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

    actions = [
        "marcar_como_candidatos",
        "descartar_de_catalogo_publico",
        "iniciar_curaduria",
        "marcar_apto_kit",
        "desmarcar_apto_kit",
        "recalcular_precios",
    ]

    @admin.action(description="Marcar seleccionados como CANDIDATO a catálogo público")
    def marcar_como_candidatos(self, request, queryset):
        filas = queryset.update(estado_curaduria="CANDIDATO")
        self.message_user(request, f"{filas} productos han sido marcados como CANDIDATO.")

    @admin.action(description="Descartar de catálogo público (conservar en catálogo maestro)")
    def descartar_de_catalogo_publico(self, request, queryset):
        filas = queryset.update(estado_curaduria="DESCARTADO_CATALOGO_PUBLICO")
        self.message_user(request, f"{filas} productos han sido marcados como DESCARTADO_CATALOGO_PUBLICO.")

    @admin.action(description="Iniciar proceso de curaduría pedagógica")
    def iniciar_curaduria(self, request, queryset):
        filas = queryset.update(estado_curaduria="EN_CURADURIA")
        self.message_user(request, f"{filas} productos han pasado a EN_CURADURIA.")

    @admin.action(description="Marcar como APTO PARA KIT educativo")
    def marcar_apto_kit(self, request, queryset):
        filas = queryset.update(apto_para_kit=True)
        self.message_user(request, f"{filas} productos marcados como aptos para kits.")

    @admin.action(description="Desmarcar aptitud para kits")
    def desmarcar_apto_kit(self, request, queryset):
        filas = queryset.update(apto_para_kit=False)
        self.message_user(request, f"{filas} productos desmarcados de kits.")

    @admin.action(description="Recalcular precios sugeridos con parámetros vigentes")
    def recalcular_precios(self, request, queryset):
        for prod in queryset:
            prod.calcular_precios_sugeridos()
            prod.save()
        self.message_user(request, f"Precios sugeridos recalculados para {queryset.count()} productos.")
