import RPi.GPIO as GPIO
import time
import math
from auxmodule.AuxFunctions import getMedianMeasure


class HCSR04:

    def __init__(self, trigger_pin: int, echo_pin: int, mode=None):

        if mode is None:
            mode = GPIO.getmode()
            if mode is None:
                raise Exception('GPIO Mode not configured')

        self.trigger_pin = trigger_pin
        self.echo_pin = echo_pin
        GPIO.setup(self.trigger_pin, GPIO.OUT)
        GPIO.setup(self.echo_pin, GPIO.IN)

    def getDistance(self):
        GPIO.output(self.trigger_pin, True)
        time.sleep(0.00015)
        GPIO.output(self.trigger_pin, False)
        GPIO.wait_for_edge(self.echo_pin, GPIO.RISING, timeout=5000)
        start_time = time.time()
        GPIO.wait_for_edge(self.echo_pin, GPIO.FALLING, timeout=5000)
        end_time = time.time()
        distance = (end_time - start_time) / 0.000058
        return distance

    def getDistanceMedian(self, samples=5):
        return getMedianMeasure(lambda: self.getDistance(), samples)
