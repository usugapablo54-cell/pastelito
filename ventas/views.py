from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import ProtectedError
from .models import Producto
from .forms import ProductoForm

def lista_productos(request):
    productos = Producto.objects.all().order_by("nombre")
    return render(request, "ventas/lista.html", {"productos": productos})

def crear_producto(request):
    if request.method == "POST":
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("lista_productos")
    else:
        form = ProductoForm()
    return render(request, "ventas/form.html", {"form": form})

def editar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == "POST":
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            return redirect("lista_productos")
    else:
        form = ProductoForm(instance=producto)
    return render(request, "ventas/form.html", {"form": form, "producto": producto})

def eliminar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    error = None
    if request.method == "POST":
        try:
            producto.delete()
            return redirect("lista_productos")
        except ProtectedError:
            error = "No se puede eliminar este producto porque tiene ventas registradas."
    return render(request, "ventas/confirmar_eliminar.html", {"producto": producto, "error": error})

from .models import VentaRealizada
from .forms import VentaRealizadaForm
from django.db.models import Sum
from inventario.models import MovimientoInventario, TipoMovimiento

def lista_ventas_realizadas(request):
    ventas = VentaRealizada.objects.all().order_by("-fecha")
    ingreso_total = sum(v.ingreso_total for v in ventas)
    utilidad_total = sum(v.utilidad_real for v in ventas)
    return render(request, "ventas/ventas_realizadas.html", {
        "ventas": ventas,
        "ingreso_total": ingreso_total,
        "utilidad_total": utilidad_total,
    })

def crear_venta_realizada(request):
    error = None
    if request.method == "POST":
        form = VentaRealizadaForm(request.POST)
        if form.is_valid():
            venta_temp = form.save(commit=False)
            receta = venta_temp.producto.receta
            faltantes = []
            for ingrediente in receta.ingredientes.all():
                cantidad_necesaria = ingrediente.cantidad * venta_temp.cantidad
                if ingrediente.insumo.stock_actual < cantidad_necesaria:
                    faltantes.append(
                        f"{ingrediente.insumo.nombre} (disponible: {ingrediente.insumo.stock_actual}, necesario: {cantidad_necesaria})"
                    )
            if faltantes:
                error = "No hay suficiente stock de: " + ", ".join(faltantes)
            else:
                venta = form.save()
                for ingrediente in receta.ingredientes.all():
                    cantidad_usada = ingrediente.cantidad * venta.cantidad
                    MovimientoInventario.objects.create(
                        insumo=ingrediente.insumo,
                        tipo=TipoMovimiento.SALIDA,
                        cantidad=cantidad_usada,
                        referencia=f"Venta: {venta.producto.nombre} x{venta.cantidad}",
                        receta=receta,
                    )
                return redirect("lista_ventas_realizadas")
    else:
        form = VentaRealizadaForm()
    return render(request, "ventas/form_venta.html", {"form": form, "error": error})
