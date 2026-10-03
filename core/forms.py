from django import forms
from .models import DatosNegocio

class DatosNegocioForm(forms.ModelForm):
    class Meta:
        model = DatosNegocio
        fields = ["nombre", "direccion", "telefono", "logo"]
