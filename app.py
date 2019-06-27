from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from utils import fetch_reply
from pymongo import MongoClient #MongoClient is a class tht will create an object for us.
import urllib 
import datetime
import json

client = MongoClient("mongodb+srv://Tanvi:" +urllib.parse.quote("TanviGupta@123")+"@cluster0-f775h.mongodb.net/test?retryWrites=true&w=majority")
db = client.get_database('helpbot_db')
record = db.records


#print(record.count_documents({}))


app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, World!"

@app.route("/sms", methods=['POST'])
def sms_reply():
    """Respond to incoming calls with a simple text message."""
    # Fetch the message
    print(json.dumps(request.form,indent = 2))
    msg = request.form.get('Body')
    sender = request.form.get('From')
    reply, cover, mov_search = fetch_reply(msg,sender)

    # Create reply
    resp = MessagingResponse()
    if msg == 'help' or msg == 'Help' or msg =='HELP':
        reply = "Hello, I am a *_HelpBot_*. How may I help you? \n\nYou can search for news by providing us the *<new></new>s type*! \nEg: *show me sports news* \n\nYou can also search for *restaurants/cafes* in any area \nEg: *show me restaurants in gurgaon* \n\nYou can check the *temperature* of any paticular location \nEg: *what is the temperature of amritsar* \n\nYou can check movie reviews \n Eg: *Reviews of Uri*"
        resp.message(reply)
        new_record = { 'message_body': msg, 'sender_id' : sender, 'bot_reply': reply, 'sent_at' : str(datetime.datetime.now()) }
        print(new_record)
        record.insert_one(new_record)
    
    elif mov_search == 'reviews':
        resp.message(reply).media(cover)
        new_record = { 'message_body': msg, 'sender_id' : sender, 'bot_reply': reply, 'cover': cover, 'sent_at' : str(datetime.datetime.now()) }
        record.insert_one(new_record)
    
    else:
        resp.message(reply)
        new_record = { 'message_body': msg, 'sender_id' : sender, 'bot_reply': reply, 'sent_at' : str(datetime.datetime.now()) }
        record.insert_one(new_record)

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
