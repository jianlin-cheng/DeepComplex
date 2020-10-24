#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import shutil
#from libcommon import *
import os, sys, math
import numpy as np
import random
import  lib
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
from lib.Model_lib import *
epsilon = K.epsilon()


# Training hyperparameters
def read_train_param(file_config):
    if not os.path.isfile(file_config):
        print ('Error! Could not find config file ' + file_config)
        sys.exit(1)
    train_param = {}
    with open(file_config) as f:
        for line in f:
            if line.startswith('#'):
                continue
            if len(line) < 2:
                continue
            cols = line.strip().split()
            if len(cols) < 2:
                print ('Error! Config file ' + file_config + ' line ' + line + '??')
                sys.exit(1)
            if cols[0] == 'optimizer':
                train_param[cols[0]] = cols[1]
            else:
                train_param[cols[0]] = int(cols[1])
    print ('')
    print ('Read training parameters:')
    for k, v in sorted(train_param.items()):
        print ("%-15s : %-3s" %(k, v))
    print ('')
    return train_param


def build_dataset_dictionaries(path_lists):
    length_dict = {}
#    n_dict = {}
#    neff_dict = {}
    with open(path_lists + 'all_training_protein_length.txt') as f:
        for line in f:
            cols = line.strip().split()
            length_dict[cols[0]] = int(cols[1])
#    with open(path_lists + 'N.txt') as f:
#        for line in f:
#            cols = line.strip().split()
#            n_dict[cols[0]] = int(float(cols[1]))
#    with open(path_lists + 'Neff.txt') as f:
#        for line in f:
#            cols = line.strip().split()
#            neff_dict[cols[0]] = int(float(cols[1]))
    tr_l = {}
#    tr_n = {}
#    tr_e = {}
    with open(path_lists + 'train_list.txt') as f:
        for line in f:
            tr_l[line.strip()] = length_dict[line.strip()]
#            tr_n[line.strip()] = n_dict[line.strip()]
#            tr_e[line.strip()] = neff_dict[line.strip()]
    te_l = {}
#    tv_l = {}
    tv_l = {}
#    te_e = {}
    with open(path_lists + 'test_list.txt') as f:
        for line in f:
            te_l[line.strip()] = length_dict[line.strip()]
#            te_n[line.strip()] = n_dict[line.strip()]
#            te_e[line.strip()] = neff_dict[line.strip()]
    with open(path_lists + 'validation_list.txt') as f:
        for line in f:
            tv_l[line.strip()] = length_dict[line.strip()]

    print ('')
    print ('Data counts:')
    print ('Total       : ' + str(len(length_dict)))
    print ('Train       : ' + str(len(tr_l)))
    print ('Test        : ' + str(len(te_l)))
    print ('Validation  : ' + str(len(tv_l)))
    print ('')
    return (tr_l, te_l, tv_l)
    #return (tr_l, te_l, tv_l)

def subset_pdb_dict(dict, minL, maxL, count, randomize_flag):
    selected = {}
    # return a dict with random 'X' PDBs
    if (randomize_flag == 'random'):
        pdbs = list(dict.keys())
        random.shuffle(pdbs)
        i = 0
        for pdb in pdbs:
            if (dict[pdb] >= minL and dict[pdb] <= maxL):
                selected[pdb] = dict[pdb]
                i = i + 1
                if i == count:
                    break
    # return first 'X' PDBs sorted by L
    if (randomize_flag == 'ordered'):
        i = 0
        for key, value in sorted(dict.items(), key=lambda  x: x[1]):
            if (dict[key] > minL and dict[key] <= maxL):
                selected[key] = value
                i = i + 1
                if i == count:
                    break
    return selected

