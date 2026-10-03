from django.urls import path
from . import views

urlpatterns = [
    path("inventario/", views.lista_movimientos, name="lista_movimientos"),
    path("inventario/nuevo/", views.crear_movimiento, name="crear_movimiento"),
]
