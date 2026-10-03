from django import forms
from .models import Proveedor

class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ['nombre', 'empresa', 'telefono', 'whatsapp', 'correo', 'direccion', 'productos_suministra']
        widgets = {
            'productos_suministra': forms.Textarea(attrs={'rows': 3}),
        }
