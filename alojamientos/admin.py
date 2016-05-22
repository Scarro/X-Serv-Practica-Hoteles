from django.contrib import admin
from .models import Alojamiento, Tag, LinkImagen, Comentario
from django.contrib.auth.models import Permission

admin.site.register(Alojamiento)
admin.site.register(Tag)
admin.site.register(LinkImagen)
admin.site.register(Comentario)
admin.site.register(Permission)