import time
from armNew import AcrobotEnv
import sys
import math
import copy
import numpy as np
import wavefront as wv
import arm 

def splitData(paired):
	arr1 = []
	arr2 = []
	for item in paired:
		arr1.append(item[0])
		arr2.append(item[1])
	return arr1, arr2

def makeConfigSpace()
	myArm = arm.RNArm(basePoint=[0, 0], linkLengths=[3.75, 2.5])
	thetaData, locs = myArm.configSpaceChecker(myArm.naiveCollisionChecker, 300)
	t1Arr, t2Arr = splitData(thetaData)
	return thetaData, t1Arr, t2Arr

# do this for all 3 paths
def indicesToInches(path):
	inchPath = []
	for entry in path:
		col = path[1]
		row = path[0]
		x = col / 2 - 7 
        y = (16 - row) / 2;
        inchPath.append([x, y])
    return inchPath

# do this for all 3 paths
def generateNSteps(inchPath, numSteps):
	discretizedList = []
	for i in range(len(inchPath) - 1):
		pi = inchPath[i]
		pnext = inchPath[i+1]
		linearPoints = np.linspace(pi, pnext, n)
		discretizedList.append(linearPoints)
	return discretizedList

def pointsToAngles(path, numSteps):
	myArm = arm.RNArm(basePoint=[0, 0], linkLengths=[3.75, 2.5])
	inchesPath = indicesToInches(path)
	# discretizedPath = generateNSteps(inchesPath, numSteps)
	listofAngles = myArm.ik2link(inchesPath)
	return listofAngles

if __name__ == '__main__':

    arm = AcrobotEnv() # set up an instance of the arm class
    numSteps = 1
    
    Kp1 = 0
    Ki1 = 0
    Kd1 = 0
    Kp2 = 0
    Ki2 = 0
    Kd2 = 0

    timeStep = 0.02 # sec
    timeForEachMove = 0.2 # sec
    stepsForEachMove = round(timeForEachMove/timeStep)

    # Make configuration space
    # Insert you code or calls to functions here
    configAngles, t1s, t2s = makeConfigSpace()

    # Get three waypoints from the user
    Ax = int(input("Type Ax: "))
    Ay = int(input("Type Ay: "))
    Bx = int(input("Type Bx: "))
    By = int(input("Type By: "))
    Cx = int(input("Type Cx: "))
    Cy = int(input("Type Cy: "))

    arm.Ax = Ax*0.0254; # Simulaiton is in SI units
    arm.Ay = Ay*0.0254; # Simulaiton is in SI units
    arm.Bx = Bx*0.0254; # Simulaiton is in SI units
    arm.By = By*0.0254; # Simulaiton is in SI units
    arm.Cx = Cx*0.0254; # Simulaiton is in SI units
    arm.Cy = Cy*0.0254; # Simulaiton is in SI units

    startPointX = 27
    startPointY = 16 

    # Plan a path
    # Insert your code or calls to functions here
    combPath1 = wv.full_path_8point(startPointX, startPointY, Ax, Ay, 'path1', convertInput=True)
    path1 = combPath1[0]
    startAx = combPath1[1]
    startAy = combPath1[2]

    combPath2 = wv.full_path_8point(startAx, startAy, Bx, By, 'path2', convertInput=True)
    path2 = combPath1[0]
    startBx = combPath1[1]
    startBy = combPath1[2]

    combPath3 = wv.full_path_8point(startBx, startBy, Cx, Cy, 'path3', convertInput=True)
    path3 = combPath1[0]

    # change the paths to IK angles and replace the first with theta, theta
    angles1 = pointsToAngles(path1)
    angles2 = pointsToAngles(path2)
    angles3 = pointsToAngles(path3)

    # Plot the paths
    plt.scatter(t1s, t2s, c='b')
    At1, At2 = splitData(angles1)
    plt.scatter(At1, At2, c='r')
    Bt1, Bt2 = splitData(angles2)
    plt.scatter(Bt1, Bt2, c='r')
    Ct1, Ct2 = splitData(angles3)
    plt.scatter(Ct1, Ct2, c='r')
    plt.show()

    allPoints = angles1 + angles2 + angles3

    numberOfWaypoints = len(allPoints) # Change this based on your path
    
    arm.reset() # start simulation
    
    for waypoint in range(numberOfWaypoints):

        # Get current waypoint

        P1error = 0
        I1error = 0
        D1error = 0
        P2error = 0
        I2error = 0
        D2error = 0
        FF1 = 0
        FF2 = 0

        lastT1 = 0
        lastT2 = 0
        lastW1 = 0
        lastW2 = 0

        pNow = allPoints[waypoint]

        if (waypoint < numberOfWaypoints):
        	pNext = allPoints[waypoint + 1]
        else:
        	pNext = pNow

        discretePath = generateNSteps([pNow, pNext], stepsForEachMove)
        index = 0
        first = True

        for moveStep in range(stepsForEachMove):
        	idealThetas = discretePath[index]
        	idealT1 = idealThetas[0]
        	idealT2 = idealThetas[1]

        	# figure out the timestep stuff
            tic = time.perf_counter()
            if (not first):
            	lastP1error = P1error
            	lastP2error = P2error
            	P1error = idealT1 - lastT1
            	P2error = idealT2 - lastT2
            	D1error = P1error - lastP1error
            	D2error = P2error - lastP2error
            	I1error += P1error
            	I2error += P2error
            else:
            	first = False

            # Calculate them
            # Control arm to reach this waypoint
            actionHere1 = FF1 + Kp1 * P1error + Kd1 * D1error + Ki1 * I1error # N torque # Change this based on your controller
            actionHere2 =  FF2 + Kp2 * P2error + Kd2 * D2error + Ki2 * I2error # N torque # Change this based on your controller
            
            arm.render() # Update rendering

            # save stuff before we step
            lastT1 = arm.state[0]
            lastT2 = arm.state[1]
            lastW1 = arm.state[2]
            lastW2 = arm.state[3]

            state, reward, terminal , __ = arm.step(actionHere1, actionHere2)
            index += 1
        
    print("Done")
    input("Press Enter to close...")
    arm.close()
