import subprocess
import os
from time import sleep

from . lights import WeeboLights


def output(file_name, retry=False, whisper=False):
    try:
        subprocess.Popen(["mpg123", file_name])
    except Exception as e:
        print("*** EXCEPTION *** (" + str(e) + ")")
        os.system("say I am having some trouble with my voice.")
    finalize()

def i_am_weebo():
    subprocess.Popen(["aplay", "audio/weebo/i_am_weebo.wav"])
    sleep(1.25)

def finalize():
    #gif_bot = GiphyBot()
    #gif_bot.stop_thread()
    #subprocess.Popen(["afplay", "audio/shutdown.wav"])
    subprocess.Popen(["aplay", "audio/weebo/beep7.wav"])
    weebo_lights = WeeboLights()
    weebo_lights.green_light(False)
    weebo_lights.blue_light(False)
    weebo_lights.clean_GPIO()
    print("*** PROCESSED ***")
