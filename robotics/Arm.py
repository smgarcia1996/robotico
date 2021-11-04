from typing import Callable, List
import math
from Vector3 import Vector3
from pyquaternion import Quaternion
import logging
from robotics.ServoClasses import Joint

from auxmodule.AuxFunctions import lerp, clampAngle, between, clamp

logger = logging.getLogger('Robotics')
logger.setLevel(logging.DEBUG)





class Arm:

    def __init__(self, origin: Vector3, offset_position: Vector3, joints: List[Joint], servoCallback: Callable[[int, float], None]):
        self.joints = joints
        self.origin = origin
        self.relative_offset = offset_position
        self.relative_position = offset_position
        self.servoCallback = servoCallback


    def toAbsolutePosition(self, position):
        return self.origin + Vector3.rotate(position + self.relative_offset, self.joints[0].orientation)
    
    def toRelativePosition(self, position):
        return Vector3.rotate(position - self.origin, self.joints[0].orientation.inverse) - self.relative_offset


    def forward_kinematics(self, angles: List[int]):
        final_position = self.origin
        rotation = Quaternion(axis=[0, 0, 1], angle=0)
        for i, angle in enumerate(angles):
            joint = self.joints[i]
            rotation *= joint.orientation
            rotation *= Quaternion(axis=[0, 0, 1], angle=math.radians(angle))
            print("l", joint.length, "r", rotation)
            print("v",Vector3.rotate(joint.length, rotation)) 
            final_position += Vector3.rotate(joint.length, rotation)
        return final_position

    def reverse_kinematics(self, position: Vector3):
        logging.debug('Reverse Kinematics')
        angles = []
        
        stages = [[self.joints[0]]]
        position -= self.origin
        
        logging.debug('Start position')
        logging.debug(position)

        for joint in self.joints[1:]:
            if (joint.orientation.axis == [0, 0, 0]).all() or (joint.orientation.axis == [0, 0, 1]).all():
                stages[-1].append(joint)
            else:
                stages.append([joint])

        logging.debug('Stages')
        logging.debug(','.join([str(len(stage)) for stage in stages]))

        for stage in stages:
            joint = stage[0]
            position = Vector3.rotate(position, joint.orientation.inverse)
            if len(stage) == 1:
                logging.debug('Single stage, position ')
                logging.debug(str(position.x) + ',' +
                              str(position.y) + ',' + str(position.z))
                angle = math.atan2(position.y, position.x)
                angles.append(math.degrees(angle))
                position = Vector3.rotate(
                    position, Quaternion(angle=angle, axis=[0, 0, 1]).inverse)
                position -= joint.length
            elif len(stage) == 2:
                logging.debug('Multiple stage, position ')
                logging.debug(str(position.x) + ',' +
                              str(position.y) + ',' + str(position.z))
                alpha, beta = self.__compoundArm(
                    stage[0].length.x, stage[1].length.x, position.x, position.y)
                stage_angles = [alpha, beta]
                for i in range(2):
                    angles.append(math.degrees(stage_angles[i]))
                    position = Vector3.rotate(
                        position, Quaternion(angle=stage_angles[i], axis=[0, 0, 1]).inverse)
                    position -= stage[i].length
            else:
                raise Exception('3 jointed stages not supported')

        return angles

    def __compoundArm(self, a, b, x, y, iterations=100):
        l = abs(math.sqrt(x*x + y*y))

        if a + b - l < 0:
            raise Exception("Not reachable")

        alfa = 1
        beta = 1

        ba = -b / a
        lb = l / b
        ab = -a / b

        for i in range(1, iterations):
            beta2 = math.acos(lb + ab*math.cos(alfa))
            alfa2 = math.asin(ba * math.sin(beta2))
            alfa = lerp(alfa, alfa2, 0.8)
            beta = lerp(beta, beta2, 0.8)

        alfa = clampAngle(alfa)
        beta = clampAngle(beta)

        if alfa < 0:
            alfa = -alfa
            beta = -beta

        coordinate_angle = math.atan2(y, x)
        alfa = coordinate_angle + alfa
        beta = coordinate_angle + beta
        return alfa, beta

    def moveToPosition(self, position: Vector3, relative=False):
        if relative:
            position = self.toAbsolutePosition(position)

        angles = self.reverse_kinematics(position)
        self.moveToAngle(angles)

    def moveToAngle(self, angles: List[float]):
        for i, angle in enumerate(angles):

            limit_low, limit_high = self.joints[i].limits
            if not between(angle, limit_low, limit_high):
                logger.debug('Clamped angle ' + str(angle) + ' ' + str(limit_low) + ' ' + str(limit_high))
                angle = clamp(angle, limit_low, limit_high)

            angle = self.joints[i].mapAngle(angle)
            self.servoCallback(self.joints[i].servo_channel, angle)
            self.joints[i].angle = angle 
        self.relative_position = self.forward_kinematics(angles)
