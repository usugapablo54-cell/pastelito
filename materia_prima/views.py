from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import ProtectedError
from .models import Insumo, CategoriaInsumo
from .forms import InsumoForm

def lista_insumos(request):
    insumos = Insumo.objects.all().order_by("nombre")
    return render(request, "materia_prima/lista.html", {"insumos": insumos})

def crear_insumo(request):
    if request.method == "POST":
        form = InsumoForm(request.POST)
        if form.is_valid():
            insumo = form.save(commit=False)
            if not insumo.stock_actual:
                insumo.stock_actual = insumo.cantidad
            insumo.save()
            from inventario.models import MovimientoInventario, TipoMovimiento
            if insumo.stock_actual > 0:
                MovimientoInventario.objects.create(
                    insumo=insumo,
                    tipo=TipoMovimiento.ENTRADA,
                    cantidad=insumo.stock_actual,
                    referencia="Registro inicial de insumo",
                )
            return redirect("lista_insumos")
    else:
        form = InsumoForm()
    return render(request, "materia_prima/form.html", {"form": form})

def editar_insumo(request, pk):
    insumo = get_object_or_404(Insumo, pk=pk)
    stock_anterior = insumo.stock_actual
    if request.method == "POST":
        form = InsumoForm(request.POST, instance=insumo)
        if form.is_valid():
            insumo_actualizado = form.save()
            diferencia = insumo_actualizado.stock_actual - stock_anterior
            if diferencia != 0:
                from inventario.models import MovimientoInventario, TipoMovimiento
                MovimientoInventario.objects.create(
                    insumo=insumo_actualizado,
                    tipo=TipoMovimiento.ENTRADA if diferencia > 0 else TipoMovimiento.SALIDA,
                    cantidad=abs(diferencia),
                    referencia="Ajuste manual desde edicion de insumo",
                )
            return redirect("lista_insumos")
    else:
        form = InsumoForm(instance=insumo)
    return render(request, "materia_prima/form.html", {"form": form, "insumo": insumo})

def eliminar_insumo(request, pk):
    insumo = get_object_or_404(Insumo, pk=pk)
    error = None
    if request.method == "POST":
        try:
            insumo.delete()
            return redirect("lista_insumos")
        except ProtectedError:
            error = "No se puede eliminar este insumo porque esta siendo usado en una o mas recetas."
    return render(request, "materia_prima/confirmar_eliminar.html", {"insumo": insumo, "error": error})

def lista_categorias(request):
    categorias = CategoriaInsumo.objects.all().order_by("nombre")
    if request.method == "POST":
        nombre = request.POST.get("nombre")
        if nombre:
            CategoriaInsumo.objects.get_or_create(nombre=nombre)
        return redirect("lista_categorias")
    return render(request, "materia_prima/categorias.html", {"categorias": categorias})

def eliminar_categoria(request, pk):
    categoria = get_object_or_404(CategoriaInsumo, pk=pk)
    if request.method == "POST":
        categoria.delete()
    return redirect("lista_categorias")

def vista_stock(request):
    insumos = Insumo.objects.all().order_by("nombre")
    valor_total = sum(i.valor_stock for i in insumos)
    return render(request, "materia_prima/stock.html", {
        "insumos": insumos,
        "valor_total": valor_total,
    })