def print_detailed_evaluations(dict_l, P3L5, P3L10, P3L20, P3L30, P3T10, P3T5, Y):
    datacount = len(dict_l)
    print ("  ID    PDB      L   Nc    Top-5  Top-10  L/30  L/20  L/10  L/5  ")
    avg_nc  = 0    # average true Nc
    avg_pc_l5  = 0 # average predicted correct L/5
    avg_pc_l10  = 0 # average predicted correct L/10
    avg_pc_l20  = 0 # average predicted correct L/20
    avg_pc_l30  = 0 # average predicted correct L/30
    avg_pc_T10  = 0 # average predicted correct Top 10
    avg_pc_T5  = 0 # average predicted correct Top 5
    avg_acc_l5 = 0.0
    avg_acc_l10 = 0.0
    avg_acc_l20 = 0.0
    avg_acc_l30 = 0.0
    avg_acc_T10 = 0.0
    avg_acc_T5 = 0.0
    list_acc_l5 = []
    list_acc_l10 = []
    list_acc_l20 = []
    list_acc_l30 = []
    list_acc_T10 = []
    list_acc_T5 = []
    i = -1
    for pdb in sorted(dict_l):
        i = i + 1
        nc = int(Y[i].sum())
        L = dict_l[pdb]
        L5 = int(L/5)
        L10 = int(L/10)
        L20 = int(L/20)
        L30 = int(L/30)
        pc_l5 = np.logical_and(Y[i], P3L5[i, :]).sum()
        pc_l10 = np.logical_and(Y[i], P3L10[i, :]).sum()
        pc_l20 = np.logical_and(Y[i], P3L20[i, :]).sum()
        pc_l30 = np.logical_and(Y[i], P3L30[i, :]).sum()
        pc_T10 = np.logical_and(Y[i], P3T10[i, :]).sum()
        pc_T5 = np.logical_and(Y[i], P3T5[i, :]).sum()
        acc_l5 = float(pc_l5) / (float(L5) + epsilon)
        acc_l10 = float(pc_l10) / (float(L10) + epsilon)
        acc_l20 = float(pc_l20) / (float(L20) + epsilon)
        acc_l30 = float(pc_l30) / (float(L30) + epsilon)
        acc_T10 = float(pc_T10) / (float(10) + epsilon)
        acc_T5 = float(pc_T5) / (float(5) + epsilon)
        list_acc_l5.append(acc_l5)
        list_acc_l10.append(acc_l10)
        list_acc_l20.append(acc_l20)
        list_acc_l30.append(acc_l30)
        list_acc_T10.append(acc_T10)
        list_acc_T5.append(acc_T5)
        print (" %3s %6s %6s %6s %.4f    %.4f    %.4f    %.4f    %.4f    %.4f" % (i, pdb, L, nc, acc_T5, acc_T10, acc_l30, acc_l20, acc_l10, acc_l5))
        avg_nc = avg_nc + nc
        avg_pc_l5 = avg_pc_l5 + pc_l5
        avg_pc_l10 = avg_pc_l10 + pc_l10
        avg_pc_l20 = avg_pc_l20 + pc_l20
        avg_pc_l30 = avg_pc_l30 + pc_l30
        avg_pc_T10 = avg_pc_T10 + pc_T10
        avg_pc_T5 = avg_pc_T5 + pc_T5
        avg_acc_l5 = avg_acc_l5 + acc_l5
        avg_acc_l10 = avg_acc_l10 + acc_l10
        avg_acc_l20 = avg_acc_l20 + acc_l20
        avg_acc_l30 = avg_acc_l30 + acc_l30
        avg_acc_T10 = avg_acc_T10 + acc_T10
        avg_acc_T5 = avg_acc_T5 + acc_T5
    avg_nc = int(avg_nc/datacount)
    avg_pc_l5 = int(avg_pc_l5/datacount)
    avg_pc_l10 = int(avg_pc_l10/datacount)
    avg_pc_l20 = int(avg_pc_l20/datacount)
    avg_pc_l30 = int(avg_pc_l30/datacount)
    avg_pc_T10 = int(avg_pc_T10/datacount)
    avg_pc_T5 = int(avg_pc_T5/datacount)
    avg_acc_l5 = avg_acc_l5/datacount
    avg_acc_l10 = avg_acc_l10/datacount
    avg_acc_l20 = avg_acc_l20/datacount
    avg_acc_l30 = avg_acc_l30/datacount
    avg_acc_T10 = avg_acc_T10/datacount
    avg_acc_T5 = avg_acc_T5/datacount
    print ("   Avg           %6s  %.4f    %.4f    %.4f    %.4f    %.4f    %.4f" % (avg_nc, avg_acc_T5, avg_acc_T5, avg_acc_l30, avg_acc_l20, avg_acc_l10, avg_acc_l5))
    print ("")
    return (list_acc_T5, list_acc_T10, list_acc_l30, list_acc_l20, list_acc_l10, list_acc_l5)

def evaluate_prediction (dict_l, P, Y, min_seq_sep):
    P2 = floor_lower_left_to_zero(P, min_seq_sep)
    datacount = len(Y[:, 0])
    L = int(math.sqrt(len(Y[0, :])))
    Y1 = floor_lower_left_to_zero(Y, min_seq_sep)
    list_acc_l5 = []
    list_acc_l10 = []
    list_acc_l20 = []
    list_acc_l30 = []
    list_acc_T10 = []
    list_acc_T5 = []
    P3L5 = ceil_top_xL_to_one(dict_l, P2, Y, 0.2)
    P3L10 = ceil_top_xL_to_one(dict_l, P2, Y, 0.1)
    P3L20 = ceil_top_xL_to_one(dict_l, P2, Y, 0.05)
    P3L30 = ceil_top_xL_to_one(dict_l, P2, Y, 0.03)
    P3T10 = ceil_top_xL_to_one(dict_l, P2, Y, 10)
    P3T5 = ceil_top_xL_to_one(dict_l, P2, Y, 5)
    (list_acc_T5, list_acc_T10, list_acc_l30, list_acc_l20, list_acc_l10, list_acc_l5) = print_detailed_evaluations(dict_l, P3L5, P3L10, P3L20, P3L30, P3T10, P3T5, Y)
    return (list_acc_T5, list_acc_T10, list_acc_l30, list_acc_l20, list_acc_l10, list_acc_l5)

def get_x_from_this_list(selected_ids, path, l_max):
    xcount = len(selected_ids)
    sample_pdb = ''
    for pdb in selected_ids:
        sample_pdb = pdb
        break
    if not os.path.exists(path+"X-"+sample_pdb+".txt"):
        x = getX(path + 'feat-'  + sample_pdb + '.txt', l_max)
    else:
        x = getX(path + 'X-'  + sample_pdb + '.txt', l_max)
    
    F = len(x[0, 0, :])
    print ("L_max=",l_max)
    X = np.zeros((xcount, l_max, l_max, F))
    i = 0
    for pdb in sorted(selected_ids):
        if not os.path.exists(path+"X-"+pdb+".txt"):
            T = getX(path + 'feat-'  + pdb + '.txt', l_max)
        else:
            T = getX(path + 'X-'  + pdb + '.txt', l_max)
        #T = getX(path + 'X-'  + pdb + '.txt', l_max)
        if len(T[0, 0, :]) != F:
            print ('ERROR! Feature length of ' + sample_pdb + ' not equal to ' + pdb)
        X[i, :, :, :] = T
        i = i + 1
    return X

def get_y_from_this_list(selected_ids, path, min_seq_sep, l_max, y_dist):
    xcount = len(selected_ids)
    sample_pdb = ''
    for pdb in selected_ids:
        sample_pdb = pdb
        break
    y = getY(path + 'Y' + y_dist + '-' + sample_pdb + '.txt', min_seq_sep, l_max)
    if (l_max * l_max != len(y)):
        print ('Error!! y does not have L * L feature values!!')
        sys.exit()
    Y = np.zeros((xcount, l_max * l_max))
    i = 0
    for pdb in sorted(selected_ids):
        Y[i, :]       = getY(path + 'Y' + y_dist + '-' + pdb + '.txt', min_seq_sep, l_max)
        i = i + 1

    return Y

