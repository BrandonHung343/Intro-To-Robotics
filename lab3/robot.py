#!/usr/bin/env python3

import brickpi3
import odometry as odom
import math

class Robot:
    def __init__(self):
        self.BP = brickpi3.BrickPi3()
        self.wheelbase = 4.25 # in inches
        self.radius = 1.125 # in inches too
        self.odom = odom.Odom(self.wheelbase, self.radius)
        # currently assumes that only ports B and C are used for motors
        # also assumes that the sensor is in S1
        self.portA = BP.PORT_A
        self.portB = BP.PORT_B
        self.portC = BP.PORT_C
        self.portD = BP.PORT_D
        # init sensors too
        self.sensorList = [BP.PORT_1, BP.PORT_2, BP.PORT_3, BP.PORT_4]
        self.BP.reset_motor_encoder(self.portB)
        self.BP.reset_motor_encoder(self.portC)
        self.rotL = 0
        self.rotR = 0

    def get_robot_battery(self):
        return self.BP.get_voltage_battery()

    def set_sensor(self, portNumber, sType):
        BP.set_sensor_type(portNumber, sType)

    def get_sensor(self, portNumber):
        port = self.sensorList[portNumber-1]
        return BP.get_sensor(self, port)

    def drive_robot_power(self, powerB, powerC):
        self.BP.set_motor_power(powerB)
        self.BP.set_motor_power(powerC)

    def get_enc_radians(self):
        degreeB = self.BP.get_motor_encoder(self.portB) / 2
        degreeC = self.BP.get_motor_encoder(self.portC) / 2
        radianB = math.pi / 180 * degreeB
        radianC = math.pi / 180 * degreeC
        return [radianB, radianC]

    # assumes the A is left motor and B is right motor
    def update_robot_odometry(self, dt):
        rads = self.get_enc_radians()
        deltaRads = [rads[0] - self.rotL, rads[1] - self.rotR]
        self.odom.update_odometry(rads[0], rads[1], dt)
        self.rotL = rads[0]
        self.rotR = rads[1]

    def get_robot_odometry(self):
        return [self.odom.x, self.odom.y, self.odom.theta]


        




