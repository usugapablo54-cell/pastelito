from django.contrib import admin
from .models import Receta, RecetaIngrediente

class RecetaIngredienteInline(admin.TabularInline):
    model = RecetaIngrediente
    extra = 1

@admin.register(Receta)
class RecetaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'rendimiento', 'costo_total', 'costo_por_unidad')
    inlines = [RecetaIngredienteInline]