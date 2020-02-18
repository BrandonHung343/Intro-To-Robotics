

def create_map():
	row = 27 # outer loop, y
	col = 36 # inner loop, x

	m = []
	for i in range(row):
		m.append([])
		for j in range(col):
			m[i].append(0)


	# walls
	for i in range(row):
		for j in range(2):
			m[i][j] = -1
			m[i][col - j - 1] = -1		

	for i in range(2):
		for j in range(col):
			m[i][j] = -1
			m[row - i - 1][j] = -1

	# big block, left
	m[10][4] = -1
	m[17][4] = -1
	m[17][5] = -1
	m[12][6] = -1
	m[13][6] = -1
	m[13][7] = -1

	m[10][3] = -1
	m[10][4] = -1
	m[10][5] = -1
	m[11][6] = -1
	m[12][7] = -1
	m[13][8] = -1
	m[14][9] = -1
	m[15][10] = -1

	for i in range(16, 22):
		m[i][11] = -1

	for j in range(8, 11):
		m[20][j] = -1

	for i in range(11, 17):
		for j in range(3, 6):
			m[i][j] = -1

	for i in range(14, 19):
		for j in range(6, 9):
			m[i][j] = -1

	for i in range(15, 21):
		m[i][9] = -1
		if i == 0:
			continue
		m[i][10] = -1

	for j in range(7, 11):
		m[19][j] = -1
		if i == 0:
			continue
		m[20][j] = -1

	# small block, left
	m[11][10] = -1
	m[11][16] = -1
	m[11][9] = -1
	m[11][17] = -1
	m[10][10] = -1
	m[10][16] = -1
	m[12][10] = -1
	m[12][16] = -1
	m[13][16] = -1

	for i in range(9, 14):
		for j in range(11, 16):
			m[i][j] = -1

	m[8][13] = -1
	m[14][13] = -1
	m[8][12] = -1
	m[8][14] = -1
	m[7][13] = -1
	m[14][12] = -1
	m[14][14] = -1
	m[15][13] = -1
	for j in range(12, 15):
		m[9][j] = -1
		m[13][j] = -1

	# small block, right

	for i in range(18, 24):
		for j in range(26, 33):
			m[i][j] = -1

	m[18][25] = -1
	m[19][25] = -1
	m[17][26] = -1
	m[17][27] = -1

	# big block, right

	m[17][16] = -1
	m[18][16] = -1
	m[19][16] = -1
	m[18][15] = -1
	m[22][18] = -1
	m[22][17] = -1
	m[22][19] = -1
	m[16][16] = -1
	m[16][17] = -1
	m[15][18] = -1
	m[17][15] = -1
	m[19][15] = -1
	m[20][16] = -1
	m[15][16] = -1
	m[15][17] = -1
	m[16][15] = -1
	m[13][18] = -1
	m[12][19] = -1

	for i in range(17, 22):
		for j in range(17, 20):
			m[i][j] = -1

	m[14][19] = -1
	m[15][19] = -1
	m[16][19] = -1
	m[16][18] = -1
	m[20][20] = -1
	m[11][22] = -1
	m[11][21] = -1
	m[11][23] = -1
	m[13][19] = -1
	m[14][18] = -1

	for i in range(12, 20):
		for j in range(20, 23):
			m[i][j] = -1

	for i in range(12, 19):
		m[i][23] = -1

	m[14][25] = -1
	m[16][24] = -1

	for i in range(12, 16):
		m[i][24] = -1
		m[i][25] = -1




	print(m)

	return m

# create_map()
