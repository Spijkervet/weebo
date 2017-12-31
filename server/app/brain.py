from .api_ai import APIAI
from .api_wa import APIWA
from .api_wiki import APIWikipedia
from .synthesizer import synthesize


def add_db_query(data, response, type=0):
    from .models import Queries
    new_query = Queries()
    new_query.question = data
    new_query.response = response
    new_query.type = type
    new_query.save()

def process(data, api, whisper=False):
    if(api == "API AI"):
        api_ai = APIAI()
        response = api_ai.request(data)
        print("*** API AI *** RESPONSE: " + response)
        if("picture" in response):
            make_picture()
            response = ""
    elif(api == "Wolfram Alpha"):
        wolframalpha = APIWA()
        response = wolframalpha.request(data)
        print("*** WOLFRAM ALPHA *** RESPONSE: " + response)
    elif(api == "Wikipedia"):
        wikipedia = APIWikipedia()
        response = wikipedia.request(data)
        print("*** WIKIPEDIA *** RESPONSE: " + response)
    else:
        response = "You didn't choose a brain"
    synthesized = synthesize(response, whisper)
    add_db_query(data, response)
    return synthesized

def say(data, whisper=False):
    synthesized = synthesize(data, whisper)
    add_db_query(data, data, type=1)
    return synthesized

def emotion(data):
    keywords = ['do you feel']
    if(any(x in data for x in keywords)):
        return "I am a machine... I don't really have emotions... yet. But thanks for asking!"
    keywords = ['are you', 'do you do']
    if(any(x in data for x in keywords)):
        return "I am doing pretty good. Thanks for asking!"
    keywords = ['sad']
    if(any(x in data for x in keywords)):
        return "Don't feel sad. Every day is a day full of new opportunities!"
    keywords = ['happy']
    if(any(x in data for x in keywords)):
        return "I'm glad you're feeling good!"
    return "I'm not sure what you mean. In the end, I'm only a machine."
