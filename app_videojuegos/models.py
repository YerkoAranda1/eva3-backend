from django.db import models

class Videojuego(models.Model):
    titulo = models.CharField(max_length=150)
    plataforma = models.CharField(max_length=50)
    genero = models.CharField(max_length=50)
    precio = models.IntegerField()
    stock = models.IntegerField()
    fecha_estreno = models.DateField(verbose_name="Fecha de estreno")

    def __str__(self):
        return self.titulo