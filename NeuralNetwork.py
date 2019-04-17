import numpy as np
import tensorflow as tf
import os

class NeuralNetwork():

	def __init__(self):
		self.sess = tf.Session()
		self.x_data = tf.placeholder(shape = [None, 8], dtype = tf.float32)
		self.y_target = tf.placeholder(shape = [None, 1], dtype = tf.float32)

		self.generation = tf.Variable(initial_value = 0, dtype = tf.uint64, name='generation')
		# set up neural network
		# A1 ---> 1st layer weights		8x64
		# b1 ---> 1st layer bias		1x64
		# A2 ---> 2nd layer weights		64x64
		# b2 ---> 2nd layer bias		1x64
		# A3 ---> output layer weights	64x1
		# b3 ---> output layer bias		1x1
		self.hidden_layer_nodes = 64

		self.A1 = tf.Variable(tf.random_normal(shape = [8, self.hidden_layer_nodes]), name = 'A1')
		self.b1 = tf.Variable(tf.random_normal(shape = [self.hidden_layer_nodes]), name = 'b1')
		self.A2 = tf.Variable(tf.random_normal(shape = [self.hidden_layer_nodes, self.hidden_layer_nodes]), name = 'A2')
		self.b2 = tf.Variable(tf.random_normal(shape = [self.hidden_layer_nodes]), name = 'b2')
		self.A3 = tf.Variable(tf.random_normal(shape = [self.hidden_layer_nodes, 1]), name = 'A3')
		self.b3 = tf.Variable(tf.random_normal(shape = [1]), name = 'b3')

		self.hidden_output1 = tf.nn.sigmoid(tf.add(tf.matmul(self.x_data, self.A1), self.b1))
		self.hidden_output2 = tf.nn.sigmoid(tf.add(tf.matmul(self.hidden_output1, self.A2), self.b2))
		self.final_output = tf.add(tf.matmul(self.hidden_output2, self.A3), self.b3)

		self.loss = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(logits = self.final_output, labels = self.y_target))
		self.my_opt = tf.train.GradientDescentOptimizer(0.05)
		self.train_step = self.my_opt.minimize(self.loss)
		self.init = tf.global_variables_initializer()
		self.sess.run(self.init)


	def trainingData(self, observed_x, observed_y):
		return self.sess.run(self.train_step, feed_dict = {self.x_data: observed_x, self.y_target: observed_y})

			
	def predict(self, observed_x):
		return self.sess.run(tf.nn.sigmoid(self.final_output), feed_dict = {self.x_data: observed_x})


	def saveModel(self):
		saver = tf.train.Saver()
		save_path = saver.save(self.sess, "./nn_trained_model/model.ckpt")
		print("Model saved in path: {0}".format(save_path))


	def restoreModel(self):
		dir_path = os.path.dirname(os.path.realpath(__file__))
		dir_path += '/nn_trained_model/checkpoint'
		exists = os.path.isfile(dir_path)

		if exists:
			saver = tf.train.Saver()
			saver.restore(self.sess, "./nn_trained_model/model.ckpt")
			print("Model restored.")
			return 0
		else:
			print("Cannot load model.")
			return -1
