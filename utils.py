import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "client-secret.json"
import requests,json
import imdb
from geopy.geocoders import Nominatim

import dialogflow_v2 as dialogflow
dialogflow_session_client = dialogflow.SessionsClient()
PROJECT_ID = "tanvigupta96-ymmdnp"

from gnewsclient import gnewsclient

client = gnewsclient.NewsClient()

def get_news(parameters):
	print(parameters)
	client.topic = parameters.get('news_type')
	client.language = parameters.get('language')
	client.location = parameters.get('geo-country')
	return client.get_news()


def get_weather(parameters):
	print(parameters)
	city = parameters.get('geo-city')
	api = "f03e03407c276103b42bbdb3d830394b"
	baseurl = "http://api.openweathermap.org/data/2.5/weather?"
	url = baseurl + "q=" + city + "&appid=" + api
	r = requests.get(url) #page requested
	#return r.json()
	if r.json()['cod'] != '404':
		cityName = r.json()['name']
		temp = round(r.json()['main']['temp']-273,2)
		humidity = r.json()['main']['humidity']
		temp_min = round(r.json()['main']['temp_min']-273,2)
		temp_max = round(r.json()['main']['temp_max']-273,2)
		description = r.json()['weather'][0]['description']
		show_details = 'Current Weather of *{}* is: \n*Temperature* : {}°C \n*Humidity* : {}% \n*Description* : {} \n*Min_Temp* : {}°C \n*Max_Temp* : {}°C'.format(cityName,temp,humidity,description,temp_max,temp_min)
		return(show_details)

	else :
		return 'City Not Found!'


def get_restaurants(parameters):
	print(parameters)
	city = parameters.get('geo-city')
	geolocator = Nominatim(user_agent="WhatsappBot")
	if(city == ''):
		location = parameters.get('location')['subadmin-area']
		loc = geolocator.geocode(location, timeout = None)
		lat = loc.latitude 
		lon = loc.longitude

	else : 
		loc = geolocator.geocode(city, timeout = None)
		lat = loc.latitude 
		lon = loc.longitude

	api_key = "dca0306887f49d37fc278cbc7651e8a6"
	headers = {'user-key' : api_key}
	r = requests.get("https://developers.zomato.com/api/v2.1/geocode?lat=" + str(lat) + "&lon=" + str(lon), headers = headers)
	show_details = 'Here is yout list of Restaurants!' 
	for i in range(5) :
		name = r.json()['nearby_restaurants'][i]['restaurant']['name']
		url = r.json()['nearby_restaurants'][i]['restaurant']['url']
		add = r.json()['nearby_restaurants'][i]['restaurant']['location']['address']
		rating = r.json()['nearby_restaurants'][i]['restaurant']['user_rating']['aggregate_rating']
		show_details += '\n*Name* : {} \n*Address* : {} \n*Ratings* : {}★ \n*Link* : {} \n\n\n'.format(name,add,rating,url)
	return(show_details)
	

def get_reviews(parameters):
	print(parameters)
	ia = imdb.IMDb()
	mov_name = parameters.get('movie_name')[0]
	movie_search = parameters.get('movie_search')
	s_results = ia.search_movie(mov_name)
	details = s_results[0]
	ia.update(details)
	cover = details['cover url']
	name = details['title']
	rating = details['rating']
	cast = ''
	for i in range(4):
		cast += str(details['cast'][i]) + ', '

	show_details = "\n*Title: {}*\n*Cast:* {} \n*Rating: {}*★".format(name,cast,rating)
	return show_details, cover, movie_search


def detect_intent_from_text(text, session_id, language_code='en'):
    session = dialogflow_session_client.session_path(PROJECT_ID, session_id)
    text_input = dialogflow.types.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.types.QueryInput(text=text_input)
    response = dialogflow_session_client.detect_intent(session=session, query_input=query_input)
    return response.query_result




def fetch_reply(msg, session_id):
	response = detect_intent_from_text(msg,session_id)

	if response.intent.display_name == 'get_news':		
		# return "news will be displayed! *{}*".format(dict(response.parameters))
		news = get_news(dict(response.parameters))
		news_str = 'Here are your *{}* news!'.format(client.topic)
		for row in news:
			news_str += "\n\n{}\n\n{}\n\n".format(row['title'],row['link'])
		print(news_str)
		return news_str[:1100],None,None

	if response.intent.display_name == 'get_weather':
		weather = get_weather(dict(response.parameters))
		return weather,None , None

	if response.intent.display_name == 'get_restaurant':
		restaurants = get_restaurants(dict(response.parameters))
		return restaurants, None, None

	if response.intent.display_name == 'get_reviews':
	 	reviews, cover, movie_search = get_reviews(dict(response.parameters))
	 	print(reviews)
	 	return reviews, cover, movie_search
	 	
	else:
		return response.fulfillment_text, None, None