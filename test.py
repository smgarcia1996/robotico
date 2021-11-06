# from peripherals.BatteryLevel import BatteryLevel
# import math
# from pyquaternion.quaternion import Quaternion
# from Vector3 import Vector3
# from robotics.RotatingPlatform import RotatingPlatform
# from robotics.ServoClasses import Servo
# from robotics.Robot import Robot
# import logging
# logging.basicConfig(level=logging.INFO)


# arm_origins = [
#     Vector3(137.1, 189.4, 0),
#     Vector3(255, 0, 0),
#     Vector3(137.1, -189.4, 0),
#     Vector3(-137.1, 189.4, 0),
#     Vector3(-255, 0, 0),
#     Vector3(-137.1, -189.4, 0)
# ]
# offset_positions = [
#     Vector3(140, 0, 0)
#     for i in range(6)
# ]
# joint_lengths = [33, 90, 110]
# joint_axis = [[0, 0, 1], [1, 0, 0], [0, 0, 1]]
# joint_angles = [0.9442, 0, -0.9442]

# joints_orientation = [
#     Quaternion(axis=joint_axis[i], angle=joint_angles[i]
#                ) * Quaternion(axis=[1, 0, 0], angle=math.pi)
#     for i in range(3)
# ] + [
#     Quaternion(axis=joint_axis[i], angle=math.pi / 2 +
#                joint_angles[i]) * Quaternion(axis=[0, 0, 1], angle=math.pi)
#     for i in range(3)
# ]

# joints_orientation = [
#     [
#         o,
#         Quaternion(axis=[1, 0, 0], angle=math.pi/2),
#         Quaternion(axis=[1, 0, 0], angle=0)
#     ] for o in joints_orientation
# ]

# joints_limits = [
#     (-90, 90),
#     (-90, 90),
#     (-90, 90)
# ]

# joints_servo_angle_transform = [
#     [(True, 90), (False, 90), (False, 0)],
#     [(True, 90), (False, 90), (False, 0)],
#     [(True, 90), (False, 90), (False, 0)],
#     [(False, 90), (True, 90), (True, 180)],
#     [(False, 90), (True, 90), (True, 180)],
#     [(False, 90), (True, 90), (True, 180)]
# ]

# joints_servo_channels = [
#     [15, 14, 13],
#     [12, 11, 10],
#     [9, 8, 31],
#     [16, 17, 18],
#     [19, 20, 21],
#     [22, 23, 27]
# ]

# r = Robot(
#     arm_origins=arm_origins,
#     offset_positions=offset_positions,
#     joints_length=[Vector3(l, 0, 0) for j in range(6) for l in joint_lengths],
#     joints_orientation=[o for a in joints_orientation for o in a],
#     joints_limits=[l for j in range(6) for l in joints_limits],
#     joints_offset_angle=[a for l in joints_servo_angle_transform for a in l],
#     joints_servo_channels=[c for s in joints_servo_channels for c in s]
# )

# f = RotatingPlatform(
#     theta=Servo(
#         (False, 101),
#         (-101, 79),
#         1
#     ),
#     phi=Servo(
#         (False, 90),
#         (-40, 90),
#         0
#     )
# )

# a = r.arms[0]
# dest = a.forward_kinematics([0, 0, 0])
# print(dest, a.origin, dest - a.origin, a.toRelativePosition(dest))

from peripherals.BatteryLevel import BatteryLevel

b = BatteryLevel()

print(b.batteryLevel)

print(b.voltage(0))
print(b.voltage(1))
