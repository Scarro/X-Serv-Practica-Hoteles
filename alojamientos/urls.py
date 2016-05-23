from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.AlojamientoListView.as_view(), name="alojamientos.todos"),
    url(r'^buscar/$', views.buscar_view, name="alojamientos.buscar"),
    url(r'^buscar/(?P<alojamiento_id>[-\w]+)/(?P<idioma>[-\w]+)$', views.detalle_view, name="alojamiento.detallebuscado"),
    url(r'^crear_comentario/(?P<alojamiento_id>[-\w]+)/$', views.crear_comentario, name='alojamientos.comentario'),
    url(r'^seleccionar/(?P<alojamiento_id>[-\w]+)/$', views.seleccionar, name="alojamientos.seleccionar"),
    url(r'^(?P<alojamiento_id>[-\w]+)/(?P<idioma>[-\w]+)$', views.detalle_view, name='alojamientos.detalle'),
]