def getY(true_file, min_seq_sep, l_max):
    # calcualte the length of the protein (the first feature)
    L = 0
    with open(true_file) as f:
        for line in f:
            if line.startswith('#'):
                continue
            L = line.strip().split()
            L = len(L)
            break
    Y = np.zeros((l_max, l_max))
    i = 0
    with open(true_file) as f:
        for line in f:
            if line.startswith('#'):
                continue
            this_line = line.strip().split()
            Y[i, 0:L] = feature2D = np.asarray(this_line)
            i = i + 1
    #for p in range(0,L):
    #    for q in range(0,L):
            # updated only for the last project 'p19' to test the effect
    #        if ( abs(q - p) < min_seq_sep):
    #            Y[p][q] = 0
    Y = Y.flatten()
    if np.any(Y>1) or np.isnan(np.sum(Y)):
        os.system("echo '"+true_file+"' >> naninY.txt")
    return Y

def train_on_this_X_Y (model_arch, train_param, X, Y, prev_weights, out_file_weights):
    print ('')
    print ('X Train shape : ' + str(X.shape))
    print ('Y Train shape : ' + str(Y.shape))
    print ('')
    model = build_model_for_this_input_shape(model_arch, X)
    if os.path.isfile(prev_weights):
        print ('Loading previously saved weights..')
        print ('')
        model.load_weights(prev_weights)
    else:
        print (model.summary())
    print ('')
    print ('Compiling model..')
    model.compile(loss = 'binary_crossentropy', optimizer = train_param['optimizer'], metrics = ['accuracy'])
    print ('')
    print ('Fitting model..')
    model.fit(X, Y, verbose = 1, batch_size = train_param['batch_size'], epochs = train_param['inner_epochs'])
    model.save_weights(out_file_weights)

def get_x_from_this_file(feature_file, max_len=0):
    L = 0
    if max_len==0: 
        with open(feature_file) as f:
            for line in f:
                if line.startswith('#'):
                    continue
                L = line.strip().split()
                L = int(round(math.exp(float(L[0]))))
                max_len=L
                break
    #x = getX(feature_file, L)
    #F = len(x[0, 0, :])
    #X = np.zeros((1, L, L, F))
    x = getX(feature_file, max_len)
    F = len(x[0, 0, :])
    X = np.zeros((1, max_len, max_len, F))
    X[0, :, :, :] = x
    return X

def evaluate_on_this_X_Y (model_arch, file_weights, file_dict, X, Y, contact_selection, eval_type):
    model = build_model_for_this_input_shape(model_arch, X)
    model.load_weights(file_weights)
    P1 = model.predict(X)
    P2 = floor_lower_left_to_zero(P1, contact_selection)
    datacount = len(Y[:, 0])
    L = int(math.sqrt(len(Y[0, :])))
    Y1 = floor_lower_left_to_zero(Y, contact_selection)
    list_acc_l5 = []
    list_acc_l2 = []
    list_acc_1l = []
    if eval_type == 'top-nc':
        P3 = ceil_top_Nc_to_one(P2, Y1)
        avg_acc = print_detailed_evaluations_top_Nc(file_dict, P3, Y1)
    elif eval_type == 'top-l-all':
        P3L5 = ceil_top_xL_to_one(file_dict, P2, Y, 0.2)
        P3L2 = ceil_top_xL_to_one(file_dict, P2, Y, 0.5)
        P31L = ceil_top_xL_to_one(file_dict, P2, Y, 1)
        (list_acc_l5, list_acc_l2, list_acc_1l) = print_detailed_evaluations(file_dict, P3L5, P3L2, P31L, Y)
    elif eval_type == 'top-l5':
        P3 = ceil_top_L5_to_one(file_dict, P2, Y)
        avg_acc = print_detailed_evaluations_top_L5(file_dict, P3, Y)
    return (list_acc_l5, list_acc_l2, list_acc_1l)


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
    if np.isnan(np.sum(X)):
        os.system("echo '"+feature_file+"' >> naninX.txt")
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
#    model = DNCON2_net(inputs=X,filters=16,layers=6,kernel_size=5,act_func="relu",normalize="BatchNormalization")
    model = DNCON2_net(inputs=X,layers=6,filters=16,kernel_size=5,act_func="relu",normalize="BatchNormalize")
    print ("Loading weights...")
    model.load_weights(file_weights)
    print ("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&  The input shape for prediction is :", X.shape)
    P = model.predict(X,batch_size=1)
    return P

def make_prediction(model_arch, file_weights, X):
#    model_arch = build_model_for_this_input_shape(model_arch, X)
    if (file_weights!=None): model_arch.load_weights(file_weights)
    print ("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&  The input shape for prediction is :", X.shape)
    P = model_arch.predict(X)
    return P

def getX_2D_format(feature_file, cov, plm, plmc, pre, spa, netout, accept_list, pdb_len = 0, notxt_flag = True, logfile = None):
  # calcualte the length of the protein (the first feature)
