from django.contrib import admin
from django.urls import path
from Views import HomeView  # Modificación en la importación
#from Views.ViewGraficas import mostrar_grafica_admin
from Views.graficos import mostrar_graficos
#from Views.graficos import obtener_datos_encuestado


urlpatterns = [
    path('admin/', admin.site.urls),
    
    #path('admin/mostrar_grafica/', mostrar_grafica_admin, name='mostrar_grafica'),


    
    path('', HomeView.home, name='home'),
    path('formulario/', HomeView.formulario, name='formulario'),
    path('procesarformulario/', HomeView.procesarformulario, name='procesarformulario'),
    path('exito/', HomeView.exito, name='exito'),
    path('terminos-y-condiciones/', HomeView.terminos_y_condiciones, name='terminos_y_condiciones'),

    path('innovacion/', HomeView.innovacion, name='innovacion'),
    path('procesar_respuestas/', HomeView.procesar_respuestas, name='procesar_respuestas'),
    
    path('resolucion-de-conflictos/', HomeView.resolucion, name='resolucion'),    
    path('procesar_respuestas_resolucion/', HomeView.procesar_respuestas_resolucion, name='procesar_respuestas_resolucion'),

    #path('graficos/', mostrar_graficos, name='mostrar_graficos'),
    
    
    path('base-graficas/', HomeView.base_graficas, name='base'),
    #path('mostrar-grafica/', HomeView.mostrar_grafica, name='mostrar_grafica'),


    #path('obtener_datos_encuestado/<int:encuestado_id>/', obtener_datos_encuestado, name='obtener_datos_encuestado'),
    path('mostrar_graficos/', mostrar_graficos, name='mostrar_graficos'),
]

