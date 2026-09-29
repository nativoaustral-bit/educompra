"""
Context processor para EduCompra Humm.
Inyecta la cantidad de artículos en la canasta 'Mi Cotización' en todas las plantillas.
"""

def canasta_context(request):
    canasta = request.session.get("mi_cotizacion", {})
    total_articulos = 0
    if isinstance(canasta, dict):
        for item in canasta.values():
            if isinstance(item, dict):
                total_articulos += int(item.get("cantidad", 0))
            elif isinstance(item, int):
                total_articulos += int(item)
    return {
        "canasta_total_items": total_articulos,
    }