#  print (feature_file)
  if logfile != None:
    chkdirs(logfile)

  L = 0
  Data = []
  feature_all_dict = dict()
  feature_index_all_dict = dict() # to make sure the feature are same ordered 
  feature_name='None'
  feature_index=0
  # print(reject_list)
  if notxt_flag == True:
    L = pdb_len
  else:
    with open(feature_file) as f:
      for line in f:
        if line.startswith('#'):
          continue
        L = line.strip().split()
        L = int(round(math.exp(float(L[0]))))
        break
    with open(feature_file) as f:
      accept_flag = 1
      for line in f:
        if line.startswith('#'):
          if line.strip() not in accept_list:
            accept_flag = 0
          else:
            accept_flag = 1
          feature_name = line.strip()
          continue
        if accept_flag == 0:
          continue
        
        if line.startswith('#'):
          continue
        this_line = line.strip().split()
        if len(this_line) == 0:
          continue
        if len(this_line) == 1:
          # 0D feature
          #continue
           feature_namenew = feature_name + ' 0D'
           feature_index +=1
           if feature_index in feature_index_all_dict:
             print("Duplicate feature name ",feature_namenew, " in file ",feature_file)
             exit;
           else:
             feature_index_all_dict[feature_index] = feature_namenew

           feature0D = np.zeros((L, L))
           feature0D[:, :] = float(this_line[0])
          # #feature0D = np.zeros((1, L))
          # #feature0D[0, :] = float(this_line[0])
          
           if feature_index in feature_all_dict:
             print("Duplicate feature name ",feature_namenew, " in file ",feature_file)
             exit;
           else:
             feature_all_dict[feature_index] = feature0D
        elif len(this_line) == L:
          # 1D feature
          # continue
          feature1D1 = np.zeros((L, L))
          feature1D2 = np.zeros((L, L))
          for i in range (0, L):
            feature1D1[i, :] = float(this_line[i])
            feature1D2[:, i] = float(this_line[i])
          
          ### load feature 1
          feature_index +=1
          feature_namenew = feature_name + ' 1D1'
          if feature_index in feature_index_all_dict:
            print("Duplicate feature name ",feature_namenew, " in file ",feature_file)
            exit;
          else:
            feature_index_all_dict[feature_index] = feature_namenew
          
          if feature_index in feature_all_dict:
            print("Duplicate feature name ",feature_namenew, " in file ",feature_file)
            exit;
          else:
            feature_all_dict[feature_index] = feature1D1
          
          ### load feature 2
          feature_index +=1
          feature_namenew = feature_name + ' 1D2'
          if feature_index in feature_index_all_dict:
            print("Duplicate feature name ",feature_namenew, " in file ",feature_file)
            exit;
          else:
            feature_index_all_dict[feature_index] = feature_namenew

          if feature_index in feature_all_dict:
            print("Duplicate feature name ",feature_namenew, " in file ",feature_file)
            exit;
          else:
            feature_all_dict[feature_index] = feature1D2
        elif len(this_line) == L * L:
          # 2D feature
          feature2D = np.asarray(this_line).reshape(L, L)
          feature_index +=1
          feature_namenew = feature_name + ' 2D'
          if feature_index in feature_index_all_dict:
            print("Duplicate feature name ",feature_namenew, " in file ",feature_file)
            exit
          else:
            feature_index_all_dict[feature_index] = feature_namenew
          
          if feature_index in feature_all_dict:
            print("Duplicate feature name ",feature_namenew, " in file ",feature_file)
            exit
          else:
            feature_all_dict[feature_index] = feature2D
        else:
          print (line)
          print ('Error!! Unknown length of feature in !!' + feature_file)
          print ('Expected length 0, ' + str(L) + ', or ' + str (L*L) + ' - Found ' + str(len(this_line)))
          sys.exit()
  #Add Covariance Matrix 
  if '# cov' in accept_list:   
      cov_rawdata = np.fromfile(cov, dtype=np.float32)
      length = int(math.sqrt(cov_rawdata.shape[0]/21/21))
      if length != L:
          print("Cov Bad Alignment, want %d get %d, pls check! %s" %(L, length, cov))
          if logfile != None:
            with open(logfile, "a") as myfile:
              myfile.write("Cov Bad Alignment, pls check! %s\n" %(cov))
            return False, False
          else:
            return False, False
            # sys.exit()
      inputs_cov = cov_rawdata.reshape(1,441,L,L) #????
      for i in range(441):
          feature2D = inputs_cov[0][i]
          feature_namenew = '# Covariance Matrix '+str(i+1)+ ' 2D'
          feature_index +=1
          if feature_index in feature_index_all_dict:
              print("Duplicate feature name ",feature_namenew, " in file ",feature_file)
              sys.exit()
          else:
              feature_index_all_dict[feature_index] = feature_namenew
          if feature_index in feature_all_dict:
              print("Duplicate feature name ",feature_namenew, " in file ",feature_file)
              sys.exit()
          else:
              feature_all_dict[feature_index] = feature2D
  #Add Pseudo_Likelihood Maximization
  if '# plm' in accept_list:  
      plm_rawdata = np.fromfile(plm, dtype=np.float32)
      length = int(math.sqrt(plm_rawdata.shape[0]/21/21))
      if length != L:
          print("Plm Bad Alignment, want %d get %d, pls check! %s" %(L, length, plm))
          if logfile != None:
            with open(logfile, "a") as myfile:
              myfile.write("Plm Bad Alignment, pls check! %s\n" %(plm))
            return False, False
          else:
            return False, False
            # sys.exit()
      inputs_plm = plm_rawdata.reshape(1,441,L,L)
      for i in range(441):
          feature2D = inputs_plm[0][i]
          feature_namenew = '# Pseudo_Likelihood Maximization '+str(i+1)+ ' 2D'
          feature_index +=1
          if feature_index in feature_index_all_dict:
              print("Duplicate feature name ",feature_namenew, " in file ",feature_file)
              sys.exit()
          else:
              feature_index_all_dict[feature_index] = feature_namenew
          if feature_index in feature_all_dict:
              print("Duplicate feature name ",feature_namenew, " in file ",feature_file)
              sys.exit()
          else:
              feature_all_dict[feature_index] = feature2D
  #Add Pseudo_Likelihood Maximization
  if '# plmc' in accept_list:  
      plmc_rawdata = np.fromfile(plmc, dtype=np.float32)
      length = int(math.sqrt(plmc_rawdata.shape[0]/21/21))
      if length != L:
          print("plmc Bad Alignment, want %d get %d, pls check! %s" %(L, length, plmc))
          if logfile != None:
            with open(logfile, "a") as myfile:
              myfile.write("plmc Bad Alignment, pls check! %s\n" %(plmc))
            return False, False
          else:
            return False, False
            # sys.exit()
      inputs_plmc = plmc_rawdata.reshape(1,441,L,L)
      for i in range(441):
          feature2D = inputs_plmc[0][i]
          feature_namenew = '# Pseudo_Likelihood Maximization '+str(i+1)+ ' 2D'
          feature_index +=1
          if feature_index in feature_index_all_dict:
              print("Duplicate feature name ",feature_namenew, " in file ",feature_file)
              sys.exit()
          else:
              feature_index_all_dict[feature_index] = feature_namenew
          if feature_index in feature_all_dict:
              print("Duplicate feature name ",feature_namenew, " in file ",feature_file)
              sys.exit()
          else:
              feature_all_dict[feature_index] = feature2D
  if '# pre' in accept_list:  
      pre_rawdata = np.fromfile(pre, dtype=np.float32)
      length = int(math.sqrt(pre_rawdata.shape[0]/21/21))
      if length != L:
          print("Pre Bad Alignment, want %d get %d, pls check! %s" %(L, length, pre))
          if logfile != None:
            with open(logfile, "a") as myfile:
              myfile.write("Pre Bad Alignment, pls check! %s\n" %(pre))
            return False, False
          else:
            return False, False
            # sys.exit()
      inputs_pre = pre_rawdata.reshape(1,441,L,L)
      for i in range(441):
          feature2D = inputs_pre[0][i]
          feature_namenew = '# Pre Maximization '+str(i+1)+ ' 2D'
          feature_index +=1
          if feature_index in feature_index_all_dict:
              print("Duplicate feature name ",feature_namenew, " in file ",feature_file)
              sys.exit()
          else:
              feature_index_all_dict[feature_index] = feature_namenew
          if feature_index in feature_all_dict:
              print("Duplicate feature name ",feature_namenew, " in file ",feature_file)
              sys.exit()
          else:
              feature_all_dict[feature_index] = feature2D
  if '# spa' in accept_list:  
      spa_rawdata = np.fromfile(spa, dtype=np.float32)
      length = int(math.sqrt(spa_rawdata.shape[0]/21/21))
      if length != L:
          print("spa Bad Alignment, want %d get %d, pls check! %s" %(L, length, spa))
          if logfile != None:
            with open(logfile, "a") as myfile:
              myfile.write("spa Bad Alignment, pls check! %s\n" %(spa))
            return False, False
          else:
            return False, False
            # sys.exit()
      inputs_spa = spa_rawdata.reshape(1,441,L,L)
      for i in range(441):
          feature2D = inputs_spa[0][i]
          feature_namenew = '# spa Maximization '+str(i+1)+ ' 2D'
          feature_index +=1
          if feature_index in feature_index_all_dict:
              print("Duplicate feature name ",feature_namenew, " in file ",feature_file)
              sys.exit()
          else:
              feature_index_all_dict[feature_index] = feature_namenew
          if feature_index in feature_all_dict:
              print("Duplicate feature name ",feature_namenew, " in file ",feature_file)
              sys.exit()
          else:
              feature_all_dict[feature_index] = feature2D
  if '# netout' in accept_list:
      netout_raw=np.load(netout)
      length = netout_raw.shape[0]
      chn = netout_raw.shape[-1]
      if length != L:
          print("Net Bad Alignment, pls check!")
          return False, False
          # sys.exit()
      inputs_netout =  netout_raw.transpose(2, 0, 1)
      inputs_netout =  inputs_netout.reshape(1,chn,L,L)
      for i in range(chn):
          feature2D = inputs_netout[0][i]
          feature_namenew = '# Network output '+str(i+1)+ ' 2D'
          feature_index +=1
          if feature_index in feature_index_all_dict:
              print("Duplicate feature name ",feature_namenew, " in file ",feature_file)
              sys.exit()
          else:
              feature_index_all_dict[feature_index] = feature_namenew
          if feature_index in feature_all_dict:
              print("Duplicate feature name ",feature_namenew, " in file ",feature_file)
              sys.exit()
          else:
              feature_all_dict[feature_index] = feature2D
