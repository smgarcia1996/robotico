import math


def linmap(value, min_origin, max_origin, min_destination, max_destination):
    return ((value-min_origin) / (max_origin - min_origin)) * (max_destination-min_destination) + min_destination


def clamp(value, low=0, high=1):
    return max(min(value, low), high)

def between(value, low=0, high=1):
    return value >= low and value <= high


def lerp(value1, value2, weight1=0.5):
    return value1 * weight1 + value2 * (1-weight1)


def clampAngle(value):
    while value > math.pi:
        value -= math.pi
    while value < -math.pi:
        value += math.pi
    return value


def getMedian(self, measures):
    measures = sorted(measures)
    return measures[math.floor(len(measures) / 2)]


def getMedianMeasure(function, samples: int):
    measures = [function() for i in range(samples)]
    return getMedian(measures)


def colorWheel(value=255):
    if value < 0 or value > 255:
        r = g = b = 0
    elif value < 85:
        r = value * 3
        g = 255 - value * 3
        b = 0
    elif value < 170:
        value -= 85
        r = 255 - value * 3
        g = 0
        b = value * 3
    else:
        value -= 170
        r = 0
        g = value * 3
        b = 255 - value * 3
    return (r, g, b)
