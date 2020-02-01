#!/usr/bin/env python3

import robot
import time 

# turns to the right in order to find the line
def find_line_right(robot):
	lightThresh = 30 # insert some threshold number, play around with it
	lightSensed = robot.get_sensor(1)
	while(lightSensed > lightThresh):
		robot.drive_robot_power(10, -10)
		time.sleep(0.05)
		lightSensed = robot.get_sensor(1)
	print('Sensed Line: ' + lightSensed)
	return lightSensed

def main():
	robot = robot.Robot()
	robot.set_sensor(1, 'light')
	baseLight = 0 # figure out the line's sensor reading by observation
	baseSpeed = [50, 50]
	lightSensor = find_line_right(robot)
	kp = 0 # figure out this value later
	kd = 0 # gotta tune this value
	# rotates to the right
	lastErr = 0
	first = True
	while(True):
		lightSensed = robot.get_sensor(1)
		err = baseLight - lightSensed
		if (first):
			first = False
			dErr = 0
		else:
			dErr = err - lastErr
		pControl = err * kp
		dControl = dErr * kd
		newPowLeft = baseSpeed[0] + (pControl + dControl)
		newPowRight = baseSpeed[1] - (pControl + dControl)
		robot.drive_robot_power(newPowLeft, newPowRight)
		lastErr = err
		time.sleep(0.05)

if __name__ == '__main__':
	main()

