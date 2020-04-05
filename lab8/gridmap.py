
def scaleAndMakePoints(scaleFactor, xList, yList):
	return [[b*scaleFactor, a*scaleFactor] for a in xList for b in yList]



def create_map():
	row = 17 # outer loop, y
	col = 29 # inner loop, x

	m = []
	for i in range(row):
		m.append([])
		for j in range(col):
			m[i].append(0)

	# TODO: Implement something that finds the closest point 
	# 		to the given thingy mahbobber

	# block indexes: x = -9 to -4 inclusive, y = 7 to 12 inclusive
	# 				 x = -3 to 0 inclusive, y = 0 to 6 inclusive
	#				 x = 1 to 6 inclusive, y = 9 to 14, inclusive

	# y coord to row: abs(y coord - 15)
	xOffset = 14
	yOffset = 0

	xCoords = [i - xOffset for i in range(col)]
	yCoords = [i - yOffset	 for i in range(row)]

	b1x = list(range(6, 11))
	b1y = list(range(4, 9))


	b2x = list(range(12, 15))
	b2y = list(range(10, 15))

	b3x = list(range(14, 17))
	b3y = list(range(10, 13))

	b4x = list(range(16, 21))
	b4y = list(range(2, 7))

	scaleFactor = 1

	block1Points = scaleAndMakePoints(scaleFactor, b1x, b1y)
	block2Points = scaleAndMakePoints(scaleFactor, b2x, b2y)
	block3Points = scaleAndMakePoints(scaleFactor, b3x, b3y)
	block4Points = scaleAndMakePoints(scaleFactor, b4x, b4y)

	for points in block1Points:
		row = points[0]
		col = points[1]
		m[row][col] = -1


	for points in block2Points:
		row = points[0]
		col = points[1]
		m[row][col] = -1


	for points in block3Points:
		row = points[0]
		col = points[1]
		m[row][col] = -1


	for points in block4Points:
		row = points[0]
		col = points[1]
		m[row][col] = -1


	for row in m:
		print(row)

	return m

# create_map()
