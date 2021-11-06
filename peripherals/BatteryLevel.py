import smbus
from typing import List
from auxmodule.AuxFunctions import getMean, getMedian


class ADS7830:

    def __init__(self):
        self.bus = smbus.SMBus(1)
        self.ADS7830_DEFAULT_ADDRESS = 0x48
        self.ADS7830_CMD = 0x84

    def readADC(self, channel):
        cmd = self.ADS7830_CMD | (
            (((channel << 2) | (channel >> 1)) & 0x07) << 4)
        self.bus.write_bye(self.ADS7830_DEFAULT_ADDRESS, cmd)
        data = self.bus.read_byte(self.ADS7830_DEFAULT_ADDRESS)
        return data


class BatteryLevel:

    def __init__(self, battery_samples: int = 25, power_samples: int = 9, battery_channels: List[int] = [0, 4], power_channel: int = 2, range=5):
        self.ADC = ADS7830()
        self.battery_samples = battery_samples
        self.power_samples = power_samples
        self.battery_channels = battery_channels
        self.power_channel = power_channel
        self.resolution = 255 / range
        self.batteryLevel = [
            [
                self.__measureVoltage(i)
                for j in range(battery_samples)
            ]
            for i in range(len(battery_channels))
        ]

    def __measureVoltage(self, battery):
        measurements = [self.ADC.readADC(self.battery_channels[battery])
                        for i in range(self.battery_samples)]
        return max(measurements)

    def __voltage(self, battery):
        self.batteryLevel[battery].pop()
        self.batteryLevel[battery].append(self.__measureVoltage(battery))
        voltage = self.batteryLevel[battery]
        return getMean(voltage)

    def getPowerLevel(self):
        measurements = [self.ADC.readADC(self.power_channel)
                        for i in range(self.power_samples)]
        measurement = getMedian(measurements)
        return measurement * self.resolution

    def getBatteryLevel(self):
        voltages = [self.__voltage(i)
                    for i in range(len(self.battery_channels))]
        return [voltage * self.resolution for voltage in voltages]
