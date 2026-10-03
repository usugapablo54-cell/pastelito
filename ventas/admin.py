from django.contrib import admin
from .models import Producto

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'costo_total_unidad', 'margen_ganancia', 'precio_sugerido', 'utilidad_unitaria')