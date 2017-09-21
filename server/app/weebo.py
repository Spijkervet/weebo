#import pyaudio
#import speech_recognition as sr
import brain
from settings import wake_words, global_lang
import subprocess
from time import sleep, time
import sys
from lights import WeeboLights

#r = sr.Recognizer()
#r.energy_threshold=4000

weebo_lights = WeeboLights()

def STT_recognizer(audio_data, lang):
    return r.recognize_google(audio_data, language=lang)


def listener():
    print("*** LISTENING ***")
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
    try:
        text = STT_recognizer(audio, lang=global_lang)
        brain.process(text, retry=False)
    except Exception as e:
        print("*** EXCEPTION *** " + e)
        brain.process("I did not understand that.", retry=True)
        listener()
        pass

def wakeword_listener():
    with sr.Microphone() as source:                # use the default microphone as the audio source
        r.adjust_for_ambient_noise(source)         # listen for 1 second to calibrate the energy threshold for$
        audio = r.listen(source)                   # now when we listen, the energy threshold is already set t$
    try:
        test_wake_word = r.recognize_google(audio) #STT_recognizer(audio, lang=global_lang)
        print(test_wake_word)
        if(any(x in test_wake_word for x in wake_words)):
            subprocess.Popen(["aplay", "audio/startup.wav"])
            listener()
            return
        else:
            print("*** WRONG WAKEWORD ***")
            wakeword_listener()
    except Exception as e:
        print("*** EXCEPTION *** " + str(e))
        wakeword_listener()
        pass

def main():
    first_time = time()
    weebo_lights.green_light(True)
    weebo_lights.blue_light(True)
    if(len(sys.argv) <= 1):
        print("*** WEEBO *** LISTENING TO WAKEWORD")
        wakeword_listener()
    else:
        subprocess.Popen(["aplay", "audio/weebo/beep8.wav"])
        weebo_lights.light_thread("red", 0.25, 10)
        brain.process(sys.argv[1], retry=False, api=True)
    print("*** WEEBO *** Time taken: " + str(time() - first_time) + "s")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("*** INTERRUPTED ***")
        weebo_lights.clean_GPIO()
