from django import forms
from .models import MovimientoInventario

class MovimientoForm(forms.ModelForm):
    class Meta:
        model = MovimientoInventario
        fields = ["insumo", "tipo", "cantidad", "referencia", "receta"]
        widgets = {
            "cantidad": forms.TextInput(attrs={"inputmode": "decimal", "placeholder": "Ej: 5"}),
        }
