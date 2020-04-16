 # lstm model
import numpy as np
import pandas as pd
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
from keras.models import model_from_json

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import tensorflow as tf

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=Warning)

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
	#filenames += ['body_acc_x_'+group+'.txt', 'body_acc_y_'+group+'.txt', 'body_acc_z_'+group+'.txt']
	# body gyroscope
	#filenames += ['body_gyro_x_'+group+'.txt', 'body_gyro_y_'+group+'.txt', 'body_gyro_z_'+group+'.txt']
	# load input data
	X = load_group(filenames, filepath)
	# load class output
	y = load_file(prefix + group + '/y_'+group+'.txt')
	return X, y

# load the dataset, returns train and test X and y elements
def load_dataset(prefix=''):
	# load all train
	trainX, trainy = load_dataset_group('train', prefix + 'HARDataset/')
	#print(trainX.shape, trainy.shape)
	# load all test
	testX, testy = load_dataset_group('test', prefix + 'HARDataset/')
	#print(testX.shape, testy.shape)
	# zero-offset class values
	trainy = trainy - 1
	testy = testy - 1
	# one hot encode y
	trainy = to_categorical(trainy)
	testy = to_categorical(testy)
	#print(trainX.shape, trainy.shape, testX.shape, testy.shape)
	return trainX, trainy, testX, testy

#acc_x=sys.argv[1]
#acc_y=sys.argv[2]
#acc_z=sys.argv[3]
#gyro_x=sys.argv[4]
#gyro_y=sys.argv[5]
#gyro_z=sys.argv[6]

# fit and evaluate a model
def evaluate_model_and_user_data_prediction(acc_x,acc_y,acc_z,trainX, trainy, testX, testy):


	import io
	import sys
	# create a text trap and redirect stdout
	text_trap = io.StringIO()
	sys.stdout = text_trap

	# load json and create model
	json_file = open('model.json', 'r')
	loaded_model_json = json_file.read()
	json_file.close()
	model = model_from_json(loaded_model_json)
	# load weights into new model
	model.load_weights("model.h5")
	#print("Loaded model from disk")

	verbose, epochs, batch_size = 0, 25, 64
	n_timesteps, n_features, n_outputs = trainX.shape[1], trainX.shape[2], trainy.shape[1]
	# reshape into subsequences (samples, time steps, rows, cols, channels)
	n_steps, n_length = 4, 32
	testX = testX.reshape((testX.shape[0], n_steps, 1, n_length, n_features))
	# evaluate model
	model.compile(loss='binary_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
	_, accuracy = model.evaluate(testX, testy, batch_size=batch_size, verbose=0)
	testX[:-1] = [acc_x, acc_y, acc_z]#, gyro_x, gyro_y, gyro_z,  float(acc_x) + float(gyro_x),float(acc_y) + float(gyro_y), float(acc_z) + float(gyro_z)]
	y_pred=model.predict(testX[:-1])
	#print("For user's input: ", testX[:-1])
	#print(type(y_pred))
	#np.set_printoptions(threshold=sys.maxsize)
	#print("The output is: ",y_pred)
	#print("Easier interpretation form output: ", np.round(y_pred, 1))

	# exit printing from trap
	sys.stdout = sys.__stdout__
	type=''
	if((y_pred[0])[0]>0.5):
		type="Activity is: Walking"
		#print("Activity is: Walking")
	if((y_pred[0])[1]>0.5):
		#print("Activity is: Walking Upstairs")
		type="Activity is: Walking Upstairs"
	if((y_pred[0])[2]>0.5):
		#print("Activity is: Walking Downstairs")
		type="Activity is: Walking Downstairs"

	if((y_pred[0])[3]>0.5):
		#print("Activity is: Sitting")
		type="Activity is: Sitting"

	if((y_pred[0])[4]>0.5):
		#print("Activity is: Standing")
		type="Activity is: Standing"

	if((y_pred[0])[5]>0.5):
		#print("Activity is: Laying")
		type="Activity is: Laying"

	return type +" with accuracy "+str(accuracy)

#trainX, trainy, testX, testy = load_dataset()
#score = evaluate_model_and_user_data_prediction(acc_x,acc_y,acc_z,trainX, trainy, testX, testy)
#print ("With accuracy: ",score*100, "%")
