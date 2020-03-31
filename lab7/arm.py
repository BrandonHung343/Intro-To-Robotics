#!/usr/bin/env python3
import math
import pickle
import numpy as np
import matplotlib.pyplot as plt

class RNArm:
	# linkLengths = 1d list of the lengths of each of the links, [1, 4.5, ...]
	def __init__(self, basePoint, linkLengths):
		self.base = basePoint
		self.links = linkLengths
				# each obstacles is [[x1, x2, x3, x4], [y1, y2, y3, 4]]
		# top left, bottom left, top right, bottom right
		self.obstacleBlocks = [[[-4, -4, -2, -2], [6, 4, 6, 4]],
							   [[1, 1, 3, 3], [7, 5, 7, 5]],
							   [[-1, -1, 1, 1], [3, 2, 3, 2]],
							   [[-1, -1, 0, 0], [2, 1, 2, 1]]]


	def naiveCollisionChecker(self, loc):
		x = loc[0]
		y = loc[1]
		for item in self.obstacleBlocks:
			leftX = item[0][0]
			rightX = item[0][2]
			topY = item[1][0]
			bottomY = item[1][1]
			if (x <= rightX and x >= leftX and y <= topY and y >= bottomY):
				return False
		return True


	# configuration space collision function must be define!
	def configSpaceChecker(self, checkFn, parts):
		theta2Range = np.linspace(0, 2 * math.pi - (2 * math.pi / parts), parts)
		theta1Range = np.linspace(0, math.pi - (math.pi / parts), parts)
		# do twice
		configAngles = []
		eeLocs = []
		for t1 in theta1Range:
			for t2 in theta2Range:
				thetaList = [t1, t2]
				eeXY = self.fk(thetaList)
				eeLocs.append(eeXY)
				if (checkFn(eeXY)):
					configAngles.append(thetaList)
		return configAngles, eeLocs	


	def fk(self, thetas):
		# thetas = 1d list of command to each joint, must be same length as self.links
		# and in the same order
		runningTheta = 0
		runningX = self.base[0]
		runningY = self.base[1]
		endPoints = []
		for i in range(len(thetas)):
			runningTheta += thetas[i]
			xi = self.links[i] * math.cos(runningTheta)
			# print(runningTheta)
			# print(xi)
			yi = self.links[i] * math.sin(runningTheta)
			# print(yi)
			endPoints.append([xi, yi])
			runningX += xi
			runningY += yi
		return [runningX, runningY]	

	# saves whatever you dump into here in a pickle
	def save(self, fnname, data):
		with open (fnname + '.pickle', 'wb') as fi:
			pickle.dump(data, fi)

	def load(self, fnname, data):
		tempData = None
		with open  (fnname + '.pickle', 'rb') as fi:
			tempData = pickle.load(fi)
		return tempData

	def plotData(self, dataX, dataY):
		plt.scatter(dataX, dataY)
		plt.show()


	











