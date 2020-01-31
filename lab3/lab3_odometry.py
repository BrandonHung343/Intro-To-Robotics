#!/usr/bin/env python3

import robot
import time 

def main():
	robot = robot.Robot()
	powPairs = [[10, 30], [-30, 30], [-20, 10]]
	for index in range(3):
		powers = powPairs[index]
		startTime = time.time()
		robot.drive_motor_power(powers[0], powers[1])
		lastTime = startTime
		currTime = lastTime
		while(currTime - startTime < 3):
			currTime = time.time()
			robot.update_robot_odometry(currTime - lastTime)
			lastTime = currTime
			time.sleep(0.05)
	print(robot.get_odometry)


if __name__ == '__main__':
	main()



