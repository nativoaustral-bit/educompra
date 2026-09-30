"""
Vistas de autenticación institucional para Administración EduCompra (/gestion/).
"""

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect


def login_view(request):
    """
    Inicio de sesión seguro para el personal de Humm en /gestion/login/.
    """
    if request.user.is_authenticated:
        if request.user.is_staff or request.user.has_perm("gestion.can_view_gestion"):
            return redirect("gestion:dashboard")

    next_url = request.GET.get("next") or request.POST.get("next") or "gestion:dashboard"

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if not user.is_active:
                messages.error(request, "Esta cuenta de usuario está desactivada.")
            elif user.is_staff or user.has_perm("gestion.can_view_gestion") or user.is_superuser:
                login(request, user)
                messages.success(request, f"Bienvenido/a, {user.first_name or user.username}.")
                return redirect(next_url)
            else:
                messages.error(request, "Su cuenta no cuenta con permisos para acceder a Administración EduCompra.")
        else:
            messages.error(request, "Usuario o contraseña incorrectos. Por favor verifique sus datos.")
    else:
        form = AuthenticationForm()

    context = {
        "form": form,
        "next": next_url,
    }
    return render(request, "gestion/login.html", context)


def logout_view(request):
    """
    Cierre de sesión seguro.
    """
    if request.user.is_authenticated:
        logout(request)
        messages.info(request, "Ha cerrado su sesión de Administración EduCompra.")
    return redirect("gestion:login")
