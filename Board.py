import numpy as np
import pyautogui
from PIL import Image
from mss import mss

class Board():

	def __init__(self, resolution_scale=1, screen_start_x=21, screen_start_y=209, game_row=8, game_col=8):
		self.resolution_scale = resolution_scale # Mac retina display has doubled the pixels from its resolution
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
		pyautogui.PAUSE = 0.05
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

	def block_color_avg(self, x, y):
		return np.mean(
			np.mean(
				self.gameBoard[
					int(y - (self.row_height / 4)):int(y + (self.row_height / 4)),
					int(x - (self.col_width / 4)):int(x + (self.col_width / 4))
				], axis=0
			), axis=0
		)

	def get_block_status(self, x, y):
		# Unopened [189. 189. 189.]
		# Opened [189. 189. 189.]
		# Flagged [122.296875  118.71875   179.8515625]
		# bombdeath [18.2734375  17.04296875 37.515625]
		# 1 [218.68359375 115.4921875  103.37109375]
		# 2 [ 84.9453125 148.4765625  83.1328125]
		# 3 [ 98.4140625  90.7734375 224.15625  ]
		# 4 [144.375     72.046875  66.296875]
		# 5 [ 75.44921875  72.9921875  147.28515625]
		# 6 [143.265625   143.7578125   70.84765625]
		# 7 [109.99609375 109.99609375 109.99609375]
		# 8 [139.90625 139.90625 139.90625]

		color = self.block_color_avg(x, y)
		tolerance = 5
		
		if (abs(color[0] - 189) <= tolerance) and (abs(color[1] - 189) <= tolerance) and (abs(color[2] - 189) <= tolerance):
			if (abs(self.gameBoard[int(y - (self.row_height / 2)), int(x - (self.col_width / 2))][0] - 255) <= tolerance) and (abs(self.gameBoard[int(y - (self.row_height / 2)), int(x - (self.col_width / 2))][1] - 255) <= tolerance) and (abs(self.gameBoard[int(y - (self.row_height / 2)), int(x - (self.col_width / 2))][2] - 255) <= tolerance):
				return 0 # Undetermined Block
			else:
				return 9 # Opened Block
		if (abs(color[0] - 218.68359375) <= tolerance) and (abs(color[1] - 115.4921875) <= tolerance) and (abs(color[2] - 103.37109375) <= tolerance):
			return 1 # 1 Blue
		if (abs(color[0] - 84.9453125) <= tolerance) and (abs(color[1] - 148.4765625) <= tolerance) and (abs(color[2] - 83.1328125) <= tolerance):
			return 2 # 2 Green
		if (abs(color[0] - 98.4140625) <= tolerance) and (abs(color[1] - 90.7734375) <= tolerance) and (abs(color[2] - 224.15625) <= tolerance):
			return 3 # 3 Red
		if (abs(color[0] - 144.375) <= tolerance) and (abs(color[1] - 72.046875) <= tolerance) and (abs(color[2] - 66.296875) <= tolerance):
			return 4 # 4 Dark Blue
		if (abs(color[0] - 75.44921875) <= tolerance) and (abs(color[1] - 72.9921875) <= tolerance) and (abs(color[2] - 147.28515625) <= tolerance):
			return 5 # 5 Dark Red
		if (abs(color[0] - 143.265625) <= tolerance) and (abs(color[1] - 143.7578125) <= tolerance) and (abs(color[2] - 70.84765625) <= tolerance):
			return 6 # 6 Cyan
		if (abs(color[0] - 109.99609375) <= tolerance) and (abs(color[1] - 109.99609375) <= tolerance) and (abs(color[2] - 109.99609375) <= tolerance):
			return 7 # 7 Black
		if (abs(color[0] - 139.90625) <= tolerance) and (abs(color[1] - 139.90625) <= tolerance) and (abs(color[2] - 139.90625) <= tolerance):
			return 8 # 8 Gray
		if (abs(color[0] - 122.296875) <= tolerance) and (abs(color[1] - 118.71875) <= tolerance) and (abs(color[2] - 179.8515625) <= tolerance):
			return -1 # Flag
		if (abs(color[0] - 18.2734375) <= tolerance) and (abs(color[1] - 17.04296875) <= tolerance) and (abs(color[2] - 37.515625) <= tolerance):
			return -2 # Current Opened Bomb
		if (abs(color[0] - 32.125) <= tolerance) and (abs(color[1] - 32.125) <= tolerance) and (abs(color[2] - 32.125) <= tolerance):
			return -3 # Other Opened Bomb
		if (abs(color[0] - 26.8984375) <= tolerance) and (abs(color[1] - 21.37109375) <= tolerance) and (abs(color[2] - 116.578125) <= tolerance):
			return -4 # Misplaced Flag
		if (abs(color[0] - 77) <= tolerance) and (abs(color[1] - 191) <= tolerance) and (abs(color[2] - 253) <= tolerance):
			return -5 # In yellow background win page
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

	def determine_board_status(self):
		# A yellow background page shows you win
		if any(-5 in row for row in self.board_status):
			return 3
		# Cannot determine
		if any(-99 in row for row in self.board_status):
			return -99
		# Empty board, new game
		if np.amax(self.board_status) == np.amin(self.board_status) == 0:
			return 0
		# Any bombs shown in the board
		if any(-2 in row for row in self.board_status):
			return 4
		# No unopened block
		if not any(0 in row for row in self.board_status):
			return 2
		# Game ongoing
		return 1	

	def click_yellow_face(self):
		clicked = False
		if not clicked:
			try:
				img = Image.open(open('img_recognition_sample/facedead.png', 'rb'))
				img = img.resize((self.resolution_scale * x for x in img.size), Image.BILINEAR)
				tl_x, tl_y = pyautogui.locateCenterOnScreen(img, grayscale=False, confidence=0.95)
				pyautogui.click(tl_x / self.resolution_scale, tl_y / self.resolution_scale)
				clicked = True
			except Exception as e:
				pass

		if not clicked:
			try:
				img = Image.open(open('img_recognition_sample/facewin.png', 'rb'))
				img = img.resize((self.resolution_scale * x for x in img.size), Image.BILINEAR)
				tl_x, tl_y = pyautogui.locateCenterOnScreen(img, grayscale=False, confidence=0.95)
				pyautogui.click(tl_x / self.resolution_scale, tl_y / self.resolution_scale)
				clicked = True
			except Exception as e:
				pass
				
		if not clicked:
			try:
				img = Image.open(open('img_recognition_sample/facesmile.png', 'rb'))
				img = img.resize((self.resolution_scale * x for x in img.size), Image.BILINEAR)
				tl_x, tl_y = pyautogui.locateCenterOnScreen(img, grayscale=False, confidence=0.95)
				pyautogui.click(tl_x / self.resolution_scale, tl_y / self.resolution_scale)
				clicked = True
			except Exception as e:
				pass

		return clicked

	def close_yellow_page(self):
		pyautogui.press('enter')
		self.update_board_status()
		if any(-5 in row for row in self.board_status):
			return False
		else:
			return True
