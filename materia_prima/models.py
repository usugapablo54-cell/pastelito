from django.db import models

class UnidadMedida(models.TextChoices):
    GRAMO = "g", "Gramo"
    KILOGRAMO = "kg", "Kilogramo"
    MILILITRO = "ml", "Mililitro"
    LITRO = "l", "Litro"
    UNIDAD = "unidad", "Unidad"
    LIBRA = "lb", "Libra"                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               


class CategoriaInsumo(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre


class Insumo(models.Model):
    nombre = models.CharField(max_length=150)
    categoria = models.ForeignKey(
        CategoriaInsumo, on_delete=models.SET_NULL, null=True, blank=True
    )
    precio_compra = models.DecimalField(max_digits=12, decimal_places=2)
    cantidad = models.DecimalField(max_digits=12, decimal_places=3)
    unidad_medida = models.CharField(max_length=10, choices=UnidadMedida.choices)
    fecha_compra = models.DateField()
    fecha_vencimiento = models.DateField(null=True, blank=True)
    stock_minimo = models.DecimalField(max_digits=12, decimal_places=3, default=0)
    stock_actual = models.DecimalField(max_digits=12, decimal_places=3, default=0)
    proveedor = models.ForeignKey(
        "proveedores.Proveedor", on_delete=models.SET_NULL, null=True, blank=True
    ) 
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    @property
    def costo_unitario(self):
        if self.cantidad:
            return self.precio_compra / self.cantidad
        return 0

    @property
    def valor_stock(self):
        return self.costo_unitario * self.stock_actual

    @property
    def stock_bajo(self):
        return self.stock_actual <= self.stock_minimo

    @property
    def dias_para_vencer(self):
        if self.fecha_vencimiento:
            from django.utils import timezone
            return (self.fecha_vencimiento - timezone.now().date()).days
        return None

    @property
    def esta_vencido(self):
        if self.fecha_vencimiento:
            from django.utils import timezone
            return self.fecha_vencimiento < timezone.now().date()
        return False

    def __str__(self):
        return self.nombre
