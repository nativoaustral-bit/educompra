"""
Decoradores de seguridad y control de acceso para la plataforma /gestion/.
Basados en permisos nativos de Django (Ajuste Obligatorio #19 de Humm).
"""

from functools import wraps
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect


def gestion_required(view_func):
    """
    Verifica que el usuario esté autenticado, activo y cuente con permisos
    para acceder a la plataforma administrativa EduCompra.
    """
    @wraps(view_func)
    @login_required(login_url="gestion:login")
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_active:
            messages.error(request, "Su cuenta de usuario se encuentra inactiva.")
            return redirect("gestion:login")

        # Superusuarios y staff tienen acceso base garantizado
        if request.user.is_superuser or request.user.is_staff:
            return view_func(request, *args, **kwargs)

        # Validación por permiso nativo Django
        if request.user.has_perm("gestion.can_view_gestion"):
            return view_func(request, *args, **kwargs)

        messages.error(request, "No cuenta con autorización para acceder a Administración EduCompra.")
        return redirect("core:home")

    return _wrapped_view


def permiso_requerido(permiso):
    """
    Exige un permiso nativo de Django específico (ej: 'gestion.can_manage_catalogo').
    Si no lo posee, eleva PermissionDenied o redirige con mensaje explicativo.
    """
    def decorator(view_func):
        @wraps(view_func)
        @gestion_required
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_superuser or request.user.has_perm(permiso):
                return view_func(request, *args, **kwargs)

            messages.error(request, f"Permiso insuficiente: Se requiere la atribución '{permiso}'.")
            return redirect("gestion:dashboard")

        return _wrapped_view
    return decorator
