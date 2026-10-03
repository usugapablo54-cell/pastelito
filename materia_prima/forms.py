from django import forms
from .models import Insumo

class InsumoForm(forms.ModelForm):
    class Meta:
        model = Insumo
        fields = [
            "nombre", "categoria", "precio_compra", "cantidad", "unidad_medida",
            "fecha_compra", "fecha_vencimiento", "stock_minimo",
            "stock_actual", "proveedor"
        ]
        widgets = {
            "fecha_compra": forms.DateInput(attrs={"type": "date"}),
            "fecha_vencimiento": forms.DateInput(attrs={"type": "date"}),
            "precio_compra": forms.TextInput(attrs={"inputmode": "decimal", "placeholder": "Ej: 2000"}),
            "cantidad": forms.TextInput(attrs={"inputmode": "decimal", "placeholder": "Ej: 1"}),
            "stock_minimo": forms.TextInput(attrs={"inputmode": "decimal", "placeholder": "Ej: 5"}),
            "stock_actual": forms.TextInput(attrs={"inputmode": "decimal", "placeholder": "Ej: 10"}),
        }
