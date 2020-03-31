# import math
# import pickle
# import numpy as np
# import matplotlib.pyplot as plt
# import arm

def main:
	myArm = arm.RNarm(basePoint=[0, 0], linkLengths=[3.75, 2.5])
	thetaData, locs = myArm.configSpaceChecker(myArm.naiveCollisionChecker, 100)
	t1Arr = []
	t2Arr = []
	for item in thetaData:
		t1Arr.append(item[0])
		t2Arr.append(item[1])

	myArm.plotData(t1Arr, t2Arr)

if __name__ == '__main__':
	main()


