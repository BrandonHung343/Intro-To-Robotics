#!/usr/bin/env python3
import sys
sys.path.append('../')
import robot as rb
import time 
import signal 

robot = rb.Robot(wheelbase=7.25, radius=1.625)


# turns to the right in order to find the line
def find_line_right(robot):
        lightThresh = 2200 # insert some threshold number, play around with it
        lightSensed = robot.get_sensor(1)
        while(lightSensed < lightThresh):
                robot.drive_robot_power(-20, 20)
                time.sleep(0.05)
                lightSensed = robot.get_sensor(1)
                # print(lightSensed)
        # print('Sensed Line: ' + str(lightSensed))
        robot.stop()
        return lightSensed

def calibrate(robot):
    while (True):
        print(robot.get_sensor(2))
        time.sleep(0.5)

def main():
        robot.stop()
        # signal.signal(signal.SIGINT, signal_handler)
        robot.set_sensor(2, 'light')
        time.sleep(1)
        baseLight = 2300 # figure out the line's sensor reading by observation
        baseSpeed = [15, 15]
        # use calibrate only if checking sensor values
        # calibrate(robot)
        # lightSensor = find_line_right(robot)
        kp = 0.1 # figure out this value later
        kd = 0.0000 # gotta tune this value
        # rotates to the right
        lastErr = 0
        first = True
        while(True):
                lightSensed = robot.get_sensor(2)
                # print(lightSensed)
                err = (lightSensed - baseLight)
                if (first):
                        first = False
                        dErr = 0
                else:
                        dErr = lastErr - err
                pControl = err * kp
                dControl = dErr * kd
                newPowLeft = baseSpeed[0] + (pControl + dControl)
                newPowRight = baseSpeed[1] - (pControl + dControl)
                robot.drive_robot_power(newPowLeft, newPowRight)
                lastErr = err
                time.sleep(0.05)

if __name__ == '__main__':
        main()

