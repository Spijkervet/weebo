import subprocess
import os
from time import sleep
from .settings import Settings
# from . lights import WeeboLights



class Output():

    def __init__(self):
        if Settings.rpi:
            print("Setting PCM,0 device (3mm jack) to default and volume to 100%.")
            subprocess.call(["amixer", "cset", "numid=3 1"])
            subprocess.call(["amixer", "sset", "PCM,0", "100%"])

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

    def error(self):
        subprocess.Popen(["play", os.path.join(Settings.base_dir, "audio/error.mp3")])

def i_am_weebo():
    subprocess.Popen(["play", os.path.join(Settings.base_dir, "audio/weebo/i_am_weebo.wav")])
    sleep(1.25)
