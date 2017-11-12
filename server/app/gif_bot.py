from .settings import giphy_api_key, global_lang, tmp_gif_file, screen_window_size
import requests
import urllib.request
import threading
import subprocess
from random import randint

class GiphyBot():

    def __init__(self):
        self.base_url = "https://api.giphy.com/v1/"

    def get_giphy(self, query, endpoint, sticker=False, limit=25, rating="G"):
        query_url = self.create_query_url(self.base_url, query, endpoint, sticker, limit, rating)
        print(query_url)
        response = requests.get(query_url)
        data = response.json()
        num_gifs = len(data['data'])
        if(num_gifs > 0):
            urllib.request.urlretrieve(data['data'][randint(0,num_gifs-1)]['images']['looping']['mp4'], tmp_gif_file)
            #self.gif_thread = threading.Thread(target=self.play_gif)
            #self.gif_thread.daemon = False
            #self.start_thread()

    def create_query_url(self, url, query, endpoint, sticker, limit, rating):
        if(sticker == False):
            url += "gifs/"
        else:
            url += "sticker/"

        if(endpoint == "search"):
            url += "search?"
        elif(endpoint == "trending"):
            url += "trending?"
        else:
            url += "random?"

        url += "api_key=" + giphy_api_key
        return (url + "&q=" + query + "&limit=" + str(limit) + "&offset=0" + "&rating=" + rating + "&lang=" + global_lang)



    def play_gif(self):
        subprocess.call(["omxplayer", "--win", screen_window_size, tmp_gif_file])

    def start_thread(self):
        self.gif_thread.start()

    def stop_thread(self):
        self.gif_thread.stop()
