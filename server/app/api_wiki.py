import wikipedia

class APIWikipedia():

    def request(self, query):
        response = wikipedia.summary(query, sentences=2)
        if(response):
            return response
        return "I'm sorry, I couldn't get a right answer for you"
