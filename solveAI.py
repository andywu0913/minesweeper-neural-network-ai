import operator
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
	return np.array(predict_input)

board = Board.Board(resolution_scale=2)
nn = NeuralNetwork.NeuralNetwork()

nn.restoreModel()

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

	tmp = {}

	for row, col in frontier:
		predict_input = create_predict_input(row, col)
		predict_result = nn.predict([predict_input])
		tmp.update({(row, col): predict_result})

	max_index = max(tmp.items(), key=operator.itemgetter(1))[0]
	max_value = tmp.get(max_index)
	min_index = min(tmp.items(), key=operator.itemgetter(1))[0]
	min_value = tmp.get(min_index)


	if abs(max_value - 0.5) > abs(min_value - 0.7):
		tmp.pop(max_index)
		x, y = board.board_position[max_index[0]][max_index[1]]
		pyautogui.click((board.screen_start_x + x) / board.resolution_scale, (board.screen_start_y + y) / board.resolution_scale)
		print('({0}, {1}) \t Confidence: {2} \t Action: Open'.format(max_index[0], max_index[1], max_value))
		board.update_board_status()
		# if board.board_status[max_index[0]][max_index[1]] == -2:
			# print(tmp)
			# print(max_value)
			# print(min_value)
	else:
		tmp.pop(min_index)
		x, y = board.board_position[min_index[0]][min_index[1]]
		pyautogui.click((board.screen_start_x + x) / board.resolution_scale, (board.screen_start_y + y) / board.resolution_scale, button = 'right')
		print('({0}, {1}) \t Confidence: {2} \t Action: Flag'.format(max_index[0], max_index[1], min_value))
		board.board_status[min_index[0]][min_index[1]] = -1
	