#  print (feature_index_all_dict)
#  print ("Length of feature=",len(feature_index_all_dict))
  return (feature_all_dict,feature_index_all_dict)

def build_dataset_dictionaries_train(path_lists):
  length_dict = {}
  with open(path_lists + 'L.txt') as f:
    for line in f:
      cols = line.strip().split()
      length_dict[cols[0]] = int(cols[1])
  tr_l = {}
  with open(path_lists + 'train.lst') as f:
    for line in f:
      if line.strip() not in length_dict:
        continue
      else:
        tr_l[line.strip()] = length_dict[line.strip()]
  return (tr_l)


def data_generator_old(path_of_lists, path_of_X, path_of_Y, min_seq_sep,dist_string, batch_size, reject_fea_file='None', 
    child_list_index=0, list_sep_flag=False, dataset_select='train', feature_2D_num = 441, if_use_binsize=False, predict_method='bin_class', Maximum_length = 500):
    accept_list = []
    if reject_fea_file != 'None':
        with open(reject_fea_file) as f:
            for line in f:
                if line.startswith('#'):
                    feature_name = line.strip()
                    feature_name = feature_name[0:]
                    accept_list.append(feature_name)
    tr_l,te_l,tv_l=build_dataset_dictionaries(path_of_lists)
    if (dataset_select == 'train'):
        dataset_list = tr_l#build_dataset_dictionaries_train(path_of_lists)
    elif (dataset_select == 'vali'):
        dataset_list = tv_l#build_dataset_dictionaries_test(path_of_lists)
    else:
        dataset_list = te_l#build_dataset_dictionaries_train(path_of_lists)

    if (list_sep_flag == False):
        training_dict = subset_pdb_dict(dataset_list, 30, Maximum_length, 20000, 'random') #can be random ordered   
        training_list = list(training_dict.keys())
        training_lens = list(training_dict.values())
        all_data_num = len(training_dict)
        loopcount = all_data_num // int(batch_size)
        # print('crop_list_num=',all_data_num)
        # print('crop_loopcount=',loopcount)
    else:
        training_dict = subset_pdb_dict(dataset_list, 30, Maximum_length, 20000, 'ordered') #can be random ordered
        all_training_list = list(training_dict.keys())
        all_training_lens = list(training_dict.values())
        if ((child_list_index + 1) * 15 > len(training_dict)):
            print("Out of list range!\n")
            child_list_index = len(training_dict)/15 - 1
        child_batch_list = all_training_list[child_list_index * 15:(child_list_index + 1) * 15]
        child_batch_list_len = all_training_lens[child_list_index * 15:(child_list_index + 1) * 15]
        all_data_num = 15
        loopcount = all_data_num // int(batch_size)
        print('crop_list_num=',all_data_num)
        print('crop_loopcount=',loopcount)
        training_list = child_batch_list
        training_lens = child_batch_list_len
    index = 0
    while(True):
        #print ("Am I here!!!!!!!!!!!!!!!!!!!!")
        if index >= loopcount:
            training_dict = subset_pdb_dict(dataset_list, 0, Maximum_length, 20000, 'random') #can be random ordered   
            training_list = list(training_dict.keys())
            training_lens = list(training_dict.values())
            index = 0
        batch_list = training_list[index * batch_size:(index + 1) * batch_size]
        batch_list_len = training_lens[index * batch_size:(index + 1) * batch_size]
        index += 1
        # print(index, end='\t')
        if if_use_binsize:
            max_pdb_lens = Maximum_length
        else:
            max_pdb_lens = max(batch_list_len)

        data_all_dict = dict()
        batch_X=[]
        batch_Y=[]
        for i in range(0, len(batch_list)):
            pdb_name = batch_list[i]
            pdb_len = batch_list_len[i]
            notxt_flag = True
            featurefile =path_of_X + 'X-'  + pdb_name + '.txt'
            if not os.path.exists(featurefile): featurefile=featurefile =path_of_X + 'feat-'  + pdb_name + '.txt'
            if ((len(accept_list) == 1 and ('# cov' not in accept_list and '# plm' not in accept_list and '# pre' not in accept_list and '# spa' not in accept_list and '# netout' not in accept_list)) or 
                  (len(accept_list) == 2 and ('# cov' not in accept_list or '# plm' not in accept_list or '# pre' not in accept_list or '# spa' not in accept_list or '# netout' not in accept_list)) or (len(accept_list) > 2)):
                notxt_flag = False
                if not os.path.isfile(featurefile):
                    print("feature file not exists: ",featurefile, " pass!")
                    continue     
            cov = path_of_X + '/cov/' + pdb_name + '.cov'
            if '# cov' in accept_list:
                if not os.path.isfile(cov):
                    print("Cov Matrix file not exists: ",cov, " pass!")
                    continue        
            plm = path_of_X + '/plm/' + pdb_name + '.plm'
            if '# plm' in accept_list:
                if not os.path.isfile(plm):
                    print("plm matrix file not exists: ",plm, " pass!")
                    continue    
            plmc = path_of_X + '/plmc/' + pdb_name + '.plmc'
            if '# plmc' in accept_list:
                if not os.path.isfile(plmc):
                    print("plmc matrix file not exists: ",plmc, " pass!")
                    continue   
            pre = path_of_X + '/pre/' + pdb_name + '.pre'
            if '# pre' in accept_list:
                if not os.path.isfile(pre):
                    print("pre matrix file not exists: ",pre, " pass!")
                    continue
            spa = path_of_X + '/spa/' + pdb_name + '.spa'
            if '# spa' in accept_list:
                if not os.path.isfile(spa):
                    print("spa matrix file not exists: ",spa, " pass!")
                    continue
            netout = path_of_X + '/net_out/' + pdb_name + '.npy'
            if '# netout' in accept_list:      
                if not os.path.isfile(netout):
                    print("netout matrix file not exists: ",netout, " pass!")
                    continue 

            if predict_method == 'bin_class':       
                targetfile = path_of_Y + '/Y' + '-'+ pdb_name + '.txt'
                if not os.path.isfile(targetfile):
                        print("target file not exists: ",targetfile, " pass!")
                        continue  
            elif predict_method == 'mul_class':
                targetfile = path_of_Y + pdb_name + '.txt'
                if not os.path.isfile(targetfile):
                        print("target file not exists: ",targetfile, " pass!")
                        continue 
            elif predict_method == 'real_dist':
                targetfile = path_of_Y + pdb_name + '.txt'
                if not os.path.isfile(targetfile):
                        print("target file not exists: ",targetfile, " pass!")
                        continue  
            else:
                targetfile = path_of_Y + '/Y' + '-'+ pdb_name + '.txt'
                if not os.path.isfile(targetfile):
                        print("target file not exists: ",targetfile, " pass!")
                        continue

            (featuredata, feature_index_all_dict) = getX_2D_format(featurefile, cov, plm, plmc, pre, spa, netout, accept_list, pdb_len, notxt_flag)
            if featuredata == False or feature_index_all_dict == False:
                print("Bad alignment, Please check!\n")
                continue
            feature_2D_all = []
            for key in sorted(feature_index_all_dict.keys()):
                featurename = feature_index_all_dict[key]
                feature = featuredata[key]
                feature = np.asarray(feature)
                if feature.shape[0] == feature.shape[1]:
                    feature_2D_all.append(feature)
                else:
                    print("Wrong dimension")
            fea_len = feature_2D_all[0].shape[0]

            F = len(feature_2D_all)
            if F != feature_2D_num:
                print("Target %s has wrong feature shape! Continue!" % pdb_name)
                continue
            #X = np.zeros((max_pdb_lens, max_pdb_lens, F))
            X = np.zeros((max_pdb_lens, max_pdb_lens, F))
            for m in range(0, F):
                X[0:fea_len, 0:fea_len, m] = feature_2D_all[m]

            # X = np.memmap(cov, dtype=np.float32, mode='r', shape=(F, max_pdb_lens, max_pdb_lens))
            # X = X.transpose(1, 2, 0)

            l_max = max_pdb_lens
            if predict_method == 'bin_class':
                Y = getY(targetfile, min_seq_sep, l_max)
                if (l_max * l_max != len(Y)):
                    print('Error!! y does not have L * L feature values!!, pdb_name = %s'%(pdb_name))
                    continue
                #Y = Y.reshape(l_max, l_max, 1)
            elif predict_method == 'mul_class':
                print("Haven't has this function! quit!\n")
                sys.exit(1)
            elif predict_method == 'real_dist':
                Y = getY(targetfile, 0, l_max)
                if (l_max * l_max != len(Y)):
                    print('Error!! y does not have L * L feature values!!, pdb_name = %s'%(pdb_name))
                    continue
                Y = Y.reshape(l_max, l_max, 1)
                # real_dist is different with bin class, bin out is l*l vector, real dist out is (l,l) matrix
                # Y = getY_dist(targetfile, 0, l_max)
                # if (l_max != len(Y)):
                #     print('Error!! y does not have L * L feature values!!, pdb_name = %s'%(pdb_name))
                #     print('len(Y) = %d, lmax = %d'%(len(Y), l_max))
                #     continue
            batch_X.append(X)
            batch_Y.append(Y)
            del X
            del Y
        batch_X =  np.array(batch_X)
        batch_Y =  np.array(batch_Y)
        print ("############# out here ##############")
        # print('X shape\n', batch_X.shape)
        # print('Y shape', batch_Y.shape)
        if len(batch_X.shape) < 4 or len(batch_Y.shape) < 4:
            # print('Data shape error, pass!\n')
            continue
        yield batch_X, batch_Y
    print ("No way out#$#$#$#$#$#$#$#$")


