import requests
from urllib import request
from . settings import tmp_speech_file, weebo_server_address, weebo_server_port


def query(text, api, whisper):
    url = "http://" + weebo_server_address + ":" + weebo_server_port + "/query?data=" + text + "&api=" + api + "&whisper=" + str(whisper)
    # request.urlretrieve(url, tmp_speech_file)
    r = requests.get(url)
    if r.status_code == 200:
        with open(tmp_speech_file, 'wb') as f:
            f.write(r.content)

def say(text, whisper):
    url = "http://" + weebo_server_address + ":" + weebo_server_port + "/say?data=" + text + "&whisper=" + str(whisper)
    r = requests.get(url)
    if r.status_code == 200:
        with open(tmp_speech_file, 'wb') as f:
            f.write(r.content)
