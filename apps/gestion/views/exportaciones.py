"""
Vistas de exportación segura de datos en formato CSV (/gestion/exportar/<recurso>/).
Genera archivos con codificación UTF-8 con BOM (utf-8-sig) para compatibilidad nativa con Microsoft Excel.
"""

import csv
from django.http import HttpResponse, Http404
from django.utils import timezone
from apps.gestion.decorators import gestion_required
from apps.catalogo.models import Producto
from apps.cotizaciones.models import SolicitudCotizacion, Establecimiento, Contacto


@gestion_required
def exportar_csv_view(request, recurso):
    """
    Exporta datos en formato CSV para: productos, solicitudes, establecimientos y contactos.
    """
    fecha_str = timezone.now().strftime("%Y%m%d_%H%M")
    response = HttpResponse(content_type="text/csv; charset=utf-8-sig")
    writer = csv.writer(response)

    if recurso == "productos":
        response["Content-Disposition"] = f'attachment; filename="educompra_productos_{fecha_str}.csv"'
        writer.writerow([
            "SKU Humm", "SKU Proveedor", "Nombre Comercial", "Categoría",
            "Marca", "Modelo", "Unidad", "Costo USD", "Costo Chile CLP",
            "Precio Neto CLP", "Precio Total CLP", "Publicado", "Estado Curaduría",
            "Validación Técnica", "Disponibilidad", "Última Actualización"
        ])
        for p in Producto.objects.all().select_related("categoria"):
            writer.writerow([
                p.sku_humm,
                p.sku_proveedor,
                p.nombre_comercial,
                p.categoria.nombre if p.categoria else "Sin categoría",
                p.marca,
                p.modelo,
                p.unidad_compra,
                p.costo_proveedor_usd,
                int(round(p.costo_puesto_chile_clp)),
                int(round(p.precio_sugerido_neto_clp)),
                int(round(p.precio_sugerido_total_clp)),
                "Sí" if p.publicado else "No",
                p.get_estado_curaduria_display(),
                p.get_estado_especificacion_neutral_display(),
                p.get_estado_stock_display(),
                p.updated_at.strftime("%Y-%m-%d %H:%M"),
            ])
        return response

    elif recurso == "solicitudes":
        response["Content-Disposition"] = f'attachment; filename="educompra_solicitudes_{fecha_str}.csv"'
        writer.writerow([
            "Código", "Fecha", "Docente", "Email", "Teléfono", "Cargo",
            "Establecimiento", "Tipo Institución", "Comuna", "Región",
            "RUT", "Total Referencial CLP", "Estado", "Responsable Humm",
            "Es Prueba", "Fuente Origen", "UTM Campaign"
        ])
        for s in SolicitudCotizacion.objects.all().select_related("responsable"):
            writer.writerow([
                s.codigo_seguimiento,
                s.created_at.strftime("%Y-%m-%d %H:%M"),
                s.nombre_solicitante,
                s.email,
                s.telefono,
                s.cargo_solicitante,
                s.establecimiento,
                s.tipo_institucion,
                s.comuna,
                s.region,
                s.rut_institucion,
                int(round(s.total_referencial_estimado)),
                s.get_estado_display(),
                s.responsable.get_full_name() or s.responsable.username if s.responsable else "Sin asignar",
                "Sí" if s.es_prueba else "No",
                s.fuente_origen,
                s.utm_campaign,
            ])
        return response

    elif recurso == "establecimientos":
        response["Content-Disposition"] = f'attachment; filename="educompra_establecimientos_{fecha_str}.csv"'
        writer.writerow([
            "Nombre", "RUT", "RBD", "Tipo Institución", "Comuna", "Región",
            "Estado Conciliación", "Primera Interacción", "Última Interacción"
        ])
        for e in Establecimiento.objects.all():
            writer.writerow([
                e.nombre,
                e.rut,
                e.rbd,
                e.get_tipo_institucion_display() if e.tipo_institucion else "",
                e.comuna,
                e.region,
                e.get_estado_conciliacion_display(),
                e.primera_interaccion.strftime("%Y-%m-%d %H:%M") if e.primera_interaccion else "",
                e.ultima_interaccion.strftime("%Y-%m-%d %H:%M") if e.ultima_interaccion else "",
            ])
        return response

    elif recurso == "contactos":
        response["Content-Disposition"] = f'attachment; filename="educompra_contactos_{fecha_str}.csv"'
        writer.writerow([
            "Nombre", "Email", "Teléfono", "Cargo", "Establecimiento Principal",
            "Es Compras", "Posible Duplicado", "Primera Interacción", "Última Interacción"
        ])
        for c in Contacto.objects.all().select_related("establecimiento_principal"):
            writer.writerow([
                c.nombre,
                c.email,
                c.telefono,
                c.cargo,
                c.establecimiento_principal.nombre if c.establecimiento_principal else "",
                "Sí" if c.es_encargado_compras else "No",
                "Sí" if c.posible_duplicado else "No",
                c.primera_interaccion.strftime("%Y-%m-%d %H:%M") if c.primera_interaccion else "",
                c.ultima_interaccion.strftime("%Y-%m-%d %H:%M") if c.ultima_interaccion else "",
            ])
        return response

    raise Http404("Recurso de exportación no válido.")
