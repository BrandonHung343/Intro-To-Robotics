#!/usr/bin/env python
import math

def Odom():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.theta = 0
        # define the following at some point
        self.radius = 0
        self.wheelbase = 0

    def calculate_vl_vr(self, rot1, rot2, dt):
        vl = rot1 * self.radius / dt
        vr = rot2 * self.radius / dt
        return [vl, vr]

    def calculate_V(self, rot1, rot2, dt):
        vs = self.calculate_vl_vr(rot1, rot2, dt)
        return (vs[0] + vs[1]) / 2

    def calculate_w(self, rot1, rot2, dt):
        # vl = vs[0], vr = vs[1]
        vs = self.calculate_vl_vr(rot1, rot2, dt)
        return (v[1] - v[0]) / self.wheelbase

    def update_odometry(self, rot1, rot2, dt):
        avg_t = dt / 6
        V = self.calculate_V(rot1, rot2, dt)
        w = self.calculate_w(rot1, rot2, dt)
        # based on the runge-katta slides on the lab
        x0 = V * math.cos(self.theta)
        x1 = V * math.cos(self.theta + dt * w/2)
        x2 = V * math.cos(self.theta + dt * w/2)
        x3 = V * math.cos(self.theta + dt * w)

        y0 = V * math.sin(self.theta)
        y1 = V * math.sin(self.theta + dt * w/2)
        y2 = V * math.sin(self.theta + dt * w/2)
        y3 = V * math.sin(self.theta + dt * w)

        self.x = self.x + avg_t * (x0 + x1 + x2 + x3)
        self.y = self.y + avg_t * (y0 + y1 + y2 + y3)
        self.theta = self.theta + w
        
