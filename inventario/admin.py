from django.contrib import admin
from .models import MovimientoInventario

@admin.register(MovimientoInventario)
class MovimientoInventarioAdmin(admin.ModelAdmin):
    list_display = ('insumo', 'tipo', 'cantidad', 'fecha', 'referencia')
    list_filter = ('tipo', 'insumo')