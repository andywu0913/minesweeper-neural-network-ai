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

# Unopened [189. 189. 189.]
# Opened [189. 189. 189.]
# Flagged [122.296875  118.71875   179.8515625]
# bombdeath [18.2734375  17.04296875 37.515625  ]
# 1 [218.68359375 115.4921875  103.37109375]
# 2 [ 84.9453125 148.4765625  83.1328125]
# 3 [ 98.4140625  90.7734375 224.15625  ]
# 4 [144.375     72.046875  66.296875]
# 5 [ 75.44921875  72.9921875  147.28515625]
# 6 [143.265625   143.7578125   70.84765625]
# 7 [109.99609375 109.99609375 109.99609375]
# 8 [139.90625 139.90625 139.90625]
