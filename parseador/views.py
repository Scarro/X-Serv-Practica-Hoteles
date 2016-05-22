from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.db.models import Count
from bs4 import BeautifulSoup

from alojamientos.models import Alojamiento, Tag, LinkImagen
from .models import EnlaceXML

import urllib2

def parsearBasicData(query):
    nombre = query.find('name').string
    telefono = query.find('phone').string
    email = query.find('email').string
    descripcion = query.find('body').string
    url = query.find('web').string
    return (nombre, telefono, email, descripcion, url)

def parsearGeoData(query):
    calle = query.find('address').string
    cpostal = query.find('zipcode').string
    ciudad = query.find('subAdministrativeArea').string
    pais = query.find('country').string
    latitud = query.find('latitude').string
    longitud = query.find('longitude').string
    return (calle, cpostal, ciudad, pais, latitud, longitud)

def parsearMultimedia(query):
    media = query.find_all('media')
    enlaces = []
    for sibling in media:
        if sibling['type'] == 'image':
            enlaces.append(sibling.url.string)
    return enlaces

def parsearExtraData(query):
    extra = query.find_all('item')
    clase = {}
    for tag in extra:
        if tag['name'] == "Categoria" and tag.string != '':
            clase['categoria'] = unicode(tag.string)
        if tag['name'] == 'SubCategoria' and tag.string != '':
            clase['subcategoria'] = unicode(tag.string)
    return clase

def agregarEtiquetas(tags,numero):
    alojamiento = Alojamiento.objects.all()[numero]
    etiqueta = tags[numero]
    if etiqueta.has_key('categoria'):
        tag1 = etiqueta['categoria']
        categoria = Tag(nombre=tag1, tipo=1)
        try:
            categoria.save();
        except:
            categoria = Tag.objects.get(nombre=tag1)
            alojamiento.tags.add(categoria)
    if etiqueta.has_key('subcategoria'):
        tag2 = etiqueta['subcategoria']
        subcategoria = Tag(nombre=tag2, tipo=2)
        try:
            subcategoria.save()
        except:
            subcategoria = Tag.objects.get(nombre=tag2)
            alojamiento.tags.add(subcategoria)


def agregarMultimedia(mult, numero):
    alojamiento = Alojamiento.objects.all()[numero]
    multimedia = mult[numero]
    for item in multimedia:
        if item != 'vacio':
            LinkImagen.objects.create(alojamiento=alojamiento,url=item)

def recargar(self):
    try:
        enlaces = EnlaceXML.objects.all()
        enlaces.delete()
    except:
        pass
    url = "http://datos.madrid.es/portal/site/egob/menuitem.c05c1f754a33a9fbe4b2e4b284f1a5a0/?vgnextoid=df42a73970504510VgnVCM2000001f4a900aRCRD&vgnextchannel=374512b9ace9f310VgnVCM100000171f5a0aRCRD&vgnextfmt=default"
    soup = BeautifulSoup(urllib2.urlopen(url).read(), "lxml")
    lang = ['es', 'en', 'fr', 'ger', 'it', 'pg', 'rs']
    number = 0
    if soup:
        enlaces = []
        a = soup.find_all('a')
        for enlace in a:
            clase = enlace.get('class')
            if clase != None and len(clase) > 1:
                if clase[1] == 'ico-xml':
                    idioma = lang[number]
                    link = enlace.get('href')
                    link = "http://datos.madrid.es" + link
                    resultado = EnlaceXML(idioma=idioma, url=link)
                    enlaces.append(resultado)
                    number += 1
    for enlace in enlaces:
        enlace.save()
    return ;

def parsearAlojamiento(alojamiento_id, idioma):
    alojamiento = Alojamiento.objects.get(id=alojamiento_id)
    url = EnlaceXML.objects.get(idioma=idioma)

    soup = BeautifulSoup(urllib2.urlopen(url.url).read(), 'lxml-xml')
    numero = (int(alojamiento_id) % 665)
    servicios = soup.find_all('service')
    numerohoteles = len(servicios)
    numero = (int(alojamiento_id) % numerohoteles)

    servicio = servicios[numero]
    existe = False
    for tag in servicio.descendants:
        if tag.name == 'basicData':
            descripcion = tag.find('body').string
            descripcion = BeautifulSoup(descripcion, 'lxml').text

    return descripcion


def actualizarAlojamientos(request):
    try:
        Alojamiento.objects.all().delete()
    except:
        pass
    seleccionado = EnlaceXML.objects.get(idioma='es')
    url = seleccionado.url
    soup = BeautifulSoup(urllib2.urlopen(url).read(), 'lxml-xml')
#    soup = BeautifulSoup(open("media/alojamientos.xml"), "lxml-xml")
    if soup:
        todos = soup.find_all('service')
        if todos:
            numero = 0
            alojamientos = []
            imagenes = []
            tags = []
            existe = False
            for numero in range(len(todos)):
            #for numero in range(20):
                for tag in todos[numero].descendants:
                    if tag.name == 'basicData':
                        basicData = parsearBasicData(tag)
                        descripcion = BeautifulSoup(basicData[3], 'lxml').text
                        if basicData[4] != "" and  basicData[0] != "":
                            alojamiento = Alojamiento(nombre=basicData[0], telefono=basicData[1], email=basicData[2], descripcion=descripcion, url=basicData[4])
                            alojamientos.append(alojamiento)
                            existe = True
                    if tag.name == 'geoData' and existe:
                        geoData = parsearGeoData(tag)
                        alojamiento.calle = geoData[0]
                        alojamiento.cpostal = geoData[1]
                        alojamiento.ciudad = geoData[2]
                        alojamiento.pais = geoData[3]
                        alojamiento.latitud = geoData[4]
                        alojamiento.longitud = geoData[5]
                    if tag.name == 'multimedia' and existe:
                        multimedia = parsearMultimedia(tag)
                        if multimedia == []:
                            multimedia = ['vacio']
                        imagenes.append(multimedia)
                    if tag.name == 'extradata' and existe:
                        extra = parsearExtraData(tag)
                        tags.append(extra)
                existe = False
                if (len(alojamientos) > 200) or (numero == (len(todos)-1)):
                    for alojamiento in alojamientos:
                        alojamiento.save()
                    alojamientos = []
            numero = 0
            rango = Alojamiento.objects.all().count()
            for numero in range(rango):
                agregarEtiquetas(tags, numero)
                agregarMultimedia(imagenes, numero)

    return redirect(reverse('alojamientos.todos'))