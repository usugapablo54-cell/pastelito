from django.db import models

class Producto(models.Model):
    nombre = models.CharField(max_length=150)
    receta = models.OneToOneField(
        'recetas.Receta', on_delete=models.CASCADE, related_name='producto'
    )
    gastos_fijos_asignados = models.DecimalField(
        max_digits=12, decimal_places=2, default=0,
        help_text="Parte proporcional de gastos fijos (arriendo, servicios, etc.) por unidad"
    )
    mano_de_obra = models.DecimalField(
        max_digits=12, decimal_places=2, default=0,
        help_text="Costo de mano de obra por unidad"
    )
    margen_ganancia = models.DecimalField(
        max_digits=5, decimal_places=2, default=30,
        help_text="Porcentaje de ganancia deseado, ej: 30 para 30%"
    )
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    @property
    def costo_ingredientes_unidad(self):
        return self.receta.costo_por_unidad

    @property
    def costo_total_unidad(self):
        return (
            self.costo_ingredientes_unidad
            + self.gastos_fijos_asignados
            + self.mano_de_obra
        )

    @property
    def precio_sugerido(self):
        costo = self.costo_total_unidad
        margen = self.margen_ganancia / 100
        return costo * (1 + margen)

    @property
    def utilidad_unitaria(self):
        return self.precio_sugerido - self.costo_total_unidad

    def __str__(self):
        return self.nombre

class VentaRealizada(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='ventas')
    cantidad = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    precio_unitario = models.DecimalField(max_digits=12, decimal_places=2)
    fecha = models.DateField()
    creado_en = models.DateTimeField(auto_now_add=True)

    @property
    def ingreso_total(self):
        return self.precio_unitario * self.cantidad

    @property
    def costo_total(self):
        return self.producto.costo_total_unidad * self.cantidad

    @property
    def utilidad_real(self):
        return self.ingreso_total - self.costo_total

    def __str__(self):
        return f"{self.producto.nombre} x{self.cantidad} ({self.fecha})"

    class Meta:
        ordering = ['-fecha']
