import time
from armNew import AcrobotEnv
import sys
import math
import copy
import numpy as np
import wavefront as wv
import arm as armLib 
import gridmap as gd
import matplotlib.pyplot as plt

def splitData(paired):
	arr1 = []
	arr2 = []
	for item in paired:
		arr1.append(item[0])
		arr2.append(item[1])
	return arr1, arr2

def makeConfigSpace():
	myArm = armLib.RNArm(basePoint=[0, 0], linkLengths=[3.75, 2.5])
	thetaData, locs = myArm.configSpaceChecker(myArm.naiveCollisionChecker, 300)
	t1Arr, t2Arr = splitData(thetaData)
	return thetaData, t1Arr, t2Arr

# do this for all 3 paths
def indicesToInches(path):
	inchPath = []
	for entry in path:
		col = entry[1]
		row = entry[0]
		y = 8 - col / 2 
		x = (row - 14) / 2
		inchPath.append([x, y])
	print("Inchpath:")
	print(inchPath)
	return inchPath

# do this for all 3 paths
# inchapth is always 2 points longs
def generateNSteps(inchPath, numSteps):
	pi = inchPath[0]
	pnext = inchPath[1]
	linearPoints = np.linspace(pi, pnext, numSteps)
	return linearPoints

def pointsToAngles(path): #, numSteps):
	myArm = armLib.RNArm(basePoint=[0, 0], linkLengths=[3.75, 2.5])
	inchesPath = indicesToInches(path)
	# discretizedPath = generateNSteps(inchesPath, numSteps)
	listofAngles = myArm.ik2link(inchesPath)
	return listofAngles

def sanityCheckPoints(thetaList):
	myArm = armLib.RNArm(basePoint=[0, 0], linkLengths=[3.75, 2.5])
	print('Sanity Check: ', end='')
	for angPair in thetaList:
		t1 = angPair[0]
		t2 = angPair[1]
		print(myArm.fk([t1, t2]), end=', ')

