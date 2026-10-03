from django.db import models

class TipoMovimiento(models.TextChoices):
    ENTRADA = 'entrada', 'Entrada'
    SALIDA = 'salida', 'Salida'

class MovimientoInventario(models.Model):
    insumo = models.ForeignKey(
        'materia_prima.Insumo', on_delete=models.CASCADE, related_name='movimientos'
    )
    tipo = models.CharField(max_length=10, choices=TipoMovimiento.choices)
    cantidad = models.DecimalField(max_digits=12, decimal_places=3)
    fecha = models.DateTimeField(auto_now_add=True)
    referencia = models.CharField(
        max_length=200, blank=True,
        help_text="Ej: 'Compra a proveedor X' o 'Producción receta Y'"
    )
    receta = models.ForeignKey(
        'recetas.Receta', on_delete=models.SET_NULL, null=True, blank=True,
        help_text="Si la salida fue por producción de una receta"
    )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.tipo == TipoMovimiento.ENTRADA:
            self.insumo.stock_actual += self.cantidad
        else:
            self.insumo.stock_actual -= self.cantidad
        self.insumo.save(update_fields=['stock_actual'])

    def __str__(self):
        return f"{self.get_tipo_display()} - {self.insumo.nombre} ({self.cantidad})"

    class Meta:
        ordering = ['-fecha']