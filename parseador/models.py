from __future__ import unicode_literals

from django.db import models


class EnlaceXML(models.Model):
    idioma = models.CharField(max_length=100)
    url = models.CharField(max_length=300)

    class Meta:
        verbose_name= "EnlaceXML"
        verbose_name_plural = "EnlacesXML"

    def __unicode__(self):
        return self.idioma