from os import system
from .api import say, query
from .output import Output
from .settings import tmp_speech_file

class Weebo():
    def __init__(self):
        print("*** INIT *** WEEBO")
        self.output = Output()

    def process(self, query_data, _api, _say=True, whisper=False):
        from time import time

        print("*** WEEBO *** Received query: {}".format(query_data))
        first_time = time()

        # weebo_lights = WeeboLights()

        # weebo_lights.green_light(True)
        # weebo_lights.blue_light(True)

        # subprocess.Popen(["aplay", "app/audio/weebo/beep8.wav"])
        # weebo_lights.red_light(True)
        # weebo_lights.red_light(0.25, 10)
        # weebo_lights.light_thread("red", 0.25, 10)

        if(_say):
            say(query_data, whisper)
        else:
            query(query_data, _api, whisper)


        self.output.output(tmp_speech_file)
        print("*** WEEBO *** Time taken: " + str(time() - first_time) + "s")
        '''
        from .gif_bot import GiphyBot

        giphy = GiphyBot()
        if giphy.get_giphy(query_data, "search"):
            giphy.play()
        '''
