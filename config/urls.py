from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("pwa.urls")),
    path("", include("core.urls")),
    path("", include("materia_prima.urls")),
    path("", include("proveedores.urls")),
    path("", include("gastos.urls")),
    path("", include("recetas.urls")),
    path("", include("ventas.urls")),
    path("", include("inventario.urls")),
    path("", include("reportes.urls")),
]
