from django.shortcuts import render

from alojamientos.models import Alojamiento
from usuarios.models import PerfilUsuario
from django.contrib.auth.models import User
from django.db.models import Count
from usuarios.views import colorSet, sizeSet

def index_view(request):
    alojamientos = Alojamiento.objects.filter(comentario_alojamiento__isnull=False)
    alojamientos = alojamientos.annotate(num_comentarios = Count('comentario_alojamiento'))
    alojamientos = alojamientos.order_by('-num_comentarios')[:10]

    if alojamientos.count() == 0:
        alojamientos = False

    usuarios = PerfilUsuario.objects.all()
    usercolor = colorSet(request.user.username)
    usersize = sizeSet(request.user.username)
    context = {
        'alojamientos': alojamientos,
        'usuarios': usuarios,
        'usercolor': usercolor,
        'usersize': usersize,
    }
    return render(request, 'principal.html', context)

def about(request):
    context = {
        'about': 'about'
    }
    return render(request, 'about.html', context)