import numpy as np
import pyautogui
import Board
import random

board = Board.Board(resolution_scale=2)

def check_start_end(board, autorestart=False):
	status = board.determine_board_status()
	# Random click any block for empty board
	if status == 0:
		random_x, random_y = board.board_position[random.randrange(board.game_row)][random.randrange(board.game_col)]
		pyautogui.click((board.screen_start_x + random_x) / board.resolution_scale, (board.screen_start_y + random_y) / board.resolution_scale)
		board.update_board_status()
		print('New Game Start.')
	# Dead, restart
	elif status == 4:
		print('Lose.')
		board.click_yellow_face()
		if not autorestart:
			exit()
	## Yellow background page shows you win
	elif status == 3:
		board.close_yellow_page()
		print('Win Page.')
		if not autorestart:
			exit()
	# Every block is opened
	elif status == 2:
		board.click_yellow_face()
		print('Win.')
		if not autorestart:
			exit()
	# Cannot determine
	elif status == -99:
		exit()

def check_surrounding(board, row, col):
	bomb_num = board.board_status[row][col]
	current_surrounding = []
	for i in range(max(0, row - 1), min(board.game_row, row + 2)):
		for j in range(max(0, col - 1), min(board.game_col, col + 2)):
			if i == row and j == col:
				continue
			elif board.board_status[i, j] == -1:
				bomb_num -= 1
			elif board.board_status[i, j] == 0:
				current_surrounding.append([i, j]);
	# Detemine Bomb
	if bomb_num == len(current_surrounding):
		for i, j in current_surrounding:
			# print '(' + str(row) + ', ' + str(col) + ')' +  str([i, j])
			pyautogui.click((board.screen_start_x + board.board_position[i][j][0]) / board.resolution_scale, (board.screen_start_y + board.board_position[i][j][1]) / board.resolution_scale, button = 'right')
			board.board_status[i, j] = -1

	# Open block
	if bomb_num == 0:
		for i, j in current_surrounding:
			pyautogui.click((board.screen_start_x + board.board_position[i][j][0]) / board.resolution_scale, (board.screen_start_y + board.board_position[i][j][1]) / board.resolution_scale)
			block_status_temp = board.get_block_status(board.board_position[i][j][0], board.board_position[i][j][1])
			board.update_board_status()


for x in range(0, 100):
	while 1:
		board.update_board_status()
		check_start_end(board, autorestart=False)
		for i in range(0, board.game_row):
			for j in range(0, board.game_col):
				if 1 <= board.board_status[i][j] <= 8:
					check_surrounding(board, i, j)


