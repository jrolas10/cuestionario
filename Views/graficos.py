from django.shortcuts import render
from Cuestionario.models import Encuestado, Categoria, Pregunta, Respuesta
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import base64

def ajustar_texto(texto, max_length=15):
    words = texto.split()
    lines = []
    current_line = ''
    for word in words:
        if len(current_line + word) <= max_length:
            current_line += word + ' '
        else:
            lines.append(current_line)
            current_line = word + ' '
    lines.append(current_line)
    return '\n'.join(lines)

def mostrar_graficos(request):
    if request.method == 'POST':
        encuestado_id = request.POST.get('encuestado')

        try:
            encuestado = Encuestado.objects.get(id=encuestado_id)
            categoria_innovacion = Categoria.objects.get(nombre='resolucion de conflictos')

            preguntas_innovacion = Pregunta.objects.filter(categoria=categoria_innovacion)

            datos_respuestas = {}
            for pregunta in preguntas_innovacion:
                respuestas_pregunta = Respuesta.objects.filter(encuestado=encuestado, pregunta=pregunta)
                valor_respondido = respuestas_pregunta[0].valor if respuestas_pregunta.exists() else 0
                datos_respuestas[pregunta.texto] = valor_respondido

            colores = ['skyblue', 'salmon', 'lightgreen', 'orange', 'lightblue']

            plt.figure(figsize=(10, 6))

            for i, pregunta in enumerate(preguntas_innovacion):
                respuestas_pregunta = Respuesta.objects.filter(encuestado=encuestado, pregunta=pregunta)
                valor_respondido = respuestas_pregunta[0].valor if respuestas_pregunta.exists() else 0

                texto_etiqueta = ajustar_texto(pregunta.texto)
                plt.bar(texto_etiqueta, valor_respondido, color=colores[i % len(colores)])

            plt.ylabel('Valor Respondido')
            plt.title('Valor respondido a preguntas de Innovación')
            plt.ylim(0, 5)  # Establecer límites del eje y de 0 a 5
            plt.tight_layout()

            buffer = io.BytesIO()
            plt.savefig(buffer, format='png')
            buffer.seek(0)

            grafico_base64 = base64.b64encode(buffer.getvalue()).decode()

            buffer.close()
            plt.close()

            detalles_encuestado = {
                'nombre': encuestado.nombre,
                'grupo': encuestado.grupo.nombre,
                'carrera': encuestado.carrera.nombre,
                'semestre': encuestado.semestre,
                'edad': encuestado.edad,
                'correo': encuestado.correo_electronico,
            }

            encuestados = Encuestado.objects.all()
            return render(request, 'grafico.html', {
                'encuestado': encuestado,
                'grafico_base64': grafico_base64,
                'detalles_encuestado': detalles_encuestado,
                'encuestados': encuestados,
            })

        except (Encuestado.DoesNotExist, Categoria.DoesNotExist) as e:
            return render(request, 'error.html', {'error_message': str(e)})
    else:
        encuestados = Encuestado.objects.all()
        return render(request, 'grafico.html', {'encuestados': encuestados})