def data_generator(data_dict,path_of_lists, path_of_X, path_of_Y, min_seq_sep,dist_string, batch_size, reject_fea_file='None', 
    child_list_index=0, list_sep_flag=False, dataset_select='train', feature_2D_num = 441, if_use_binsize=False, predict_method='bin_class', Maximum_length = 500):
    accept_list = []
    if reject_fea_file != 'None':
        with open(reject_fea_file) as f:
            for line in f:
                if line.startswith('#'):
                    feature_name = line.strip()
                    feature_name = feature_name[0:]
                    accept_list.append(feature_name)
    tr_l,te_l,tv_l=build_dataset_dictionaries(path_of_lists)
    if (dataset_select == 'train'):
        dataset_list = tr_l#build_dataset_dictionaries_train(path_of_lists)
    elif (dataset_select == 'vali'):
        dataset_list = tv_l#build_dataset_dictionaries_test(path_of_lists)
    else:
        dataset_list = te_l#build_dataset_dictionaries_train(path_of_lists)
    dataset_list=data_dict
#    print (len(data_dict))
    if (list_sep_flag == False):
        training_dict = data_dict #subset_pdb_dict(dataset_list, 30, Maximum_length, 20000, 'random') #can be random ordered   
        training_list = list(training_dict.keys())
        training_lens = list(training_dict.values())
        all_data_num = len(training_dict)
        loopcount = all_data_num // int(batch_size)
        # print('crop_list_num=',all_data_num)
        # print('crop_loopcount=',loopcount)
    else:
        training_dict = data_dict #subset_pdb_dict(dataset_list, 30, Maximum_length, 20000, 'ordered') #can be random ordered
        all_training_list = list(training_dict.keys())
        all_training_lens = list(training_dict.values())
        if ((child_list_index + 1) * 15 > len(training_dict)):
            print("Out of list range!\n")
            child_list_index = len(training_dict)/15 - 1
        child_batch_list = all_training_list[child_list_index * 15:(child_list_index + 1) * 15]
        child_batch_list_len = all_training_lens[child_list_index * 15:(child_list_index + 1) * 15]
        all_data_num = 15
        loopcount = all_data_num // int(batch_size)
        print('crop_list_num=',all_data_num)
        print('crop_loopcount=',loopcount)
        training_list = child_batch_list
        training_lens = child_batch_list_len
    index = 0
    while(True):
