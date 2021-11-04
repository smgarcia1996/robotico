from typing import Callable
from robotics.ServoClasses import Servo
from robotics.ServoController import ServoController

class RotatingPlatform:

    def __init__(self, theta: Servo = None, phi: Servo = None, psi: Servo = None):
        self.theta = theta
        self.phi = phi
        self.psi = psi
        self.servoController = ServoController()

    def rotate(self, angle_theta: float = 0, angle_phi: float = 0, angle_psi: float = 0):
        if self.theta is not None:
            theta = self.theta.mapAngle(angle_theta)
            self.servoController.moveServo(self.theta.servo_channel, theta)
            self.theta.angle = theta
        
        if self.phi is not None:
            phi = self.phi.mapAngle(angle_phi)
            self.servoController.moveServo(self.phi.servo_channel, phi)
            self.phi.angle = phi
    
        if self.psi is not None:
            psi = self.psi.mapAngle(angle_psi)
            self.servoController.moveServo(self.psi.servo_channel, psi)
            self.psi.angle = psi
    