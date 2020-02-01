#!/usr/bin/env python3

import robot as rob
import time 

def main():
        robot = rob.Robot()
        powPairs = [[10, 30], [-30, 30], [-20, 10]]
        for index in range(len(powPairs)):
                powers = powPairs[index]
                startTime = time.time()
                robot.drive_robot_power(powers[0], powers[1])
                lastTime = startTime
                currTime = lastTime
                while(currTime - startTime < 3):
                        currTime = time.time()
                        robot.update_robot_odometry(currTime - lastTime)
                        print("x, y, theta", end=' ')
                        print(robot.get_robot_odometry())
                        print("Time = " + str(currTime - lastTime))
                        lastTime = currTime
                        # might cause some issues in the near future, will see
                        time.sleep(0.05)
            robot.stop()
            time.sleep(3)
        robot.stop()

if __name__ == '__main__':
        main()



