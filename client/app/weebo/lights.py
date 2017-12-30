import RPi.GPIO as GPIO
from time import sleep

class WeeboLights():
    """WEEBO LIGHTS, RPi only."""

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
