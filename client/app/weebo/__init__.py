import requests
import os
from .output import Output
from .settings import Settings

import multiprocessing
import speech_recognition as sr
from .data import WeeboData

import time
import subprocess

if Settings.rpi:
    from .lights import WeeboLights

class Weebo():
    def __init__(self):
        print("*** INIT *** WEEBO")
        self.output = Output()

        if Settings.rpi:
            self.weebo_lights = WeeboLights()
            self.weebo_lights.startup()

        if Settings.enable_idle:
            self.idle_time = 360 # seconds
            self.idle_task = multiprocessing.Process(target=self.idle)
            self.idle_task.start()
            # self.idle_task.terminate()
        # self.speech_recognition()

        startup_task = multiprocessing.Process(target=self.startup)
        startup_task.start()

    def play_audio(self, path=None):
        subprocess.call(["play", "-v 1.5", os.path.join(Settings.base_dir, "audio/weebo/beep0.wav")], stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

        if Settings.rpi:
            self.light_process()

        if path:
            subprocess.call(["play", os.path.join(Settings.base_dir, path)], stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
            self.reset()


    def startup(self):
        print("*** STARTUP SERVICE ***")
        self.play_audio("audio/startup.mp3")

    def reset(self):
        self.stop()
        if Settings.rpi:
            if self.weebo_lights:
                self.weebo_lights.green_light(False)
                self.weebo_lights.blue_light(False)
                self.weebo_lights.clean_GPIO()

    def fortune_cookie(self):
        fortune_process = subprocess.Popen(["fortune", "-s"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return fortune_process.stdout.read().decode('utf-8').strip()

    def idle(self):
        print("IDLE")
        while(True):
            time.sleep(self.idle_time)
            text = self.fortune_cookie()
            data = WeeboData()
            data.query = text
            data.say = True
            self.process(data)
        return

    def stop(self):
        #gif_bot = GiphyBot()
        #gif_bot.stop_thread()
        #subprocess.Popen(["afplay", "app/audio/shutdown.wav"])
        subprocess.call(["play", "-v 2", os.path.join(Settings.base_dir, "audio/weebo/beep7.wav")], stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        print("*** PROCESSED ***")

    def process(self, data):

        print("*** WEEBO *** Received query: {}".format(data.query))
        first_time = time.time()

        self.play_audio()

        if(data.say):
            self.say(data.query, data.whisper)
        else:
            self.query(data.query, data.api, data.whisper)

        self.talk_process()

        print("*** WEEBO *** Time taken: " + str(time.time() - first_time) + "s")

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
        print(url)
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
        self.stop()
        return

    def talk_process(self):
        talk_process = multiprocessing.Process(target=self.talk)
        talk_process.start()


    def lights(self):
        self.weebo_lights.green_light(True)
        self.weebo_lights.blue_light(True)
        self.weebo_lights.red_light(0.25, 10)
        return

    def light_process(self):
        light_process = multiprocessing.Process(target=self.lights)
        light_process.start()
