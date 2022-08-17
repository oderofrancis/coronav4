from django.urls import path

from .country import *


urlpatterns =[

	# select country

    path('africa/country',africa_country,name='africa_country'),

    path('asia/country',asia_country,name='asia_country'),

    path('america/country',america_country,name='america_country'),

    path('latin/country',latin_country,name='latin_country'),

    path('europe/country',europe_country,name='europe_country'),

    path('oceania/country',oceania_country,name='oceania_country'),

]