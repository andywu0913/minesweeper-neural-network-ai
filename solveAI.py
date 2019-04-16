import numpy as np
import random
import pyautogui
import tensorflow as tf
import Board
import NeuralNetwork
import cv2

board = Board.Board(resolution_scale=2)
nn = NeuralNetwork.NeuralNetwork()

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

