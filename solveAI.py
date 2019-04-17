import numpy as np
import random
import pyautogui
import tensorflow as tf
import Board
import NeuralNetwork
import cv2

BLOCK_OPEN_THRESHOLD = 0.3

def manipulate_array(array, operation):
	array = np.insert(array, 4, 999).reshape(3, 3)
	if operation == 'R90':
		return np.delete(np.rot90(array).flatten(), 4)
	if operation == 'R180':
		return np.delete(np.rot90(array, 2).flatten(), 4)
	if operation == 'R270':
		return np.delete(np.rot90(array, 3).flatten(), 4)
	if operation == 'FUD':
		return np.delete(np.flipud(array).flatten(), 4)
	if operation == 'FLR':
		return np.delete(np.fliplr(array).flatten(), 4)
	if operation == 'T':
		return np.delete(array.transpose().flatten(), 4)
	if operation == 'SUBT':
		return np.delete(np.rot90(array, 2).transpose().flatten(), 4)
	else:
		return False

board = Board.Board(resolution_scale=2)
nn = NeuralNetwork.NeuralNetwork()

nn.restoreModel()

for generation in range(0, 10000):
	print('Current Generation: {0}.'.format(generation))
	print('Model Cumulative Generations: {0}.'.format(nn.getCounter()))
	board.update_board_status()
	if(board.determine_board_status() == 0):
		random_x, random_y = board.board_position[random.randrange(board.game_row)][random.randrange(board.game_col)]
		pyautogui.click((board.screen_start_x + random_x) / board.resolution_scale, (board.screen_start_y + random_y) / board.resolution_scale)
		board.update_board_status()
		print('Start New Game.')

	while board.determine_board_status() == 1:
		frontier = set()
		board.update_board_status()
		for row in range(0, board.game_row):
			for col in range(0, board.game_col):
				if 1 <= board.board_status[row][col] <= 8:
					for i in range(max(0, row - 1), min(board.game_row, row + 2)):
						for j in range(max(0, col - 1), min(board.game_col, col + 2)):
							if i == row and j == col:
								continue
							elif board.board_status[i][j] == 0:
								frontier.add((i, j));
		# print(frontier)

		for block in frontier:
			left   = (True if block[1] == 0                    else False)
			right  = (True if block[1] == (board.game_col - 1) else False)
			top    = (True if block[0] == 0                    else False)
			bottom = (True if block[0] == (board.game_row - 1) else False)
			predict_input = [
				board.board_status[block[0] - 1][block[1] - 1] if not top    and not left  else 0.5,
				board.board_status[block[0] - 1][block[1]    ] if not top                  else 0.5,
				board.board_status[block[0] - 1][block[1] + 1] if not top    and not right else 0.5,
				board.board_status[block[0]    ][block[1] - 1] if not                left  else 0.5,
				board.board_status[block[0]    ][block[1] + 1] if not                right else 0.5,
				board.board_status[block[0] + 1][block[1] - 1] if not bottom and not left  else 0.5,
				board.board_status[block[0] + 1][block[1]    ] if not bottom               else 0.5,
				board.board_status[block[0] + 1][block[1] + 1] if not bottom and not right else 0.5
			]

			# print(predict_input)
			predict_result = nn.predict([predict_input])
			print(predict_result)

			train_input = []
			train_input.append(predict_input)
			train_input.append(manipulate_array(predict_input, 'R90'))
			train_input.append(manipulate_array(predict_input, 'R180'))
			train_input.append(manipulate_array(predict_input, 'R270'))
			train_input.append(manipulate_array(predict_input, 'FUD'))
			train_input.append(manipulate_array(predict_input, 'FLR'))
			train_input.append(manipulate_array(predict_input, 'T'))
			train_input.append(manipulate_array(predict_input, 'SUBT'))
			# print(np.array(train_input))

			x, y = board.board_position[block[0]][block[1]]
			if predict_result >= BLOCK_OPEN_THRESHOLD: #BLOCK_OPEN_THRESHOLD
				pyautogui.click((board.screen_start_x + x) / board.resolution_scale, (board.screen_start_y + y) / board.resolution_scale)
				board.update_board_status()
				if board.board_status[block[0]][block[1]] == -2:
					nn.trainingData(train_input, np.full((8, 1), 0.1))
					break
				else:
					nn.trainingData(train_input, np.full((8, 1), 1.0))
			else:
				pyautogui.click((board.screen_start_x + x) / board.resolution_scale, (board.screen_start_y + y) / board.resolution_scale, button = 'right')
				board.board_status[block[0]][block[1]] = -1

	nn.counterIncrement()

	if(board.determine_board_status() == 4):
		board.click_yellow_face()

	if generation % 10 == 0:
		nn.saveModel(False)

	if generation % 100 == 0:
		nn.saveModel(nn.getCounter())
