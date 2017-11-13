import wolframalpha
from .settings import wolfram_alpha_id


class APIWA():

    def __init__(self):
        self.wa_client = wolframalpha.Client(wolfram_alpha_id)

    def request(self, query):
        request = self.wa_client.query(query)
        if next(request.results).text:
            return next(request.results).text
        return "I'm sorry, I couldn't get a right answer for you"
