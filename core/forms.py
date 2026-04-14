# core/forms.py
from django import forms
from django.core.exceptions import ValidationError
from .models import pago, contrato, ZonaTrabajo, empleado,cargo, Foto
from django.contrib.auth.forms import AuthenticationForm

class PagoForm(forms.ModelForm):
    class Meta:
        model = pago
        fields = "__all__"
        error_messages = {
            "monto": {"required": "El monto es obligatorio."},
            "fecha_pago": {"required": "La fecha de pago es obligatoria."},
        }

    def clean_monto(self):
        monto = self.cleaned_data.get("monto")
        if monto is not None and monto <= 0:
            raise ValidationError("El monto debe ser mayor que cero.")
        return monto

    def clean_fecha_pago(self):
        fecha = self.cleaned_data.get("fecha_pago")
        if not fecha:
            raise ValidationError("La fecha de pago es obligatoria.")
        return fecha
    
class ContratoForm(forms.ModelForm):
    class Meta:
        model = contrato
        fields = [
            'empleado', 'departamento', 'cargo',
            'turno_has_jornada',          # ← AÑADIDO
            'fecha_inicio', 'fecha_fin',
            'detalle_contrato', 'pdf',
        ]
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'fecha_fin': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'detalle_contrato': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }

    # Opcional: ordena y etiqueta bonitos los select
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            # aplica clase Bootstrap a todos los widgets que no la traigan
            if not isinstance(field.widget, forms.CheckboxInput):
                css = field.widget.attrs.get('class', '')
                field.widget.attrs['class'] = (css + ' form-control').strip()

        if 'empleado' in self.fields:
            self.fields['empleado'].label_from_instance = lambda obj: f"{obj.run} — {obj}"
        if 'cargo' in self.fields:
            self.fields['cargo'].label_from_instance = lambda obj: obj.nombre
        if 'departamento' in self.fields:
            self.fields['departamento'].label_from_instance = lambda obj: obj.nombre
        if 'turno_has_jornada' in self.fields:
            self.fields['turno_has_jornada'].label = "Turno / Jornada"


class ZonaTrabajoForm(forms.ModelForm):
    class Meta:
        model = ZonaTrabajo
        fields = ["nombre", "area", "ubicacion", "supervisor", "notas", "status"]
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
            "area": forms.TextInput(attrs={"class": "form-control"}),
            "ubicacion": forms.TextInput(attrs={"class": "form-control"}),
            "supervisor": forms.TextInput(attrs={"class": "form-control"}),
            "notas": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "status": forms.Select(attrs={"class": "form-select"}),
        }

class EmpleadoZonaForm(forms.ModelForm):
    class Meta:
        model = empleado
        fields = ["zona_trabajo"]
        widgets = {
            "zona_trabajo": forms.Select(attrs={"class": "form-select"})
        }

class CargoForm(forms.ModelForm):
    class Meta:
        model = cargo                     # tu modelo está en minúsculas
        fields = ["nombre", "description"]  # usa "descripcion" si ese es tu campo
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control", "placeholder": "Nombre del cargo"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Descripción"}),
        }


from django import forms
from django.contrib.auth.models import User

class PerfilForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
        }


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Usuario',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingresa tu usuario'
        })
    )
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingresa tu contraseña'
        })
    )


class FotoForm(forms.ModelForm):
    class Meta:
        model = Foto
        fields = ['titulo', 'descripcion', 'imagen', 'activa']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'activa': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
