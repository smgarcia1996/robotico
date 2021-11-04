import math
from pyquaternion import Quaternion
import numpy as np
from dataclasses import dataclass


class Vector3:

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, v):
        return Vector3(self.x + v.x, self.y + v.y, self.z + v.z)

    def __sub__(self, v):
        return Vector3(self.x - v.x, self.y - v.y, self.z - v.z)

    def __str__(self):
        return ",".join([str(self.x), str(self.y), str(self.z)])

    def modulus_sq(self):
        return self.x * self.x + self.y * self.y + self.z * self.z

    def modulus(self):
        return math.sqrt(self.modulus_sq())

    def to_spherical(self):
        return (Vector3.cartesian_to_spherical(self.x, self.y, self.z))

    @staticmethod
    def rotate(v, rotation: Quaternion):
        v_rotated = rotation.rotate(np.array([v.x, v.y, v.z]))
        return Vector3(v_rotated[0], v_rotated[1], v_rotated[2])

    @staticmethod
    def dot(v1, v2):
        return v1.x * v2.x + v1.y * v2.y + v1.z * v2.z

    @staticmethod
    def cross(v1, v2):
        x = v1.y * v2.z - v1.z * v2.y
        y = v1.z * v2.x - v1.x * v2.z
        z = v1.x * v2.y - v1.y * v2.x
        return Vector3(x, y, z)

    @staticmethod
    def angle(v1, v2):
        # radians
        sine = Vector3.cross(v1, v2).modulus()
        cosine = Vector3.dot(v1, v2)
        angle = math.atan2(sine, cosine)
        return angle

    @staticmethod
    def spherical_to_cartesian(radius, theta, phi):
        # angles in radians
        x = radius * math.cos(theta) * math.cos(phi)
        y = radius * math.sin(theta) * math.cos(phi)
        z = radius * math.sin(phi)
        return (x, y, z)

    @staticmethod
    def cartesian_to_spherical(x, y, z):
        # angles in radians
        theta = math.atan2(y, x)
        radius = math.sqrt(x*x + y*y + z*z)
        phi = math.asin(z/radius)
        return (radius, theta, phi)
