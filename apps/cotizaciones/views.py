from django.shortcuts import render
from .models import SolicitudCotizacion

def resumen_solicitud(request, codigo):
    """Vista placeholder para consultar estado de una solicitud con su código."""
    solicitud = SolicitudCotizacion.objects.filter(codigo_seguimiento=codigo).first()
    context = {"solicitud": solicitud}
    return render(request, "core/home.html", context)
