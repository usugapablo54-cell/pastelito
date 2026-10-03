from django.shortcuts import render, redirect
from django.utils import timezone
from django.db.models import Sum
from materia_prima.models import Insumo
from gastos.models import Gasto
from ventas.models import Producto
from recetas.models import Receta
from .models import DatosNegocio
from .forms import DatosNegocioForm
import subprocess
from django.http import HttpResponse
from django.conf import settings
from datetime import datetime


def dashboard(request):
    hoy = timezone.now()

    insumos = Insumo.objects.all()
    valor_inventario = sum(i.valor_stock for i in insumos)
    productos_poco_stock = [i for i in insumos if i.stock_bajo]
    insumos_por_vencer = [i for i in insumos if i.dias_para_vencer is not None and i.dias_para_vencer <= 7]
    insumos_vencidos = [i for i in insumos if i.esta_vencido]

    gastos_mes = Gasto.objects.filter(fecha__year=hoy.year, fecha__month=hoy.month)
    total_gastos_mes = gastos_mes.aggregate(total=Sum('monto'))['total'] or 0

    gastos_recientes = Gasto.objects.order_by('-fecha')[:5]

    total_recetas = Receta.objects.count()
    total_productos = Producto.objects.count()

    from ventas.models import VentaRealizada
    ventas_mes = VentaRealizada.objects.filter(fecha__year=hoy.year, fecha__month=hoy.month)
    ingreso_mes = sum(v.ingreso_total for v in ventas_mes)
    utilidad_mes = sum(v.utilidad_real for v in ventas_mes)

    context = {
        'total_gastos_mes': total_gastos_mes,
        'valor_inventario': valor_inventario,
        'productos_poco_stock': productos_poco_stock,
        'insumos_por_vencer': insumos_por_vencer,
        'gastos_recientes': gastos_recientes,
        'total_recetas': total_recetas,
        'total_productos': total_productos,
        'total_insumos': insumos.count(),
        'ingreso_mes': ingreso_mes,
        'utilidad_mes': utilidad_mes,
        'insumos_vencidos': insumos_vencidos,
    }
    return render(request, 'core/dashboard.html', context)


def configuracion(request):
    datos, _ = DatosNegocio.objects.get_or_create(pk=1)
    if request.method == "POST":
        form = DatosNegocioForm(request.POST, request.FILES, instance=datos)
        if form.is_valid():
            form.save()
    else:
        form = DatosNegocioForm(instance=datos)
    return render(request, "core/configuracion.html", {"form": form})


def descargar_backup(request):
    from django.conf import settings as dj_settings
    db_path = dj_settings.DATABASES['default']['NAME']
    filename = f"dummy_{datetime.now().strftime('%Y%m%d_%H%M%S')}.sqlite3"
    with open(db_path, 'rb') as f:
        response = HttpResponse(f.read(), content_type='application/octet-stream')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response

    response = HttpResponse(result.stdout, content_type="application/sql")
    response["Content-Disposition"] = f'attachment; filename="{filename}"'
    return response

from .models import Cierre
from django.utils import timezone as tz
from inventario.models import MovimientoInventario

def lista_cierres(request):
    cierres = Cierre.objects.all()
    return render(request, 'core/cierres.html', {'cierres': cierres})

def crear_cierre(request):
    hoy = tz.now().date()

    gastos_hoy = Gasto.objects.filter(fecha=hoy)
    total_gastos_hoy = gastos_hoy.aggregate(total=Sum('monto'))['total'] or 0

    from ventas.models import VentaRealizada
    ventas_hoy = VentaRealizada.objects.filter(fecha=hoy)
    total_ingresos_hoy = sum(v.ingreso_total for v in ventas_hoy)
    total_utilidad_hoy = sum(v.utilidad_real for v in ventas_hoy)

    movimientos_hoy_qs = MovimientoInventario.objects.filter(fecha__date=hoy)
    movimientos_hoy = movimientos_hoy_qs.count()
    insumos_hoy = Insumo.objects.filter(creado_en__date=hoy).count()
    poco_stock = len([i for i in Insumo.objects.all() if i.stock_bajo])

    if request.method == 'POST':
        notas = request.POST.get('notas', '')
        cierre, created = Cierre.objects.update_or_create(
            fecha=hoy,
                        defaults={
                'total_gastos': total_gastos_hoy,
                'total_ingresos': total_ingresos_hoy,
                'total_utilidad': total_utilidad_hoy,
                'total_movimientos': movimientos_hoy,
                'insumos_creados': insumos_hoy,
                'productos_con_poco_stock': poco_stock,
                'notas': notas,
            }
        )
        return redirect('lista_cierres')

    context = {
        'hoy': hoy,
        'total_gastos_hoy': total_gastos_hoy,
        'total_ingresos_hoy': total_ingresos_hoy,
        'total_utilidad_hoy': total_utilidad_hoy,
        'gastos_hoy': gastos_hoy,
        'ventas_hoy': ventas_hoy,
        'movimientos_hoy_qs': movimientos_hoy_qs,
        
    }
    return render(request, 'core/hacer_cierre.html', context)

def lobby(request):
    return render(request, 'core/lobby.html')

