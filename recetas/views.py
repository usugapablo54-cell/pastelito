from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import ProtectedError
from .models import Receta
from .forms import RecetaForm, IngredienteFormSet

def lista_recetas(request):
    recetas = Receta.objects.all().order_by("nombre")
    return render(request, "recetas/lista.html", {"recetas": recetas})

def crear_receta(request):
    if request.method == "POST":
        form = RecetaForm(request.POST)
        if form.is_valid():
            receta = form.save()
            formset = IngredienteFormSet(request.POST, instance=receta)
            if formset.is_valid():
                formset.save()
                return redirect("lista_recetas")
        else:
            formset = IngredienteFormSet(request.POST)
    else:
        form = RecetaForm()
        formset = IngredienteFormSet()
    return render(request, "recetas/form.html", {"form": form, "formset": formset})

def editar_receta(request, pk):
    receta = get_object_or_404(Receta, pk=pk)
    if request.method == "POST":
        form = RecetaForm(request.POST, instance=receta)
        formset = IngredienteFormSet(request.POST, instance=receta)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect("lista_recetas")
    else:
        form = RecetaForm(instance=receta)
        formset = IngredienteFormSet(instance=receta)
    return render(request, "recetas/form.html", {"form": form, "formset": formset, "receta": receta})

def eliminar_receta(request, pk):
    receta = get_object_or_404(Receta, pk=pk)
    error = None
    if request.method == "POST":
        try:
            receta.delete()
            return redirect("lista_recetas")
        except ProtectedError:
            error = "No se puede eliminar esta receta porque esta siendo usada en un producto o tiene ventas registradas."
    return render(request, "recetas/confirmar_eliminar.html", {"receta": receta, "error": error})

