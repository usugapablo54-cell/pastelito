from django.db import models

class CategoriaGasto(models.TextChoices):
    GAS = 'gas', 'Gas'
    AGUA = 'agua', 'Agua'
    ENERGIA = 'energia', 'Energía'
    INTERNET = 'internet', 'Internet'
    ARRIENDO = 'arriendo', 'Arriendo'
    OTRO = 'otro', 'Otro'

class Gasto(models.Model):
    categoria = models.CharField(max_length=20, choices=CategoriaGasto.choices)
    descripcion = models.CharField(max_length=200, blank=True)
    monto = models.DecimalField(max_digits=12, decimal_places=2)
    fecha = models.DateField()
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_categoria_display()} - {self.fecha}"

    class Meta:
        ordering = ['-fecha']