from django.db import models

class Carrera(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Grupo(models.Model):
    nombre = models.CharField(max_length=100)
    carrera = models.ForeignKey(Carrera, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Pregunta(models.Model):
    texto = models.CharField(max_length=255)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)

    def __str__(self):
        return self.texto

class Encuestado(models.Model):
    nombre = models.CharField(max_length=100)
    edad = models.SmallIntegerField()
    sexo = models.CharField(max_length=20)
    estado_civil = models.CharField(max_length=20)
    carrera = models.ForeignKey(Carrera, on_delete=models.CASCADE)
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE)
    semestre = models.SmallIntegerField()
    correo_electronico = models.EmailField(default='sincorreo@electronico.com')

    def __str__(self):
        return self.nombre

class Respuesta(models.Model):
    encuestado = models.ForeignKey(Encuestado, on_delete=models.CASCADE)
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE)
    valor = models.SmallIntegerField()

    def __str__(self):
        return f"Encuesta de {self.encuestado.nombre} - Pregunta: {self.pregunta.texto}"
