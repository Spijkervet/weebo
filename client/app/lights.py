import RPi.GPIO as GPIO
from time import sleep
import threading

"""WEEBO LIGHTS"""
class WeeboLights():

    def __init__(self):
        print("*** WEEBO *** Lights initiated")
        self.red_light_gpio = 17
        self.green_light_gpio = 18
        self.blue_light_gpio = 4

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        GPIO.setup(self.blue_light_gpio, GPIO.OUT)
        GPIO.setup(self.green_light_gpio, GPIO.OUT)
        GPIO.setup(self.red_light_gpio, GPIO.OUT)


    def light_thread(self, light_type, delay_time, iterations):
        if(light_type == "red"):
            light_func = self.red_light
        elif(light_type == "blue"):
            light_func = self.blue_light
        elif(light_type == "green"):
            light_func = self.green_light
        else:
            return
        thread = threading.Thread(target=light_func, args=(delay_time, iterations))
        thread.daemon = False
        thread.start()

    def red_light(self, delay_time, iterations):
        for i in range(iterations):
            GPIO.output(self.red_light_gpio, GPIO.HIGH)
            sleep(delay_time)
            GPIO.output(self.red_light_gpio, GPIO.LOW)
            sleep(delay_time)

    def green_light(self, turn_on):
        if(turn_on):
            GPIO.output(self.green_light_gpio, GPIO.HIGH)
        else:
            GPIO.output(self.green_light_gpio, GPIO.LOW)

    def blue_light(self, turn_on):
        if(turn_on):
            GPIO.output(self.blue_light_gpio, GPIO.HIGH)
        else:
            GPIO.output(self.blue_light_gpio, GPIO.LOW)

    def clean_GPIO(self):
        GPIO.cleanup()
