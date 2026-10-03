from django.db import models

class Receta(models.Model):
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True)
    rendimiento = models.DecimalField(
        max_digits=10, decimal_places=2, default=1,
        help_text="Cuántas unidades produce esta receta (ej: 12 panes, 20 porciones)"
    )
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    @property
    def costo_total(self):
        total = 0
        for ingrediente in self.ingredientes.all():
            total += ingrediente.costo
        return total

    @property
    def costo_por_unidad(self):
        if self.rendimiento:
            return self.costo_total / self.rendimiento
        return 0

    def __str__(self):
        return self.nombre


class RecetaIngrediente(models.Model):
    receta = models.ForeignKey(
        Receta, on_delete=models.CASCADE, related_name='ingredientes'
    )
    insumo = models.ForeignKey(
        'materia_prima.Insumo', on_delete=models.CASCADE, related_name='usado_en_recetas'
    )
    cantidad = models.DecimalField(
        max_digits=12, decimal_places=3,
        help_text="Cantidad usada, en la misma unidad de medida del insumo"
    )

    @property
    def costo(self):
        return self.insumo.costo_unitario * self.cantidad

    def __str__(self):
        return f"{self.insumo.nombre} en {self.receta.nombre}"

    class Meta:
        unique_together = ('receta', 'insumo')
