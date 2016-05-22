# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse, reverse_lazy
from django.core import serializers
from django.http import HttpResponse

from .forms import RegistroUserForm, EditarColorForm, EditarEmailForm, EditarSizeForm, EditarTituloForm

from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib import admin
from django.contrib.auth.hashers import make_password

from alojamientos.models import Comentario
from .models import PerfilUsuario

import sys
import os

def colorSet(usuario):
    color = False
    try:
        usercolor = PerfilUsuario.objects.get(nombre=usuario)
        color = usercolor.color
    except:
        pass
    return color

def sizeSet(usuario):
    size = False
    try:
        usersize = PerfilUsuario.objects.get(nombre=usuario)
        size = usersize.size
    except:
        pass
    return size

def comprobarUsuario(request, usuario):
    mismo = False
    if request.user.username == usuario:
        mismo = True
    try:
        user = User.objects.get(username=usuario)
        user = PerfilUsuario.objects.get(user=user)
    except:
        user = False
    return (user, mismo)

def index_view(request, usuario):
    (user, mismo) = comprobarUsuario(request, usuario)
    usercolor = colorSet(request.user.username)
    usersize = sizeSet(request.user.username)

    try:
        usuario = PerfilUsuario.objects.get(nombre=usuario)
        seleccionados = usuario.alojamiento_set.all()
    except:
        seleccionados = False

    context = {
        'mismo': mismo,
        'usuario': user,
        'nombre': usuario,
        'usercolor': usercolor,
        'usersize': usersize,
        'seleccionados': seleccionados,
    }
    return render(request, 'usuarios/seleccionados.html', context)

def registro_view(request):
    if request.method == 'POST':
        form = RegistroUserForm(request.POST, request.FILES)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            username = cleaned_data.get('username')
            password = cleaned_data.get('password')
            email = cleaned_data.get('email')
            #foto...
            user_model = User.objects.create_user(username=username, password=password)
            # le otorgo el permiso de agregar comentarios a cada nuevo usuario
            content_type = ContentType.objects.get_for_model(Comentario)
            permisocomentar = Permission.objects.get(content_type=content_type, codename='add_comentario')
            user_model.user_permissions.add(permisocomentar)
            user_model.email = email
            user_model.save()
            user_profile = PerfilUsuario(nombre=user_model.username)
            user_profile.user = user_model
            user_profile.save()
            return redirect(reverse('usuarios.gracias', kwargs={'usuario':username}))
    else:
        form = RegistroUserForm
    context = {
        'form': form,
    }
    return render(request, 'usuarios/registro.html', context)

def login_view(request):
    # Si el usuario esta ya logueado, lo redireccionamos a index_view
    if request.user.is_authenticated():
        user = request.user.username
        return redirect(reverse('usuarios.index', kwargs={'usuario':user}))
    mensaje = ''
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                # Por ahora uso esta comprobacion
                # para registrar mi root en PerfilUsuario
                # Mirar como hacer de mejor manera
                if username == 'guybrush':
                    user_model = User.objects.get(username=username)
                    try:
                        user_profile = PerfilUsuario.objects.get(user=user_model)
                    except:
                        user_profile = PerfilUsuario(nombre=username)
                        user_profile.user = user_model
                        user_profile.save()
                return redirect(reverse('main.index'))
            else:
                # Redireccionar informando que la cuenta esta inactiva
                pass
        mensaje = 'Nombre de usuario o contraseña incorrecta'
    context = {
        'mensaje': mensaje,
    }
    return render(request, 'usuarios/login.html', context)


@login_required
def logout_view(request, usuario):
    logout(request)
    messages.success(request, usuario + ': has sido desconectado con exito.')
    return redirect(reverse('main.index'))

def gracias_view(request, usuario):
    context = {
        'mensaje': "Gracias por registrarte " + usuario,
    }
    return render(request, 'usuarios/gracias.html', context)

@login_required
def editar_email(request, usuario):
    if request.method == 'POST':
        form = EditarEmailForm(request.POST, request=request)
        if form.is_valid():
            request.user.email = form.cleaned_data['email']
            request.user.save()
            messages.success(request, 'El email ha sido cambiado con exito!.')
        direccion = "/" + request.user.username + "/"
        return redirect(direccion)
    else:
        form = EditarEmailForm(
            request=request,
            initial={'email': request.user.email})
        (user, mismo) = comprobarUsuario(request, usuario)
        usercolor = colorSet(request.user.username)
        usersize = sizeSet(request.user.username)
        context = {
            'form': form,
            'usuario':user,
            'mismo': mismo,
            'usercolor': usercolor,
            'usersize': usersize,
        }
    return render(request, 'usuarios/editar_email.html', context)

@login_required
def editar_color(request, usuario):
    if request.method == "POST":
        form = EditarColorForm(request.POST, request=request)
        if form.is_valid():
            user = User.objects.get(username=request.user.username)
            user = PerfilUsuario.objects.get(user=user)
            user.color = form['color'].value()
            user.save()
            messages.success(request, "El color ha sido modificado (si no es valido, por defecto se pondrá en blanco)")
        direccion = "/" + request.user.username + "/"
        return redirect(direccion)
    else:
        form = EditarColorForm(
            request=request
            )
        (user, mismo) = comprobarUsuario(request, usuario)
        usercolor = colorSet(request.user.username)
        usersize = sizeSet(request.user.username)
        context = {
            'form': form,
            'usuario': user,
            'mismo': mismo,
            'usercolor': usercolor,
            'usersize': usersize,
        }
        return render(request, 'usuarios/editar_color.html', context)

@login_required
def editar_size(request, usuario):
    if request.method == "POST":
        form = EditarSizeForm(request.POST, request=request)
        if form.is_valid():
            user = User.objects.get(username=request.user.username)
            user = PerfilUsuario.objects.get(user=user)
            user.size = form['size'].value()
            user.save()
            messages.success(request, "El tamaño ha sido modificado")
        direccion = "/" + request.user.username + "/"
        return redirect(direccion)
    else:
        form = EditarSizeForm(
            request=request
            )
        (user, mismo) = comprobarUsuario(request, usuario)
        usercolor = colorSet(request.user.username)
        usersize = sizeSet(request.user.username)
        context = {
            'form': form,
            'usuario': user,
            'mismo': mismo,
            'usercolor': usercolor,
            'usersize': usersize,
        }
        return render(request, 'usuarios/editar_size.html', context)

@login_required
def editar_titulo(request, usuario):
    if request.method == "POST":
        form = EditarTituloForm(request.POST, request=request)
        if form.is_valid():
            user = User.objects.get(username=request.user.username)
            user = PerfilUsuario.objects.get(user=user)
            user.titulo = form['titulo'].value()
            user.save()
            messages.success(request, "El titulo de la página principal ha sido modificado")
        direccion = "/" + request.user.username + "/"
        return redirect(direccion)
    else:
        form = EditarTituloForm(
            request=request
            )
        (user, mismo) = comprobarUsuario(request, usuario)
        usercolor = colorSet(request.user.username)
        usersize = sizeSet(request.user.username)
        context = {
            'form': form,
            'usuario': user,
            'mismo': mismo,
            'usercolor': usercolor,
            'usersize': usersize,
        }
        return render(request, 'usuarios/editar_titulo.html', context)

def xml_view(request, usuario):

    usuario = PerfilUsuario.objects.get(nombre=usuario)
    seleccionados = usuario.alojamiento_set.all()

    data = serializers.serialize('xml', seleccionados)

    print data

    return HttpResponse(data, content_type='application/xml')