from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index_view, name="usuarios.index"),
    url(r'^gracias/$', views.gracias_view, name="usuarios.gracias"),
    url(r'^logout/$', views.logout_view, name="usuarios.logout"),
    url(r'^editar_email/$', views.editar_email, name='usuarios.editar_email'),
    url(r'^editar_color/$', views.editar_color, name='usuarios.editar_color'),
    url(r'^editar_size/$', views.editar_size, name='usuarios.editar_size'),
    url(r'^editar_titulo/$', views.editar_titulo, name='usuarios.editar_titulo'),
    url(r'^xml/$', views.xml_view, name='usuarios.xml')
#    url(r'^editar_contrasena/$', views.editar_contrasena, name='usuarios.editar_contrasena'),
]