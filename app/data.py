import os
from django.contrib.gis.utils import LayerMapping
from .models import *

# Auto-generated `LayerMapping` dictionary for World model
world_mapping = {
    'un': 'UN',
    'name': 'NAME',
    'lon': 'LON',
    'lat': 'LAT',
    'geom': 'MULTIPOLYGON',
}


world_shp = os.path.abspath(os.path.join(os.path.dirname(__file__),'data','world.shp'))

def run(verbose=True):

	lm = LayerMapping(World,world_shp,world_mapping,transform=False,encoding='iso-8859-1')
    
	lm.save(strict=True,verbose=verbose)