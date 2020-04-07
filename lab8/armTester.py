import math
import pickle
import numpy as np
import matplotlib.pyplot as plt
import arm as armLib

def fk_tester():
	myArm = armLib.RNArm(basePoint=[0, 0], linkLengths=[3.75, 2.5])
	while (True):
		t1 = input('Theta 1: ')
		t2 = input('Theta 2: ')
		print(myArm.fk([float(t1), float(t2)]))


if __name__ == '__main__':
	fk_tester()