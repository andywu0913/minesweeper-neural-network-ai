import numpy as np
import tensorflow as tf


class NeuralNetwork():

	def __init__(self):
		self.sess = tf.Session()
		self.x_data = tf.placeholder(shape = [None, 9], dtype = tf.float32)
		self.y_target = tf.placeholder(shape = [None, 1], dtype = tf.float32)

		# set up neural network
		# A1 ---> 1st layer weights		9x81
		# b1 ---> 1st layer bias		1x81
		# A2 ---> 2nd layer weights		81x81
		# b2 ---> 2nd layer bias		1x81
		# A3 ---> output layer weights	81x1
		# b3 ---> output layer bias		1x1
		self.hidden_layer_nodes = 81

		self.A1 = tf.Variable(tf.random_normal(shape = [9, self.hidden_layer_nodes]))
		self.b1 = tf.Variable(tf.random_normal(shape = [self.hidden_layer_nodes]))
		self.A2 = tf.Variable(tf.random_normal(shape = [self.hidden_layer_nodes, self.hidden_layer_nodes]))
		self.b2 = tf.Variable(tf.random_normal(shape = [self.hidden_layer_nodes]))
		self.A3 = tf.Variable(tf.random_normal(shape = [self.hidden_layer_nodes, 1]))
		self.b3 = tf.Variable(tf.random_normal(shape = [1]))

		self.hidden_output1 = tf.nn.relu(tf.add(tf.matmul(self.x_data, self.A1), self.b1))
		self.hidden_output2 = tf.nn.relu(tf.add(tf.matmul(self.hidden_output1, self.A2), self.b2))
		self.final_output = tf.nn.relu(tf.add(tf.matmul(self.hidden_output2, self.A3), self.b3))

		self.loss = tf.reduce_mean(tf.square(self.y_target - self.final_output))
		self.my_opt = tf.train.GradientDescentOptimizer(0.005)
		self.train_step = self.my_opt.minimize(self.loss)
		self.init = tf.global_variables_initializer()
		self.sess.run(self.init)


	def trainingData(self, observed_x, observed_y):
		return self.sess.run(self.train_step, feed_dict = {self.x_data: observed_x, self.y_target: observed_y})
			

	def predict(self, observed_x):
		return self.sess.run(self.final_output, feed_dict = {self.x_data: observed_x})



