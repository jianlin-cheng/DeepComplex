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
from keras.models import model_from_json
import tensorflow as tf
import numpy as np
import math
import os
import sys
import random
import keras.backend as K
import os, sys
from DNCON_lib import *
# from readRR import readRRFile
 
import numpy as np
from keras.models import model_from_json, load_model
from keras import metrics, initializers, utils, regularizers
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


def writeToRRFile(pred,filename,L,_fasta,label_flag=False ):
    pred_new=np.zeros((L,L))
    pred_new=pred[0:L,0:L]
    np.savetxt(filename+"_cmap.txt",pred_new)
    fasta=_fasta
    with open (filename+"_rr.txt","w") as f:
        f.write(fasta+"\n")
        for i in range(L):
            for j in range(L):
                if label_flag:
                    if pred[i][j]== 1.0: f.write(str(i+1)+" "+str(j+1)+" 0 6.0 "+str(pred[i][j])+"\n")
                else:
                    f.write(str(i+1)+" "+str(j+1)+" 0 6.0 "+str(pred[i][j])+"\n")

def read_fastaonly(_input):
    array = []
    file = open(_input, "r")
    if file.mode == 'r':
        array = file.read().splitlines()
    file.close()
    counter = 0
    msa = ""

 
    fasta = array[1]


    return fasta


def usage():
  print(" usage"+"\n")
  print(" program  <full path of fasta_file > <full path of feature_path > <full path of  output_dir> <target_id>" +"\n")
#best weight
WEIGHT_PATH = "/exports/store2/deepcomplex/deepcomplex/deep_complex/homo_predictor/best_val_weights_64.hdf5"

#get fasta
fasta_file = sys.argv[1]
fasta = read_fastaonly(fasta_file)

#get feature  
feature_path = sys.argv[2]
 
#output_dir
output_dir = sys.argv[3]

target_id = sys.argv[4]

if not os.path.exists(fasta_file):
    print(" fasta not found "+ str(fasta_file)+"\n")
    usage()
if not os.path.exists(feature_path):
    print(" feature not found "+ str(feature_path)+"\n")
    usage()

if not os.path.exists(output_dir):
    print(" output dir  not found "+ str(fasta)+"\n")
    os.system( "mkdir -p "+str(output_dir))
    print ("So "+ str(output_dir)+"  has been created " +"\n")

length_fasta = len(fasta)

_inputs=np.zeros((length_fasta,length_fasta,56))
model =  DNCON2_tr_rosetta_ResNet(inputs=_inputs,filters=32,residual_block_num=60,kernel_size=3)
model.summary()
opt=Nadam(lr=0.0001, beta_1=0.9, beta_2=0.999, epsilon=1e-08)
model.compile(loss="binary_crossentropy", optimizer=opt, metrics=["accuracy"])
model.load_weights(WEIGHT_PATH)

print ("Getting X-features for "+target_id)
X=get_x_from_this_file(feature_path,length_fasta)
print ("Making predictions for: "+target_id)
print ("X.shape=",X.shape)

 

P=model.predict([X],batch_size=1)
P=P.squeeze().reshape(length_fasta,length_fasta)


filename=output_dir+target_id
writeToRRFile(P,filename,L=length_fasta,_fasta =fasta)

