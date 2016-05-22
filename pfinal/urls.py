"""pfinal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from . import views as main_views
from usuarios import views as usuario_views

urlpatterns = [
    url(r'^admin', admin.site.urls),
    url(r'^admin/', admin.site.urls),
    url(r'^$', main_views.index_view, name='main.index'),
    url(r'^alojamientos/', include('alojamientos.urls')),
    url(r'registro/$', usuario_views.registro_view, name="usuarios.registro"),
    url(r'login/$', usuario_views.login_view, name="usuarios.login"),
    url(r'^parseador/', include('parseador.urls')),
    url(r'^about/', main_views.about, name='main.about'),
    url(r'^(?P<usuario>[-\w]+)/', include('usuarios.urls')),
    url(r'^(?P<usuario>[-\w]+)$', usuario_views.index_view, name="main.usuario"),
]
