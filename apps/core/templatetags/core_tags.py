"""
Filtros y tags personalizados para EduCompra Humm.
Incluye formateo de precios con separador de miles chileno (punto).
"""

from decimal import Decimal
from django import template

register = template.Library()


@register.filter(name="separador_miles")
def separador_miles(value):
    """
    Formatea un número o monto con separador de miles chileno (punto).
    Redondea al entero más cercano sin decimales (estándar CLP).

    Ejemplos:
        14990                -> '14.990'
        Decimal('26912.00')  -> '26.912'
        1234567              -> '1.234.567'
        500                  -> '500'
        0                    -> '0'
        None                 -> ''
        ''                   -> ''
    """
    if value is None or value == "":
        return ""
    try:
        if isinstance(value, Decimal):
            val_int = int(round(value))
        elif isinstance(value, (int, float)):
            val_int = int(round(value))
        else:
            val_str = str(value).strip()
            if not val_str:
                return ""
            val_int = int(round(float(val_str)))
        return f"{val_int:,}".replace(",", ".")
    except Exception:
        return str(value)


@register.filter(name="formato_precio")
def formato_precio(value):
    """Alias para separador_miles."""
    return separador_miles(value)


@register.filter(name="formato_clp")
def formato_clp(value):
    """
    Formatea un monto como '$14.990' con símbolo de moneda y separador de miles.
    """
    res = separador_miles(value)
    if res == "":
        return ""
    return f"${res}"
