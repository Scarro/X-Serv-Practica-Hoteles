from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^actualizar/$', views.actualizarAlojamientos, name="parseador.actualizar"),
]