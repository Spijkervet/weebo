import os
import platform

class Settings():

    base_dir = os.path.abspath(os.path.dirname(__file__))

    # check if we have the raspberry pi packages.
    try:
        import RPi.GPIO
        rpi = True
    except ImportError as e:
        print(e, "Setting rpi to False in weebo/settings.")
        rpi = False
        pass

    enable_idle = False

    weebo_server_address = "192.168.1.26"
    weebo_server_port = "4000"

    wake_words = ["Weebo", "wei", "weber", "we", "Weaver"]
    tmp_speech_file = "/var/tmp/tmp_speech.mp3"
    tmp_gif_file = "/var/tmp/tmp_gif.mp4"
    screen_window_size = "0 0 800 480"

    giphy_api_key = "8e078baa2c0649c98c85cd5aec3ffd95"
