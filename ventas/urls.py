from django.urls import path
from . import views

urlpatterns = [
    path("ventas/", views.lista_productos, name="lista_productos"),
    path("ventas/nuevo/", views.crear_producto, name="crear_producto"),
    path("ventas/<int:pk>/editar/", views.editar_producto, name="editar_producto"),
    path("ventas/<int:pk>/eliminar/", views.eliminar_producto, name="eliminar_producto"),
    path("ventas-realizadas/", views.lista_ventas_realizadas, name="lista_ventas_realizadas"),
    path("ventas-realizadas/nueva/", views.crear_venta_realizada, name="crear_venta_realizada"),
]
