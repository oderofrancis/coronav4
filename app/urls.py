from django.urls import path

from .views import *

from .country import *

urlpatterns = [
    path('',home,name='home'),

    path('world/',world,name='world'),

    path('africa/',africa,name='africa'),

    path('america/',america,name='america'),

    path('asia/',asia,name='asia'),

    path('europe/',europe,name='europe'),

    path('latin/',latin,name='latin'),

    path('oceania/',oceania,name='oceania'),

    # data

    path('world_con/',world_con,name='world_con'),

    path('world_death/',world_death,name='world_death'),


    path('africa_con/',africa_con,name='africa_con'),

    path('africa_death/',africa_death,name='africa_death'),


    path('america_con/',america_con,name='america_con'),

    path('america_death/',america_death,name='america_death'),



    path('latin_con/',latin_con,name='latin_con'),

    path('latin_death/',latin_death,name='latin_death'),



    path('asia_con/',asia_con,name='asia_con'),

    path('asia_death/',asia_death,name='asia_death'),


    path('europe_con/',europe_con,name='europe_con'),

    path('europe_death/',europe_death,name='europe_death'),


    path('oceania_con/',oceania_con,name='oceania_con'),

    path('oceania_death/',oceania_death,name='oceania_death'),


]