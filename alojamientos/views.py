from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from parseador.views import parsearAlojamiento
from .models import Alojamiento, Tag, LinkImagen, Comentario
from usuarios.models import PerfilUsuario
from .forms import BuscadorForm, ComentarioCreateForm
from usuarios.views import colorSet, sizeSet


class AlojamientoListView(generic.ListView):
    template_name = 'alojamientos/todos.html'
    model = Alojamiento
    context_object_name = 'alojamientos'
    paginate_by = 10
#   ordering

    def get_context_data(self, **kargs):
        # Obtenemos el contexto de la clase base
        context = super(AlojamientoListView, self).get_context_data(**kargs)
        # Agregamos nuevas variables de contexto al diccionario
        CHOICES = (
        ('nombre', 'Nombre'),
        ('categoria', 'Categoria'),
        ('subcategoria', 'Subcategoria')
         )
        form = BuscadorForm(CHOICES)
        context['usercolor'] = self.usercolor
        context['usersize'] = self.usersize
        context['form'] = form
        context['buscador'] = "si"
        context['titulo'] = 'Buscar por categoria'
        context['nombre_btn'] = 'Buscar'
        context['todos'] = True

        return context

    def dispatch(self, request, *args, **kwargs):
        self.usercolor = colorSet(request.user.username)
        self.usersize = sizeSet(request.user.username)
        return super(AlojamientoListView, self).dispatch(request, *args, **kwargs)


def detalle_view(request, alojamiento_id, idioma):
    try:
        alojamiento = Alojamiento.objects.get(id=alojamiento_id)
    except:
        return redirect(reverse('alojamientos.todos'))
    fotos = []
    try:
        fotos = alojamiento.foto_alojamiento.all()
    except:
        pass
    try:
        comentarios = alojamiento.comentario_alojamiento.all().order_by('-creado')
    except:
        pass
    usuario = PerfilUsuario(nombre=request.user.username)
#    print Alojamiento.objects.filter(seleccionado__nombre=request.user.username)
    try:
        alojamiento.seleccionado.get(nombre=request.user.username)
        seleccionado = True
    except:
        seleccionado = False

    descripcion = False
    if idioma != 'es':
        descripcion = parsearAlojamiento(alojamiento_id, idioma)

    usercolor = colorSet(request.user.username)
    usersize = sizeSet(request.user.username)
    context = {
        'alojamiento': alojamiento,
        'fotos': fotos,
        'comentarios': comentarios,
        'usercolor': usercolor,
        'usersize': usersize,
        'seleccionado': seleccionado,
        'idioma': descripcion
    }

    return render(request, 'alojamientos/detalle.html', context)

def buscar_view(request):
    if request.method == "POST":
        form = BuscadorForm(request.POST, request.FILES)
        if form.is_valid:
            alojamientos = []
            categoria =  request.POST['categoria']
            texto = request.POST['texto']
            if categoria != 'nombre':
                if categoria == 'categoria':
                    categorias = Tag.objects.filter(nombre__icontains=texto, tipo=1)
                    for categoria in categorias:
                        alojamientosaux = categoria.alojamiento_set.all()
                        for alojamiento in alojamientosaux:
                            alojamientos.append(alojamiento)
                elif categoria == 'subcategoria':
                    categorias = Tag.objects.filter(nombre__icontains=texto, tipo=2)
                    for categoria in categorias:
                        alojamientosaux = categoria.alojamiento_set.all()
                        for alojamiento in alojamientosaux:
                            alojamientos.append(alojamiento)
            else:
                alojamientos = Alojamiento.objects.filter(nombre__icontains=texto)
    usercolor = colorSet(request.user.username)
    usersize = sizeSet(request.user.username)
    context = {
        'alojamientos': alojamientos,
        'usercolor': usercolor,
        'usersize': usersize,
    }
    template = 'alojamientos/todos.html'
    return render(request, template, context)

@login_required
def seleccionar(request, alojamiento_id):
    try:
        alojamiento=Alojamiento.objects.get(id=alojamiento_id)
        nombre = request.user.username
        usuario = PerfilUsuario.objects.get(nombre=nombre)
        alojamiento.seleccionado.add(usuario)
        seleccionado = True
    except:
        pass
    context = {
        'seleccionado': seleccionado
    }
    return redirect(reverse('alojamientos.detalle', args=[alojamiento_id, 'es']))

@login_required
def crear_comentario(request, alojamiento_id):
    form = ComentarioCreateForm
    print alojamiento_id
    
    if request.method == "POST":
        form = ComentarioCreateForm(request.POST, request.FILES)

        if form.is_valid():
            cleaned_data = form.cleaned_data
            user= User.objects.get(username=request.user.username)
            alojamiento = Alojamiento.objects.get(id=alojamiento_id)
            title = cleaned_data.get('title')
            body = cleaned_data.get('body')
            comentario = Comentario.objects.create(usuario=user, alojamiento=alojamiento, title=title, body=body)

            return redirect(reverse('alojamientos.detalle', args=[alojamiento_id, 'es']))

    template = 'alojamientos/comentario_form.html'
    usercolor = colorSet(request.user.username)
    usersize = sizeSet(request.user.username)
    context = {
        'titulo': "Crear Comentario",
        'nombre_btn': "Crear",
        'form': form,
        'usercolor': usercolor,
        'usersize': usersize,
    }

    return render(request, template, context)