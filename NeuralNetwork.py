import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
import os

class NeuralNetwork():

	def __init__(self):
		self.sess = tf.Session()

		self.x_data = tf.placeholder(shape = [None, 24], dtype = tf.float32)
		self.y_target = tf.placeholder(shape = [None, 1], dtype = tf.float32)

		self.generation = tf.Variable(initial_value = 0, name = 'generation')
		self.opened_counter = np.array([], dtype = int)
		self.win_counter = np.array([], dtype = int)

		# set up neural network
		# A1 ---> 1st layer weights		24x120
		# b1 ---> 1st layer bias		1x120
		# A2 ---> 2nd layer weights		120x120
		# b2 ---> 2nd layer bias		1x120
		# A3 ---> 3nd layer weights		120x120
		# b3 ---> 3nd layer bias		1x120
		# A4 ---> 4nd layer weights		120x120
		# b4 ---> 4nd layer bias		1x120
		# A5 ---> output layer weights	120x1
		# b5 ---> output layer bias		1x1
		self.hidden_layer_nodes = 120

		self.A1 = tf.Variable(tf.random_normal(shape = [24, self.hidden_layer_nodes]), name = 'A1')
		self.b1 = tf.Variable(tf.random_normal(shape = [self.hidden_layer_nodes]), name = 'b1')
		
		self.A2 = tf.Variable(tf.random_normal(shape = [self.hidden_layer_nodes, self.hidden_layer_nodes]), name = 'A2')
		self.b2 = tf.Variable(tf.random_normal(shape = [self.hidden_layer_nodes]), name = 'b2')
		
		self.A3 = tf.Variable(tf.random_normal(shape = [self.hidden_layer_nodes, self.hidden_layer_nodes]), name = 'A3')
		self.b3 = tf.Variable(tf.random_normal(shape = [self.hidden_layer_nodes]), name = 'b3')

		self.A4 = tf.Variable(tf.random_normal(shape = [self.hidden_layer_nodes, self.hidden_layer_nodes]), name = 'A4')
		self.b4 = tf.Variable(tf.random_normal(shape = [self.hidden_layer_nodes]), name = 'b4')

		self.A5 = tf.Variable(tf.random_normal(shape = [self.hidden_layer_nodes, 1]), name = 'A5')
		self.b5 = tf.Variable(tf.random_normal(shape = [1]), name = 'b5')

		self.hidden_output1 = tf.nn.sigmoid(tf.add(tf.matmul(self.x_data, self.A1), self.b1))
		self.hidden_output2 = tf.nn.sigmoid(tf.add(tf.matmul(self.hidden_output1, self.A2), self.b2))
		self.hidden_output3 = tf.nn.sigmoid(tf.add(tf.matmul(self.hidden_output2, self.A3), self.b3))
		self.hidden_output4 = tf.nn.sigmoid(tf.add(tf.matmul(self.hidden_output3, self.A4), self.b4))
		self.final_output = tf.add(tf.matmul(self.hidden_output4, self.A5), self.b5)

		self.loss = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(logits = self.final_output, labels = self.y_target))
		self.my_opt = tf.train.AdamOptimizer()
		self.train_step = self.my_opt.minimize(self.loss)
		self.init = tf.global_variables_initializer()
		self.sess.run(self.init)


	def trainingData(self, observed_x, observed_y):
		return self.sess.run(self.train_step, feed_dict = {self.x_data: observed_x, self.y_target: observed_y})

			
	def predict(self, observed_x):
		return self.sess.run(tf.nn.sigmoid(self.final_output), feed_dict = {self.x_data: observed_x})


	def saveModel(self, generation):
		saver = tf.train.Saver()
		if generation == False:
			save_path = saver.save(self.sess, './nn_trained_model/model.ckpt')
			np.save('./nn_trained_model/opened_counter.npy', self.opened_counter)
			np.save('./nn_trained_model/win_counter.npy', self.win_counter)
		else:
			save_path = saver.save(self.sess, './nn_trained_model/generation_{0}/model.ckpt'.format(generation))
			np.save('./nn_trained_model/generation_{0}/opened_counter.npy'.format(generation), self.opened_counter)
			np.save('./nn_trained_model/generation_{0}/win_counter.npy'.format(generation), self.win_counter)
			plt.plot(self.opened_counter, 'k-')
			plt.title('Numbers of block NN opened per Game')
			plt.xlabel('Game')
			plt.ylabel('Opened Block')
			plt.legend(loc = 'lower right')
			plt.savefig('./nn_trained_model/generation_{0}/stat.png'.format(generation))
			plt.clf()
		print('Model saved in path: {0}'.format(save_path))


	def restoreModel(self):
		dir_path = os.path.dirname(os.path.realpath(__file__))
		dir_path += '/nn_trained_model/checkpoint'
		exists = os.path.isfile(dir_path)

		if exists:
			saver = tf.train.Saver()
			saver.restore(self.sess, './nn_trained_model/model.ckpt')
			self.opened_counter = np.load('./nn_trained_model/opened_counter.npy')
			self.win_counter = np.load('./nn_trained_model/win_counter.npy')
			print('Model restored.')
			return 0
		else:
			print('Cannot load model.')
			return -1


	def counterIncrement(self):
		return self.sess.run(tf.assign_add(self.generation, 1))


	def getCounter(self):
		return self.sess.run(self.generation)


	def append_opened_counter(self, count):
		self.opened_counter = np.append(self.opened_counter, count)


	def append_win_counter(self, generation):
		self.win_counter = np.append(self.win_counter, generation)