#        print ("Am I here!!!!!!!!!!!!!!!!!!!!")
        if index >= loopcount:
            training_dict = data_dict #subset_pdb_dict(dataset_list, 0, Maximum_length, 20000, 'random') #can be random ordered   
            training_list = list(training_dict.keys())
            training_lens = list(training_dict.values())
            index = 0
        batch_list = training_list[index * batch_size:(index + 1) * batch_size]
        batch_list_len = training_lens[index * batch_size:(index + 1) * batch_size]
        index += 1
        # print(index, end='\t')
        if if_use_binsize:
            max_pdb_lens = Maximum_length
        else:
            max_pdb_lens = max(batch_list_len)

        data_all_dict = dict()
        batch_X=[]
        batch_Y=[]
#        print ("Loop_count=",loopcount," Index=",index," len(batch_list)=",len(batch_list)," batch_size=",batch_size)
        for i in range(0, len(batch_list)):
            pdb_name = batch_list[i]
            pdb_len = batch_list_len[i]
            notxt_flag = True
            featurefile =path_of_X + 'X-'  + pdb_name + '.txt'
            if not os.path.exists(featurefile): featurefile=featurefile =path_of_X + 'feat-'  + pdb_name + '.txt'
            if ((len(accept_list) == 1 and ('# cov' not in accept_list and '# plm' not in accept_list and '# pre' not in accept_list and '# spa' not in accept_list and '# netout' not in accept_list)) or 
                  (len(accept_list) == 2 and ('# cov' not in accept_list or '# plm' not in accept_list or '# pre' not in accept_list or '# spa' not in accept_list or '# netout' not in accept_list)) or (len(accept_list) > 2)):
                notxt_flag = False
                if not os.path.isfile(featurefile):
                    print("feature file not exists: ",featurefile, " pass!")
                    continue     
            cov = path_of_X + '/cov/' + pdb_name + '.cov'
            if '# cov' in accept_list:
                if not os.path.isfile(cov):
                    print("Cov Matrix file not exists: ",cov, " pass!")
                    continue        
            plm = path_of_X + '/plm/' + pdb_name + '.plm'
            if '# plm' in accept_list:
                if not os.path.isfile(plm):
                    print("plm matrix file not exists: ",plm, " pass!")
                    continue    
            plmc = path_of_X + '/plmc/' + pdb_name + '.plmc'
            if '# plmc' in accept_list:
                if not os.path.isfile(plmc):
                    print("plmc matrix file not exists: ",plmc, " pass!")
                    continue   
            pre = path_of_X + '/pre/' + pdb_name + '.pre'
            if '# pre' in accept_list:
                if not os.path.isfile(pre):
                    print("pre matrix file not exists: ",pre, " pass!")
                    continue
            spa = path_of_X + '/spa/' + pdb_name + '.spa'
            if '# spa' in accept_list:
                if not os.path.isfile(spa):
                    print("spa matrix file not exists: ",spa, " pass!")
                    continue
            netout = path_of_X + '/net_out/' + pdb_name + '.npy'
            if '# netout' in accept_list:      
                if not os.path.isfile(netout):
                    print("netout matrix file not exists: ",netout, " pass!")
                    continue 

            if predict_method == 'bin_class':       
                targetfile = path_of_Y + '/Y' + '-'+ pdb_name + '.txt'
                if not os.path.isfile(targetfile):
                        print("target file not exists: ",targetfile, " pass!")
                        continue  
            elif predict_method == 'mul_class':
                targetfile = path_of_Y + pdb_name + '.txt'
                if not os.path.isfile(targetfile):
                        print("target file not exists: ",targetfile, " pass!")
                        continue 
            elif predict_method == 'real_dist':
                targetfile = path_of_Y + pdb_name + '.txt'
                if not os.path.isfile(targetfile):
                        print("target file not exists: ",targetfile, " pass!")
                        continue  
            else:
                targetfile = path_of_Y + '/Y' + '-'+ pdb_name + '.txt'
                if not os.path.isfile(targetfile):
                        print("target file not exists: ",targetfile, " pass!")
                        continue

            (featuredata, feature_index_all_dict) = getX_2D_format(featurefile, cov, plm, plmc, pre, spa, netout, accept_list, pdb_len, notxt_flag)
            if featuredata == False or feature_index_all_dict == False:
                print("Bad alignment, Please check!\n")
                continue
            feature_2D_all = []
