from django.contrib import admin
from .models import Insumo

@admin.register(Insumo)
class InsumoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio_compra', 'cantidad', 'unidad_medida', 'stock_actual', 'stock_minimo', 'stock_bajo', 'valor_stock', 'fecha_vencimiento')
    list_filter = ('unidad_medida', 'proveedor')
    search_fields = ('nombre',)