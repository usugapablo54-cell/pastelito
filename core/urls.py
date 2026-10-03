from django.urls import path
from . import views

urlpatterns = [
    path("", views.lobby, name="lobby"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("configuracion/", views.configuracion, name="configuracion"),
    path("configuracion/backup/", views.descargar_backup, name="descargar_backup"),
    path("cierres/", views.lista_cierres, name="lista_cierres"),
    path("cierres/nuevo/", views.crear_cierre, name="crear_cierre"),
]