#            print (feature_index_all_dict.keys())
            for key in sorted(feature_index_all_dict.keys()):
                featurename = feature_index_all_dict[key]
                feature = featuredata[key]
                feature = np.asarray(feature)
                if feature.shape[0] == feature.shape[1]:
                    feature_2D_all.append(feature)
                else:
                    print("Wrong dimension")
            fea_len = feature_2D_all[0].shape[0]

            F = len(feature_2D_all)
#            print ("F=",F)
#            print ("feature_2D_all.shape=",feature_2D_all[0].shape)
            if F != feature_2D_num:
                print("Target %s has wrong feature shape! Continue!" % pdb_name)
                continue
            #X = np.zeros((max_pdb_lens, max_pdb_lens, F))
            X = np.zeros((max_pdb_lens, max_pdb_lens, F))
            for m in range(0, F):
                X[0:fea_len, 0:fea_len, m] = feature_2D_all[m]

            # X = np.memmap(cov, dtype=np.float32, mode='r', shape=(F, max_pdb_lens, max_pdb_lens))
            # X = X.transpose(1, 2, 0)

            l_max = max_pdb_lens
            if predict_method == 'bin_class':
                Y = getY(targetfile, min_seq_sep, l_max)
                if (l_max * l_max != len(Y)):
                    print('Error!! y does not have L * L feature values!!, pdb_name = %s'%(pdb_name))
                    continue
                #Y = Y.reshape(l_max, l_max, 1)
            elif predict_method == 'mul_class':
                print("Haven't has this function! quit!\n")
                sys.exit(1)
            elif predict_method == 'real_dist':
                Y = getY(targetfile, 0, l_max)
                if (l_max * l_max != len(Y)):
                    print('Error!! y does not have L * L feature values!!, pdb_name = %s'%(pdb_name))
                    continue
                Y = Y.reshape(l_max, l_max, 1)
                # real_dist is different with bin class, bin out is l*l vector, real dist out is (l,l) matrix
                # Y = getY_dist(targetfile, 0, l_max)
                # if (l_max != len(Y)):
                #     print('Error!! y does not have L * L feature values!!, pdb_name = %s'%(pdb_name))
                #     print('len(Y) = %d, lmax = %d'%(len(Y), l_max))
                #     continue
        if np.any(Y>1) or np.isnan(np.sum(Y)):
            os.system("echo '"+pdb_name+"' >> naninY.txt")
            del X, Y
            continue
        if np.isnan(np.sum(X)):
            os.system("echo '"+pdb_name+"' >> naninX.txt")
            del X, Y
            continue
        batch_X.append(X)
        batch_Y.append(Y)
        del X
        del Y
        batch_X =  np.array(batch_X)
        batch_Y =  np.array(batch_Y)
#        print ("############# out here ##############")
        # print('X shape\n', batch_X.shape)
        # print('Y shape', batch_Y.shape)
#        print ("batch_X.shape=",batch_X.shape," batch_Y.shape=",batch_Y.shape)
#        print ("lengths of batches=",len(batch_X),len(batch_Y))
        if len(batch_X.shape) < 4 or len(batch_Y.shape) < 2:
            # print('Data shape error, pass!\n')
            continue
        
        yield batch_X, batch_Y
#    print ("No way out#$#$#$#$#$#$#$#$")
