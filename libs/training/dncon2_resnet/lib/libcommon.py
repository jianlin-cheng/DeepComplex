#!/usr/bin/python
# Badri Adhikari, 6-15-2017
# Subroutines for training and prediction

from Model_lib import *
from keras.models import Sequential
from keras.layers import Activation, Flatten
from keras.layers import Convolution2D, Conv2D
from keras.layers.normalization import BatchNormalization
from keras.optimizers import Nadam, Adam
import numpy as np
import math
import os
import sys
import random
import keras.backend as K
epsilon = K.epsilon()

# Model architectures / Layers information
def read_model_arch(file_config):
    if not os.path.isfile(file_config):
        print ('Error! Could not find config file ' + file_config)
        sys.exit(1)
    layers = {}
    with open(file_config) as f:
        for line in f:
            if line.startswith('#'):
                continue
            if len(line) < 2:
                continue
            cols = line.strip().split()
            if len(cols) != 5:
                print ('Error! Config file ' + file_config + ' line ' + line + '??')
                sys.exit(1)
            layers[cols[0]] = cols[1] + ' ' + cols[2] + ' ' +  cols[3] + ' ' + cols[4] 
    print ('')
    print ('Reading model architecture:')
    for k, v in sorted(layers.items()):
        print (k + ' : ' + v)
    print ('')
    return layers

# Feature file that has 0D, 1D, and 2D features (L is the first feature)
# Output size (a little >= L) to which all the features will be rolled up to as 2D features
def getX(feature_file, l_max):
    # calcualte the length of the protein (the first feature)
    reject_list = []
    reject_list.append('# PSSM')
    reject_list.append('# AA composition')
    L = 0
    with open(feature_file) as f:
        for line in f:
            if line.startswith('#'):
                continue
            L = line.strip().split()
            L = int(round(math.exp(float(L[0]))))
            break
    Data = []
    with open(feature_file,"r") as f:
        accept_flag = 1
        for line in f:
            if line.startswith('#'):
                if line.strip() in reject_list:
                    accept_flag = 0
                else:
                    accept_flag = 1
                continue
            if accept_flag == 0:
                continue
            if line.startswith('#'):
                continue
            this_line = line.strip().split()
            if len(this_line) == 0:
                continue
            if len(this_line) == 1:
                # 0D/Scalar feature
                feature2D = np.zeros((L, L))
                feature2D[:, :] = float(this_line[0])
                Data.append(feature2D)
            elif len(this_line) == L:
                # 1D feature
                feature2D1 = np.zeros((L, L))
                feature2D2 = np.zeros((L, L))
                for i in range (0, L):
                    feature2D1[i, :] = float(this_line[i])
                    feature2D2[:, i] = float(this_line[i])
                Data.append(feature2D1)
                Data.append(feature2D2)
            elif len(this_line) == L * L:
                # 2D feature
                feature2D = np.asarray(this_line).reshape(L, L)
                Data.append(feature2D)
            else:
                print (line)
                print ('Error!! Unknown length of feature in !!' + feature_file)
                print ('Expected length 0, ' + str(L) + ', or ' + str (L*L) + ' - Found ' + str(len(this_line)))
                sys.exit()
    F = len(Data)
    X = np.zeros((l_max, l_max, F))
    for i in range (0, F):
        X[0:L, 0:L, i] = Data[i]
    return X

def build_model_for_this_input_shape(model_arch, X):
    model = Sequential()
    for layer in range(1, 1000):
        if 'layer' + str(layer) not in model_arch:
            break
        parameters = model_arch['layer' + str(layer)]
        cols = parameters.split()
        num_kernels = int(cols[0])
        filter_size = int(cols[1])
        b_norm_flag = cols[2]
        activ_funct = cols[3]
        if layer == 1:
            #model.add(Convolution2D(num_kernels, filter_size, filter_size, border_mode='same', input_shape=X[0, :, :, :].shape))
            model.add(Conv2D(num_kernels, (filter_size, filter_size), padding='same', input_shape=X[0, :, :, :].shape))
        else:
            #model.add(Convolution2D(num_kernels, filter_size, filter_size, border_mode='same'))
            model.add(Conv2D(num_kernels, (filter_size, filter_size), padding='same'))
        if b_norm_flag == '1':
            model.add(BatchNormalization())
        model.add(Activation(activ_funct))
    model.add(Flatten())
    return model

def make_prediction_new(model_arch, file_weights, X):
    model = DNCON2_net(inputs=X,filters=16,layers=6,kernel_size=5,act_func="relu",normalize="BatchNormalization")
    model.load_weights(file_weights)
    print ("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&  The input shape for prediction is :", X.shape)
    P = model.predict(X)
    return P

def make_prediction_ResNet(model_arch, file_weights, X):
    model = DNCON2_ResNet(inputs=X,filters=16,residual_block_num=6,kernel_size=5,act_func="relu",normalize="BatchNormalization")
    model.load_weights(file_weights)
    print ("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&  The input shape for prediction is :", X.shape)
    P = model.predict(X)
    return P

def make_prediction(model_arch, file_weights, X):
    model = build_model_for_this_input_shape(model_arch, X)
    model.load_weights(file_weights)
    print ("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&  The input shape for prediction is :", X.shape)
    P = model.predict(X)
    return P
