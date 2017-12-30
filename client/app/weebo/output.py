import subprocess
import os
from time import sleep

# from . lights import WeeboLights

base_dir = os.path.abspath(os.path.dirname(__file__))

class Output():
    def output(self, file_name):
        try:
            if os.path.isfile(file_name):
                # .call and not .Popen, synchronous (this is run in another process anyway).
                subprocess.call(["play", "-v 1", file_name], stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
            else:
                self.error()

        except Exception as e:
            print("*** EXCEPTION *** (" + str(e) + ")")
            os.system("say I am having some trouble with my voice.")

        if os.path.isfile(file_name):
            os.remove(file_name)
        subprocess.call(["play", "-v 2", os.path.join(base_dir, "audio/weebo/beep7.wav")], stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

    def error(self):
        subprocess.Popen(["play", os.path.join(base_dir, "audio/error.mp3")])

def i_am_weebo():
    subprocess.Popen(["play", os.path.join(base_dir, "audio/weebo/i_am_weebo.wav")])
    sleep(1.25)

def finalize():

    #gif_bot = GiphyBot()
    #gif_bot.stop_thread()
    #subprocess.Popen(["afplay", "app/audio/shutdown.wav"])

    # weebo_lights = WeeboLights()
    # weebo_lights.green_light(False)
    # weebo_lights.blue_light(False)
    # weebo_lights.clean_GPIO()
    print("*** PROCESSED ***")
