import time
from typing import Tuple
from rpi_ws281x import *
from auxmodule.AuxFunctions import colorWheel


class LEDRing:

    def __init__(self, count: int, pin: int, freq: int = 800000, dma_channel=10, brighness=255, invert=False, channel=0):
        self.count = count
        self.colors = [Color(0, 0, 0) for i in range(count)]
        self.strip = Adafruit_NeoPixel(
            count, pin, freq, dma_channel, invert, brighness, channel)

    def setColor(self, index: int, color: Tuple[int, int, int]):
        r, g, b = color
        color = Color(r, g, b)
        self.colors[index] = color
        self.strip.setPixelColor(index, color)
        self.strip.show()

    def rainbow(self):
        values = [colorWheel((i/self.count) * 255)
                  for i in range(1, self.count+1)]
        self.colors = [Color(a, b, c) for a, b, c in values]
