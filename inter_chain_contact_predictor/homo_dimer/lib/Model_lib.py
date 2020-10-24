#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul  4 01:25:01 2020

@author: farhan
"""

#this script library stores all the models that we have developed

from keras.layers import Conv2D
from keras.layers.normalization import BatchNormalization
from keras.optimizers import Nadam, Adam
from keras.layers import Input, Dense, Reshape, Activation, Flatten, Embedding, Dropout, Lambda, add, concatenate, Concatenate, ConvLSTM2D, LSTM, average, MaxPooling2D, multiply, MaxPooling3D
from keras.layers import GlobalAveragePooling2D, Permute
from keras.layers.advanced_activations import LeakyReLU, PReLU
from keras.layers.convolutional import UpSampling2D, Conv2D, Conv1D
from keras.models import Sequential, Model
from keras.utils import multi_gpu_model
from keras.utils.generic_utils import Progbar
from keras.constraints import maxnorm
from keras.activations import tanh, softmax
from keras import metrics, initializers, utils, regularizers
import tensorflow as tf
import numpy as np
import math
import os
import sys
import random
import keras.backend as K
epsilon = K.epsilon()

######################################################################################################################################################
def classic_basic_block_conv2D_norm_relu(filters, kernel_size, strides=1,act_func="relu", normalize="BatchNormalize", use_bias=True):
    def f(input):
        if True:
            conv=Conv2D(filters=filters, kernel_size=kernel_size, strides=strides, padding="same", use_bias=use_bias)(input)
        else:
            conv=Conv2D(filters=filters, kernel_size=kernel_size, strides=strides, padding="same", use_bias=use_bias)(input)
        if (normalize==None):
            norm_layer=conv
        else:
            if "Batch" in normalize or "batch" in normalize:
                #norm_layer=BatchNormalization(axis=-1)(conv)
                norm_layer=BatchNormalization(axis=-1)(conv)
            elif "Instance" in normalize or "instance" in normalize:
                #norm_layer=InstanceNormalization(axis=-1)(conv)
                pass
                norm_layer=InstanceNormalization()(conv)
            else:
                norm_layer=conv
        return Activation(act_func)(norm_layer)
    return f

######################################################################################################################################################

######################################################################################################################################################
def basic_block_conv2D_norm_relu(filters, kernel_size, kernel_regularizer=regularizers.l2(1e-4),strides=1,act_func="relu", normalize="BatchNormalize", use_bias=True, kernel_initializer="he_normal"):
    def f(input):
        if kernel_regularizer==None:
            conv=Conv2D(filters=filters, kernel_size=kernel_size, strides=strides, kernel_initializer=kernel_initializer, padding="same", use_bias=use_bias)(input)
        else:
            conv=Conv2D(filters=filters, kernel_size=kernel_size, strides=strides, kernel_initializer=kernel_initializer, padding="same", use_bias=use_bias, kernel_regularizer=kernel_regularizer)(input)
        if (normalize==None):
            norm_layer=conv
        else:
            if "Batch" in normalize or "batch" in normalize:
                #norm_layer=BatchNormalization(axis=-1)(conv)
                norm_layer=BatchNormalization(axis=-1)(conv)
            elif "Instance" in normalize or "instance" in normalize:
                #norm_layer=InstanceNormalization(axis=-1)(conv)
                pass
                norm_layer=InstanceNormalization()(conv)
            else:
                norm_layer=conv
        return Activation(act_func)(norm_layer)
    return f

######################################################################################################################################################
def _handle_dimension_ordering():
    global ROW_AXIS
    global COL_AXIS
    global CHANNEL_AXIS
    print ("K.image_dim_ordering()====",K.image_dim_ordering())
    if K.image_dim_ordering() == 'tf':
        ROW_AXIS = 1
        COL_AXIS = 2
        CHANNEL_AXIS = 3
    else:
        CHANNEL_AXIS = 1
        ROW_AXIS = 2
        COL_AXIS = 3

def basic_block_conv2D_norm_elu(filters, kernel_size, kernel_regularizer=regularizers.l2(1e-4),act_func="elu", normalize="Instance",   dropout='0.15',
                                strides=1,use_bias = True,kernel_initializer = "he_normal",_dilation_rate=0):

    def f(input):
        if kernel_regularizer == None:
                if _dilation_rate == 0:
                    conv = Conv2D(filters=filters, kernel_size=kernel_size, strides=strides,
                                   padding="same",    use_bias=use_bias)(input)
                else:
                    conv = Conv2D(filters=filters, kernel_size=kernel_size, strides=strides,
                                  padding="same", use_bias=use_bias,dilation_rate=_dilation_rate)(input)
        else:
            if _dilation_rate == 0:
                conv = Conv2D(filters=filters, kernel_size=kernel_size, strides=strides,
                              kernel_initializer=kernel_initializer, padding="same", use_bias=use_bias,
                              kernel_regularizer=kernel_regularizer)(input)
            else:
                conv = Conv2D(filters=filters, kernel_size=kernel_size, strides=strides,
                              kernel_initializer=kernel_initializer, padding="same", use_bias=use_bias,
                              kernel_regularizer=kernel_regularizer, dilation_rate=_dilation_rate)(input)

        if dropout != None:
            dropout_layer = Dropout(0.15)(conv)
        else:
            dropout_layer = Dropout(0)(conv)

        if normalize == None and dropout != None:
            norm_layer = conv(dropout_layer)
        else:
            # norm_layer = InstanceNormalization()(conv)
            norm_layer = BatchNormalization()(dropout_layer)



        return Activation(act_func)(norm_layer)
    return f

######################################################################################################################################################
def add_input(input, residual):
    input_shape = K.int_shape(input)
    residual_shape = K.int_shape(residual)
    # stride_width = int(round(input_shape[ROW_AXIS] / residual_shape[ROW_AXIS]))
    # stride_height = int(round(input_shape[COL_AXIS] / residual_shape[COL_AXIS]))
    stride_width = 1
    stride_height = 1
    equal_channels = input_shape[CHANNEL_AXIS] == residual_shape[CHANNEL_AXIS]

    shortcut = input
    # 1 X 1 conv if shape is different. Else identity.
    # if stride_width > 1 or stride_height > 1 or not equal_channels:
    #     shortcut = Conv2D(filters=residual_shape[CHANNEL_AXIS],
    #                       kernel_size=(1, 1),
    #                       strides=(stride_width, stride_height),
    #                       padding="valid",
    #                       kernel_initializer="he_normal",
    #                       kernel_regularizer=regularizers.l2(0.0001))(input)
    if not equal_channels:
        print ("Input Shape:", input_shape)
        print ("Residual output shape:", residual_shape)
        print ("Input and output channels are not equal. Performing Convolution on input to make shapes equal.")
        shortcut = Conv2D(filters=residual_shape[CHANNEL_AXIS],
                          kernel_size=(1, 1),
                          strides=(stride_width, stride_height),
                          padding="valid",
                          kernel_initializer="he_normal")(input)
    return add([shortcut, residual])

######################################################################################################################################################
def DNCON2_net_classic(inputs,layers,filters,kernel_size,act_func="relu",normalize="BatchNormalize"):
    input_shape=(inputs.shape[0],inputs.shape[1],inputs.shape[2])
    #input_shape=(None,None,inputs.shape[2])
    print ("This input shape is :", inputs.shape)
    contact_input=Input(shape=input_shape)
    _handle_dimension_ordering()
    
    block = classic_basic_block_conv2D_norm_relu(filters=filters, kernel_size=kernel_size, act_func=act_func, normalize=normalize)(contact_input)
    
    for _ in range(layers-1):
        block = classic_basic_block_conv2D_norm_relu(filters=filters, kernel_size=kernel_size, act_func=act_func, normalize=normalize)(block)
    
    block=classic_basic_block_conv2D_norm_relu(filters=1, kernel_size=kernel_size, act_func="sigmoid", normalize=None)(block)
    block=Flatten()(block)
    return Model(inputs=contact_input, outputs=block)

######################################################################################################################################################
def DNCON2_net(inputs,layers,filters,kernel_size,kernel_regularizer=regularizers.l2(1e-4),act_func="relu",normalize="BatchNormalize",kernel_initializer="he_normal"):
    print ("Input shape fed to model: ",inputs.shape)
    input_shape=(inputs.shape[0],inputs.shape[1],inputs.shape[2])
    #input_shape=(None,None,inputs.shape[2])
    print ("This input shape is :", inputs.shape)
    contact_input=Input(shape=input_shape)
    _handle_dimension_ordering()
    
    block = basic_block_conv2D_norm_relu(filters=filters, kernel_size=kernel_size, act_func=act_func, kernel_regularizer=kernel_regularizer, normalize=normalize, kernel_initializer=kernel_initializer)(contact_input)
    
    for _ in range(layers-1):
        block = basic_block_conv2D_norm_relu(filters=filters, kernel_size=kernel_size, act_func=act_func, kernel_regularizer=kernel_regularizer, normalize=normalize, kernel_initializer=kernel_initializer)(block)
    
    block=basic_block_conv2D_norm_relu(filters=1, kernel_size=kernel_size, act_func="sigmoid", kernel_regularizer=kernel_regularizer,normalize=None)(block)
    block=Flatten()(block)
    return Model(inputs=contact_input, outputs=block)

######################################################################################################################################################
def DNCON2_ResNet(inputs,residual_block_num,filters,kernel_size,act_func,normalize,kernel_regularizer=regularizers.l2(1e-4),kernel_initializer="he_normal"):
    print ("Input shape fed to model: ",inputs.shape)
    input_shape=inputs.shape#(inputs.shape[1],inputs.shape[2],inputs.shape[3])
    print ("This input shape is :", inputs.shape)
    contact_input=Input(shape=input_shape)
    _handle_dimension_ordering()
    
    #First block input + conv2d + conv2d + add
    first_block = basic_block_conv2D_norm_relu(filters=filters, kernel_size=kernel_size, act_func=act_func, kernel_regularizer=kernel_regularizer, normalize=normalize, kernel_initializer=kernel_initializer)(contact_input)
    block = basic_block_conv2D_norm_relu(filters=filters, kernel_size=kernel_size, act_func=act_func, kernel_regularizer=kernel_regularizer, normalize=normalize, kernel_initializer=kernel_initializer)(first_block)
    block = add_input(first_block,block)
    
    for _ in range(residual_block_num-1):
        block = basic_block_conv2D_norm_relu(filters=filters, kernel_size=kernel_size, act_func=act_func, kernel_regularizer=kernel_regularizer, normalize=normalize, kernel_initializer=kernel_initializer)(block)
        block = basic_block_conv2D_norm_relu(filters=filters, kernel_size=kernel_size, act_func=act_func, kernel_regularizer=kernel_regularizer, normalize=normalize, kernel_initializer=kernel_initializer)(block)
        block = add_input(first_block,block)

    block=basic_block_conv2D_norm_relu(filters=1, kernel_size=kernel_size, act_func="sigmoid", kernel_regularizer=kernel_regularizer, normalize=None)(block)
    block=Flatten()(block)
    return Model(inputs=contact_input, outputs=block)

######################################################################################################################################################

def DNCON2_tr_rosetta_ResNet(inputs,residual_block_num,filters,kernel_size):
    input_shape=(inputs.shape[0],inputs.shape[1],inputs.shape[2])

    print ("This input shape is :", inputs.shape)

    contact_input=Input(shape=input_shape)
    _handle_dimension_ordering()
    #1x1


    first_block =   basic_block_conv2D_norm_elu(filters=filters, kernel_size=1, act_func='elu',
                                             kernel_regularizer=None, normalize='Instance',dropout='0.15',_dilation_rate=0)(contact_input)
    # block = basic_block_conv2D_norm_elu(filters=filters, kernel_size=kernel_size, act_func='elu',
    #                                     kernel_regularizer=None, normalize='Instance', dropout=None,_dilation_rate=0)(first_block)
    block = add_input(contact_input, first_block)
    dilation_rate =1
    for _ in range(residual_block_num-1):

        #2d conv with elu and instance normalization and dropout
        block = basic_block_conv2D_norm_elu(filters=filters, kernel_size=kernel_size, act_func='elu',
                                             kernel_regularizer=None, normalize='Instance',dropout='0.15',_dilation_rate=dilation_rate)(block)

        # 2d conv with elu and instance normalization and without  dropout
        block = basic_block_conv2D_norm_elu(filters=filters, kernel_size=kernel_size, act_func='elu',
                                             kernel_regularizer=None,  normalize='Instance' ,dropout=None,_dilation_rate=dilation_rate)(block)
        block = add_input(first_block, block)
        dilation_rate = dilation_rate * 2
        if dilation_rate >16:
            dilation_rate = 1


    block = basic_block_conv2D_norm_elu(filters=1, kernel_size=kernel_size,act_func='sigmoid',
                                         kernel_regularizer=None, normalize=None ,dropout=None)(block)

    block=Flatten()(block)
    return Model(inputs=contact_input, outputs=block)