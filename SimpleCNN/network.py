import tflearn
from tflearn.layers.merge_ops import merge
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.conv import conv_2d, max_pool_2d
from tflearn.layers.estimator import regression
from tflearn.data_utils import to_categorical

# Building the network
def ANN():
	dropout_value = 0.35

	# Building the network
	network = input_data(shape=[None, 28, 28, 1], name='input')

	# Branch 1
	branch1 = conv_2d(network, 100, [2, 2], activation = 'relu', name = 'B1Conv2d_2x2')
	#branch1 = dropout(branch1, dropout_value)

	# Branch 2
	branch2 = conv_2d(branch1, 100, [2, 2], activation = 'relu', name = 'B2Conv2d_2x2')
	#branch2 = dropout(branch2, dropout_value)

	# Fully connected 1
	full_1 = fully_connected(branch2, 1000, activation='relu')
	full_1 = dropout(full_1, dropout_value)

	# Fully connected 2
	full_2 = fully_connected(full_1, 1000, activation='relu')
	full_2 = dropout(full_2, dropout_value)

	# Output layer
	network = fully_connected(full_2, 10, activation = 'softmax')
	network = tflearn.regression(network, optimizer = 'momentum',
	                         loss  = 'categorical_crossentropy',
	                         learning_rate = 0.1)
	'''
	network = regression(network, optimizer = 'adam', learning_rate = 0.001,
	                     loss = 'categorical_crossentropy', name ='target')
	'''
	model = tflearn.DNN(network, tensorboard_verbose = 0, tensorboard_dir = './logs', best_checkpoint_path = './checkpoints/best/best_val', max_checkpoints = 1)
	
	return model