from django.shortcuts import render, redirect
from .models import MovimientoInventario
from .forms import MovimientoForm

def lista_movimientos(request):
    movimientos = MovimientoInventario.objects.all().order_by("-fecha")
    return render(request, "inventario/lista.html", {"movimientos": movimientos})

def crear_movimiento(request):
    error = None
    if request.method == "POST":
        form = MovimientoForm(request.POST)
        if form.is_valid():
            movimiento = form.save(commit=False)
            if movimiento.tipo == TipoMovimiento.SALIDA and movimiento.insumo.stock_actual < movimiento.cantidad:
                error = f"No hay suficiente stock de {movimiento.insumo.nombre} (disponible: {movimiento.insumo.stock_actual}, solicitado: {movimiento.cantidad})"
            else:
                movimiento.save()
                return redirect("lista_movimientos")
    else:
        form = MovimientoForm()
    return render(request, "inventario/form.html", {"form": form, "error": error})