#!/usr/bin/python
# Badri Adhikari, 6-15-2017
# Modified by Farhan Quadir, 05-20-2020
# Subroutines used in training and testing

import shutil
from libcommon import * 
from Model_lib import *
import os, sys, math
import numpy as np
#import random

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

# Floor everything below the triangle of interest to zero
def floor_lower_left_to_zero(XP, min_seq_sep):
    X = np.copy(XP)
    datacount = len(X[:, 0])
    L = int(math.sqrt(len(X[0, :])))
    X_reshaped = X.reshape(datacount, L, L)
    """
    for p in range(0,L):
        for q in range(0,L):
            if ( q - p < min_seq_sep):
                X_reshaped[:, p, q] = 0
    """
    X = X_reshaped.reshape(datacount, L * L)
    return X

# Ceil top xL predictions to 1, others to zero
def ceil_top_xL_to_one(ref_file_dict, XP, Y, x):
    X_ceiled = np.copy(XP)
    i = -1
    for pdb in sorted(ref_file_dict):
        i = i + 1
        if x<1 : 
            xL = int(x * ref_file_dict[pdb])
        else:
            xL=int(x)
        X_ceiled[i, :] = np.zeros(len(XP[i, :]))
        X_ceiled[i, np.argpartition(XP[i, :], -xL)[-xL:]] = 1
    return X_ceiled

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
            if (dict[pdb] > minL and dict[pdb] <= maxL):
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
    return Y

def train_on_this_X_Y (model_arch, train_param, X, Y, prev_weights, out_file_weights):
    print ('')
    print ('X Train shape : ' + str(X.shape))
    print ('Y Train shape : ' + str(Y.shape))
    print ('')
    model = DNCON2_net(inputs=X,filters=16,layers=6,kernel_size=5,act_func="relu",normalize="BatchNormalization")
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

def get_x_from_this_file(feature_file):
	L = 0
	with open(feature_file) as f:
		for line in f:
			if line.startswith('#'):
				continue
			L = line.strip().split()
			L = int(round(math.exp(float(L[0]))))
			break
	x = getX(feature_file, L)
	F = len(x[0, 0, :])
	X = np.zeros((1, L, L, F))
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
