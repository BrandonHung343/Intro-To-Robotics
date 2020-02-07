import sys
sys.path.append('../')
import robot as rob
import time

def startBot():
	robot = rob.Robot()
    robot.stop()
    robot.set_sensor(1, 'light') # potentiall change the port numbers later
    robot.set_sensor(2, 'light') # potentially change the port numbers later
    time.sleep(1)
    return robot

def test_sensors(robot):
	while (True):
		print('Sensor 1: ' + str(robot.get_sensor(1)))
		print('Sensor 2: ' + str(robot.get_sensor(2)))
		time.sleep(0.5)

def main():
	test_sense = False
	robot = startBot()
	Kp = 0
	Kd = 0
	Ki = 0
	lastError = 0
	first = True
	DError = 0
	IError = 0
	lastTime = 0
	if (test_sense):
		test_sensors(robot)
	while (True):
		currTime = time.time()
		sensor1 = robot.get_sensor(1)
		sensor2 = robot.get_sensor(2)
		sensorError = sensor2 - sensor1 # double check this value direction
		if (first):
			first = False
		else:
			dt = currTime - lastTime
			DError = Kd * ((sensorError - lastError) / dt)
			IError = IError + Ki * sensorError * dt
		PError = Kp * sensorError
		motorController = PError + DError + IError
		robot.drive_robot_power(motorController, motorController)
		lastTime = currTime
		lastError = sensorError
		time.sleep(0.01)


if __name__ == '__main__':
	main()