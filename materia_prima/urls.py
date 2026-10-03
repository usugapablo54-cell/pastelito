from django.urls import path
from . import views

urlpatterns = [
    path("materia-prima/", views.lista_insumos, name="lista_insumos"),
    path("materia-prima/nuevo/", views.crear_insumo, name="crear_insumo"),
    path("materia-prima/<int:pk>/editar/", views.editar_insumo, name="editar_insumo"),
    path("materia-prima/<int:pk>/eliminar/", views.eliminar_insumo, name="eliminar_insumo"),
    path("materia-prima/categorias/", views.lista_categorias, name="lista_categorias"),
    path("materia-prima/categorias/<int:pk>/eliminar/", views.eliminar_categoria, name="eliminar_categoria"),
    path("stock/", views.vista_stock, name="vista_stock"),
]
