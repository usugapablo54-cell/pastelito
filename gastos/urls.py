from django.urls import path
from . import views

urlpatterns = [
    path('gastos/', views.lista_gastos, name='lista_gastos'),
    path('gastos/nuevo/', views.crear_gasto, name='crear_gasto'),
    path('gastos/<int:pk>/editar/', views.editar_gasto, name='editar_gasto'),
    path('gastos/<int:pk>/eliminar/', views.eliminar_gasto, name='eliminar_gasto'),
]
