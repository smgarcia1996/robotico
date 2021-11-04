
from typing import List, Tuple
from Vector3 import Vector3
from pyquaternion import Quaternion
from robotics.Arm import Arm, Joint
from robotics.ServoController import ServoController


class Robot:

    def __init__(self, arm_origins: List[Vector3], offset_positions: List[Vector3],
                 joints_length: List[Vector3], joints_orientation: List[Quaternion], joints_offset_angle: List[Tuple[bool, float]],
                 joints_limits: List[Tuple[float, float]], joints_servo_channels: List[int]):

        if len(arm_origins) != len(offset_positions) or \
                len(joints_length) != len(joints_orientation) or \
                len(joints_length) != len(joints_offset_angle) or \
                len(joints_length) != len(joints_limits) or \
                len(joints_length) % len(arm_origins) != 0:
            raise Exception("Invalid data size")

        self.servoController = ServoController()
        n_arms = len(arm_origins)
        joints_per_arm = len(joints_length) // len(arm_origins)
        self.arms = [
            Arm(
                arm_origins[i],
                offset_positions[i],
                [
                    Joint(
                        joints_length[i*joints_per_arm + j],
                        joints_orientation[i*joints_per_arm + j],
                        joints_offset_angle[i*joints_per_arm + j],
                        joints_limits[i*joints_per_arm + j],
                        joints_servo_channels[i*joints_per_arm + j]
                    )
                    for j in range(joints_per_arm)
                ],
                self.servoController.moveServo)
            for i in range(n_arms)
        ]

        self.elevation = 0

    def setElevation(self, z: float):
        for arm in self.arms:
            arm.moveToPosition(
                arm.actuator_position - Vector3(0, 0, z - self.elevation))

    def move(self, x: float, y: float, speed: float = 1, leg_height=20):

        for arm in self.arms:
            final_position = arm.actuator_position + Vector3(x, y, 0)
            middle_position = arm.actuator_position + \
                Vector3(x/2, y/2, leg_height)
            arm.moveToPosition(middle_position)
            arm.moveToPosition(final_position)
