import tflearn
import numpy as np
from tqdm import tqdm

from tflearn.layers.merge_ops import merge
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.conv import conv_2d, max_pool_2d
from tflearn.layers.estimator import regression
from tflearn.data_utils import to_categorical
from tflearn.data_preprocessing import ImagePreprocessing

# Building the network
def ANN(WIDTH, HEIGHT, CHANNELS, LABELS):
	dropout_value = 0.35

	# Real-time data preprocessing
	img_prep = ImagePreprocessing()
	img_prep.add_featurewise_zero_center()
	img_prep.add_featurewise_stdnorm()

	# Building the network
	network = input_data(shape=[None, WIDTH, HEIGHT, CHANNELS],
		data_preprocessing=img_prep,
		name='input')

	# Branch 1
	branch1 = conv_2d(network, 32, [2, 2], activation = 'relu', name = 'B1Conv2d_2x2')

	# Branch 2
	branch2 = conv_2d(network, 32, [3, 3], activation = 'relu', name = 'B2Conv2d_3x3')
	
	# Branch 3
	branch3 = conv_2d(network, 32, [5, 5], activation = 'relu', name = 'B3Conv2d_5x5')
	
	# Branch 4
	branch4 = conv_2d(network, 32, [7, 7], activation = 'relu', name = 'B4Conv2d_7x7')
	
	# Merging the branches
	merged_layers = merge((branch1, branch2, branch3, branch4), mode = 'elemwise_sum', name = 'Merge')

	# Fully connected 1
	merged_layers = fully_connected(merged_layers, 1000, activation='relu')
	merged_layers = dropout(merged_layers, dropout_value)

	# Fully connected 2
	merged_layers = fully_connected(merged_layers, 1000, activation='relu')
	merged_layers = dropout(merged_layers, dropout_value)

	# Output layer
	merged_layers = fully_connected(merged_layers, LABELS, activation = 'softmax')
	network = regression(merged_layers, optimizer = 'adam', learning_rate = 0.0005,
	                     loss = 'categorical_crossentropy', name ='target')

	model = tflearn.DNN(network, tensorboard_verbose = 0, tensorboard_dir = './logs', best_checkpoint_path = './checkpoints/best/best_val', max_checkpoints = 1)
	return model

def big_dataset_prediction(model, DATA = []):
    # Predicting
    test_data_predicted = np.empty((0, 10))
    test_data_predicted_label = np.empty((0, 10))
    print('Prediction in progress...')
    for i in tqdm(range(0, DATA.shape[0])):
        current_example = DATA[i].reshape([-1,28,28,1])
        test_data_predicted = np.append(test_data_predicted, model.predict(current_example), axis = 0)
        test_data_predicted_label = np.append(test_data_predicted_label, model.predict_label(current_example), axis = 0)

    print('The test data has been successfully labeled.')
    print('*' * 70)
    return test_data_predicted_label
