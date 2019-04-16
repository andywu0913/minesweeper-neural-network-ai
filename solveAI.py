import numpy as np
import random
import pyautogui
import tensorflow as tf
import Board
import NeuralNetwork
import cv2

board = Board.Board(resolution_scale=2)
nn = NeuralNetwork.NeuralNetwork()

nn.restoreModel()

for generation in range(0,10):
	board.update_board_status()
	if(board.determine_board_status() == 0):
		random_x, random_y = board.board_position[random.randrange(board.game_row)][random.randrange(board.game_col)]
		pyautogui.click((board.screen_start_x + random_x) / board.resolution_scale, (board.screen_start_y + random_y) / board.resolution_scale)
		board.update_board_status()
		print('Start New Game.')

	frontier = set()
	while board.determine_board_status() == 1:
		print('while')
		for row in range(0, board.game_row):
			for col in range(0, board.game_col):
				if 1 <= board.board_status[row][col] <= 8:
					for i in range(max(0, row - 1), min(board.game_row, row + 2)):
						for j in range(max(0, col - 1), min(board.game_col, col + 2)):
							if i == row and j == col:
								continue
							elif board.board_status[i, j] == 0:
								frontier.add((i, j));
		print(frontier)

		for block in frontier:
			left   = (True if block[1] == 0                    else False)
			right  = (True if block[1] == (board.game_col - 1) else False)
			top    = (True if block[0] == 0                    else False)
			bottom = (True if block[0] == (board.game_row - 1) else False)
			predict_input = [
				board.board_status[block[0] - 1][block[1] - 1] if not top    and not left  else -99,
				board.board_status[block[0] - 1][block[1]    ] if not top                  else -99,
				board.board_status[block[0] - 1][block[1] + 1] if not top    and not right else -99,
				board.board_status[block[0]    ][block[1] - 1] if not                left  else -99,
				board.board_status[block[0]    ][block[1] + 1] if not                right else -99,
				board.board_status[block[0] + 1][block[1] - 1] if not bottom and not left  else -99,
				board.board_status[block[0] + 1][block[1]    ] if not bottom               else -99,
				board.board_status[block[0] + 1][block[1] + 1] if not bottom and not right else -99
			]
			print(predict_input)
			# predict_result = nn.predict(predict_input)





# nn.saveModel()
