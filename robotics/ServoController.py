import logging
import math
import Adafruit_PCA9685
from auxmodule.AuxFunctions import linmap


class ServoController:
    def __init__(self):
        self.channel_16_controller = Adafruit_PCA9685.PCA9685(0x41)
        self.channel_32_controller = Adafruit_PCA9685.PCA9685(0x40)
        self.channel_16_controller.set_pwm_freq(50)
        self.channel_32_controller.set_pwm_freq(50)

    def moveServo(self, channel: int, angle: float) -> None:
        # print('moving ', channel, angle)
        duty_cycle = linmap(
            linmap(angle, 0, 180, 500, 2500), 0, 20000, 0, 4095)
        # print(duty_cycle)
        if channel >= 16 and channel < 32:
            controller = self.channel_32_controller
            channel -= 16
            controller.set_pwm(channel, 0, int(duty_cycle))
        else:
            controller = self.channel_16_controller
            controller.set_pwm(channel, 0, int(duty_cycle))
        
        

    def relaxServo(self, channel):

        if channel < 16:
            controller = self.channel_16_controller
        elif channel < 32:
            controller = self.channel_32_controller
            channel -= 16

        controller.set_pwm(channel, 4096, 4096)
