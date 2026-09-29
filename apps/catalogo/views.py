"""
Vistas del catálogo público de EduCompra Humm.
Aplica estrictamente la regla única de visibilidad centralizada: Producto.objects.publicables(user).
"""

from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse, Http404
from .models import Producto, Categoria, TecnologiaCompatible

DISCLAIMER_PRECIOS = (
    "Precios referenciales en pesos chilenos con IVA incluido para fines de presupuesto y "
    "postulación a fondos. La cotización formal final será emitida por Humm confirmando "
    "disponibilidad y costos logísticos."
)


def catalogo_lista_view(request):
    """
    Listado del catálogo público con buscador, filtros y ordenamiento.
    Usa la regla centralizada Producto.objects.publicables(user=request.user).
    """
    qs = Producto.objects.publicables(user=request.user).select_related("categoria").prefetch_related("tecnologias_compatibles", "imagenes")

    # Búsqueda por texto (nombre, descripción, sku)
    q = request.GET.get("q", "").strip()
    if q:
        qs = qs.filter(
            Q(nombre_comercial__icontains=q)
            | Q(descripcion_educativa__icontains=q)
            | Q(descripcion_corta__icontains=q)
            | Q(sku_proveedor__icontains=q)
            | Q(sku_humm__icontains=q)
            | Q(marca__icontains=q)
        )

    # Filtro por categoría
    categoria_slug = request.GET.get("categoria", "").strip()
    categoria_activa = None
    if categoria_slug:
        categoria_activa = Categoria.objects.filter(slug=categoria_slug, activa=True).first()
        if categoria_activa:
            qs = qs.filter(categoria=categoria_activa)

    # Filtro por tecnología compatible
    tecnologia_slug = request.GET.get("tecnologia", "").strip()
    tecnologia_activa = None
    if tecnologia_slug:
        tecnologia_activa = TecnologiaCompatible.objects.filter(slug=tecnologia_slug, activa=True).first()
        if tecnologia_activa:
            qs = qs.filter(tecnologias_compatibles=tecnologia_activa)

    # Filtro por nivel de uso / complejidad
    dificultad = request.GET.get("dificultad", "").strip().upper()
    if dificultad in dict(Producto.NIVELES_DIFICULTAD):
        qs = qs.filter(nivel_dificultad=dificultad)

    # Ordenamiento
    orden = request.GET.get("orden", "destacados")
    if orden == "precio_asc":
        qs = qs.order_by("precio_sugerido_total_clp", "nombre_comercial")
    elif orden == "precio_desc":
        qs = qs.order_by("-precio_sugerido_total_clp", "nombre_comercial")
    elif orden == "nombre":
        qs = qs.order_by("nombre_comercial")
    else:  # destacados por defecto
        qs = qs.order_by("-destacado", "nombre_comercial")

    total_encontrados = qs.count()

    # Paginación
    paginator = Paginator(qs, 12)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # Categorías y tecnologías con productos publicables para la barra lateral
    publicables_ids = Producto.objects.publicables(user=request.user).values_list("id", flat=True)
    categorias_disponibles = Categoria.objects.filter(
        productos__id__in=publicables_ids,
        activa=True
    ).distinct().order_by("orden", "nombre")

    tecnologias_disponibles = TecnologiaCompatible.objects.filter(
        productos__id__in=publicables_ids,
        activa=True
    ).distinct().order_by("orden", "nombre")

    # Indicador de modo preview para staff
    es_preview_staff = request.user.is_authenticated and request.user.is_staff

    context = {
        "page_obj": page_obj,
        "total_encontrados": total_encontrados,
        "categorias": categorias_disponibles,
        "tecnologias": tecnologias_disponibles,
        "categoria_activa": categoria_activa,
        "tecnologia_activa": tecnologia_activa,
        "dificultad_activa": dificultad,
        "q": q,
        "orden": orden,
        "es_preview_staff": es_preview_staff,
        "disclaimer_precios": DISCLAIMER_PRECIOS,
    }
    return render(request, "catalogo/lista.html", context)


def producto_detalle_view(request, slug):
    """
    Ficha detallada del producto pedagógico.
    Si el producto no es publicable para el usuario actual, devuelve 404 estricto.
    """
    producto = get_object_or_404(
        Producto.objects.publicables(user=request.user)
        .select_related("categoria", "proveedor")
        .prefetch_related("tecnologias_compatibles", "imagenes"),
        slug=slug
    )

    # Productos relacionados en la misma categoría
    relacionados = Producto.objects.publicables(user=request.user).filter(
        categoria=producto.categoria
    ).exclude(id=producto.id)[:4]

    es_preview_staff = request.user.is_authenticated and request.user.is_staff

    context = {
        "producto": producto,
        "relacionados": relacionados,
        "es_preview_staff": es_preview_staff,
        "disclaimer_precios": DISCLAIMER_PRECIOS,
    }
    return render(request, "catalogo/detalle.html", context)


def sitemap_view(request):
    """
    Sitemap XML canónico para SEO.
    Solo expone productos estrictamente públicos (publicado=True, activo=True, VALIDADO).
    """
    # Para sitemap público NUNCA se utiliza usuario staff (visibilidad pública pura)
    productos = Producto.objects.publicables(user=None).order_by("nombre_comercial")
    
    xml_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
        '  <url>',
        '    <loc>https://educompra.humm.cl/</loc>',
        '    <changefreq>daily</changefreq>',
        '    <priority>1.0</priority>',
        '  </url>',
        '  <url>',
        '    <loc>https://educompra.humm.cl/catalogo/</loc>',
        '    <changefreq>daily</changefreq>',
        '    <priority>0.9</priority>',
        '  </url>',
    ]

    for p in productos:
        lastmod = p.updated_at.strftime("%Y-%m-%d")
        xml_lines.append(f'  <url>')
        xml_lines.append(f'    <loc>https://educompra.humm.cl/catalogo/{p.slug}/</loc>')
        xml_lines.append(f'    <lastmod>{lastmod}</lastmod>')
        xml_lines.append(f'    <changefreq>weekly</changefreq>')
        xml_lines.append(f'    <priority>0.8</priority>')
        xml_lines.append(f'  </url>')

    xml_lines.append('</urlset>')
    content = "\n".join(xml_lines)
    return HttpResponse(content, content_type="application/xml")


def robots_view(request):
    """
    Robots.txt para rastreadores de motores de búsqueda.
    """
    content = """User-agent: *
Allow: /
Allow: /catalogo/
Disallow: /admin/
Disallow: /cotizaciones/
Disallow: /mi-cotizacion/
Disallow: /solicitar-cotizacion/
Disallow: /solicitud-recibida/

Sitemap: https://educompra.humm.cl/sitemap.xml
"""
    return HttpResponse(content, content_type="text/plain")
