from django.shortcuts import render
from django.core.serializers import serialize
from django.http import HttpResponse
from .models import World


import pandas as pd
import geopandas as gpd
import math

# Create your views here.

def home(request):

	context = {}

	return render(request,'continent/home.html',context)


# world data analysis


def world(request):

	confirmed=r'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'

	death=r'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv'

	data_cont = pd.read_csv(r'https://raw.githubusercontent.com/oderofrancis/rona/main/Countries-Continents.csv')

	# confirmed = r'/media/afroteop/da442186-249a-498d-9496-21fc43465d5f/corona_data/csse_covid_19_data/csse_covid_19_time_series/confirmed_global.csv'

	# death = r'/media/afroteop/da442186-249a-498d-9496-21fc43465d5f/corona_data/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv'
	
	# confirmed cases
	
	confirmed = pd.read_csv(confirmed)

	death = pd.read_csv(death)

	totalconfirmed = confirmed[confirmed.columns[-1]].sum()

	totalconfirmed = "{:,}".format(totalconfirmed)

	confirmeds = confirmed[['Country/Region',confirmed.columns[-1]]].groupby('Country/Region').sum()

	confirmeds = confirmeds.reset_index()

	confirmeds.columns = ['country','confirmed']

	confirmeds = confirmeds.sort_values(by='confirmed',ascending=False)

	# add separator for thousand

	confirmed_values = confirmeds['confirmed'].map('{:,.0f}'.format)

	confirmed_values = confirmed_values.values.tolist()

	confirmed_names = confirmeds['country'].str.replace(' ', '-').values.tolist()


	# more analysis for confirmed

	confirmed_col_diff = confirmed[[confirmed.columns[-2],confirmed.columns[-1]]]

	confirmed_col_diff.columns = ['confirmed1','confirmed']

	confirmed_col_diff = confirmed_col_diff.diff(axis=1)

	country = confirmed[['Country/Region']]

	country.columns = ['country']

	result_confirmed = pd.concat([country, confirmed_col_diff], axis=1)

	result_confirmed = result_confirmed[['country','confirmed']]

	total_increase = result_confirmed['confirmed'].sum()

	total_increase = "{:,}".format(total_increase)

	result_confirmed = result_confirmed.sort_values(by='confirmed',ascending=False)

	result_confirmed = result_confirmed.head(10)

	result_confirmed_values = result_confirmed['confirmed'].values.tolist()

	result_confirmed_names = result_confirmed['country'].str.replace(' ', '-').values.tolist()


	# death cases

	totaldeath = death[death.columns[-1]].sum()

	totaldeath = "{:,}".format(totaldeath)

	deaths = death[['Country/Region',death.columns[-1]]].groupby('Country/Region').sum()

	deaths = deaths.reset_index()

	deaths.columns = ['country','death']

	deaths = deaths.sort_values(by='death',ascending=False)

	# convert into integer

	deaths['death'] = deaths['death'].astype('int')

	# add separator for thousand

	death_values = deaths['death'].map('{:,.0f}'.format)

	death_values = death_values.values.tolist()

	death_names = deaths['country'].str.replace(' ', '-').values.tolist()


	# more analysis for death

	death_col_diff = death[[death.columns[-2],death.columns[-1]]]

	death_col_diff.columns = ['death1','death']

	death_col_diff = death_col_diff.diff(axis=1)

	country = death[['Country/Region']]

	country.columns = ['country']

	result_death = pd.concat([country, death_col_diff], axis=1)

	result_death = result_death[['country','death']]

	total_death_increase = result_death['death'].sum()

	total_death_increase = "{:,}".format(total_death_increase)

	result_death = result_death.sort_values(by='death',ascending=False)

	result_death = result_death.head(10)

	result_death_values = result_death['death'].values.tolist()

	result_death_names = result_death['country'].str.replace(' ', '-').values.tolist()

	# world statistics

	data = confirmed[[confirmed.columns[-10],
    confirmed.columns[-9],confirmed.columns[-8],confirmed.columns[-7],
    confirmed.columns[-6],confirmed.columns[-5],confirmed.columns[-4],
    confirmed.columns[-3],confirmed.columns[-2],confirmed.columns[-1]
    ]]

	data_col_dates = data.columns

	data_col_dates = data_col_dates.values.tolist()

	# today = data_col_dates.values.tolist()


	data_col1 = data[data.columns[0]].sum()

	data_col2 = data[data.columns[1]].sum()

	data_col3 = data[data.columns[2]].sum()

	data_col4 = data[data.columns[3]].sum()

	data_col5 = data[data.columns[4]].sum()

	data_col6 = data[data.columns[5]].sum()

	data_col7 = data[data.columns[6]].sum()

	data_col8 = data[data.columns[7]].sum()

	data_col9 = data[data.columns[8]].sum()

	data_col10 = data[data.columns[9]].sum()


	data_col = [
	    data_col1,data_col2,data_col3,data_col4,data_col5,
	    data_col6,data_col7,data_col8,data_col9,data_col10,
	    ]
	

	# variables

	context = {
	'totalconfirmed':totalconfirmed,'confirmed_values':confirmed_values,
	'confirmed_names':confirmed_names,'totaldeath':totaldeath,'death_values':death_values,
	'death_names':death_names,'result_confirmed_values':result_confirmed_values,
	'result_confirmed_names':result_confirmed_names,'total_increase':total_increase,
	'total_death_increase':total_death_increase,'result_death_values':result_death_values,
	'result_death_names':result_death_names,'data_col_dates':data_col_dates,
	'data_col':data_col
	}


	return render(request,'continent/world.html',context)


# world confirmed cases

def world_con(request):

	confirmed=r'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'

	world = gpd.read_file(r'https://raw.githubusercontent.com/oderofrancis/africa-corona/main/world.geojson')

	confirmed = pd.read_csv(confirmed)

	# geojson data

	data_con = confirmed[['Country/Region',confirmed.columns[-1]]]

	data_con.columns = ['country','confirmed']

	world = world[['NAME', 'geometry']]

	world.columns = ['country','geometry']

	geo_data_con = pd.merge(left=data_con, 
	                right=world, how='left', 
	                left_on='country', right_on='country'
	            )

	geo_data_con = gpd.GeoDataFrame(geo_data_con)

	geo_data_con = geo_data_con.to_json()

	return HttpResponse(geo_data_con,content_type='application/json')


# world death

def world_death(request):

	death = pd.read_csv(r'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv')

	world = gpd.read_file(r'https://raw.githubusercontent.com/oderofrancis/africa-corona/main/world.geojson')

	# geojson data

	data_death = death[['Country/Region',death.columns[-1]]]

	data_death.columns = ['country','death']

	world = world[['NAME', 'geometry']]

	world.columns = ['country','geometry']

	geo_data_death = pd.merge(left=data_death, 
	                right=world, how='left', 
	                left_on='country', right_on='country'
	            )

	geo_data_death = gpd.GeoDataFrame(geo_data_death)

	geo_data_con = geo_data_death.to_json()

	return HttpResponse(geo_data_death,content_type='application/json')




# africa data analysis

def africa(request):

	confirmed = pd.read_csv(r'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')

	death = pd.read_csv(r'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv')

	data_cont = pd.read_csv(r'https://raw.githubusercontent.com/oderofrancis/rona/main/Countries-Continents.csv')

	data_africa_m = confirmed.rename(columns = {'Country/Region':'country'})

	data_africa_m = data_africa_m.drop('Province/State',axis=1)

	data_africa_m = data_africa_m.drop('Lat',axis=1)

	data_africa_m = data_africa_m.drop('Long',axis=1)

	data_cont.columns = ['continent','country']

	data_africa_m = pd.merge(left=data_cont, 
		                right=data_africa_m, how='left', 
		                left_on='country', right_on='country'
		            )

	data_africa_m = data_africa_m[data_africa_m['continent'] == 'Africa']



	africa_con = data_africa_m[['country',data_africa_m.columns[-1]]].groupby('country').sum()

	africa_con = africa_con.reset_index()

	africa_con.columns = ['country','confirmed']

	totalafrica = africa_con['confirmed'].sum()

	totalafrica = "{:,}".format(int(totalafrica))

	africa_con = africa_con.sort_values(by='confirmed',ascending=False)

	# convert into integer

	africa_con['confirmed'] = africa_con['confirmed'].astype('int')

	# add separator for thousand

	africa_con_values = africa_con['confirmed'].map('{:,.0f}'.format)

	africa_con_values = africa_con_values.values.tolist()

	africa_con_names = africa_con['country'].str.replace(' ', '-').values.tolist()


	# more analysis for africa confirmed

	confirmed_col_diff = data_africa_m[[data_africa_m.columns[-2],data_africa_m.columns[-1]]]

	confirmed_col_diff.columns = ['confirmed1','confirmed']

	confirmed_col_diff = confirmed_col_diff.diff(axis=1)

	country = data_africa_m[['country']]

	country.columns = ['country']

	result_confirmed = pd.concat([country, confirmed_col_diff], axis=1)

	result_confirmed = result_confirmed[['country','confirmed']]

	total_increase = result_confirmed['confirmed'].sum()

	total_increase = int(total_increase)

	total_increase = "{:,}".format(total_increase)

	result_confirmed = result_confirmed.sort_values(by='confirmed',ascending=False)

	result_confirmed = result_confirmed.head(10)

	result_confirmed_values = result_confirmed['confirmed'].values.tolist()

	result_confirmed_names = result_confirmed['country'].str.replace(' ', '-').values.tolist()
	



	# death analysis


	data_africa_d = death.rename(columns = {'Country/Region':'country'})

	data_africa_d = data_africa_d.drop('Province/State',axis=1)

	data_africa_d = data_africa_d.drop('Lat',axis=1)

	data_africa_d = data_africa_d.drop('Long',axis=1)

	data_cont.columns = ['continent','country']

	data_africa_d = pd.merge(left=data_cont, 
		                right=data_africa_d, how='left', 
		                left_on='country', right_on='country'
		            )

	data_africa_d = data_africa_d[data_africa_d['continent'] == 'Africa']



	africa_death = data_africa_d[['country',data_africa_m.columns[-1]]].groupby('country').sum()

	africa_death = africa_death.reset_index()

	africa_death.columns = ['country','death']

	totalafrica_d = africa_death['death'].sum()

	totalafrica_d = int(totalafrica_d)

	totalafrica_d = "{:,}".format(totalafrica_d)

	africa_death = africa_death.sort_values(by='death',ascending=False)

	# convert into integer

	africa_death['death'] = africa_death['death'].astype('int')

	# add separator for thousand

	africa_death_values = africa_death['death'].map('{:,.0f}'.format)

	africa_death_values = africa_death_values.values.tolist()

	africa_death_names = africa_death['country'].str.replace(' ', '-').values.tolist()


	# more analysis for death


	death_col_diff = data_africa_d[[data_africa_d.columns[-2],data_africa_d.columns[-1]]]

	death_col_diff.columns = ['death1','death']

	death_col_diff = death_col_diff.diff(axis=1)

	country = data_africa_d[['country']]

	country.columns = ['country']

	result_death = pd.concat([country, death_col_diff], axis=1)

	result_death = result_death[['country','death']]

	total_increase_d = result_death['death'].sum()

	total_increase_d = int(total_increase_d)

	total_increase_d = "{:,}".format(total_increase_d)

	result_death = result_death.sort_values(by='death',ascending=False)

	result_death = result_death.head(10)

	result_death_values = result_death['death'].values.tolist()

	result_death_names = result_death['country'].str.replace(' ', '-').values.tolist()




	# africa stats

	data = data_africa_m[[data_africa_m.columns[-10],
	   data_africa_m.columns[-9],data_africa_m.columns[-8],data_africa_m.columns[-7],
	    data_africa_m.columns[-6],data_africa_m.columns[-5],data_africa_m.columns[-4],
	    data_africa_m.columns[-3],data_africa_m.columns[-2],data_africa_m.columns[-1]
	    ]]

	data_col_dates = data.columns

	data_col_dates = data_col_dates.values.tolist()



	data_col1 = data[data.columns[0]].sum()

	data_col2 = data[data.columns[1]].sum()

	data_col3 = data[data.columns[2]].sum()

	data_col4 = data[data.columns[3]].sum()

	data_col5 = data[data.columns[4]].sum()

	data_col6 = data[data.columns[5]].sum()

	data_col7 = data[data.columns[6]].sum()

	data_col8 = data[data.columns[7]].sum()

	data_col9 = data[data.columns[8]].sum()

	data_col10 = data[data.columns[9]].sum()


	data_col = [
		data_col1,data_col2,data_col3,data_col4,data_col5,
	    data_col6,data_col7,data_col8,data_col9,data_col10,
		]


	# show map

	showmap = 'True'


	context = {
		'totalafrica':totalafrica,'africa_con_values':africa_con_values,
		'africa_con_names':africa_con_names,'totalafrica_d':totalafrica_d,
		'africa_death_values':africa_death_values,'africa_death_names':africa_death_names,
		'data_col_dates':data_col_dates,'data_col':data_col,'result_confirmed_values':result_confirmed_values,
		'result_confirmed_names':result_confirmed_names,'total_increase':total_increase,'total_increase_d':total_increase_d,
		'result_death_values':result_death_values,'result_death_names':result_death_names,

		'showmap':showmap

	}

	return render(request,'continent/africa.html',context)

# africa confirmed

def africa_con(request):

	confirmed=pd.read_csv(r'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')

	data_cont = pd.read_csv(r'https://raw.githubusercontent.com/oderofrancis/rona/main/Countries-Continents.csv')

	world = gpd.read_file(r'https://raw.githubusercontent.com/oderofrancis/africa-corona/main/world.geojson')

	data_con = confirmed[['Country/Region',confirmed.columns[-1]]]

	data_con.columns = ['country','confirmed']

	data_cont.columns = ['continent','country']

	world = world[['NAME', 'geometry']]

	world.columns = ['country','geometry']


	data_africa = pd.merge(left=data_cont, 
	                right=data_con, how='left', 
	                left_on='country', right_on='country'
	            )

	data_africa = pd.merge(left=data_africa, 
	                right=world, how='left', 
	                left_on='country', right_on='country'
	            )

	data_africa = data_africa[data_africa['continent'] == 'Africa']

	geo_data_africa = gpd.GeoDataFrame(data_africa)

	geo_data_africa = geo_data_africa.to_json()

	return HttpResponse(geo_data_africa,content_type='application/json')



# africa death

def africa_death(request):

	death = pd.read_csv(r'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv')

	data_cont = pd.read_csv(r'https://raw.githubusercontent.com/oderofrancis/rona/main/Countries-Continents.csv')

	world = gpd.read_file(r'https://raw.githubusercontent.com/oderofrancis/africa-corona/main/world.geojson')

	data_death = death[['Country/Region',death.columns[-1]]]

	data_death.columns = ['country','death']

	data_cont.columns = ['continent','country']

	world = world[['NAME', 'geometry']]

	world.columns = ['country','geometry']


	data_africa_death = pd.merge(left=data_cont, 
	                right=data_death, how='left', 
	                left_on='country', right_on='country'
	            )

	data_africa_death = pd.merge(left=data_africa_death, 
	                right=world, how='left', 
	                left_on='country', right_on='country'
	            )

	data_africa_death = data_africa_death[data_africa_death['continent'] == 'Africa']

	geo_data_africa = gpd.GeoDataFrame(data_africa_death)

	geo_data_africa = geo_data_africa.to_json()


	return HttpResponse(geo_data_africa,content_type='application/json')







# asia data analysis

def asia(request):

	confirmed = pd.read_csv(r'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')

	death = pd.read_csv(r'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv')

	data_cont = pd.read_csv(r'https://raw.githubusercontent.com/oderofrancis/rona/main/Countries-Continents.csv')


	data_asia_m = confirmed.rename(columns = {'Country/Region':'country'})

	data_asia_m = data_asia_m.drop('Province/State',axis=1)

	data_asia_m = data_asia_m.drop('Lat',axis=1)

	data_asia_m = data_asia_m.drop('Long',axis=1)

	data_cont.columns = ['continent','country']

	data_asia_m = pd.merge(left=data_cont, 
		                right=data_asia_m, how='left', 
		                left_on='country', right_on='country'
		            )

	data_asia_m = data_asia_m[data_asia_m['continent'] == 'Asia']



	asia_con = data_asia_m[['country',data_asia_m.columns[-1]]].groupby('country').sum()

	asia_con = asia_con.reset_index()

	asia_con.columns = ['country','confirmed']

	totalasia = asia_con['confirmed'].sum()

	totalasia = int(totalasia)

	totalasia = "{:,}".format(totalasia)

	asia_con = asia_con.sort_values(by='confirmed',ascending=False)

	# convert into integer

	asia_con['confirmed'] = asia_con['confirmed'].astype('int')

	# add separator for thousand

	asia_con_values = asia_con['confirmed'].map('{:,.0f}'.format)

	asia_con_values = asia_con_values.values.tolist()

	asia_con_names = asia_con['country'].str.replace(' ', '-').values.tolist()


	# more analysis for asia confirmed

	confirmed_col_diff = data_asia_m[[data_asia_m.columns[-2],data_asia_m.columns[-1]]]

	confirmed_col_diff.columns = ['confirmed1','confirmed']

	confirmed_col_diff = confirmed_col_diff.diff(axis=1)

	country = data_asia_m[['country']]

	country.columns = ['country']

	result_confirmed = pd.concat([country, confirmed_col_diff], axis=1)

	result_confirmed = result_confirmed[['country','confirmed']]

	total_increase = result_confirmed['confirmed'].sum()

	total_increase = int(total_increase)

	total_increase = "{:,}".format(total_increase)

	result_confirmed = result_confirmed.sort_values(by='confirmed',ascending=False)

	result_confirmed = result_confirmed.head(10)

	result_confirmed_values = result_confirmed['confirmed'].values.tolist()

	result_confirmed_names = result_confirmed['country'].str.replace(' ', '-').values.tolist()
	



	# death analysis


	data_asia_d = death.rename(columns = {'Country/Region':'country'})

	data_asia_d = data_asia_d.drop('Province/State',axis=1)

	data_asia_d = data_asia_d.drop('Lat',axis=1)

	data_asia_d = data_asia_d.drop('Long',axis=1)

	data_cont.columns = ['continent','country']

	data_asia_d = pd.merge(left=data_cont, 
		                right=data_asia_d, how='left', 
		                left_on='country', right_on='country'
		            )

	data_asia_d = data_asia_d[data_asia_d['continent'] == 'Asia']



	asia_death = data_asia_d[['country',data_asia_m.columns[-1]]].groupby('country').sum()

	asia_death = asia_death.reset_index()

	asia_death.columns = ['country','death']

	totalasia_d = asia_death['death'].sum()

	totalasia_d = int(totalasia_d)

	totalasia_d = "{:,}".format(totalasia_d)

	asia_death = asia_death.sort_values(by='death',ascending=False)

	# convert into integer

	asia_death['death'] = asia_death['death'].astype('int')

	# convert into integer

	asia_death['death'] = asia_death['death'].astype('int')

	# add separator for thousand

	asia_death_values = asia_death['death'].map('{:,.0f}'.format)

	asia_death_values = asia_death_values.values.tolist()

	asia_death_names = asia_death['country'].str.replace(' ', '-').values.tolist()


	# more analysis for death


	death_col_diff = data_asia_d[[data_asia_d.columns[-2],data_asia_d.columns[-1]]]

	death_col_diff.columns = ['death1','death']

	death_col_diff = death_col_diff.diff(axis=1)

	country = data_asia_d[['country']]

	country.columns = ['country']

	result_death = pd.concat([country, death_col_diff], axis=1)

	result_death = result_death[['country','death']]

	total_increase_d = result_death['death'].sum()

	total_increase_d = int(total_increase_d)

	total_increase_d = "{:,}".format(total_increase_d)

	result_death = result_death.sort_values(by='death',ascending=False)

	result_death = result_death.head(10)

	result_death_values = result_death['death'].values.tolist()

	result_death_names = result_death['country'].str.replace(' ', '-').values.tolist()



	# asia stats

	data = data_asia_m[[data_asia_m.columns[-10],
	   data_asia_m.columns[-9],data_asia_m.columns[-8],data_asia_m.columns[-7],
	    data_asia_m.columns[-6],data_asia_m.columns[-5],data_asia_m.columns[-4],
	    data_asia_m.columns[-3],data_asia_m.columns[-2],data_asia_m.columns[-1]
	    ]]

	data_col_dates = data.columns

	data_col_dates = data_col_dates.values.tolist()



	data_col1 = data[data.columns[0]].sum()

	data_col2 = data[data.columns[1]].sum()

	data_col3 = data[data.columns[2]].sum()

	data_col4 = data[data.columns[3]].sum()

	data_col5 = data[data.columns[4]].sum()

	data_col6 = data[data.columns[5]].sum()

	data_col7 = data[data.columns[6]].sum()

	data_col8 = data[data.columns[7]].sum()

	data_col9 = data[data.columns[8]].sum()

	data_col10 = data[data.columns[9]].sum()


	data_col = [
		data_col1,data_col2,data_col3,data_col4,data_col5,
	    data_col6,data_col7,data_col8,data_col9,data_col10,
		]

	# showmap

	showmap = 'True'



	context = {
		'totalasia':totalasia,'asia_con_values':asia_con_values,
		'asia_con_names':asia_con_names,'totalasia_d':totalasia_d,
		'asia_death_values':asia_death_values,'asia_death_names':asia_death_names,
		'data_col_dates':data_col_dates,'data_col':data_col,
		'result_confirmed_values':result_confirmed_values,
		'result_confirmed_names':result_confirmed_names,
		'total_increase':total_increase,'total_increase_d':total_increase_d,
		'result_death_values':result_death_values,'result_death_names':result_death_names,

		'showmap':showmap

	}

	return render(request,'continent/asia.html',context)



# asia confirmed

def asia_con(request):

	confirmed=pd.read_csv(r'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')

	data_cont = pd.read_csv(r'https://raw.githubusercontent.com/oderofrancis/rona/main/Countries-Continents.csv')

	world = gpd.read_file(r'https://raw.githubusercontent.com/oderofrancis/africa-corona/main/world.geojson')

	data_con = confirmed[['Country/Region',confirmed.columns[-1]]]

	data_con.columns = ['country','confirmed']

	data_cont.columns = ['continent','country']

	world = world[['NAME', 'geometry']]

	world.columns = ['country','geometry']


	data_asia = pd.merge(left=data_cont, 
	                right=data_con, how='left', 
	                left_on='country', right_on='country'
	            )

	data_asia = pd.merge(left=data_asia, 
	                right=world, how='left', 
	                left_on='country', right_on='country'
	            )

	data_asia = data_asia[data_asia['continent'] == 'Asia']

	geo_data_asia = gpd.GeoDataFrame(data_asia)

	geo_data_asia = geo_data_asia.to_json()

	return HttpResponse(geo_data_asia,content_type='application/json')



# asia death

def asia_death(request):

	death = pd.read_csv(r'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv')

	data_cont = pd.read_csv(r'https://raw.githubusercontent.com/oderofrancis/rona/main/Countries-Continents.csv')

	world = gpd.read_file(r'https://raw.githubusercontent.com/oderofrancis/africa-corona/main/world.geojson')

	data_death = death[['Country/Region',death.columns[-1]]]

	data_death.columns = ['country','death']

	data_cont.columns = ['continent','country']

	world = world[['NAME', 'geometry']]

	world.columns = ['country','geometry']


	data_asia_death = pd.merge(left=data_cont, 
	                right=data_death, how='left', 
	                left_on='country', right_on='country'
	            )

	data_asia_death = pd.merge(left=data_asia_death, 
	                right=world, how='left', 
	                left_on='country', right_on='country'
	            )

	data_asia_death = data_asia_death[data_asia_death['continent'] == 'Asia']

	geo_data_asia = gpd.GeoDataFrame(data_asia_death)

	geo_data_asia = geo_data_asia.to_json()


	return HttpResponse(geo_data_asia,content_type='application/json')







# america data analysis

def america(request):

	confirmed = pd.read_csv(r'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')

	death = pd.read_csv(r'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv')

	data_cont = pd.read_csv(r'https://raw.githubusercontent.com/oderofrancis/rona/main/Countries-Continents.csv')


	data_america_m = confirmed.rename(columns = {'Country/Region':'country'})

	data_america_m = data_america_m.drop('Province/State',axis=1)

	data_america_m = data_america_m.drop('Lat',axis=1)

	data_america_m = data_america_m.drop('Long',axis=1)

	data_cont.columns = ['continent','country']

	data_america_m = pd.merge(left=data_cont, 
		                right=data_america_m, how='left', 
		                left_on='country', right_on='country'
		            )

	data_america_m = data_america_m[data_america_m['continent'] == 'North America']



	america_con = data_america_m[['country',data_america_m.columns[-1]]].groupby('country').sum()

	america_con = america_con.reset_index()

	america_con.columns = ['country','confirmed']

	totalamerica = america_con['confirmed'].sum()

	totalamerica = "{:,}".format(int(totalamerica))

	america_con = america_con.sort_values(by='confirmed',ascending=False)

	# convert into integer

	america_con['confirmed'] = america_con['confirmed'].astype('int')

	# add separator for thousand

	america_con_values = america_con['confirmed'].map('{:,.0f}'.format)

	america_con_values = america_con_values.values.tolist()

	america_con_names = america_con['country'].str.replace(' ', '-').values.tolist()


	# more analysis for aamericaa confirmed

	confirmed_col_diff = data_america_m[[data_america_m.columns[-2],data_america_m.columns[-1]]]

	confirmed_col_diff.columns = ['confirmed1','confirmed']

	confirmed_col_diff = confirmed_col_diff.diff(axis=1)

	country = data_america_m[['country']]

	country.columns = ['country']

	result_confirmed = pd.concat([country, confirmed_col_diff], axis=1)

	result_confirmed = result_confirmed[['country','confirmed']]

	total_increase = result_confirmed['confirmed'].sum()

	total_increase = "{:,}".format(int(total_increase))

	result_confirmed = result_confirmed.sort_values(by='confirmed',ascending=False)

	result_confirmed = result_confirmed.head(10)

	result_confirmed_values = result_confirmed['confirmed'].values.tolist()

	result_confirmed_names = result_confirmed['country'].str.replace(' ', '-').values.tolist()
	



	# death analysis


	data_america_d = death.rename(columns = {'Country/Region':'country'})

	data_america_d = data_america_d.drop('Province/State',axis=1)

	data_america_d = data_america_d.drop('Lat',axis=1)

	data_america_d = data_america_d.drop('Long',axis=1)

	data_cont.columns = ['continent','country']

	data_america_d = pd.merge(left=data_cont, 
		                right=data_america_d, how='left', 
		                left_on='country', right_on='country'
		            )

	data_america_d = data_america_d[data_america_d['continent'] == 'North America']



	america_death = data_america_d[['country',data_america_m.columns[-1]]].groupby('country').sum()

	america_death = america_death.reset_index()

	america_death.columns = ['country','death']

	totalamerica_d = america_death['death'].sum()

	totalamerica_d = "{:,}".format(int(totalamerica_d))

	america_death = america_death.sort_values(by='death',ascending=False)

	# convert into integer

	america_death['death'] = america_death['death'].astype('int')

	# add separator for thousand

	america_death_values = america_death['death'].map('{:,.0f}'.format)

	america_death_values = america_death_values.values.tolist()

	america_death_names = america_death['country'].str.replace(' ', '-').values.tolist()


	# more analysis for death


	death_col_diff = data_america_d[[data_america_d.columns[-2],data_america_d.columns[-1]]]

	death_col_diff.columns = ['death1','death']

	death_col_diff = death_col_diff.diff(axis=1)

	country = data_america_d[['country']]

	country.columns = ['country']

	result_death = pd.concat([country, death_col_diff], axis=1)

	result_death = result_death[['country','death']]

	total_increase_d = result_death['death'].sum()

	total_increase_d = "{:,}".format(int(total_increase_d))

	result_death = result_death.sort_values(by='death',ascending=False)

	result_death = result_death.head(10)

	result_death_values = result_death['death'].values.tolist()

	result_death_names = result_death['country'].str.replace(' ', '-').values.tolist()




	# america stats

	data = data_america_m[[data_america_m.columns[-10],
	   data_america_m.columns[-9],data_america_m.columns[-8],data_america_m.columns[-7],
	    data_america_m.columns[-6],data_america_m.columns[-5],data_america_m.columns[-4],
	    data_america_m.columns[-3],data_america_m.columns[-2],data_america_m.columns[-1]
	    ]]

	data_col_dates = data.columns

	data_col_dates = data_col_dates.values.tolist()



	data_col1 = data[data.columns[0]].sum()

	data_col2 = data[data.columns[1]].sum()

	data_col3 = data[data.columns[2]].sum()

	data_col4 = data[data.columns[3]].sum()

	data_col5 = data[data.columns[4]].sum()

	data_col6 = data[data.columns[5]].sum()

	data_col7 = data[data.columns[6]].sum()

	data_col8 = data[data.columns[7]].sum()

	data_col9 = data[data.columns[8]].sum()

	data_col10 = data[data.columns[9]].sum()


	data_col = [
		data_col1,data_col2,data_col3,data_col4,data_col5,
	    data_col6,data_col7,data_col8,data_col9,data_col10,
		]

	# show our map

	showmap = 'True'


	context = {
		'totalamerica':totalamerica,'america_con_values':america_con_values,
		'america_con_names':america_con_names,'totalamerica_d':totalamerica_d,
		'america_death_values':america_death_values,'america_death_names':america_death_names,
		'data_col_dates':data_col_dates,'data_col':data_col,
		'result_confirmed_values':result_confirmed_values,
		'result_confirmed_names':result_confirmed_names,
		'total_increase':total_increase,'total_increase_d':total_increase_d,
		'result_death_values':result_death_values,'result_death_names':result_death_names,

		'showmap':showmap

	}

	return render(request,'continent/america.html',context)

# america confirmed

def america_con(request):

	confirmed=pd.read_csv(r'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')

	data_cont = pd.read_csv(r'https://raw.githubusercontent.com/oderofrancis/rona/main/Countries-Continents.csv')

	world = gpd.read_file(r'https://raw.githubusercontent.com/oderofrancis/africa-corona/main/world.geojson')

	data_con = confirmed[['Country/Region',confirmed.columns[-1]]]

	data_con.columns = ['country','confirmed']

	data_cont.columns = ['continent','country']

	world = world[['NAME', 'geometry']]

	world.columns = ['country','geometry']


	data_america = pd.merge(left=data_cont, 
	                right=data_con, how='left', 
	                left_on='country', right_on='country'
	            )

	data_america = pd.merge(left=data_america, 
	                right=world, how='left', 
	                left_on='country', right_on='country'
	            )

	data_america = data_america[data_america['continent'] == 'North America']

	geo_data_america = gpd.GeoDataFrame(data_america)

	geo_data_america = geo_data_america.to_json()

	return HttpResponse(geo_data_america,content_type='application/json')



# america death

def america_death(request):

	death = pd.read_csv(r'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv')

	data_cont = pd.read_csv(r'https://raw.githubusercontent.com/oderofrancis/rona/main/Countries-Continents.csv')

	world = gpd.read_file(r'https://raw.githubusercontent.com/oderofrancis/africa-corona/main/world.geojson')

	data_death = death[['Country/Region',death.columns[-1]]]

	data_death.columns = ['country','death']

	data_cont.columns = ['continent','country']

	world = world[['NAME', 'geometry']]

	world.columns = ['country','geometry']


	data_america_death = pd.merge(left=data_cont, 
	                right=data_death, how='left', 
	                left_on='country', right_on='country'
	            )

	data_america_death = pd.merge(left=data_america_death, 
	                right=world, how='left', 
	                left_on='country', right_on='country'
	            )

	data_america_death = data_america_death[data_america_death['continent'] == 'North America']

	geo_data_america = gpd.GeoDataFrame(data_america_death)

	geo_data_america = geo_data_america.to_json()


	return HttpResponse(geo_data_america,content_type='application/json')





# latin america



def latin(request):

	confirmed = pd.read_csv(r'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')

	death = pd.read_csv(r'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv')

	data_cont = pd.read_csv(r'https://raw.githubusercontent.com/oderofrancis/rona/main/Countries-Continents.csv')


	latin = confirmed.rename(columns = {'Country/Region':'country'})

	latin = latin.drop('Province/State',axis=1)

	latin = latin.drop('Lat',axis=1)

	latin = latin.drop('Long',axis=1)

	data_cont.columns = ['continent','country']

	latin = pd.merge(left=data_cont, 
		                right=latin, how='left', 
		                left_on='country', right_on='country'
		            )

	latin = latin[latin['continent'] == 'South America']



	latin_con = latin[['country',latin.columns[-1]]].groupby('country').sum()

	latin_con = latin_con.reset_index()

	latin_con.columns = ['country','confirmed']

	totallatin = latin_con['confirmed'].sum()

	totallatin = "{:,}".format(int(totallatin))

	latin_con = latin_con.sort_values(by='confirmed',ascending=False)

	# convert into integer

	latin_con['confirmed'] = latin_con['confirmed'].astype('int')

	# add separator for thousand

	latin_con_values = latin_con['confirmed'].map('{:,.0f}'.format)

	latin_con_values = latin_con_values.values.tolist()

	latin_con_names = latin_con['country'].str.replace(' ', '-').values.tolist()


	# more analysis for latin confirmed

	confirmed_col_diff = latin[[latin.columns[-2],latin.columns[-1]]]

	confirmed_col_diff.columns = ['confirmed1','confirmed']

	confirmed_col_diff = confirmed_col_diff.diff(axis=1)

	country = latin[['country']]

	country.columns = ['country']

	result_confirmed = pd.concat([country, confirmed_col_diff], axis=1)

	result_confirmed = result_confirmed[['country','confirmed']]

	total_increase = result_confirmed['confirmed'].sum()

	total_increase = "{:,}".format(int(total_increase))

	result_confirmed = result_confirmed.sort_values(by='confirmed',ascending=False)

	result_confirmed = result_confirmed.head(10)

	result_confirmed_values = result_confirmed['confirmed'].values.tolist()

	result_confirmed_names = result_confirmed['country'].str.replace(' ', '-').values.tolist()
	



	# death analysis


	latin_d = death.rename(columns = {'Country/Region':'country'})

	latin_d = latin_d.drop('Province/State',axis=1)

	latin_d = latin_d.drop('Lat',axis=1)

	latin_d = latin_d.drop('Long',axis=1)

	data_cont.columns = ['continent','country']

	latin_d = pd.merge(left=data_cont, 
		                right=latin_d, how='left', 
		                left_on='country', right_on='country'
		            )

	latin_d = latin_d[latin_d['continent'] == 'South America']



	latin_death = latin_d[['country',latin_d.columns[-1]]].groupby('country').sum()

	latin_death = latin_death.reset_index()

	latin_death.columns = ['country','death']

	totallatin_d = latin_death['death'].sum()

	totallatin_d = "{:,}".format(int(totallatin_d))

	latin_death = latin_death.sort_values(by='death',ascending=False)

	# convert into integer

	latin_death['death'] = latin_death['death'].astype('int')

	# add separator for thousand

	latin_death_values = latin_death['death'].map('{:,.0f}'.format)

	latin_death_values = latin_death_values.values.tolist()

	latin_death_names = latin_death['country'].str.replace(' ', '-').values.tolist()


	# more analysis for death


	death_col_diff = latin_d[[latin_d.columns[-2],latin_d.columns[-1]]]

	death_col_diff.columns = ['death1','death']

	death_col_diff = death_col_diff.diff(axis=1)

	country = latin_d[['country']]

	country.columns = ['country']

	result_death = pd.concat([country, death_col_diff], axis=1)

	result_death = result_death[['country','death']]

	total_increase_d = result_death['death'].sum()

	total_increase_d = "{:,}".format(int(total_increase_d))

	result_death = result_death.sort_values(by='death',ascending=False)

	result_death = result_death.head(10)

	result_death_values = result_death['death'].values.tolist()

	result_death_names = result_death['country'].str.replace(' ', '-').values.tolist()




	# africa stats

	data = latin[[latin.columns[-10],
	   latin.columns[-9],latin.columns[-8],latin.columns[-7],
	    latin.columns[-6],latin.columns[-5],latin.columns[-4],
	    latin.columns[-3],latin.columns[-2],latin.columns[-1]
	    ]]

	data_col_dates = data.columns

	data_col_dates = data_col_dates.values.tolist()



	data_col1 = data[data.columns[0]].sum()

	data_col2 = data[data.columns[1]].sum()

	data_col3 = data[data.columns[2]].sum()

	data_col4 = data[data.columns[3]].sum()

	data_col5 = data[data.columns[4]].sum()

	data_col6 = data[data.columns[5]].sum()

	data_col7 = data[data.columns[6]].sum()

	data_col8 = data[data.columns[7]].sum()

	data_col9 = data[data.columns[8]].sum()

	data_col10 = data[data.columns[9]].sum()


	data_col = [
		data_col1,data_col2,data_col3,data_col4,data_col5,
	    data_col6,data_col7,data_col8,data_col9,data_col10,
		]


	showmap = 'True'


	context = {
		'totallatin':totallatin,'latin_con_values':latin_con_values,
		'latin_con_names':latin_con_names,'totallatin_d':totallatin_d,
		'latin_death_values':latin_death_values,'latin_death_names':latin_death_names,
		'data_col_dates':data_col_dates,'data_col':data_col,
		'result_confirmed_values':result_confirmed_values,
		'result_confirmed_names':result_confirmed_names,
		'total_increase':total_increase,'total_increase_d':total_increase_d,
		'result_death_values':result_death_values,'result_death_names':result_death_names,

		'showmap':showmap

	}

	return render(request,'continent/latin.html',context)

# Latin america confirmed

def latin_con(request):

	confirmed=pd.read_csv(r'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')

	data_cont = pd.read_csv(r'https://raw.githubusercontent.com/oderofrancis/rona/main/Countries-Continents.csv')

	world = gpd.read_file(r'https://raw.githubusercontent.com/oderofrancis/africa-corona/main/world.geojson')

	data_con = confirmed[['Country/Region',confirmed.columns[-1]]]

	data_con.columns = ['country','confirmed']

	data_cont.columns = ['continent','country']

	world = world[['NAME', 'geometry']]

	world.columns = ['country','geometry']


	data_latin = pd.merge(left=data_cont, 
	                right=data_con, how='left', 
	                left_on='country', right_on='country'
	            )

	data_latin = pd.merge(left=data_latin, 
	                right=world, how='left', 
	                left_on='country', right_on='country'
	            )

	data_latin = data_latin[data_latin['continent'] == 'South America']

	geo_data_latin = gpd.GeoDataFrame(data_latin)

	geo_data_latin = geo_data_latin.to_json()

	return HttpResponse(geo_data_latin,content_type='application/json')



# Latin latin death

def latin_death(request):

	death = pd.read_csv(r'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv')

	data_cont = pd.read_csv(r'https://raw.githubusercontent.com/oderofrancis/rona/main/Countries-Continents.csv')

	world = gpd.read_file(r'https://raw.githubusercontent.com/oderofrancis/africa-corona/main/world.geojson')

	data_death = death[['Country/Region',death.columns[-1]]]

	data_death.columns = ['country','death']

	data_cont.columns = ['continent','country']

	world = world[['NAME', 'geometry']]

	world.columns = ['country','geometry']


	data_latin_death = pd.merge(left=data_cont, 
	                right=data_death, how='left', 
	                left_on='country', right_on='country'
	            )

	data_latin_death = pd.merge(left=data_latin_death, 
	                right=world, how='left', 
	                left_on='country', right_on='country'
	            )

	data_latin_death = data_latin_death[data_latin_death['continent'] == 'South America']

	geo_data_latin = gpd.GeoDataFrame(data_latin_death)

	geo_data_latin = geo_data_latin.to_json()


	return HttpResponse(geo_data_latin,content_type='application/json')





# europe data analysis


def europe(request):

	confirmed = pd.read_csv(r'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')

	death = pd.read_csv(r'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv')

	data_cont = pd.read_csv(r'https://raw.githubusercontent.com/oderofrancis/rona/main/Countries-Continents.csv')


	europe = confirmed.rename(columns = {'Country/Region':'country'})

	europe =europe.drop('Province/State',axis=1)

	europe =europe.drop('Lat',axis=1)

	europe =europe.drop('Long',axis=1)

	data_cont.columns = ['continent','country']

	europe = pd.merge(left=data_cont, 
			                right=europe, how='left', 
			                left_on='country', right_on='country'
			            )

	europe = europe[europe['continent'] == 'Europe']



	europe_con = europe[['country',europe.columns[-1]]].groupby('country').sum()

	europe_con =europe_con.reset_index()

	europe_con.columns = ['country','confirmed']

	totaleurope =europe_con['confirmed'].sum()

	totaleurope = "{:,}".format(int(totaleurope))

	europe_con =europe_con.sort_values(by='confirmed',ascending=False)

	# convert into integer

	europe_con['confirmed'] = europe_con['confirmed'].astype('int')

	# add separator for thousand

	europe_con_values = europe_con['confirmed'].map('{:,.0f}'.format)

	europe_con_values = europe_con_values.values.tolist()

	europe_con_names =europe_con['country'].str.replace(' ', '-').values.tolist()


	# more analysis for europe confirmed

	confirmed_col_diff = europe[[europe.columns[-2],europe.columns[-1]]]

	confirmed_col_diff.columns = ['confirmed1','confirmed']

	confirmed_col_diff = confirmed_col_diff.diff(axis=1)

	country =europe[['country']]

	country.columns = ['country']

	result_confirmed = pd.concat([country, confirmed_col_diff], axis=1)

	result_confirmed = result_confirmed[['country','confirmed']]

	total_increase = result_confirmed['confirmed'].sum()

	total_increase = "{:,}".format(int(total_increase))

	result_confirmed = result_confirmed.sort_values(by='confirmed',ascending=False)

	result_confirmed = result_confirmed.head(10)

	result_confirmed_values = result_confirmed['confirmed'].values.tolist()

	result_confirmed_names = result_confirmed['country'].str.replace(' ', '-').values.tolist()



	# death analysis


	europe_d = death.rename(columns = {'Country/Region':'country'})

	europe_d =europe_d.drop('Province/State',axis=1)

	europe_d =europe_d.drop('Lat',axis=1)

	europe_d = europe_d.drop('Long',axis=1)

	data_cont.columns = ['continent','country']

	europe_d = pd.merge(left=data_cont, 
		                right=europe_d, how='left', 
		                left_on='country', right_on='country'
		            )

	europe_d = europe_d[europe_d['continent'] == 'Europe']



	europe_death = europe_d[['country',europe_d.columns[-1]]].groupby('country').sum()

	europe_death = europe_death.reset_index()

	europe_death.columns = ['country','death']

	totaleurope_d = europe_death['death'].sum()

	totaleurope_d = "{:,}".format(int(totaleurope_d))

	europe_death = europe_death.sort_values(by='death',ascending=False)

	# convert into integer

	europe_death['death'] = europe_death['death'].astype('int')

	# add separator for thousand

	europe_death_values = europe_death['death'].map('{:,.0f}'.format)

	europe_death_values = europe_death_values.values.tolist()

	europe_death_names = europe_death['country'].str.replace(' ', '-').values.tolist()


	# more analysis for death


	death_col_diff = europe_d[[europe_d.columns[-2],europe_d.columns[-1]]]

	death_col_diff.columns = ['death1','death']

	death_col_diff = death_col_diff.diff(axis=1)

	country = europe[['country']]

	country.columns = ['country']

	result_death = pd.concat([country, death_col_diff], axis=1)

	result_death = result_death[['country','death']]

	total_increase_d = result_death['death'].sum()

	total_increase_d = "{:,}".format(int(total_increase_d))

	result_death = result_death.sort_values(by='death',ascending=False)

	result_death = result_death.head(10)

	result_death_values = result_death['death'].values.tolist()

	result_death_names = result_death['country'].str.replace(' ', '-').values.tolist()




	# africa stats

	data = europe[[europe.columns[-10],
	   europe.columns[-9],europe.columns[-8],europe.columns[-7],
	    europe.columns[-6],europe.columns[-5],europe.columns[-4],
	    europe.columns[-3],europe.columns[-2],europe.columns[-1]
	    ]]

	data_col_dates = data.columns

	data_col_dates = data_col_dates.values.tolist()



	data_col1 = data[data.columns[0]].sum()

	data_col2 = data[data.columns[1]].sum()

	data_col3 = data[data.columns[2]].sum()

	data_col4 = data[data.columns[3]].sum()

	data_col5 = data[data.columns[4]].sum()

	data_col6 = data[data.columns[5]].sum()

	data_col7 = data[data.columns[6]].sum()

	data_col8 = data[data.columns[7]].sum()

	data_col9 = data[data.columns[8]].sum()

	data_col10 = data[data.columns[9]].sum()


	data_col = [
		data_col1,data_col2,data_col3,data_col4,data_col5,
	    data_col6,data_col7,data_col8,data_col9,data_col10,
		]


	# show map

	showmap = 'True'


	context = {
		'totaleurope':totaleurope,'europe_con_values':europe_con_values,
		'europe_con_names':europe_con_names,'totaleurope_d':totaleurope_d,
		'europe_death_values':europe_death_values,'europe_death_names':europe_death_names,
		'data_col_dates':data_col_dates,'data_col':data_col,
		'result_confirmed_values':result_confirmed_values,
		'result_confirmed_names':result_confirmed_names,
		'total_increase':total_increase,'total_increase_d':total_increase_d,
		'result_death_values':result_death_values,'result_death_names':result_death_names,

		'showmap':showmap

	}

	return render(request,'continent/europe.html',context)

# europe confirmed

def europe_con(request):

	confirmed=pd.read_csv(r'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')

	data_cont = pd.read_csv(r'https://raw.githubusercontent.com/oderofrancis/rona/main/Countries-Continents.csv')

	world = gpd.read_file(r'https://raw.githubusercontent.com/oderofrancis/africa-corona/main/world.geojson')

	data_con = confirmed[['Country/Region',confirmed.columns[-1]]]

	data_con.columns = ['country','confirmed']

	data_cont.columns = ['continent','country']

	world = world[['NAME', 'geometry']]

	world.columns = ['country','geometry']


	data_europe = pd.merge(left=data_cont, 
	                right=data_con, how='left', 
	                left_on='country', right_on='country'
	            )

	data_europe = pd.merge(left=data_europe, 
	                right=world, how='left', 
	                left_on='country', right_on='country'
	            )

	data_europe = data_europe[data_europe['continent'] == 'Europe']

	geo_data_europe = gpd.GeoDataFrame(data_europe)

	geo_data_europe = geo_data_europe.to_json()

	return HttpResponse(geo_data_europe,content_type='application/json')



#  europe death

def europe_death(request):

	death = pd.read_csv(r'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv')

	data_cont = pd.read_csv(r'https://raw.githubusercontent.com/oderofrancis/rona/main/Countries-Continents.csv')

	world = gpd.read_file(r'https://raw.githubusercontent.com/oderofrancis/africa-corona/main/world.geojson')

	data_death = death[['Country/Region',death.columns[-1]]]

	data_death.columns = ['country','death']

	data_cont.columns = ['continent','country']

	world = world[['NAME', 'geometry']]

	world.columns = ['country','geometry']


	data_europe_death = pd.merge(left=data_cont, 
	                right=data_death, how='left', 
	                left_on='country', right_on='country'
	            )

	data_europe_death = pd.merge(left=data_europe_death, 
	                right=world, how='left', 
	                left_on='country', right_on='country'
	            )

	data_europe_death = data_europe_death[data_europe_death['continent'] == 'Europe']

	geo_data_europe = gpd.GeoDataFrame(data_europe_death)

	geo_data_europe = geo_data_europe.to_json()


	return HttpResponse(geo_data_europe,content_type='application/json')




# oceania data analysis

def oceania(request):

	confirmed = pd.read_csv(r'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')

	death = pd.read_csv(r'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv')

	data_cont = pd.read_csv(r'https://raw.githubusercontent.com/oderofrancis/rona/main/Countries-Continents.csv')

	data_oceania_m = confirmed.rename(columns = {'Country/Region':'country'})

	data_oceania_m = data_oceania_m.drop('Province/State',axis=1)

	data_oceania_m = data_oceania_m.drop('Lat',axis=1)

	data_oceania_m = data_oceania_m.drop('Long',axis=1)

	data_cont.columns = ['continent','country']

	data_oceania_m = pd.merge(left=data_cont, 
		                right=data_oceania_m, how='left', 
		                left_on='country', right_on='country'
		            )

	data_oceania_m = data_oceania_m[data_oceania_m['continent'] == 'Oceania']



	oceania_con = data_oceania_m[['country',data_oceania_m.columns[-1]]].groupby('country').sum()

	oceania_con = oceania_con.reset_index()

	oceania_con.columns = ['country','confirmed']

	totaloceania = oceania_con['confirmed'].sum()

	totaloceania = "{:,}".format(int(totaloceania))

	oceania_con = oceania_con.sort_values(by='confirmed',ascending=False)

	# convert into integer

	oceania_con['confirmed'] = oceania_con['confirmed'].astype('int')

	# add separator for thousand

	oceania_con_values = oceania_con['confirmed'].map('{:,.0f}'.format)

	oceania_con_values = oceania_con_values.values.tolist()

	oceania_con_names = oceania_con['country'].str.replace(' ', '-').values.tolist()


	# more analysis for  confirmed

	confirmed_col_diff = data_oceania_m[[data_oceania_m.columns[-2],data_oceania_m.columns[-1]]]

	confirmed_col_diff.columns = ['confirmed1','confirmed']

	confirmed_col_diff = confirmed_col_diff.diff(axis=1)

	country = data_oceania_m[['country']]

	country.columns = ['country']

	result_confirmed = pd.concat([country, confirmed_col_diff], axis=1)

	result_confirmed = result_confirmed[['country','confirmed']]

	total_increase = result_confirmed['confirmed'].sum()

	total_increase = "{:,}".format(int(total_increase))

	result_confirmed = result_confirmed.sort_values(by='confirmed',ascending=False)

	result_confirmed = result_confirmed.head(10)

	result_confirmed_values = result_confirmed['confirmed'].values.tolist()

	result_confirmed_names = result_confirmed['country'].str.replace(' ', '-').values.tolist()
	



	# death analysis


	data_oceania_d = death.rename(columns = {'Country/Region':'country'})

	data_oceania_d = data_oceania_d.drop('Province/State',axis=1)

	data_oceania_d = data_oceania_d.drop('Lat',axis=1)

	data_oceania_d = data_oceania_d.drop('Long',axis=1)

	data_cont.columns = ['continent','country']

	data_oceania_d = pd.merge(left=data_cont, 
		                right=data_oceania_d, how='left', 
		                left_on='country', right_on='country'
		            )

	data_oceania_d = data_oceania_d[data_oceania_d['continent'] == 'Oceania']



	oceania_death = data_oceania_d[['country',data_oceania_m.columns[-1]]].groupby('country').sum()

	oceania_death = oceania_death.reset_index()

	oceania_death.columns = ['country','death']

	totaloceania_d = oceania_death['death'].sum()

	totaloceania_d = "{:,}".format(int(totaloceania_d))

	oceania_death = oceania_death.sort_values(by='death',ascending=False)

	# convert into integer

	oceania_death['death'] = oceania_death['death'].astype('int')

	# add separator for thousand

	oceania_death_values = oceania_death['death'].map('{:,.0f}'.format)

	oceania_death_values = oceania_death_values.values.tolist()

	oceania_death_names = oceania_death['country'].str.replace(' ', '-').values.tolist()


	# more analysis for death


	death_col_diff = data_oceania_d[[data_oceania_d.columns[-2],data_oceania_d.columns[-1]]]

	death_col_diff.columns = ['death1','death']

	death_col_diff = death_col_diff.diff(axis=1)

	country = data_oceania_d[['country']]

	country.columns = ['country']

	result_death = pd.concat([country, death_col_diff], axis=1)

	result_death = result_death[['country','death']]

	total_increase_d = result_death['death'].sum()

	total_increase_d = "{:,}".format(int(total_increase_d))

	result_death = result_death.sort_values(by='death',ascending=False)

	result_death = result_death.head(10)

	result_death_values = result_death['death'].values.tolist()

	result_death_names = result_death['country'].str.replace(' ', '-').values.tolist()




	# oceania stats

	data = data_oceania_m[[data_oceania_m.columns[-10],
	   data_oceania_m.columns[-9],data_oceania_m.columns[-8],data_oceania_m.columns[-7],
	    data_oceania_m.columns[-6],data_oceania_m.columns[-5],data_oceania_m.columns[-4],
	    data_oceania_m.columns[-3],data_oceania_m.columns[-2],data_oceania_m.columns[-1]
	    ]]

	data_col_dates = data.columns

	data_col_dates = data_col_dates.values.tolist()



	data_col1 = data[data.columns[0]].sum()

	data_col2 = data[data.columns[1]].sum()

	data_col3 = data[data.columns[2]].sum()

	data_col4 = data[data.columns[3]].sum()

	data_col5 = data[data.columns[4]].sum()

	data_col6 = data[data.columns[5]].sum()

	data_col7 = data[data.columns[6]].sum()

	data_col8 = data[data.columns[7]].sum()

	data_col9 = data[data.columns[8]].sum()

	data_col10 = data[data.columns[9]].sum()


	data_col = [
		data_col1,data_col2,data_col3,data_col4,data_col5,
	    data_col6,data_col7,data_col8,data_col9,data_col10,
		]


	# showmap

	showmap = 'True'


	context = {
		'totaloceania':totaloceania,'oceania_con_values':oceania_con_values,
		'oceania_con_names':oceania_con_names,'totaloceania_d':totaloceania_d,
		'oceania_death_values':oceania_death_values,'oceania_death_names':oceania_death_names,
		'data_col_dates':data_col_dates,'data_col':data_col,'result_confirmed_values':result_confirmed_values,
		'result_confirmed_names':result_confirmed_names,'total_increase':total_increase,'total_increase_d':total_increase_d,
		'result_death_values':result_death_values,'result_death_names':result_death_names,

		'showmap':showmap

	}

	return render(request,'continent/oceania.html',context)

# oceania confirmed

def oceania_con(request):

	confirmed=pd.read_csv(r'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')

	data_cont = pd.read_csv(r'https://raw.githubusercontent.com/oderofrancis/rona/main/Countries-Continents.csv')

	world = gpd.read_file(r'https://raw.githubusercontent.com/oderofrancis/africa-corona/main/world.geojson')

	data_con = confirmed[['Country/Region',confirmed.columns[-1]]]

	data_con.columns = ['country','confirmed']

	data_cont.columns = ['continent','country']

	world = world[['NAME', 'geometry']]

	world.columns = ['country','geometry']


	data_oceania = pd.merge(left=data_cont, 
	                right=data_con, how='left', 
	                left_on='country', right_on='country'
	            )

	data_oceania = pd.merge(left=data_oceania, 
	                right=world, how='left', 
	                left_on='country', right_on='country'
	            )

	data_oceania = data_oceania[data_oceania['continent'] == 'Oceania']

	geo_data_oceania = gpd.GeoDataFrame(data_oceania)

	geo_data_oceania = geo_data_oceania.to_json()

	return HttpResponse(geo_data_oceania,content_type='application/json')



# oceania death

def oceania_death(request):

	death = pd.read_csv(r'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv')

	data_cont = pd.read_csv(r'https://raw.githubusercontent.com/oderofrancis/rona/main/Countries-Continents.csv')

	world = gpd.read_file(r'https://raw.githubusercontent.com/oderofrancis/africa-corona/main/world.geojson')

	data_death = death[['Country/Region',death.columns[-1]]]

	data_death.columns = ['country','death']

	data_cont.columns = ['continent','country']

	world = world[['NAME', 'geometry']]

	world.columns = ['country','geometry']


	data_oceania_death = pd.merge(left=data_cont, 
	                right=data_death, how='left', 
	                left_on='country', right_on='country'
	            )

	data_oceania_death = pd.merge(left=data_oceania_death, 
	                right=world, how='left', 
	                left_on='country', right_on='country'
	            )

	data_oceania_death = data_oceania_death[data_oceania_death['continent'] == 'Oceania']

	geo_data_oceania = gpd.GeoDataFrame(data_oceania_death)

	geo_data_oceania = geo_data_oceania.to_json()


	return HttpResponse(geo_data_oceania,content_type='application/json')
