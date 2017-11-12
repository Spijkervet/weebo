from .api_ai import APIAI
from .gif_bot import GiphyBot
from .synthesizer import synthesize
def process(data, api=True, whisper=False):

    if(api):
        api_ai = APIAI()
        response = api_ai.request(data)
        print("*** API AI *** RESPONSE: " + response)
        if("picture" in response):
            make_picture()
            response = ""

    giphy = GiphyBot()
    giphy.get_giphy(data, "search")
    return synthesize(response, whisper)

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