if __name__ == '__main__':

    arm = AcrobotEnv() # set up an instance of the arm class
    numSteps = 1
    myArm = armLib.RNArm(basePoint=[0, 0], linkLengths=[3.75, 2.5])
    
    Kp1 = 0.065 # was 0.10
    Ki1 = 0
    Kd1 = 0.17 # 0.0135
    Kp2 = 0.0065
    Ki2 = 0
    Kd2 = 0.005 # 0.055

    timeStep = 0.02 # sec
    timeForEachMove = 0.16 # sec
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
    path2 = combPath2[0]
    startBx = combPath2[1]
    startBy = combPath2[2]

    combPath3 = wv.full_path_8point(startBx, startBy, Cx, Cy, 'path3', convertInput=True)
    path3 = combPath3[0]

    # change the paths to IK angles and replace the first with theta, theta
    angles1 = pointsToAngles(path1)
    nAngles1 = [[ang[0], ang[1] + 2 * math.pi] if ang[1] < 0 else ang for ang in angles1]
    print(angles1)
    sanityCheckPoints(angles1)
    angles2 = pointsToAngles(path2)
    nAngles2 = [[ang[0], ang[1] + 2 * math.pi] if ang[1] < 0 else ang for ang in angles2]
    print(angles2)
    sanityCheckPoints(angles2)
    angles3 = pointsToAngles(path3)
    nAngles3 = [[ang[0], ang[1] + 2 * math.pi] if ang[1] < 0 else ang for ang in angles3]
    print(angles3)
    sanityCheckPoints(angles3)

    # Plot the paths
    plt.scatter(t1s, t2s, c='b')
    At1, At2 = splitData(nAngles1)
    plt.plot(At1, At2, c='r')
    Bt1, Bt2 = splitData(nAngles2)
    plt.plot(Bt1, Bt2, c='g')
    Ct1, Ct2 = splitData(nAngles3)
    plt.plot(Ct1, Ct2, c='y')
    plt.show()

    allPoints = angles1 + angles2 + angles3
    wp1 = len(angles1)
    wp2 = len(angles2)
    wp3 = len(angles3)

    numberOfWaypoints = len(allPoints) # Change this based on your path
    
    arm.reset() # start simulation

    m1 = 0.000365
    m2 = 0.00000158850
    g  = 9.8

    lastAction1 = 0
    lastAction2 = 0
    D2cap = 0.0016
    D1cap = 0.3

    print('\nAllpoints: ', allPoints)
    # quit()

    
    for waypoint in range(numberOfWaypoints - 1):
        
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

		# Get current waypoint
        pNow = allPoints[waypoint]

        if (waypoint < numberOfWaypoints):
        	pNext = allPoints[waypoint + 1]
        else:
        	pNext = pNow

        discretePath = generateNSteps([pNow, pNext], stepsForEachMove)
        print("Dpath:", discretePath)
        sanityCheckPoints(discretePath)
        index = 0
        first = True

        for timeStep in range(stepsForEachMove):
        	idealThetas = discretePath[index]
        	print()
        	print(idealThetas)
        	idealT1 = idealThetas[0]
        	idealT2 = idealThetas[1]
        	print('Should be at x=%.3f, y=%.3f' % tuple(myArm.fk([idealT1, idealT2])))

        	currT1 = arm.state[0]
        	currT2 = arm.state[1] + currT1

        	print("currT1 = %.5f, currT2 = %.5f" % (currT1, currT2))

        	# figure out the timestep stuff
        	tic = time.perf_counter()
        	if (not first):
        		lastP1error = P1error
	        	lastP2error = P2error
	        	
        		P1error = idealT1 - currT1
        		P2error = idealT2 - arm.state[1]
        			
	        	
	        	D1error = P1error - lastP1error
	        	D2error = P2error - lastP2error
	        	if (D1error	> D1cap or D1error	< -D1cap):
        			D1error	= np.sign(D1error) * D1cap	
	        	
        		if (D2error	> D2cap or D2error	< -D2cap):
        			D2error	= np.sign(D2error) * D2cap
	        	I1error += P1error
	        	I2error += P2error
	        	FF1 = m1 * g * np.cos(currT1)
	        	FF2 = m2 * g * np.cos(currT2)

		        # Calculate them
		        # Control arm to reach this waypoint
	        	actionHere1 = FF1 + Kp1 * P1error + Kd1 * D1error + Ki1 * I1error # N torque # Change this based on your controller
	        	actionHere2 =  FF2 + Kp2 * P2error + Kd2 * D2error + Ki2 * I2error # N torque 
	        else:
	        	first = False
	        	actionHere1 = lastAction1
	        	actionHere2 = lastAction2
	        	print('First')

 			# save stuff before we step
	    
        	# if (lastT1 > math.pi/2):
        	FF1 = m1 * g * np.cos(currT1)
        	FF2 = m2 * g * np.cos(currT2)

	        # Calculate them
	        # Control arm to reach this waypoint
        	actionHere1 = FF1 + Kp1 * P1error + Kd1 * D1error + Ki1 * I1error # N torque # Change this based on your controller
        	actionHere2 =  FF2 + Kp2 * P2error + Kd2 * D2error + Ki2 * I2error # N torque # Change this based on your controller
	        # testing
	        # actionHere1 = 0.003
	        # actionHere2 = 0.000085
        	

	        # save stuff before we step
        	
        	# print(lastT1)


        	lastW1 = arm.state[2]
        	lastW2 = arm.state[3]

        	

        	state, reward, terminal , __ = arm.step(actionHere1, actionHere2)
        	arm.render() # Update rendering
        	index += 1
        	print("P1error = %.3f, P2error = %.3f, D1error = %.3f, D2error = %.3f" % (P1error, P2error, D1error, D2error))
        	print("KP1 = %.6f, kP2 = %.6f, kD1 = %.6f, kD2 = %.6f" % (Kp1 * P1error, Kp2 * P2error, Kd1 * D1error, Kd2 * D2error))
        	print("A1 = %.5f, A2 = %.5f" % (actionHere1, actionHere2))

        	
        	# input('Next')
        	lastAction1 = actionHere1
        	lastAction2 = actionHere2
        	time.sleep(0.02)

        if (waypoint == wp1 -1 or waypoint == wp1 + wp2 - 1 or waypoint == wp1 + wp2 + wp3 - 2):
        	print('Pnow:', pNow)
        	print("EE loc on display step:", myArm.fk([arm.state[0], arm.state[1]]))
        	input('Next Place')
    print("Done")
    input("Press Enter to close...")
    arm.close()
