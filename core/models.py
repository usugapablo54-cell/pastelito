from django.db import models

class DatosNegocio(models.Model):
    nombre = models.CharField(max_length=150, default="Mi Negocio")
    direccion = models.CharField(max_length=250, blank=True)
    telefono = models.CharField(max_length=20, blank=True)
    logo = models.ImageField(upload_to='logos/', blank=True, null=True)

    def __str__(self):
        return self.nombre
class Cierre(models.Model):
    fecha = models.DateField(unique=True)
    total_gastos = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_movimientos = models.IntegerField(default=0)
    insumos_creados = models.IntegerField(default=0)
    productos_con_poco_stock = models.IntegerField(default=0)
    notas = models.TextField(blank=True, help_text="Notas u observaciones del dia")
    creado_en = models.DateTimeField(auto_now_add=True)
    total_ingresos = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_utilidad = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    class Meta:
        ordering = ['-fecha']

    def __str__(self):
        return f"Cierre {self.fecha}"