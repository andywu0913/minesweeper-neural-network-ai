import numpy as np
import pyautogui
from mss import mss
import random

class Board():

	def __init__(self):
		self.resolution_scale = 2
		self.game_row = 24	# Beginner: 8  Intermediate: 16  Expert: 16  Max: 24
		self.game_col = 32	# Beginner: 8  Intermediate: 16  Expert: 31  Max: 32
		self.row_height = 16 * self.resolution_scale
		self.col_width  = 16 * self.resolution_scale
		self.screen_start_x = 42
		self.screen_start_y = 418

		self.gameBoard = None
		self.board_status = np.zeros((self.game_row, self.game_col), dtype=int)
		self.board_position = [[[0, 0] for x in range(self.game_col)] for y in range(self.game_row)]

		np.set_printoptions(linewidth=np.inf)
		pyautogui.PAUSE = 0.02
		self.locate_gameBoard_coordinate()
		self.make_position_table()
		
	def locate_gameBoard_coordinate(self):
		try:
			x, y = pyautogui.locateCenterOnScreen('images/board_left_top.png', grayscale=True, confidence=0.95)
			self.screen_start_x = x
			self.screen_start_y = y
			print('Left top game board coordinate = (' + str(x) + ', ' + str(y) + ')')
		except:
			print('Auto locate game board coordinate failed. Use default value (' + str(self.screen_start_x) + ', ' + str(self.screen_start_y) + ').')

	def make_position_table(self):
		for i in range(0, self.game_row):
			y = self.row_height / 2 + self.row_height * i
			for j in range(0, self.game_col):
				x = self.col_width / 2 + self.col_width * j
				self.board_position[i][j] = [x, y]

	def get_block_status(self, x, y):
		if np.array_equal(self.gameBoard[y - (self.row_height / 8), x - (self.row_height / 8)], np.array([143, 143, 143])):
			return -2 # Opened Bomb
		if np.array_equal(self.gameBoard[y + (self.row_height / 8), x], np.array([42, 42, 42])):
			return -1 # Flag
		if np.array_equal(self.gameBoard[y- self.row_height / 2, x- self.col_width / 2], np.array([255, 255, 255])):
			return 0 # Undetermined Block
		if np.array_equal(self.gameBoard[y, x], np.array([251, 36, 11])):
			return 1 # 1 Blue
		if np.array_equal(self.gameBoard[y, x], np.array([28, 126, 25])):
			return 2 # 2 Green
		if np.array_equal(self.gameBoard[y, x], np.array([27, 13, 252])):
			return 3 # 3 Red
		if np.array_equal(self.gameBoard[y, x], np.array([121, 11, 2])):
			return 4 # 4 Dark Blue
		if np.array_equal(self.gameBoard[y, x], np.array([7, 3, 122])):
			return 5 # 5 Dark Red
		if np.array_equal(self.gameBoard[y, x], np.array([122, 123, 16])):
			return 6 # 6 Cyan
		if np.array_equal(self.gameBoard[y, x + self.col_width / 8], np.array([0, 0, 0])):
			return 7 # 7 Black
		if np.array_equal(self.gameBoard[y, x], np.array([123, 123, 123])):
			return 8 # 8 Gray
		if np.mean(self.gameBoard[y - (self.row_height / 8):y + (self.row_height / 8), x - (self.col_width / 8):x + (self.col_width / 8)]) == 189:
			return 9 # Opened Block
		else:
			return -99 # Cannot determine

	def update_board_status(self):
		with mss() as sct:
			gameBoardImg = sct.grab({
				"top"   : self.screen_start_y             / self.resolution_scale,
				"left"  : self.screen_start_x             / self.resolution_scale,
				"width" : self.game_col * self.col_width  / self.resolution_scale,
				"height": self.game_row * self.row_height / self.resolution_scale
			})
			self.gameBoard = np.array(gameBoardImg)[:, :, :-1]
		for i in range(0, self.game_row):
			for j in range(0, self.game_col):
				self.board_status[i, j] = self.get_block_status(self.board_position[i][j][0], self.board_position[i][j][1])
		print(np.matrix(self.board_status))
		print('\n')

	def check_surrounding(self, row, col):
		bomb_num = self.board_status[row][col]
		current_surrounding = []
		for i in range(max(0, row - 1), min(self.game_row, row + 2)):
			for j in range(max(0, col - 1), min(self.game_col, col + 2)):
				if i == row and j == col:
					continue
				elif self.board_status[i, j] == -1:
					bomb_num -= 1
				elif self.board_status[i, j] == 0:
					current_surrounding.append([i, j]);
		# Detemine Bomb
		if bomb_num == len(current_surrounding):
			for i, j in current_surrounding:
				# print '(' + str(row) + ', ' + str(col) + ')' +  str([i, j])
				pyautogui.click(self.screen_start_x / 2 + self.board_position[i][j][0] / 2, self.screen_start_y / 2 + self.board_position[i][j][1] / 2, button = 'right')
				self.board_status[i, j] = -1

		# Open block
		if bomb_num == 0:
			for i, j in current_surrounding:
				pyautogui.click(self.screen_start_x / 2 + self.board_position[i][j][0] / 2, self.screen_start_y / 2 + self.board_position[i][j][1] / 2)
				block_status_temp = self.get_block_status(self.board_position[i][j][0], self.board_position[i][j][1])
				self.update_board_status()

	def check_start_end(self):
		# Starting of the game
		if np.mean(self.board_status) == 0:
			random_block = self.board_position[random.randrange(self.game_row)][random.randrange(self.game_col)]
			pyautogui.click(self.screen_start_x / 2 + random_block[0] / 2, self.screen_start_y / 2 + random_block[1] / 2)
		# A bomb shown in any block
		elif any(-2 in row for row in self.board_status):
			print('Lose')
			exit()
		# Yellow background page shows you win
		elif (not any(0 in row for row in self.board_status) or np.array_equal(self.gameBoard[0][0], np.array([77, 191, 253]))):
			# if :
			print('Win')
			# pyautogui.moveTo([210, 265])
			# pyautogui.click()
			# pyautogui.moveTo([85, 185])
			# pyautogui.click()
			exit()

