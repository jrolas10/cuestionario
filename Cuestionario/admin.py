from django.contrib import admin
from .models import Carrera, Grupo, Categoria, Pregunta, Encuestado, Respuesta

class RespuestaInline(admin.TabularInline):
    model = Respuesta
    extra = 0

class EncuestadoInline(admin.TabularInline):
    model = Encuestado
    extra = 0
    fields = ('nombre', 'edad', 'sexo', 'estado_civil', 'semestre', 'correo_electronico')

@admin.register(Encuestado)
class EncuestadoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'edad', 'sexo', 'estado_civil', 'carrera', 'grupo', 'semestre', 'correo_electronico')
    list_filter = ('carrera', 'grupo', 'semestre')
    search_fields = ('nombre', 'correo_electronico')
    inlines = [RespuestaInline]

class GrupoInline(admin.TabularInline):
    model = Grupo
    extra = 0
    fields = ('nombre',)

@admin.register(Carrera)
class CarreraAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    inlines = [GrupoInline]

@admin.register(Grupo)
class GrupoAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    inlines = [EncuestadoInline]

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "encuestado":
            grupo_id = request.resolver_match.kwargs['object_id']
            grupo = Grupo.objects.get(pk=grupo_id)
            kwargs["queryset"] = Encuestado.objects.filter(grupo=grupo)
        return super().formfield_for_manytomany(db_field, request, **kwargs)

@admin.register(Pregunta)
class PreguntaAdmin(admin.ModelAdmin):
    list_display = ('texto', 'categoria')
    list_filter = ('categoria',)

admin.site.register(Categoria)




