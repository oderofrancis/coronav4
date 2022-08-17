from django.contrib import admin
from .models import *
from leaflet.admin import LeafletGeoAdmin

# Register your models here.


class WorldAdmin(LeafletGeoAdmin):

	list_display=("name","un")

admin.site.register(World,WorldAdmin)