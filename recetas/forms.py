from django import forms
from django.forms import inlineformset_factory
from .models import Receta, RecetaIngrediente

class RecetaForm(forms.ModelForm):
    class Meta:
        model = Receta
        fields = ["nombre", "descripcion", "rendimiento"]
        widgets = {
            "rendimiento": forms.TextInput(attrs={"inputmode": "decimal", "placeholder": "Ej: 12"}),
        }

IngredienteFormSet = inlineformset_factory(
    Receta, RecetaIngrediente,
    fields=["insumo", "cantidad"],
    widgets={
        "cantidad": forms.TextInput(attrs={"inputmode": "decimal", "placeholder": "Ej: 0.5"}),
    },
    extra=3, can_delete=True
)
