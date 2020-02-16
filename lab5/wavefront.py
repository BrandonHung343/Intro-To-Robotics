import numpy as np
import transforms as tf
import math
import copy

def get_8_neighbors(grid, x, y):
	ylen = len(grid)
	xlen = len(grid[0])
	neighbors = []
	if (x >= xlen or y >= ylen):
		return []
	if (x > 0):
		if (y > 0):
			neighbors.append([x-1, y-1])
		if (y < ylen - 1):
			neighbors.append([x-1, y+1])
		neighbors.append([x-1, y])

	if (x < xlen - 1):
		if (y > 0):
			neighbors.append([x+1, y-1])
		if (y < ylen - 1):
			neighbors.append([x+1, y+1])
		neighbors.append([x+1, y])

	if (y > 0):
		neighbors.append([x, y-1])
	if (y < ylen - 1):
		neighbors.append([x, y+1])

	return neighbors

def get_4_neighbors(grid, x, y):
	ylen = len(grid)
	xlen = len(grid[0])
	neighbors = []

	if (x >= xlen or y >= ylen):
		return []
	if (y > 0):
		neighbors.append([x, y-1])
	if (x < xlen - 1):
		neighbors.append([x+1, y])
	if (y < ylen - 1):
		neighbors.append([x, y+1])
	if (x > 0):
		neighbors.append([x-1, y])
	
	return neighbors


def wave4(grid, x, y):
	queue = []
	queue.append([x, y])
	count = 1
	grid[y][x] = count
	while (len(queue) > 0):
		node = queue.pop(0)
		# print(node)
		# print(queue)
		# print(grid)
		xInd = node[0]
		yInd = node[1]
		neighbors = get_4_neighbors(grid, xInd, yInd)
		# print(neighbors)
		for neighbor in neighbors:
			xN = neighbor[0]
			yN = neighbor[1]
			# print(neighbor)
			if (grid[yN][xN] == 0):
				# print('yeet')
				# print(neighbor)
				queue.append(neighbor)
				grid[yN][xN] = grid[yInd][xInd] + 1
				# print(grid)
	return grid

def wave8(grid, x, y):
	queue = []
	queue.append([x, y])
	count = 1
	grid[y][x] = count
	while (len(queue) > 0):
		node = queue.pop(0)
		# print(node)
		# print(queue)
		# print(grid)
		xInd = node[0]
		yInd = node[1]
		neighbors = get_8_neighbors(grid, xInd, yInd)
		# print(neighbors)
		for neighbor in neighbors:
			xN = neighbor[0]
			yN = neighbor[1]
			# print(neighbor)
			if (grid[yN][xN] == 0):
				# print('yeet')
				# print(neighbor)
				queue.append(neighbor)
				grid[yN][xN] = grid[yInd][xInd] + 1
				# print(grid)
	return grid

def make_random_grid(xsize, ysize, obs_prob):
	grid = np.random.choice(np.arange(-1, 1), size=(ysize, xsize), p=[obs_prob, 1-obs_prob])
	return grid


def pretty_print(grid):
	with open('grid.txt', 'w') as fi:
		# f_string = '%s ' * (len(grid))

		for row in grid:
			joinrows = ' '.join(str(x).rjust(3) for x in row)
			# writeString = joinrows.rjust(12)
			fi.write(joinrows) #writeString)
			fi.write('\n')


def test_grid(four):
	xsize = 5
	ysize = 5
	startx = 3
	starty = 1
	obs_prob = 0.3
	grid = make_random_grid(xsize, ysize, obs_prob)
	if (not four):
		wvgrid = wave8(grid, startx, starty)
	else:
		wvgrid = wave4(grid, startx, starty)
	pretty_print(wvgrid)
	return wvgrid


def find_path_4_recurse(grid, startx, starty, path, last_count):
	squareOne = grid[starty][startx]
	if (squareOne <= 0 or squareOne >= last_count):
		return None
	elif (squareOne == 1):
		return 1
	else:
		neighbors = get_4_neighbors(grid, startx, starty)
		for neighbor in neighbors:
			# print('ss', startx, starty)
			# print(neighbor)
			sol = find_path_4_recurse(grid, neighbor[0], neighbor[1], path, squareOne)
			# print(sol)
			if (sol is not None):
				path.append(neighbor)
				return path
		return None

def find_path_8_recurse(grid, startx, starty, path, last_count):
	squareOne = grid[starty][startx]
	if (squareOne <= 0 or squareOne >= last_count):
		return None
	elif (squareOne == 1):
		return 1
	else:
		neighbors = get_8_neighbors(grid, startx, starty)
		for neighbor in neighbors:
			# print('ss', startx, starty)
			# print(neighbor)
			sol = find_path_8_recurse(grid, neighbor[0], neighbor[1], path, squareOne)
			# print(sol)
			if (sol is not None):
				path.append(neighbor)
				return path
		return None


def find_path(grid, startx, starty, four=False):
	if grid[starty][startx] <= 0:
		return None
	if four:
		path = find_path_4_recurse(grid, startx, starty, [], grid[starty][startx] + 1)
	else:
		path = find_path_8_recurse(grid, startx, starty, [], grid[starty][startx] + 1)
	path.append([startx, starty])
	path.reverse()
	return path

def path_relative_to_start(path, xi, yi, thi):
	# assumes transforms are a rotation, then a translation
	first = True
	lastTh = thi
	pathRobotFrame = []
	tempPath = copy.deepcopy(path)
	
	for j in range(len(tempPath) - 1):
		item = tempPath[j]
		nextItem = tempPath[j + 1]
		xj = item[0]
		yj = item[1]	
		xk = nextItem[0]
		yk = nextItem[1]
		

		transTgr = tf.invert_transform(tf.get_transform(xj, yj, 0))
		transTpg = tf.get_transform(xk, yk, 0)
		transTpr = tf.chain_transforms(transTgr, transTpg)
		transPpr = tf.get_pose_vec(transTpr)

		finTh = math.atan2(yk - yj, xk - xj)
		rotTgr = tf.invert_transform(tf.get_transform(0, 0, finTh))
		rotTpg = tf.get_transform(0, 0, lastTh)
		rotTpr = tf.chain_transforms(rotTgr, rotTpg)
		rotPpr = tf.get_pose_vec(rotTpr)

		
		pathRobotFrame.append(transPpr)
		pathRobotFrame.append(rotPpr)
		lastTh = finTh
	tempPath.insert(0, [xi, yi, thi])
	return pathRobotFrame











