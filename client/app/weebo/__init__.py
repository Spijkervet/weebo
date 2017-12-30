import requests
from os import system
from .output import Output
from .settings import Settings

import multiprocessing
import speech_recognition as sr
from .data import WeeboData

import time

if Settings.rpi:
    from .lights import WeeboLights

class Weebo():
    def __init__(self):
        print("*** INIT *** WEEBO")
        self.output = Output()
        # self.speech_recognition()

    def process(self, data):
        from time import time

        print("*** WEEBO *** Received query: {}".format(data.query))
        first_time = time()

        if(data.say):
            self.say(data.query, data.whisper)
        else:
            self.query(data.query, data.api, data.whisper)

        self.talk_process()

        if Settings.rpi:
            self.light_process()
        print("*** WEEBO *** Time taken: " + str(time() - first_time) + "s")
        '''
        from .gif_bot import GiphyBot

        giphy = GiphyBot()
        if giphy.get_giphy(query_data, "search"):
            giphy.play()
        '''


    def query(self, text, api, whisper):
        url = "http://" + Settings.weebo_server_address + ":" + Settings.weebo_server_port + "/query?data=" + text + "&api=" + api + "&whisper=" + str(whisper)
        try:
            r = requests.get(url)
            if r.status_code == 200:
                with open(Settings.tmp_speech_file, 'wb') as f:
                    f.write(r.content)
            return True
        except Exception as e:
            print(e)
            pass

    def say(self, text, whisper):
        url = "http://" + Settings.weebo_server_address + ":" + Settings.weebo_server_port + "/say?data=" + text + "&whisper=" + str(whisper)
        try:
            r = requests.get(url)
            if r.status_code == 200:
                with open(Settings.tmp_speech_file, 'wb') as f:
                    f.write(r.content)
        except Exception as e:
            print(e)
            pass


    def speech_recog(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            audio_data = None
            r.adjust_for_ambient_noise(source, duration=0.5)
            r.pause_threshold = 0.5
            print("SPEAK")
            try:
                audio_data = r.listen(source, timeout=2.0)
            except Exception as e:
                pass

            if audio_data:
                try:
                    text = r.recognize_google(audio_data, language="en-US")
                    print("You said: " + text)
                    data = WeeboData()
                    data.query = text
                    data.say = True
                    self.process(data)
                except sr.UnknownValueError:
                    print("Google Speech Recognition could not understand audio")
                except sr.RequestError as e:
                    print("Could not request results from Google Speech Recognition service; {0}".format(e))
                except LookupError:
                    print("Oops! Didn't catch that")
        return

    def speech_recognition(self):
        speech_recog = multiprocessing.Process(target=self.speech_recog)
        speech_recog.start()

    def talk(self):
        self.output.output(Settings.tmp_speech_file)
        return

    def talk_process(self):
        talk_process = multiprocessing.Process(target=self.talk)
        talk_process.start()


    def lights(self):
        print("LIGHTS")
        weebo_lights = WeeboLights()

        weebo_lights.green_light(True)
        weebo_lights.blue_light(True)
        weebo_lights.red_light(0.25, 10)
        subprocess.call(["play", "app/audio/weebo/beep8.wav"], stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        return

    def light_process(self):
        light_process = multiprocessing.Process(target=self.lights)
        light_process.start()
