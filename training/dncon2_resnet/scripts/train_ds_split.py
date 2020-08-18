#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 01:10:42 2020

@author: farhan
"""

import shutil
import sys, os
project_root = os.path.abspath(sys.argv[0]).rstrip(sys.argv[0]).rstrip("scripts/")
if not project_root.endswith("/"): project_root+="/"
sys.path.insert(0, project_root + "lib")
from libtrain import *
import numpy as np

print ("Project Root Directory: ",project_root)

def print_detailed_accuracy_on_this_data(id_string, file_weights):
    print ('')
    all_list_acc_l5 = []
    all_list_acc_l10 = []
    all_list_acc_l20 = []
    all_list_acc_l30 = []
    all_list_acc_T10 = []
    all_list_acc_T5 = []
    for group in range(0, 3):
        L = LTR1
        X = XTR1
        Y = YTR1
        if 'TRAIN' in id_string:
            if 'VAL' in id_string:
                XTR1=XTV1
                YTR1=YTV1
                LTR1=LTV1
                XTR2=XTV2
                YTR2=YTV2
                LTR2=LTV2
                XTR3=XTV3
                YTR3=YTV3
                LTR3=LTV3
            print ('Printing detailed results for TRAIN group ' + str(group))
            if group == 0:
                P = make_prediction(model_arch, file_weights, XTR1)
                (list_acc_T5, list_acc_T10, list_acc_l30, list_acc_l20, list_acc_l10, list_acc_l5) = evaluate_prediction(LTR1, P, YTR1, 0)
                all_list_acc_l5.extend(list_acc_l5)
                all_list_acc_l10.extend(list_acc_l10)
                all_list_acc_l20.extend(list_acc_l20)
                all_list_acc_l30.extend(list_acc_l30)
                all_list_acc_T10.extend(list_acc_T10)
                all_list_acc_T5.extend(list_acc_T5)
            if group == 1:
                P = make_prediction(model_arch, file_weights, XTR2)
                (list_acc_T5, list_acc_T10, list_acc_l30, list_acc_l20, list_acc_l10, list_acc_l5) = evaluate_prediction(LTR2, P, YTR2, 0)
                all_list_acc_l5.extend(list_acc_l5)
                all_list_acc_l10.extend(list_acc_l10)
                all_list_acc_l20.extend(list_acc_l20)
                all_list_acc_l30.extend(list_acc_l30)
                all_list_acc_T10.extend(list_acc_T10)
                all_list_acc_T5.extend(list_acc_T5)
            if group == 2:
                P = make_prediction(model_arch, file_weights, XTR3)
                (list_acc_T5, list_acc_T10, list_acc_l30, list_acc_l20, list_acc_l10, list_acc_l5) = evaluate_prediction(LTR3, P, YTR3, 0)
                all_list_acc_l5.extend(list_acc_l5)
                all_list_acc_l10.extend(list_acc_l10)
                all_list_acc_l20.extend(list_acc_l20)
                all_list_acc_l30.extend(list_acc_l30)
                all_list_acc_T10.extend(list_acc_T10)
                all_list_acc_T5.extend(list_acc_T5)
        if 'TEST' in id_string:
            print ('Printing detailed results for TEST group ' + str(group))
            if group == 0:
                P = make_prediction(model_arch, file_weights, XTE1)
                (list_acc_T5, list_acc_T10, list_acc_l30, list_acc_l20, list_acc_l10, list_acc_l5) = evaluate_prediction(LTE1, P, YTE1, 0)
                all_list_acc_l5.extend(list_acc_l5)
                all_list_acc_l10.extend(list_acc_l10)
                all_list_acc_l20.extend(list_acc_l20)
                all_list_acc_l30.extend(list_acc_l30)
                all_list_acc_T10.extend(list_acc_T10)
                all_list_acc_T5.extend(list_acc_T5)
            if group == 1:
                P = make_prediction(model_arch, file_weights, XTE2)
                (list_acc_T5, list_acc_T10, list_acc_l30, list_acc_l20, list_acc_l10, list_acc_l5) = evaluate_prediction(LTE2, P, YTE2, 0)
                all_list_acc_l5.extend(list_acc_l5)
                all_list_acc_l10.extend(list_acc_l10)
                all_list_acc_l20.extend(list_acc_l20)
                all_list_acc_l30.extend(list_acc_l30)
                all_list_acc_T10.extend(list_acc_T10)
                all_list_acc_T5.extend(list_acc_T5)
            if group == 2:
                P = make_prediction(model_arch, file_weights, XTE3)
                (list_acc_T5, list_acc_T10, list_acc_l30, list_acc_l20, list_acc_l10, list_acc_l5) = evaluate_prediction(LTE3, P, YTE3, 0)
                all_list_acc_l5.extend(list_acc_l5)
                all_list_acc_l10.extend(list_acc_l10)
                all_list_acc_l20.extend(list_acc_l20)
                all_list_acc_l30.extend(list_acc_l30)
                all_list_acc_T10.extend(list_acc_T10)
                all_list_acc_T5.extend(list_acc_T5)
    acc_l5 = sum(all_list_acc_l5) / len(all_list_acc_l5)
    acc_l10 = sum(all_list_acc_l10) / len(all_list_acc_l10)
    acc_l20 = sum(all_list_acc_l20) / len(all_list_acc_l20)
    acc_l30 = sum(all_list_acc_l30) / len(all_list_acc_l30)
    acc_lT10 = sum(all_list_acc_T10) / len(all_list_acc_T10)
    acc_lT5 = sum(all_list_acc_T5) / len(all_list_acc_T5)
    print ('----------------------------------------------------------------------------------------------')
    print ('Cycle DataSet      Acc-L/5  Acc-L/2  Acc-L')
    print ('' + id_string + ' %.3f    %.3f    %.3f    %.3f    %.3f    %.3f' %(acc_T5, acc_T10, acc_l30, acc_l20, acc_l10, acc_l5))
    print ('----------------------------------------------------------------------------------------------')
    return (acc_T5, acc_T10, acc_l30, acc_l20, acc_l10, acc_l5)

def print_feature_summary(X):
    print ('FeatID         Avg        Med        Max        Sum        Avg[30]    Med[30]    Max[30]    Sum[30]')
    for ii in range(0, len(X[0, 0, 0, :])):
        (m,s,a,d) = (X[0, :, :, ii].flatten().max(), X[0, :, :, ii].flatten().sum(), X[0, :, :, ii].flatten().mean(), np.median(X[0, :, :, ii].flatten()))
        (m30,s30,a30, d30) = (X[0, 30, :, ii].flatten().max(), X[0, 30, :, ii].flatten().sum(), X[0, 30, :, ii].flatten().mean(), np.median(X[0, 30, :, ii].flatten()))
        print (' Feat%2s %10.4f %10.4f %10.4f %10.1f     %10.4f %10.4f %10.4f %10.4f' %(ii, a, d, m, s, a30, d30, m30, s30))

def next_group(current_group):
    if current_group == 0:
        return 1
    if current_group == 1:
        return 2
    if current_group == 2:
        return 0

dist_string = sys.argv[1]
dist_string=""
pathX = os.path.abspath(sys.argv[2])+"/" #/data/farhan/SoftwareTools/HomopolymerProject/data/homodimers/feat
pathY = os.path.abspath(sys.argv[3])+"/" #/data/farhan/SoftwareTools/HomopolymerProject/data/homodimers/scripts/Y-Labels
path_lists = os.path.abspath(sys.argv[4])+"/" #'/home/bap54/data/DNcon2-data/lists-test-train/'

print ('')
print ('Parameters:')
print('dist_string   ' + dist_string)
print('pathX         ' + pathX)
print('pathY         ' + pathY)
print ('')

model_arch = read_model_arch(project_root + 'scripts/model-arch.config')
train_param = read_train_param(project_root + 'scripts/train-param.config')
train_l, test_l, val_l = build_dataset_dictionaries(path_lists)
#print (len (train_l), len (test_l), len(val_l))

# Make combined dictionaries as well
all_l = train_l.copy()
all_l.update(test_l)
all_l.update(val_l)
print ('Total Number of Training and Test dataset = ' + str(len(all_l)))
maxLengthinDataset=max(all_l.values())
print ("All=",max(all_l.values()))
print("Test=",max(test_l.values()))
print("Val=",max(val_l.values()))
#sys.exit()
print ('Loading all Training data into memory..')
#Retrieve a dictionary of IDS to train: minL to maxL, count=1000, randomly or sequentially 
#Modify to select all data: maxL=maxLengthinDataset, count=len(tr_l)
LTR1 = subset_pdb_dict(train_l,   0, 1000, 1, 'random')
LTR2 = subset_pdb_dict(train_l, 1000, 2000, 1, 'random')
LTR3 = subset_pdb_dict(train_l, 2000, 3050, 1, 'random')
print ('Loading sets X1, X2, and X3..')
XTR1 = get_x_from_this_list(LTR1, pathX, 1000)
XTR2 = get_x_from_this_list(LTR2, pathX, 2000)
XTR3 = get_x_from_this_list(LTR3, pathX, 3050)
print ('Loading Y1, Y2, and Y3 ..')
YTR1 = get_y_from_this_list(LTR1, pathY, 0, 1000, dist_string)
YTR2 = get_y_from_this_list(LTR2, pathY, 0, 2000, dist_string)
YTR3 = get_y_from_this_list(LTR3, pathY, 0, 3050, dist_string)

sys.stdout.flush()
print ('Load Validation data into memory..')
LTV1 = subset_pdb_dict(val_l,   0, 1000, 1, 'ordered')
LTV2 = subset_pdb_dict(val_l, 1000, 2000, 1, 'ordered')
LTV3 = subset_pdb_dict(val_l, 2000, 3050, 1, 'ordered')
print ('Loading sets X1, X2, and X3..')
XTV1 = get_x_from_this_list(LTV1, pathX, 1000)
XTV2 = get_x_from_this_list(LTV2, pathX, 2000)
XTV3 = get_x_from_this_list(LTV3, pathX, 3050)
print ('Loading Y1, Y2, and Y3 ..')
YTV1 = get_y_from_this_list(LTV1, pathY, 24, 1000, dist_string)
YTV2 = get_y_from_this_list(LTV2, pathY, 24, 2000, dist_string)
YTV3 = get_y_from_this_list(LTV3, pathY, 24, 3050, dist_string)

sys.stdout.flush()
print ('Load Test data into memory..')
LTE1 = subset_pdb_dict(test_l,   0, 1000, 1, 'ordered')
LTE2 = subset_pdb_dict(test_l, 1000, 2000, 1, 'ordered')
LTE3 = subset_pdb_dict(test_l, 2000, 3050, 1, 'ordered')
print ('Loading sets X1, X2, and X3..')
XTE1 = get_x_from_this_list(LTE1, pathX, 1000)
XTE2 = get_x_from_this_list(LTE2, pathX, 2000)
XTE3 = get_x_from_this_list(LTE3, pathX, 3050)
print ('Loading Y1, Y2, and Y3 ..')
YTE1 = get_y_from_this_list(LTE1, pathY, 24, 1000, dist_string)
YTE2 = get_y_from_this_list(LTE2, pathY, 24, 2000, dist_string)
YTE3 = get_y_from_this_list(LTE3, pathY, 24, 3050, dist_string)

# cycle the training groups during training

os.system('rm -f *.hdf5')
group = 0

for cyc in range (0, train_param['outer_epochs']):
    sys.stdout.flush()
    if cyc % 40 == 0:
        if os.path.exists('./weights.hdf5'):
            print ('')
            print ('Reached 40 epochs, removing weights file to flush learning..')
            os.remove('./weights.hdf5')
    if os.path.exists('./cycle-' + str(cyc) + '.hdf5'):
        print ('Skipping ' + 'cycle-' + str(cyc) + '.hdf5 ..')
        continue
    X = XTR1
    Y = YTR1
    if group == 1:
        X = XTR2
        Y = YTR2
    if group == 2:
        X = XTR3
        Y = YTR3
    if cyc == 0:
        print_feature_summary(X)
    print ('')
    print ('Group : ' + str(group))
    print ('Cycle : ' + str(cyc) + ' of ' + str(train_param['outer_epochs']))
    train_on_this_X_Y(model_arch, train_param, X, Y, './weights.hdf5')
    print ('')
    print ('Save the weights & model for this cycle..')
    shutil.copy2('./weights.hdf5', './cycle-' + str(cyc) + '.hdf5')
    group = next_group(group)
    print ('')
    cyc_id = str(cyc)
    cyc_id = cyc_id.rjust(5, '0')
    print ('Evaluate on Training data..')
    (acc_T5, acc_T10, acc_l30, acc_l20, acc_l10, acc_l5)=print_detailed_accuracy_on_this_data(cyc_id + ' SAMPLE-TRAIN', './cycle-' + str(cyc) + '.hdf5')
    with open ("training_acc.txt","a+") as f:
        epoch = cyc
        if (epoch == 0):
            f.write("Epoch\tPrec-T5\PrecT10\tL/30\tL/20/tL/10\tL/10\tL/5\n")
        f.wrtie(str(epoch)+"\t"+str(round(acc_T5,4))+"\t"+str(round(acc_T10,4))+"\t"+str(round(acc_l30,4))+"\t"+str(round(acc_l20,4))+"\t"+str(round(acc_l10,4))+"\t"+str(round(acc_l5,4))+"\n")
        
    print ('Evaluate on Validation data..')
    (acc_T5, acc_T10, acc_l30, acc_l20, acc_l10, acc_l5)=print_detailed_accuracy_on_this_data(cyc_id + ' VAL-TRAIN', './cycle-' + str(cyc) + '.hdf5')
    with open ("validation_acc.txt","a+") as f:
        epoch = cyc
        if (epoch == 0):
            f.write("Epoch\tPrec-T5\PrecT10\tL/30\tL/20/tL/10\tL/10\tL/5\n")
        f.wrtie(str(epoch)+"\t"+str(round(acc_T5,4))+"\t"+str(round(acc_T10,4))+"\t"+str(round(acc_l30,4))+"\t"+str(round(acc_l20,4))+"\t"+str(round(acc_l10,4))+"\t"+str(round(acc_l5,4))+"\n")
    print ('Evaluate on full Test data..')
    (acc_T5, acc_T10, acc_l30, acc_l20, acc_l10, acc_l5)=print_detailed_accuracy_on_this_data(cyc_id + ' ALL-TEST    ', './cycle-' + str(cyc) + '.hdf5')
    with open ("testing_acc.txt","a+") as f:
        epoch = cyc
        if (epoch == 0):
            f.write("Epoch\tPrec-T5\PrecT10\tL/30\tL/20/tL/10\tL/10\tL/5\n")
        f.wrtie(str(epoch)+"\t"+str(round(acc_T5,4))+"\t"+str(round(acc_T10,4))+"\t"+str(round(acc_l30,4))+"\t"+str(round(acc_l20,4))+"\t"+str(round(acc_l10,4))+"\t"+str(round(acc_l5,4))+"\n")

