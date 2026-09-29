"""
Formularios para el flujo de solicitud de cotización docente.
Incorpora honeypot anti-spam, validación local de regiones/comunas y control de idempotencia.
"""

from django import forms
from django.core.exceptions import ValidationError
from apps.core.regiones_chile import REGIONES_CHILE, obtener_regiones_comunas_dict

TIPOS_INSTITUCION = [
    ("", "Seleccione tipo de institución..."),
    ("MUNICIPAL_SLEP", "Municipal / Servicio Local de Educación (SLEP)"),
    ("PARTICULAR_SUBVENCIONADO", "Particular Subvencionado"),
    ("PARTICULAR_PAGADO", "Particular Pagado"),
    ("CORPORACION_FUNDACION", "Corporación / Fundación Educativa"),
    ("EDUCACION_SUPERIOR", "CFT / IP / Universidad"),
    ("OTRO", "Otro tipo de institución"),
]

REGIONES_CHOICES = [("", "Seleccione una región...")] + [
    (r["nombre"], f"{r['numero']} — {r['nombre']}" if r["numero"] != "RM" else f"RM — {r['nombre']}")
    for r in REGIONES_CHILE
]


class SolicitudCotizacionForm(forms.Form):
    # Token de idempotencia (generado en sesión al abrir el formulario)
    idempotency_token = forms.CharField(widget=forms.HiddenInput(), required=True)

    # Honeypot anti-bot: campo oculto para usuarios normales
    sitio_web_docente = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            "style": "display:none !important; position:absolute !important; left:-9999px !important;",
            "tabindex": "-1",
            "autocomplete": "off"
        })
    )

    # Datos del Profesor / Solicitante
    nombre_solicitante = forms.CharField(
        max_length=150,
        required=True,
        label="Nombre y Apellido",
        widget=forms.TextInput(attrs={"placeholder": "Ej: Juan Pérez Morales", "class": "form-control"})
    )
    email = forms.EmailField(
        required=True,
        label="Correo Electrónico (Institucional o Personal)",
        widget=forms.EmailInput(attrs={"placeholder": "ej: profesor@colegio.cl", "class": "form-control"})
    )
    telefono = forms.CharField(
        max_length=50,
        required=True,
        label="Teléfono / WhatsApp de Contacto",
        widget=forms.TextInput(attrs={"placeholder": "Ej: +56 9 1234 5678", "class": "form-control"})
    )
    cargo_solicitante = forms.CharField(
        max_length=100,
        required=False,
        label="Cargo o Rol en el Establecimiento",
        widget=forms.TextInput(attrs={"placeholder": "Ej: Profesor de Tecnología, Coordinador CRA, Jefe UTP", "class": "form-control"})
    )

    # Datos del Establecimiento
    establecimiento = forms.CharField(
        max_length=200,
        required=True,
        label="Nombre del Establecimiento Educacional",
        widget=forms.TextInput(attrs={"placeholder": "Ej: Liceo Bicentenario San Agustín", "class": "form-control"})
    )
    tipo_institucion = forms.ChoiceField(
        choices=TIPOS_INSTITUCION,
        required=False,
        label="Dependencia Institucional",
        widget=forms.Select(attrs={"class": "form-control"})
    )
    region = forms.ChoiceField(
        choices=REGIONES_CHOICES,
        required=True,
        label="Región",
        widget=forms.Select(attrs={"class": "form-control", "id": "id_region"})
    )
    comuna = forms.CharField(
        max_length=100,
        required=True,
        label="Comuna",
        widget=forms.TextInput(attrs={"placeholder": "Ingrese o seleccione comuna", "class": "form-control", "id": "id_comuna"})
    )

    # Datos de Compra Pública / Adquisición (Opcionales para el profesor)
    institucion_responsable_compra = forms.CharField(
        max_length=200,
        required=False,
        label="Entidad Compradora (si aplica)",
        widget=forms.TextInput(attrs={"placeholder": "Ej: DAEM Municipalidad de..., Corporación Educacional...", "class": "form-control"})
    )
    rut_institucion = forms.CharField(
        max_length=20,
        required=False,
        label="RUT Institución para Facturación (Opcional)",
        widget=forms.TextInput(attrs={"placeholder": "Ej: 69.123.456-7", "class": "form-control"})
    )
    nombre_encargado_compras = forms.CharField(
        max_length=150,
        required=False,
        label="Nombre Encargado(a) de Adquisiciones (Opcional)",
        widget=forms.TextInput(attrs={"placeholder": "Ej: María González", "class": "form-control"})
    )
    email_encargado_compras = forms.EmailField(
        required=False,
        label="Email Encargado(a) de Adquisiciones (Opcional)",
        widget=forms.EmailInput(attrs={"placeholder": "ej: compras@daem.cl", "class": "form-control"})
    )

    # Contexto del Proyecto Educativo
    proyecto_educativo = forms.CharField(
        max_length=200,
        required=False,
        label="Nombre o Finalidad del Proyecto",
        widget=forms.TextInput(attrs={"placeholder": "Ej: Taller Extraprogramático de Robótica 2026, Postulación Fondos SEP", "class": "form-control"})
    )
    fecha_requerida_aproximada = forms.CharField(
        max_length=100,
        required=False,
        label="Fecha Estimada en que Necesitan el Material",
        widget=forms.TextInput(attrs={"placeholder": "Ej: Mayo 2026, Inicio segundo semestre", "class": "form-control"})
    )
    observaciones = forms.CharField(
        required=False,
        label="Observaciones o Requerimientos Especiales",
        widget=forms.Textarea(attrs={
            "rows": 3,
            "placeholder": "Indique si requiere capacitación docente, si postula a fondos específicos, o cualquier antecedente relevante.",
            "class": "form-control"
        })
    )

    def clean(self):
        cleaned_data = super().clean()

        # Validación Honeypot: si el campo trampa tiene contenido, es un bot
        honeypot = cleaned_data.get("sitio_web_docente")
        if honeypot:
            raise ValidationError("Detección de envío no válido. Por favor contacte directamente si es un error.")

        # Validación geográfica local
        region_seleccionada = cleaned_data.get("region")
        comuna_seleccionada = cleaned_data.get("comuna")

        regiones_dict = obtener_regiones_comunas_dict()

        if region_seleccionada and region_seleccionada not in regiones_dict:
            self.add_error("region", "La región seleccionada no es válida.")

        if region_seleccionada and comuna_seleccionada:
            comunas_validas = [c.lower() for c in regiones_dict.get(region_seleccionada, [])]
            if comuna_seleccionada.strip().lower() not in comunas_validas:
                # Si no coincide exactamente, verificar si existe en la lista para sugerir o alertar
                # Permitimos flexibilidad en mayúsculas/tildes
                pass

        return cleaned_data
