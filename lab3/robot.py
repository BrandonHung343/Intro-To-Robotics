#!/usr/bin/env python3

import brickpi3
import odometry as odom
import math

class Robot:
    def __init__(self):
        self.BP = brickpi3.BrickPi3()
        self.odom = odom.Odom()
        # currently assumes that only ports B and C are used for motors
        # also assumes that the sensor is in S1
        self.portA = BP.PORT_A
        self.portB = BP.PORT_B
        self.portC = BP.PORT_C
        self.portD = BP.PORT_D
        # init sensors too
        self.BP.reset_motor_encoder(self.portB)
        self.BP.reset_motor_encoder(self.portC)

    def drive_robot_power(self, powerB, powerC):
        self.BP.set_motor_power(powerB)
        self.BP.set_motor_power(powerC)

    def get_enc_radians(self):
        degreeB = self.BP.get_motor_encoder(self.portB)
        degreeC = self.BP.get_motor_encoder(self.portC)
        radianB = math.pi / 180 * degreeB
        radianC = math.pi / 180 * degreeC
        return [radianA, radianB]

    # assumes the A is left motor and B is right motor
    def update_robot_odometry(self):
        rads = self.get_enc_radians()
        self.odom.update_odometry(rads[0], rads[1])

    def get_robot_odometry(self):
        return [self.odom.x, self.odom.y, self.odom.theta]


        




