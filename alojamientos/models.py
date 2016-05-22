from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from usuarios.models import PerfilUsuario


class Tag(models.Model):
    nombre = models.CharField(max_length=100)
    slug = models.CharField(max_length=100, unique=True)
    tipo = models.IntegerField()

    class Meta:
        verbose_name = "Etiqueta"
        verbose_name_plural = "Etiquetas"

    def __unicode__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        self.slug = slugify(self.nombre)
        return super(Tag, self).save(*args, **kwargs)


class Alojamiento(models.Model):
    nombre = models.CharField(max_length=200, unique=True)
    slug = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20, blank= True, null=True)
    email = models.EmailField(max_length=254, blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    url = models.CharField(max_length=300)
    tags = models.ManyToManyField(Tag)
    #(calle, cpostal, ciudad, pais, latitud, longitud)
    calle = models.CharField(max_length=200, blank= True, null=True)
    cpostal = models.IntegerField(blank= True, null=True)
    ciudad = models.CharField(max_length=100, blank= True, null=True)
    pais = models.CharField(max_length=100, blank= True, null=True)
    latitud = models.FloatField(blank= True, null=True)
    longitud = models.FloatField(blank= True, null=True)
    seleccionado = models.ManyToManyField(PerfilUsuario)

    class Meta:
        verbose_name = "Alojamiento"
        verbose_name_plural = "Alojamientos"

    def __unicode__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        self.slug = slugify(self.nombre)
        return super(Alojamiento, self).save(*args, **kwargs)


class LinkImagen(models.Model):
    alojamiento = models.ForeignKey(
        Alojamiento, 
        related_name="foto_alojamiento",
        on_delete=models.CASCADE,
    )
    url = models.CharField(max_length=300)

    class Meta:
        verbose_name = "LinkImagen"
        verbose_name_plural = "LinksImagenes"
    
    def __unicode__(self):
        return self.alojamiento.nombre

class Comentario(models.Model):
    usuario = models.ForeignKey(User, related_name="comentario_usuario", on_delete=models.CASCADE)
    alojamiento = models.ForeignKey(Alojamiento, related_name="comentario_alojamiento", on_delete=models.CASCADE)
    title = models.CharField(max_length=300)
    body = models.TextField()
    creado = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.title

    # Direccion a la que redirecciona una vez agregado un comentario
    def get_absolute_url(self):
        return reverse('alojamientos.detalle', kwargs={'alojamiento_id':self.id})