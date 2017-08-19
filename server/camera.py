import subprocess
from time import sleep

def make_picture():
    subprocess.Popen(["aplay", "audio/weebo/okay_smile.wav"])
    subprocess.Popen(["aplay", "audio/weebo/flash_charge.wav"])
    sleep(3.5)
    subprocess.Popen(["aplay", "audio/weebo/shutter_click.wav"])
    sleep(1)
    subprocess.Popen(["aplay", "audio/weebo/bravo_encore.wav"])
    subprocess.Popen(["omxplayer", "video/weebo/bravo_encore.mov"])
    sleep(5)
    print("SHOW PICTURE")
