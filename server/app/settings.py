import os

wake_words = ["Weebo", "wei", "weber", "we", "Weaver"]
global_lang = "en-us"
speech_service = "google" # amazon google
aws_voice_id = "Salli" #Lotte for Dutch.
aws_speech_sample_rate = 22050
wolfram_alpha_id = "TYX4Q4-VG8YW8YL4T"
tmp_speech_file = "/var/tmp/tmp_speech.mp3"


def get_ai_token():
    try:
        return os.environ['api_ai_access_token']
    except:
        print("*** ERROR *** You do not have an api_ai_access_token")
        pass
    return ""

api_ai_access_token = get_ai_token()
