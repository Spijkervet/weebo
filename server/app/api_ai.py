import apiai
import json
from settings import api_ai_access_token


class APIAI():

    def __init__(self):
        self.ai = apiai.ApiAI(api_ai_access_token)

    def request(self, query):
        request = self.ai.text_request()
        request.lang = 'en'
        request.query = query
        response = json.loads(request.getresponse().read().decode('utf-8'))
        print(response)
        responseStatus = response['status']['code']
        if(responseStatus == 200):
            return (response['result']['fulfillment']['messages'][0]['speech'])
        else:
            return "Something went wrong in the API dot AI service."
