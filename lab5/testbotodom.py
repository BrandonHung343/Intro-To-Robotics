import sys
sys.path.append('../')
import time
import robot as rb
# import matplotlib.pyplot as plt
import math 

def test_encoder(robot):
    while (True):
        print(robot.get_encoder_readings())
        time.sleep(0.1)

def test_odom(robot):
    nowTime = time.time()
    first = True
    while (True):
        if (first):
            first = False
        else:    
            dt = time.time() - nowTime
            robot.update_odometry(dt)
            print('Odom', robot.get_odometry())
            print('Displacement of L, R', robot.get_wheel_displacement())
        time.sleep(0.1)

def test_driven_odom(robot, powL, powR):
    nowTime = time.time()
    startTime = nowTime
    first = True
    currTime = 0
    while (True):
        currTime = time.time() 
        if (first):
            first = False

        else:    
            dt = currTime - nowTime
            robot.update_odometry(dt)
            print('Time %.3f' % (currTime - startTime))
            print('Odom', robot.get_odometry())
            print('Displacement of L, R', robot.get_wheel_displacement())
            print('Enc Readgins', robot.get_encoder_readings())

        robot.drive_robot_power(powL, powR)
        # powL = -powL
        # powR = -powR
        nowTime = currTime
        time.sleep(0.1)

def test_sequence_odom(robot, powList):
    for item in powList:
        nowTime = time.time()
        startTime = nowTime
        first = True
        currTime = nowTime
        powL = item[0]
        powR = item[1]
        while (currTime - startTime < 2):
            currTime = time.time() 
            robot.drive_robot_power(powL, powR) 
            if (first):
                first = False
            else:
                dt = currTime - nowTime
                robot.update_odometry(dt)
                print('Time %.3f' % (currTime - startTime))
                print('Odom', robot.get_odometry())
                print('Displacement of L, R', robot.get_wheel_displacement())
                print('Enc Readgins', robot.get_encoder_readings())
                nowTime = currTime
            time.sleep(0.1)
        print('\n')
    robot.stop()


def main():
        robot = rb.Robot(wheelbase=3.75, radius=1.125)
        robot.stop()
        time.sleep(1)
        test_enc = False
        test_od = False
        test_drOd = False
        test_seq = True
        dataX = []
        dataY = []
        dataTh = []
        speedList = [[-10, 10], [20, 20], [10, 30], [20, -10]]
        if (test_enc):
            test_encoder(robot)
        elif (test_od):
            test_odom(robot)
        elif (test_drOd):
            test_driven_odom(robot, 10, 10)
        elif (test_seq):
            test_sequence_odom(robot, speedList)
        plt.plot(dataX, dataY)
        plt.show()



if __name__ == '__main__':
        main()
