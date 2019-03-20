import Board
import cv2
import time

board = Board.Board()
time.sleep(1)

while 1:
	board.update_board_status()
	board.check_start_end()
	for i in range(0, board.game_row):
		for j in range(0, board.game_col):
			if 1 <= board.board_status[i][j] <= 8:
				board.check_surrounding(i, j)