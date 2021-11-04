from typing import Tuple
from pyquaternion import Quaternion
from Vector3 import Vector3

class Servo:
    def __init__(self, offset_angle: Tuple[bool, float], limits: Tuple[float, float], servo_channel: int):
        self.limits = limits
        self.angle = offset_angle
        self.offset_angle = offset_angle
        self.servo_channel = servo_channel
    
    def mapAngle(self, angle):
        reverse, offset = self.offset_angle
        return angle * (-1 if reverse else 1) + offset

class Joint(Servo):
    def __init__(self, length: Vector3, orientation: Quaternion, offset_angle: Tuple[bool, float], limits: Tuple[float, float], servo_channel: int):
        self.length = length
        self.orientation = orientation
        super().__init__(offset_angle, limits, servo_channel)