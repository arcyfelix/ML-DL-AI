import tflearn
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.conv import conv_2d, max_pool_2d
from tflearn.layers.estimator import regression
from tflearn.data_preprocessing import ImagePreprocessing

# Building the network
def ANN(WIDTH, HEIGHT, CHANNELS, LABELS):

	# Real-time data preprocessing
	img_prep = ImagePreprocessing()
	img_prep.add_featurewise_zero_center()
	img_prep.add_featurewise_stdnorm()

	# Building the network
	network = input_data(shape=[None, WIDTH, HEIGHT, CHANNELS],
		data_preprocessing=img_prep,
		name='input')

	network = conv_2d(network, 64, 3, activation = 'relu')
	network = conv_2d(network, 64, 3, activation = 'relu')
	network = max_pool_2d(network, 2, strides = 2)

	network = conv_2d(network, 128, 3, activation = 'relu')
	network = conv_2d(network, 128, 3, activation = 'relu')
	network = max_pool_2d(network, 2, strides = 2)

	network = conv_2d(network, 256, 3, activation = 'relu')
	network = conv_2d(network, 256, 3, activation = 'relu')
	network = conv_2d(network, 256, 3, activation = 'relu')
	network = max_pool_2d(network, 2, strides = 2)

	network = conv_2d(network, 512, 3, activation = 'relu')
	network = conv_2d(network, 512, 3, activation = 'relu')
	network = conv_2d(network, 512, 3, activation = 'relu')
	network = max_pool_2d(network, 2, strides = 2)

	network = conv_2d(network, 512, 3, activation = 'relu')
	network = conv_2d(network, 512, 3, activation = 'relu')
	network = conv_2d(network, 512, 3, activation = 'relu')
	network = max_pool_2d(network, 2, strides = 2)

	network = fully_connected(network, 4096, activation = 'relu')
	network = dropout(network, 0.5)
	network = fully_connected(network, 4096, activation = 'relu')
	network = dropout(network, 0.5)

	# Output layer
	merged_layers = fully_connected(network, LABELS, activation = 'softmax')
	network = regression(merged_layers, optimizer = 'adam', learning_rate = 0.0005,
	                     loss = 'categorical_crossentropy', name ='target')

	model = tflearn.DNN(network, tensorboard_verbose = 0, tensorboard_dir = './logs', best_checkpoint_path = './checkpoints/best/best_val', max_checkpoints = 1)
	return model