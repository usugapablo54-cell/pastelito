from django.contrib import admin
from .models import Proveedor

@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'empresa', 'telefono', 'whatsapp', 'correo')
    search_fields = ('nombre', 'empresa')