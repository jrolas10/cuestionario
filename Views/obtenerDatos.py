
from django.http import JsonResponse
from Cuestionario.models import Encuestado
def obtener_datos_encuestado(request, encuestado_id):
    try:
        encuestado = Encuestado.objects.get(pk=encuestado_id)
        detalles = {
            'nombre': encuestado.nombre,
            'grupo': encuestado.grupo.nombre,
            'carrera': encuestado.carrera.nombre,
            'semestre': encuestado.semestre,
            'edad': encuestado.edad,
            'correo': encuestado.correo_electronico,
        }
        return JsonResponse(detalles)
    except Encuestado.DoesNotExist:
        return JsonResponse({})
