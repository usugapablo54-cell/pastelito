from .models import DatosNegocio

def datos_negocio(request):
    datos, _ = DatosNegocio.objects.get_or_create(pk=1)
    return {"datos_negocio": datos}
