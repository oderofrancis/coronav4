from django.db import models
from django.contrib.gis.db import models

# Create your models here.

class World(models.Model):
    un = models.BigIntegerField()
    name = models.CharField(max_length=254)
    lon = models.FloatField()
    lat = models.FloatField()
    geom = models.MultiPolygonField(srid=4326)

    def __str__(self):
    	return self.name

    class Meta:
        verbose_name_plural="World"