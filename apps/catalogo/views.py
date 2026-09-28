from django.shortcuts import render
from .models import Producto, Categoria

def lista_catalogo(request):
    """Vista placeholder para la Fase 1. En Fase 4 se implementará el catálogo interactivo."""
    categorias = Categoria.objects.filter(activa=True)
    productos_destacados = Producto.objects.filter(publicado=True, activo=True, destacado=True)[:6]
    context = {
        "categorias": categorias,
        "productos_destacados": productos_destacados,
    }
    return render(request, "core/home.html", context)
