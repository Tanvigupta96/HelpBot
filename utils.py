import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "client-secret.json"
import requests,json
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
		return news_str[:1100]

	if response.intent.display_name == 'get_weather':
		weather = get_weather(dict(response.parameters))
		return weather


	else:
		return response.fulfillment_text