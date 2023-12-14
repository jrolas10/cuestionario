from django.http import HttpResponse
from django.template.loader import get_template
from django.shortcuts import render, redirect
from Cuestionario.models import Encuestado, Pregunta, Respuesta, Carrera, Grupo, Categoria
from django.shortcuts import get_object_or_404
from .decorators import encuestado_autenticado

def home(request):
    plantilla = get_template('inicio.html')
    return HttpResponse(plantilla.render())


def base_graficas(request):
    plantilla = get_template('base_graficas.html')
    return HttpResponse(plantilla.render())


def formulario(request):
    # Obtener carreras y grupos desde la base de datos
    carreras = Carrera.objects.values_list('nombre', flat=True).distinct()
    grupos = Grupo.objects.values_list('nombre', flat=True).distinct()

    context = {
        'carreras': carreras,
        'grupos': grupos,
    }

    plantilla = get_template('formulario.html')
    return HttpResponse(plantilla.render(context, request))


@encuestado_autenticado
def innovacion(request):
    encuestado_id = request.session.get('encuestado_id')
    if encuestado_id:
        categoria_innovacion = Categoria.objects.get(nombre='innovacion')  # Cambia el nombre de la categoría
        preguntas = Pregunta.objects.filter(categoria=categoria_innovacion)
        return render(request, 'PreguntasUno.html', {'preguntas': preguntas, 'encuestado_id': encuestado_id})
    else:
        return HttpResponse('Encuestado no encontrado', status=404)

@encuestado_autenticado
def resolucion(request):
    encuestado_id = request.session.get('encuestado_id')
    if encuestado_id:
        categoria_resolucion = Categoria.objects.get(nombre='resolucion de conflictos')  # Cambia el nombre de la categoría
        preguntas = Pregunta.objects.filter(categoria=categoria_resolucion)
        return render(request, 'PreguntasDos.html', {'preguntas': preguntas, 'encuestado_id': encuestado_id})
    else:
        return HttpResponse('Encuestado no encontrado', status=404)






def terminos_y_condiciones(request):
    plantilla = get_template('terminos_condiciones.html')
    return HttpResponse(plantilla.render())

def exito(request):
    plantilla = get_template('exito.html')
    return HttpResponse(plantilla.render())

def procesarformulario(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombreCompleto')
        edad = request.POST.get('edad')
        sexo = request.POST.get('sexo')
        estado_civil = request.POST.get('estadoCivil')
        nombre_carrera = request.POST.get('carrera')
        grupo = request.POST.get('grupo')
        semestre = request.POST.get('semestre')
        correo_electronico = request.POST.get('correoElectronico')

        # Obtener la instancia de Carrera correspondiente al nombre proporcionado
        try:
            carrera_obj = Carrera.objects.get(nombre=nombre_carrera)
        except Carrera.DoesNotExist:
            # Manejar el caso cuando la carrera no existe
            return HttpResponse('La carrera seleccionada no existe', status=404)
        try:
            grupo_obj = Grupo.objects.get(nombre=grupo)
        except Grupo.DoesNotExist:
            return HttpResponse('El grupo seleccionado no existe', status=404)
        
        encuestado = Encuestado(
            nombre=nombre,
            edad=edad,
            sexo=sexo,
            estado_civil=estado_civil,
            carrera=carrera_obj,
            semestre=semestre,
            grupo=grupo_obj,
            correo_electronico=correo_electronico
        )
        encuestado.save()
        request.session['encuestado_id'] = encuestado.id  # Guardar el ID en la sesión

        return redirect('innovacion')
    else:
        return HttpResponse('Método no permitido para esta vista', status=405)



def procesar_respuestas(request):
    if request.method == 'POST':
        encuestado_id = request.session.get('encuestado_id')
        if encuestado_id:
            encuestado = get_object_or_404(Encuestado, pk=encuestado_id)
            # Obtener las preguntas de la categoría 'innovacion'
            categoria_innovacion = Categoria.objects.get(nombre='innovacion')
            preguntas_innovacion = Pregunta.objects.filter(categoria=categoria_innovacion)
            for pregunta in preguntas_innovacion:
                valor_respuesta = request.POST.get(f'pregunta{pregunta.id}', '')
                respuesta = Respuesta(encuestado=encuestado, pregunta=pregunta, valor=valor_respuesta)
                respuesta.save()
            return redirect('resolucion')
        else:
            return HttpResponse('Encuestado no encontrado', status=404)
    else:
        return HttpResponse('Método no permitido para esta vista', status=405)



def procesar_respuestas_resolucion(request):
    if request.method == 'POST':
        encuestado_id = request.session.get('encuestado_id')
        if encuestado_id:
            encuestado = get_object_or_404(Encuestado, pk=encuestado_id)
            
            categoria_resolucion = Categoria.objects.get(nombre='resolucion de conflictos')
            preguntas_resolucion = Pregunta.objects.filter(categoria=categoria_resolucion)
            for pregunta in preguntas_resolucion:
                valor_respuesta = request.POST.get(f'pregunta{pregunta.id}', '')
                respuesta = Respuesta(encuestado=encuestado, pregunta=pregunta, valor=valor_respuesta)
                respuesta.save()
            return redirect('exito')
        else:
            return HttpResponse('Encuestado no encontrado', status=404)
    else:
        return HttpResponse('Método no permitido para esta vista', status=405)


import matplotlib.pyplot as plt
from django.shortcuts import render
from Cuestionario.models import Respuesta
import base64
from io import BytesIO

def mostrar_grafica(request):
    # Obtener datos para la gráfica desde las respuestas de la encuesta
    # Por ejemplo, obtener el recuento de respuestas por categoría
    categorias = ['Categoría A', 'Categoría B', 'Categoría C']
    valores = [Respuesta.objects.filter(pregunta__categoria__nombre='Categoría A').count(),
               Respuesta.objects.filter(pregunta__categoria__nombre='Categoría B').count(),
               Respuesta.objects.filter(pregunta__categoria__nombre='Categoría C').count()]

    # Generar gráfica con Matplotlib
    plt.figure(figsize=(8, 6))
    plt.bar(categorias, valores)
    plt.xlabel('Categorías')
    plt.ylabel('Cantidad de respuestas')
    plt.title('Respuestas por categoría')

    # Ajustes adicionales para presentación
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Guardar la gráfica en un objeto BytesIO
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    grafica_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    buffer.close()

    # Renderizar la plantilla HTML con la gráfica como base64
    return render(request, 'mostrar_grafica.html', {'grafica_base64': grafica_base64})
