from django.db import models

class Proveedor(models.Model):
    nombre = models.CharField(max_length=150)
    empresa = models.CharField(max_length=150, blank=True)
    telefono = models.CharField(max_length=20, blank=True)
    whatsapp = models.CharField(max_length=20, blank=True)
    correo = models.EmailField(blank=True)
    direccion = models.CharField(max_length=250, blank=True)
    productos_suministra = models.TextField(
        blank=True, help_text="Descripción de los productos que suministra"
    )
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre