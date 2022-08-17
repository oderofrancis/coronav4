from django.shortcuts import render
import pandas as pd


import requests
from bs4 import BeautifulSoup



def africa_country(request):

	# select country

	countrynames = request.POST.get('countrynames')

	# data reading and extraction

	confirmed = pd.read_csv(r'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')

	# (?# death = pd.read_csv(r'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv'))

	data_cont = pd.read_csv(r'https://raw.githubusercontent.com/oderofrancis/rona/main/Countries-Continents.csv')

	# analysis

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




	# analysis for a single country

	confirmed['country'] = confirmed['Country/Region'].str.replace(' ', '-')

	countryname = pd.DataFrame(confirmed[confirmed['country']==countrynames][confirmed.columns[4:-1]].sum().reset_index())


	countryname.columns = ['country','values']

	# adding lag values to our dataset

	countryname['lagVal'] = countryname['values'].shift(1).fillna(0)

	countryname['incrementVal'] = countryname['values']-countryname['lagVal']

	countryname['rollingMean'] = countryname['incrementVal'].rolling(window=4).mean().fillna(0)

	axisvalues=countryname.index.tolist()

	datasetforline = [

	    {'yAxisID': 'y-axis-1','label':'Daily Cumulated Data',
	    'data':countryname['values'].values.tolist(),
	    'borderColor':'#03a9fc','backgroundColor':'#03a9fc','fill':'false'
	    },

	    {'yAxisID': 'y-axis-2','label':'Rolling Mean 4 days',
	    'data':countryname['rollingMean'].values.tolist(),
	    'borderColor':'#fc5203','backgroundColor':'#fc5203','fill':'false'
	    }
	]


	# analysis of positivity

	#  positivity rates

	# data from web scrapping

	data_conts = pd.read_csv(r'https://raw.githubusercontent.com/oderofrancis/rona/main/Countries-Continents.csv')

	url = "https://www.worldometers.info/world-population/population-by-country/"

	r = requests.get(url)

	soup = BeautifulSoup(r.content)

	countries = soup.find_all("table")[0]

	df = pd.read_html(str(countries))[0]

	df = df[['Country (or dependency)','Population (2020)']]

	df.columns = ['Country','population']

	df['country'] = df['Country'].str.replace(' ', '-')

	df = df.reindex(columns=['country','population'])

	# # confirmed cases

	confirmed = confirmed[['Country/Region',confirmed.columns[-1]]]

	confirmed.columns = ['Country','confirmed']

	confirmed['country'] = confirmed['Country'].str.replace(' ', '-')

	confirmed = confirmed.reindex(columns=['country','confirmed'])

	# continent analysis

	data_conts['country'] = data_conts['Country'].str.replace(' ', '-')

	data_conts = data_conts[['Continent','country']]

	data_conts.columns = ['continent','country']

	# #corona with continent

	data = pd.merge(left=data_conts, 
						right=confirmed, how='left', 
						left_on='country', right_on='country'
					)

	# # merged data with country population

	data = pd.merge(left=data, 
						right=df, how='left', 
						left_on='country', right_on='country'
					)

	# # poditive rate

	data['postivity'] = round(data['confirmed'].div(data['population']),2)

	country_positivity = data[data['country']==countrynames]

	country_positivity = float(country_positivity[country_positivity.columns[-1]])

	# continent positive rate

	total_continent = data[data['continent']=='Africa']

	continent_positivity = total_continent[total_continent.columns[-1]].mean()

	


	# showmap

	showmap = 'False'


	context = {
		'totalafrica':totalafrica,'africa_con_values':africa_con_values,
		'africa_con_names':africa_con_names,'countrynames':countrynames,
		'datasetforline':datasetforline,'axisvalues':axisvalues,

		'showmap':showmap,
		'country_positivity':country_positivity,'continent_positivity':continent_positivity


	}

	return render(request,'continent/africa.html',context)





# Asia

def asia_country(request):

	# select country

	countrynames = request.POST.get('countrynames')

	# analysis

	confirmed = pd.read_csv(r'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')

	# death = pd.read_csv(r'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv')

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




	# analysis for a single country

	confirmed['country'] = confirmed['Country/Region'].str.replace(' ', '-')

	countryname = pd.DataFrame(confirmed[confirmed['country']==countrynames][confirmed.columns[4:-1]].sum().reset_index())

	countryname.columns = ['country','values']

	# adding lag values to our dataset

	countryname['lagVal'] = countryname['values'].shift(1).fillna(0)

	countryname['incrementVal'] = countryname['values']-countryname['lagVal']

	countryname['rollingMean'] = countryname['incrementVal'].rolling(window=4).mean().fillna(0)

	axisvalues=countryname.index.tolist()

	datasetforline = [

	    {'yAxisID': 'y-axis-1','label':'Daily Cumulated Data',
	    'data':countryname['values'].values.tolist(),
	    'borderColor':'#03a9fc','backgroundColor':'#03a9fc','fill':'false'
	    },

	    {'yAxisID': 'y-axis-2','label':'Rolling Mean 4 days',
	    'data':countryname['rollingMean'].values.tolist(),
	    'borderColor':'#fc5203','backgroundColor':'#fc5203','fill':'false'
	    }
	]



	# showmap

	showmap = 'False'


	context = {
		'totalasia':totalasia,'asia_con_values':asia_con_values,
		'asia_con_names':asia_con_names,'countrynames':countrynames,
		'datasetforline':datasetforline,'axisvalues':axisvalues,

		'showmap':showmap

	}

	return render(request,'continent/asia.html',context)


# america

def america_country(request):

	# select country

	countrynames = request.POST.get('countrynames')

	# analysis

	confirmed = pd.read_csv(r'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')

	# death = pd.read_csv(r'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv')

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




	# analysis for a single country

	confirmed['country'] = confirmed['Country/Region'].str.replace(' ', '-')

	countryname = pd.DataFrame(confirmed[confirmed['country']==countrynames][confirmed.columns[4:-1]].sum().reset_index())


	countryname.columns = ['country','values']

	# adding lag values to our dataset

	countryname['lagVal'] = countryname['values'].shift(1).fillna(0)

	countryname['incrementVal'] = countryname['values']-countryname['lagVal']

	countryname['rollingMean'] = countryname['incrementVal'].rolling(window=4).mean().fillna(0)

	axisvalues=countryname.index.tolist()

	datasetforline = [

	    {'yAxisID': 'y-axis-1','label':'Daily Cumulated Data',
	    'data':countryname['values'].values.tolist(),
	    'borderColor':'#03a9fc','backgroundColor':'#03a9fc','fill':'false'
	    },

	    {'yAxisID': 'y-axis-2','label':'Rolling Mean 4 days',
	    'data':countryname['rollingMean'].values.tolist(),
	    'borderColor':'#fc5203','backgroundColor':'#fc5203','fill':'false'
	    }
	]



	# showmap

	showmap = 'False'


	context = {
		'totalamerica':totalamerica,'america_con_values':america_con_values,
		'america_con_names':america_con_names,'countrynames':countrynames,
		'datasetforline':datasetforline,'axisvalues':axisvalues,

		'showmap':showmap

	}

	return render(request,'continent/america.html',context)






# South America

def latin_country(request):

	# select country

	countrynames = request.POST.get('countrynames')

	# analysis

	confirmed = pd.read_csv(r'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')

	# death = pd.read_csv(r'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv')

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




	latin = latin[['country',latin.columns[-1]]].groupby('country').sum()

	latin = latin.reset_index()

	latin.columns = ['country','confirmed']

	totallatin = latin['confirmed'].sum()

	totallatin = "{:,}".format(int(totallatin))

	latin = latin.sort_values(by='confirmed',ascending=False)

	# convert into integer

	latin['confirmed'] = latin['confirmed'].astype('int')

	# add separator for thousand

	latin_con_values = latin['confirmed'].map('{:,.0f}'.format)

	latin_con_values = latin_con_values.values.tolist()

	latin_con_names = latin['country'].values.tolist()




	# analysis for a single country

	confirmed['country'] = confirmed['Country/Region'].str.replace(' ', '-')

	countryname = pd.DataFrame(confirmed[confirmed['Country/Region']==countrynames][confirmed.columns[4:-1]].sum().reset_index())

	countryname.columns = ['country','values']

	# adding lag values to our dataset

	countryname['lagVal'] = countryname['values'].shift(1).fillna(0)

	countryname['incrementVal'] = countryname['values']-countryname['lagVal']

	countryname['rollingMean'] = countryname['incrementVal'].rolling(window=4).mean().fillna(0)

	axisvalues=countryname.index.tolist()

	datasetforline = [

	    {'yAxisID': 'y-axis-1','label':'Daily Cumulated Data',
	    'data':countryname['values'].values.tolist(),
	    'borderColor':'#03a9fc','backgroundColor':'#03a9fc','fill':'false'
	    },

	    {'yAxisID': 'y-axis-2','label':'Rolling Mean 4 days',
	    'data':countryname['rollingMean'].values.tolist(),
	    'borderColor':'#fc5203','backgroundColor':'#fc5203','fill':'false'
	    }
	]



	# showmap

	showmap = 'False'


	context = {
		'totallatin':totallatin,'latin_con_values':latin_con_values,
		'latin_con_names':latin_con_names,'countrynames':countrynames,
		'datasetforline':datasetforline,'axisvalues':axisvalues,

		'showmap':showmap

	}

	return render(request,'continent/latin.html',context)





# # europe

def europe_country(request):

	# select country

	countrynames = request.POST.get('countrynames')

	# analysis

	confirmed = pd.read_csv(r'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')

	# death = pd.read_csv(r'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv')

	data_cont = pd.read_csv(r'https://raw.githubusercontent.com/oderofrancis/rona/main/Countries-Continents.csv')

	data_europe_m = confirmed.rename(columns = {'Country/Region':'country'})

	data_europe_m = data_europe_m.drop('Province/State',axis=1)

	data_europe_m = data_europe_m.drop('Lat',axis=1)

	data_europe_m = data_europe_m.drop('Long',axis=1)

	data_cont.columns = ['continent','country']

	data_europe_m = pd.merge(left=data_cont, 
		                right=data_europe_m, how='left', 
		                left_on='country', right_on='country'
		            )

	data_europe_m = data_europe_m[data_europe_m['continent'] == 'Europe']



	europe_con = data_europe_m[['country',data_europe_m.columns[-1]]].groupby('country').sum()

	europe_con = europe_con.reset_index()

	europe_con.columns = ['country','confirmed']

	totaleurope =europe_con['confirmed'].sum()

	totaleurope = "{:,}".format(int(totaleurope))

	europe_con =europe_con.sort_values(by='confirmed',ascending=False)

	# convert into integer

	europe_con['confirmed'] = europe_con['confirmed'].astype('int')

	# add separator for thousand

	europe_con_values = europe_con['confirmed'].map('{:,.0f}'.format)

	europe_con_values = europe_con_values.values.tolist()

	europe_con_names = europe_con['country'].str.replace(' ', '-').values.tolist()




	# analysis for a single country

	confirmed['country'] = confirmed['Country/Region'].str.replace(' ', '-')

	countryname = pd.DataFrame(confirmed[confirmed['country']==countrynames][confirmed.columns[4:-1]].sum().reset_index())


	countryname.columns = ['country','values']

	# adding lag values to our dataset

	countryname['lagVal'] = countryname['values'].shift(1).fillna(0)

	countryname['incrementVal'] = countryname['values']-countryname['lagVal']

	countryname['rollingMean'] = countryname['incrementVal'].rolling(window=4).mean().fillna(0)

	axisvalues=countryname.index.tolist()

	datasetforline = [

	    {'yAxisID': 'y-axis-1','label':'Daily Cumulated Data',
	    'data':countryname['values'].values.tolist(),
	    'borderColor':'#03a9fc','backgroundColor':'#03a9fc','fill':'false'
	    },

	    {'yAxisID': 'y-axis-2','label':'Rolling Mean 4 days',
	    'data':countryname['rollingMean'].values.tolist(),
	    'borderColor':'#fc5203','backgroundColor':'#fc5203','fill':'false'
	    }
	]



	# showmap

	showmap = 'False'


	context = {
		'totaleurope':totaleurope,'europe_con_values':europe_con_values,
		'europe_con_names':europe_con_names,'countrynames':countrynames,
		'datasetforline':datasetforline,'axisvalues':axisvalues,

		'showmap':showmap

	}

	return render(request,'continent/europe.html',context)






# # oceania


def oceania_country(request):

	# select country

	countrynames = request.POST.get('countrynames')

	# analysis

	confirmed = pd.read_csv(r'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')

	# death = pd.read_csv(r'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv')

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



	# analysis for a single country

	confirmed['country'] = confirmed['Country/Region'].str.replace(' ', '-')

	countryname = pd.DataFrame(confirmed[confirmed['country']==countrynames][confirmed.columns[4:-1]].sum().reset_index())


	countryname.columns = ['country','values']

	# adding lag values to our dataset

	countryname['lagVal'] = countryname['values'].shift(1).fillna(0)

	countryname['incrementVal'] = countryname['values']-countryname['lagVal']

	countryname['rollingMean'] = countryname['incrementVal'].rolling(window=4).mean().fillna(0)

	axisvalues=countryname.index.tolist()

	datasetforline = [

	    {'yAxisID': 'y-axis-1','label':'Daily Cumulated Data',
	    'data':countryname['values'].values.tolist(),
	    'borderColor':'#03a9fc','backgroundColor':'#03a9fc','fill':'false'
	    },

	    {'yAxisID': 'y-axis-2','label':'Rolling Mean 4 days',
	    'data':countryname['rollingMean'].values.tolist(),
	    'borderColor':'#fc5203','backgroundColor':'#fc5203','fill':'false'
	    }
	]



	# showmap

	showmap = 'False'


	context = {
		'totaloceania':totaloceania,'oceania_con_values':oceania_con_values,
		'oceania_con_names':oceania_con_names,'countrynames':countrynames,
		'datasetforline':datasetforline,'axisvalues':axisvalues,

		'showmap':showmap

	}

	return render(request,'continent/oceania.html',context)