import numpy as np
import tensorflow as tf
import Board
import cv2

board = Board.Board(resolution_scale=2)
sess = tf.Session()


x = tf.placeholder(tf.float32, shape=(None, 8))


for x in range(0, 100):
	while 1:
		board.update_board_status()
		board.check_start_end()
		for i in range(0, board.game_row):
			for j in range(0, board.game_col):
				if 1 <= board.board_status[i][j] <= 8:
					board.check_surrounding(i, j)