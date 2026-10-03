from django.urls import path
from . import views

urlpatterns = [
    path("recetas/", views.lista_recetas, name="lista_recetas"),
    path("recetas/nuevo/", views.crear_receta, name="crear_receta"),
    path("recetas/<int:pk>/editar/", views.editar_receta, name="editar_receta"),
    path("recetas/<int:pk>/eliminar/", views.eliminar_receta, name="eliminar_receta"),
]
