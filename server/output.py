from gtts import gTTS
import boto3
from contextlib import closing
import subprocess
from settings import global_lang, speech_service, aws_voice_id, aws_speech_sample_rate, tmp_speech_file
import os
from time import sleep
from lights import WeeboLights
from gif_bot import GiphyBot


def aws_ssml_processing(text, whisper):
    if(whisper):
        text = '<speak><amazon:effect name="whispered">' + text + '</amazon:effect></speak>'
    else:
        text = '<speak><prosody pitch="high">' + text + '</prosody></speak>'
    return text

def amazon_aws_request(text):
    client = boto3.client('polly')
    response = client.synthesize_speech(
        Text=text,
        VoiceId=aws_voice_id,
        OutputFormat="mp3",
        SampleRate=str(aws_speech_sample_rate),
        TextType='ssml'
    )

    if("AudioStream" in response):
        with closing(response["AudioStream"]) as stream:
            try:
                with open(tmp_speech_file, "wb") as file:
                    file.write(stream.read())
            except IOError as error:
                print(error)
                pass

def output(text, retry, whisper=False):
    if text:
        print(text)
        try:
            if(speech_service == "google"):
                tts = gTTS(text=text, lang=global_lang, slow=False)
                tts.save(tmp_speech_file)
            elif(speech_service == "amazon"):
                processed_text = aws_ssml_processing(text, whisper)
                amazon_aws_request(processed_text)
                #subprocess.call(["aws", "polly", "synthesize-speech", "--output-format", "mp3", "--sample-rate", str(aws_speech_sample_rate), "--voice-id", aws_voice_id, "--text-type", "ssml", "--text", text, tmp_speech_file])
            subprocess.call(["mpg123", tmp_speech_file])
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
