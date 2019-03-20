import numpy as np
import pyautogui
from mss import mss
import cv2
import time
import random

resolution_scale = 2
game_row = 24	# Beginner: 8  Intermediate: 16  Expert: 16  Max: 24
game_col = 32	# Beginner: 8  Intermediate: 16  Expert: 31  Max: 32
row_height = 32
col_width = 32
screen_start_x = 42
screen_start_y = 416

gameBoard = None
board_status = np.zeros((game_row, game_col), dtype = int)
board_position = [[[0, 0] for x in range(game_col)] for y in range(game_row)]


def locate_gameBoard_coordinate():
	global screen_start_x
	global screen_start_y
	try:
		x, y = pyautogui.locateCenterOnScreen('images/board_left_top.png', grayscale=True, confidence=0.95)
		screen_start_x = x
		screen_start_y = y
		print('Left top game board coordinate = (' + str(x) + ', ' + str(y) + ')')
	except:
		print('Auto locate game board coordinate failed. Use default value.')

def make_position_table():
	global board_position
	for i in range(0, game_row):
		y = row_height / 2 + row_height * i
		for j in range(0, game_col):
			x = col_width / 2 + col_width * j
			board_position[i][j] = [x, y]

def get_block_status(x, y):
	if np.array_equal(gameBoard[y - (row_height / 8), x - (row_height / 8)], np.array([143, 143, 143])):
		return -2 # Opened Bomb
	if np.array_equal(gameBoard[y + (row_height / 8), x], np.array([42, 42, 42])):
		return -1 # Flag
	if np.array_equal(gameBoard[y- row_height / 2, x- col_width / 2], np.array([255, 255, 255])):
		return 0 # Undetermined Block
	if np.array_equal(gameBoard[y, x], np.array([251, 36, 11])):
		return 1 # 1 Blue
	if np.array_equal(gameBoard[y, x], np.array([28, 126, 25])):
		return 2 # 2 Green
	if np.array_equal(gameBoard[y, x], np.array([27, 13, 252])):
		return 3 # 3 Red
	if np.array_equal(gameBoard[y, x], np.array([121, 11, 2])):
		return 4 # 4 Dark Blue
	if np.array_equal(gameBoard[y, x], np.array([7, 3, 122])):
		return 5 # 5 Dark Red
	if np.array_equal(gameBoard[y, x], np.array([122, 123, 16])):
		return 6 # 6 Cyan
	if np.array_equal(gameBoard[y, x + col_width / 8], np.array([0, 0, 0])):
		return 7 # 7 Black
	if np.array_equal(gameBoard[y, x], np.array([123, 123, 123])):
		return 8 # 8 Gray
	if np.mean(gameBoard[y - (row_height / 8):y + (row_height / 8), x - (col_width / 8):x + (col_width / 8)]) == 189:
		return 9 # Opened Block
	else:
		return -99 # Cannot determine

def update_board_status():
	global gameBoard
	with mss() as sct:
		gameBoardImg = sct.grab({
			"top"   : screen_start_y        / 2,
			"left"  : screen_start_x        / 2,
			"width" : game_col * col_width  / 2,
			"height": game_row * row_height / 2
		})
		gameBoard = np.array(gameBoardImg)[:, :, :-1]
	for i in range(0, game_row):
		for j in range(0, game_col):
			board_status[i, j] = get_block_status(board_position[i][j][0], board_position[i][j][1])
	print(np.matrix(board_status))
	print('\n')

def check_surrounding(row, col):
	global board_status
	bomb_num = board_status[row][col]
	current_surrounding = []
	for i in range(max(0, row - 1), min(game_row, row + 2)):
		for j in range(max(0, col - 1), min(game_col, col + 2)):
			if i == row and j == col:
				continue
			elif board_status[i, j] == -1:
				bomb_num -= 1
			elif board_status[i, j] == 0:
				current_surrounding.append([i, j]);
	# Detemine Bomb
	if bomb_num == len(current_surrounding):
		for i, j in current_surrounding:
			# print '(' + str(row) + ', ' + str(col) + ')' +  str([i, j])
			pyautogui.click(screen_start_x / 2 + board_position[i][j][0] / 2, screen_start_y / 2 + board_position[i][j][1] / 2, button = 'right')
			board_status[i, j] = -1

	# Open block
	if bomb_num == 0:
		for i, j in current_surrounding:
			pyautogui.click(screen_start_x / 2 + board_position[i][j][0] / 2, screen_start_y / 2 + board_position[i][j][1] / 2)
			block_status_temp = get_block_status(board_position[i][j][0], board_position[i][j][1])
			update_board_status()

def check_start_end():
	# Starting of the game
	if np.mean(board_status) == 0:
		random_block = board_position[random.randrange(game_row)][random.randrange(game_col)]
		pyautogui.click(screen_start_x / 2 + random_block[0] / 2, screen_start_y / 2 + random_block[1] / 2)
	# A bomb shown in any block
	elif any(-2 in row for row in board_status):
		print('Lose')
		exit()
	# Yellow background page shows you win
	elif (not any(0 in row for row in board_status) or np.array_equal(gameBoard[0][0], np.array([77, 191, 253]))):
		# if :
		print('Win')
		# pyautogui.moveTo([210, 265])
		# pyautogui.click()
		# pyautogui.moveTo([85, 185])
		# pyautogui.click()
		exit()

locate_gameBoard_coordinate()
make_position_table()
np.set_printoptions(linewidth=np.inf)
pyautogui.PAUSE = 0.02
time.sleep(1)

while 1:
	update_board_status()
	check_start_end()
	for i in range(0, game_row):
		for j in range(0, game_col):
			if 1 <= board_status[i][j] <= 8:
				check_surrounding(i, j)





				# gameBoard[0:4, 0:4] = (0, 255, 0) # Left Top
				# gameBoard[0:4, col_width * game_col - 4:col_width * game_col] = (0, 255, 0) # Right Top
				# gameBoard[row_height * game_row - 4:row_height * game_row, 0:4] = (0, 255, 0) # Left Bottom
				# gameBoard[row_height * game_row - 4:row_height * game_row, col_width * game_col - 4:col_width * game_col] = (0, 255, 0) # Right Bottom
				# gameBoard[row_height * game_row / 2 - 2:row_height * game_row / 2 + 2, col_width * game_col / 2 - 2:col_width * game_col / 2 + 2] = (0, 255, 0) # Right Bottom



				# cv2.namedWindow('Game Board', cv2.WINDOW_NORMAL)
				# cv2.moveWindow('Game Board', 600, 500)
				# cv2.imshow('Game Board', gameBoard)
				# cv2.waitKey()
				# cv2.destroyAllWindows()


# pyautogui.click(70, 300)
# pyautogui.moveTo(100, 150)
# pyautogui.moveRel(0, 10)  # move mouse 10 pixels down
# pyautogui.dragTo(100, 150)
# pyautogui.dragRel(0, 10)
