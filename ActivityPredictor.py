 # lstm model
from numpy import mean
from numpy import std
from numpy import dstack
from pandas import read_csv
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Flatten
from keras.layers import Dropout
from keras.layers import LSTM
from keras.utils import to_categorical
from matplotlib import pyplot
from keras.layers import TimeDistributed
from keras.layers import ConvLSTM2D
import sys
import numpy as np
import pandas as pd
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer


# load a single file as a numpy array
def load_file(filepath):
	dataframe = read_csv(filepath, header=None, delim_whitespace=True)
	return dataframe.values

# load a list of files and return as a 3d numpy array
def load_group(filenames, prefix=''):
	loaded = list()
	for name in filenames:
		data = load_file(prefix + name)
		loaded.append(data)
	# stack group so that features are the 3rd dimension
	loaded = dstack(loaded)
	return loaded

# load a dataset group, such as train or test
def load_dataset_group(group, prefix=''):
	filepath = prefix + group + '/Inertial Signals/'
	# load all 9 files as a single array
	filenames = list()
	# total acceleration
	filenames += ['total_acc_x_'+group+'.txt', 'total_acc_y_'+group+'.txt', 'total_acc_z_'+group+'.txt']
	# body acceleration
	filenames += ['body_acc_x_'+group+'.txt', 'body_acc_y_'+group+'.txt', 'body_acc_z_'+group+'.txt']
	# body gyroscope
	filenames += ['body_gyro_x_'+group+'.txt', 'body_gyro_y_'+group+'.txt', 'body_gyro_z_'+group+'.txt']
	# load input data
	X = load_group(filenames, filepath)
	# load class output
	y = load_file(prefix + group + '/y_'+group+'.txt')
	return X, y

# load the dataset, returns train and test X and y elements
def load_dataset(prefix=''):
	# load all train
	trainX, trainy = load_dataset_group('train', prefix + 'HARDataset/')
	print(trainX.shape, trainy.shape)
	# load all test
	testX, testy = load_dataset_group('test', prefix + 'HARDataset/')
	print(testX.shape, testy.shape)
	# zero-offset class values
	trainy = trainy - 1
	testy = testy - 1
	# one hot encode y
	trainy = to_categorical(trainy)
	testy = to_categorical(testy)
	print(trainX.shape, trainy.shape, testX.shape, testy.shape)
	return trainX, trainy, testX, testy

acc_x=sys.argv[1]
acc_y=sys.argv[2]
acc_z=sys.argv[3]
gyro_x=sys.argv[4]
gyro_y=sys.argv[5]
gyro_z=sys.argv[6]

# fit and evaluate a model
def evaluate_model_and_user_data_prediction(acc_x,acc_y,acc_z,gyro_x,gyro_y,gyro_z,trainX, trainy, testX, testy):

	# define model
	verbose, epochs, batch_size = 0, 25, 64
	n_timesteps, n_features, n_outputs = trainX.shape[1], trainX.shape[2], trainy.shape[1]
	# reshape into subsequences (samples, time steps, rows, cols, channels)
	n_steps, n_length = 4, 32
	trainX = trainX.reshape((trainX.shape[0], n_steps, 1, n_length, n_features))
	testX = testX.reshape((testX.shape[0], n_steps, 1, n_length, n_features))
	# define model
	model = Sequential()
	model.add(ConvLSTM2D(filters=64, kernel_size=(1,3), activation='relu', input_shape=(n_steps, 1, n_length, n_features)))
	model.add(Dropout(0.5))
	model.add(Flatten())
	model.add(Dense(100, activation='relu'))
	model.add(Dense(n_outputs, activation='softmax'))
	model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
	# fit network
	model.fit(trainX, trainy, epochs=epochs, batch_size=batch_size, verbose=verbose)
	# check predictions
	y_pred=model.predict(testX)
	print("RIGHT INITIAL LABELS")
	print(testy)
	print("LABELS PREDICTED")
	print(y_pred)
	print('\n')
	# evaluate model
	_, accuracy = model.evaluate(testX, testy, batch_size=batch_size, verbose=0)
	testX[:-1] = [acc_x, acc_y, acc_z, gyro_x, gyro_y, gyro_z,  float(acc_x) + float(gyro_x),float(acc_y) + float(gyro_y), float(acc_z) + float(gyro_z)]
	y_pred=model.predict(testX[:-1])
	print("For user's input: ", testX[:-1])
	print(type(y_pred))
	#np.set_printoptions(threshold=sys.maxsize)
	print("The output is: ",y_pred)
	print("Easier interpretation form output: ", np.round(y_pred, 1))
	if((y_pred[0])[0]==1):
		print("Activity is: Walking")
	if((y_pred[0])[1]==1):
		print("Activity is: Walking Upstairs")
	if((y_pred[0])[2]==1):
		print("Activity is: Walking Downstairs")
	if((y_pred[0])[3]==1):
		print("Activity is: Sitting")
	if((y_pred[0])[4]==1):
		print("Activity is: Standing")
	if((y_pred[0])[5]==1):
		print("Activity is: Laying")
	return accuracy

"""
def user_data_prediction(acc_x,acc_y,acc_z,testX):
	#testX[(len(testX))-1] = [acc_x, acc_y, acc_z,acc_x, acc_y, acc_z,acc_x, acc_y, acc_z]
	y_pred=model.predict(testX)
	print("The output is ",y_pred)
"""
	
# summarize scores
def summarize_results(scores):
	print(scores)
	m, s = mean(scores), std(scores)
	print('Accuracy: %.3f%% (+/-%.3f)' % (m, s))

# run an experiment
print("Trying experiment 2 times to evaluate")
def run_experiment(repeats=1):
	# load data
	trainX, trainy, testX, testy = load_dataset()
	# repeat experiment
	#user_data_prediction(acc_x,acc_y,acc_z,testX)
	scores = list()
	for r in range(repeats):
		score = evaluate_model_and_user_data_prediction(acc_x,acc_y,acc_z,gyro_x,gyro_y,gyro_z,trainX, trainy, testX, testy)
		score = score * 100.0
		print('>#%d: %.3f' % (r+1, score))
		scores.append(score)
	# summarize results
	summarize_results(scores)

# run the experiment
run_experiment()
