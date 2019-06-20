import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "client-secret.json"

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
		

	else:
		return response.fulfillment_text