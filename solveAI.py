import numpy as np
import random
import pyautogui
import tensorflow as tf
import Board
import NeuralNetwork

BLOCK_OPEN_THRESHOLD = 0.5

def add_to_frontier_set(frontier_set, row, col):
	for i in range(max(0, row - 1), min(board.game_row, row + 2)):
		for j in range(max(0, col - 1), min(board.game_col, col + 2)):
			if i == row and j == col:
				continue
			elif board.board_status[i][j] == 0:
				frontier_set.add((i, j))

def create_predict_input(row , col):
	predict_input = []
	for i in range(row - 2, row + 3):
		for j in range(col - 2, col + 3):
			if i == row and j == col:
				continue
			if i >= 0 and i < board.game_row and j >= 0 and j < board.game_col:
				predict_input.append(board.board_status[i][j])
			else:
				predict_input.append(0.5)

	# left   = (True if col == 0                    else False)
	# right  = (True if col == (board.game_col - 1) else False)
	# top    = (True if row == 0                    else False)
	# bottom = (True if row == (board.game_row - 1) else False)
	# predict_input = [
	# 	board.board_status[row - 1][col - 1] if not top    and not left  else 0.5,
	# 	board.board_status[row - 1][col    ] if not top                  else 0.5,
	# 	board.board_status[row - 1][col + 1] if not top    and not right else 0.5,
	# 	board.board_status[row    ][col - 1] if not                left  else 0.5,
	# 	board.board_status[row    ][col + 1] if not                right else 0.5,
	# 	board.board_status[row + 1][col - 1] if not bottom and not left  else 0.5,
	# 	board.board_status[row + 1][col    ] if not bottom               else 0.5,
	# 	board.board_status[row + 1][col + 1] if not bottom and not right else 0.5
	# ]
	return np.array(predict_input)

def manipulate_array(array, operation):
	array = np.insert(array, 12, 999).reshape(5, 5)
	if operation == 'R90':
		return np.delete(np.rot90(array).flatten(), 12)
	if operation == 'R180':
		return np.delete(np.rot90(array, 2).flatten(), 12)
	if operation == 'R270':
		return np.delete(np.rot90(array, 3).flatten(), 12)
	if operation == 'FUD':
		return np.delete(np.flipud(array).flatten(), 12)
	if operation == 'FLR':
		return np.delete(np.fliplr(array).flatten(), 12)
	if operation == 'T':
		return np.delete(array.transpose().flatten(), 12)
	if operation == 'SUBT':
		return np.delete(np.rot90(array, 2).transpose().flatten(), 12)
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

	opened_count = 0
	while board.determine_board_status() == 1:
		frontier = set()
		board.update_board_status()
		for row in range(0, board.game_row):
			for col in range(0, board.game_col):
				if 1 <= board.board_status[row][col] <= 8:
					add_to_frontier_set(frontier, row, col)
		print(frontier)

		for row, col in frontier:
			predict_input = create_predict_input(row, col)
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

			x, y = board.board_position[row][col]
			if predict_result >= BLOCK_OPEN_THRESHOLD: #BLOCK_OPEN_THRESHOLD
				pyautogui.click((board.screen_start_x + x) / board.resolution_scale, (board.screen_start_y + y) / board.resolution_scale)
				opened_count += 1
				board.update_board_status()
				if board.board_status[row][col] == -2:
					nn.trainingData(train_input, np.full((8, 1), 0.1))
					break
				else:
					nn.trainingData(train_input, np.full((8, 1), 1.0))
			else:
				pyautogui.click((board.screen_start_x + x) / board.resolution_scale, (board.screen_start_y + y) / board.resolution_scale, button = 'right')
				board.board_status[row][col] = -1

	nn.append_opened_counter(opened_count)
	nn.counterIncrement()

	if(board.determine_board_status() == 4):
		board.click_yellow_face()

	if generation > 0 and generation % 10 == 0:
		nn.saveModel(False)

	if generation > 0 and nn.getCounter() % 100 == 0:
		nn.saveModel(nn.getCounter())
