from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum
from .models import Gasto
from .forms import GastoForm

def lista_gastos(request):
    gastos = Gasto.objects.all().order_by('-fecha')
    resumen_por_categoria = (
        Gasto.objects.values('categoria')
        .annotate(total=Sum('monto'))
        .order_by('-total')
    )
    return render(request, 'gastos/lista.html', {
        'gastos': gastos,
        'resumen_por_categoria': resumen_por_categoria,
    })

def crear_gasto(request):
    if request.method == 'POST':
        form = GastoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_gastos')
    else:
        form = GastoForm()
    return render(request, 'gastos/form.html', {'form': form})

def editar_gasto(request, pk):
    gasto = get_object_or_404(Gasto, pk=pk)
    if request.method == 'POST':
        form = GastoForm(request.POST, instance=gasto)
        if form.is_valid():
            form.save()
            return redirect('lista_gastos')
    else:
        form = GastoForm(instance=gasto)
    return render(request, 'gastos/form.html', {'form': form, 'gasto': gasto})

def eliminar_gasto(request, pk):
    gasto = get_object_or_404(Gasto, pk=pk)
    if request.method == 'POST':
        gasto.delete()
        return redirect('lista_gastos')
    return render(request, 'gastos/confirmar_eliminar.html', {'gasto': gasto})
