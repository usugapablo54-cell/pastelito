from django import forms
from .models import Producto, VentaRealizada

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ["nombre", "receta", "gastos_fijos_asignados", "mano_de_obra", "margen_ganancia"]
        widgets = {
            "gastos_fijos_asignados": forms.TextInput(attrs={"inputmode": "decimal", "placeholder": "Ej: 500"}),
            "mano_de_obra": forms.TextInput(attrs={"inputmode": "decimal", "placeholder": "Ej: 2000"}),
            "margen_ganancia": forms.TextInput(attrs={"inputmode": "decimal", "placeholder": "Ej: 30"}),
        }

class VentaRealizadaForm(forms.ModelForm):
    class Meta:
        model = VentaRealizada
        fields = ["producto", "cantidad", "precio_unitario", "fecha"]
        widgets = {
            "fecha": forms.DateInput(attrs={"type": "date"}),
            "cantidad": forms.TextInput(attrs={"inputmode": "decimal", "placeholder": "Ej: 1"}),
            "precio_unitario": forms.TextInput(attrs={"inputmode": "decimal", "placeholder": "Ej: 5000"}),
        }
