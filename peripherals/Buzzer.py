import RPi.GPIO as GPIO
import time


class Buzzer:

    def __init__(self, pin: int, mode=None):

        if mode is None:
            mode = GPIO.getmode()
            if mode is None:
                raise Exception('GPIO Mode not configured')

        self.pin = pin
        GPIO.setup(self.pin, GPIO.OUT)

    def pulse(self, length: float):
        GPIO.output(self.pin, True)
        time.sleep(length)
        GPIO.output(self.pin, False)
