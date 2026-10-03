from django import forms
from .models import Gasto

class GastoForm(forms.ModelForm):
    class Meta:
        model = Gasto
        fields = ["categoria", "descripcion", "monto", "fecha"]
        widgets = {
            "fecha": forms.DateInput(attrs={"type": "date"}),
            "monto": forms.TextInput(attrs={"inputmode": "decimal", "placeholder": "Ej: 15000"}),
        }
