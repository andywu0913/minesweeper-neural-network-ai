import numpy as np
import pyautogui
from PIL import Image
from mss import mss
import random

class Board():

	def __init__(self, resolution_scale=1, screen_start_x=21, screen_start_y=209, game_row=8, game_col=8):
		self.resolution_scale = resolution_scale # Mac retina display has doubled the resolution
		self.screen_start_x = screen_start_x * self.resolution_scale # Position in original resolution
		self.screen_start_y = screen_start_y * self.resolution_scale # Position in original resolution
		self.game_row = game_row # Beginner: 8  Intermediate: 16  Expert: 16  Max: 24
		self.game_col = game_col # Beginner: 8  Intermediate: 16  Expert: 31  Max: 32
		self.row_height = 16 * self.resolution_scale # Original picture 16px
		self.col_width  = 16 * self.resolution_scale # Original picture 16px
		self.gameBoard = None
		self.board_status = None
		self.board_position = None

		self.locate_gameBoard_coordinate()
		self.make_position_table()
		pyautogui.PAUSE = 0.02
		np.set_printoptions(linewidth=np.inf)

	def locate_gameBoard_coordinate(self):
		try:
			img = Image.open(open('img_recognition_sample/tl.png', 'rb'))
			img = img.resize((self.resolution_scale * x for x in img.size), Image.BILINEAR)
			tl_x, tl_y = pyautogui.locateCenterOnScreen(img, grayscale=True, confidence=0.95)
			img = Image.open(open('img_recognition_sample/tr.png', 'rb'))
			img = img.resize((self.resolution_scale * x for x in img.size), Image.BILINEAR)
			tr_x, tr_y = pyautogui.locateCenterOnScreen(img, grayscale=True, confidence=0.95)
			img = Image.open(open('img_recognition_sample/bl.png', 'rb'))
			img = img.resize((self.resolution_scale * x for x in img.size), Image.BILINEAR)
			bl_x, bl_y = pyautogui.locateCenterOnScreen(img, grayscale=True, confidence=0.95)
			img = Image.open(open('img_recognition_sample/br.png', 'rb'))
			img = img.resize((self.resolution_scale * x for x in img.size), Image.BILINEAR)
			br_x, br_y = pyautogui.locateCenterOnScreen(img, grayscale=True, confidence=0.95)

			self.screen_start_x = tl_x + 10 * self.resolution_scale
			self.screen_start_y = tl_y + 46 * self.resolution_scale
			self.screen_end_x = br_x - 10 * self.resolution_scale
			self.screen_end_y = br_y - 10 * self.resolution_scale
			self.game_row = int((self.screen_end_y - self.screen_start_y) / self.row_height)
			self.game_col = int((self.screen_end_x - self.screen_start_x) / self.col_width)
			self.board_status = np.zeros((self.game_row, self.game_col), dtype=int)

			print('Full Board Coordinate:')
			print("({0:4d}, {1:4d}), ({2:4d}, {3:4d})".format(tl_x, tl_y, tr_x, tr_y))
			print("({0:4d}, {1:4d}), ({2:4d}, {3:4d})".format(bl_x, bl_y, br_x, br_y))
			print("Total rows and columns: {0}x{1}.".format(self.game_row, self.game_col))
		except:
			print("Auto locate game board coordinate failed. Use default value ({0}, {1}).".format(str(self.screen_start_x), str(self.screen_start_y)))

	def make_position_table(self):
		self.board_position = [[[0, 0] for x in range(self.game_col)] for y in range(self.game_row)]
		for i in range(0, self.game_row):
			y = self.row_height / 2 + self.row_height * i
			for j in range(0, self.game_col):
				x = self.col_width / 2 + self.col_width * j
				self.board_position[i][j] = [x, y]

	def get_block_status(self, x, y):
		if np.array_equal(self.gameBoard[int(y - (self.row_height / 8)), int(x - (self.row_height / 8))], np.array([143, 143, 143])):
			return -2 # Opened Bomb
		if np.array_equal(self.gameBoard[int(y + (self.row_height / 8)), int(x)], np.array([42, 42, 42])):
			return -1 # Flag
		if np.array_equal(self.gameBoard[int(y - self.row_height / 2), int(x - self.col_width / 2)], np.array([255, 255, 255])):
			return 0 # Undetermined Block
		if np.array_equal(self.gameBoard[int(y), int(x)], np.array([251, 36, 11])):
			return 1 # 1 Blue
		if np.array_equal(self.gameBoard[int(y), int(x)], np.array([28, 126, 25])):
			return 2 # 2 Green
		if np.array_equal(self.gameBoard[int(y), int(x)], np.array([27, 13, 252])):
			return 3 # 3 Red
		if np.array_equal(self.gameBoard[int(y), int(x)], np.array([121, 11, 2])):
			return 4 # 4 Dark Blue
		if np.array_equal(self.gameBoard[int(y), int(x)], np.array([7, 3, 122])):
			return 5 # 5 Dark Red
		if np.array_equal(self.gameBoard[int(y), int(x)], np.array([122, 123, 16])):
			return 6 # 6 Cyan
		if np.array_equal(self.gameBoard[int(y), int(x + self.col_width / 8)], np.array([0, 0, 0])):
			return 7 # 7 Black
		if np.array_equal(self.gameBoard[int(y), int(x)], np.array([123, 123, 123])):
			return 8 # 8 Gray
		if np.mean(self.gameBoard[int(y - (self.row_height / 8)):int(y + (self.row_height / 8)), int(x - (self.col_width / 8)):int(x + (self.col_width / 8))]) == 189:
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
		# print(np.matrix(self.board_status))
		# print('\n')

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
				pyautogui.click((self.screen_start_x + self.board_position[i][j][0]) / self.resolution_scale, (self.screen_start_y + self.board_position[i][j][1]) / self.resolution_scale, button = 'right')
				self.board_status[i, j] = -1

		# Open block
		if bomb_num == 0:
			for i, j in current_surrounding:
				pyautogui.click((self.screen_start_x + self.board_position[i][j][0]) / self.resolution_scale, (self.screen_start_y + self.board_position[i][j][1]) / self.resolution_scale)
				block_status_temp = self.get_block_status(self.board_position[i][j][0], self.board_position[i][j][1])
				self.update_board_status()

	def check_start_end(self):
		# Starting of the game
		if np.mean(self.board_status) == 0:
			random_block = self.board_position[random.randrange(self.game_row)][random.randrange(self.game_col)]
			pyautogui.click((self.screen_start_x + random_block[0]) / self.resolution_scale, (self.screen_start_y + random_block[1]) / self.resolution_scale)
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

