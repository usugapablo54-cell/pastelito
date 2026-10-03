from django.urls import path
from . import views

urlpatterns = [
    path("reportes/", views.reportes, name="reportes"),
    path("reportes/exportar-pdf/", views.exportar_pdf, name="exportar_pdf"),
    path("reportes/exportar-excel/", views.exportar_excel, name="exportar_excel"),
]
