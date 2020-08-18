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
from glob import glob
#from Label2cmap import toCmap

print ("Project Root Directory: ",project_root)

def toCmap(arr,fasta_file):
    l=arr.shape[0]
    l=int(np.sqrt(l))
    arr=arr.reshape(l,l)
    #print ("$$$$$$$$$ Length = ",l, "Shape=",arr.shape)
    cmap=[]
    for i in range(l):
        for j in range(l):
            if arr[i][j]!=0:
                cmap.append(str(i+1)+" "+str(j+1)+" 0 6.0 "+str(arr[i][j])+"\n")
    #print (cmap)
    cmap[-1]=cmap[-1].rstrip()
    fasta=""
    with open (fasta_file,"r") as f:
        for line in f:
            if line.startswith(">"): continue
            fasta+=line.strip()
    cmap.insert(0,fasta.strip()+"\n")
    return cmap

def calculateEvaluationStats(pred_cmap, true_cmap, name):
    prec_T5=0
    prec_T10=0
    prec_L30=0
    prec_L20=0
    prec_L10=0
    prec_L5=0
    #print ("Name: ", name, " True_shape=",true_cmap.shape," Pred_shape=",pred_cmap.shape)
    pred_cmap=pred_cmap.squeeze()
    #print ("Name: ", name, " True_shape=",true_cmap.shape," Pred_shape=",pred_cmap.shape)
    #l=int(np.sqrt(len(true_cmap)))
    #pred_cmap=toCmap(pred_cmap.reshape(l,l))
    #true_cmap=toCmap(true_cmap.reshape(l,l))
    #pred_cmap=pred_cmap.reshape(l,l)
    #true_cmap=true_cmap.reshape(l,l)
    #np.savetxt(project_root+"pred_cmap.rr",pred_cmap)
    fasta_folder="/data/farhan/SoftwareTools/HomopolymerProject/data/homodimers/scripts/final_training_set_04_13_2020/all_same_fastas/"#"/data/farhan/SoftwareTools/HomopolymerProject/data/homodimers/scripts/final_training_set_04_13_2020/fastas/"
    np.savetxt(project_root+"true_cmap.rr",true_cmap)
    pred_cmap=toCmap(pred_cmap,fasta_folder+name+".fasta")
    with open (project_root+"pred_cmap.rr","w") as f:
        f.writelines(pred_cmap)
    #os.system("python "+project_root+"lib/conevainter_usingY_Labels.py "+project_root+"true_cmap.rr "+project_root+"pred_cmap.rr")
    #print ("python "+project_root+"lib/conevainter_usingY_Labels.py "+project_root+"true_cmap.rr "+project_root+"pred_cmap.rr > "+project_root+"temp_prec.txt")
    os.system("python "+project_root+"lib/conevainter_usingY_Labels.py "+project_root+"true_cmap.rr "+project_root+"pred_cmap.rr "+fasta_folder+name+".fasta")
    os.system("python "+project_root+"lib/conevainter_usingY_Labels.py "+project_root+"true_cmap.rr "+project_root+"pred_cmap.rr "+fasta_folder+name+".fasta > "+project_root+"temp_prec.txt")
    #with open (project_root+"temp_prec.txt","r") as f:
    """
    #np.savetxt(project_root+name+"_true_cmap.rr",true_cmap)
    np.savetxt(project_root+name+"_true_cmap.rr",true_cmap)
    pred_cmap=toCmap(pred_cmap)
    #pred_cmap=toCmap(true_cmap.flatten())
    with open (project_root+name+"_pred_cmap.rr","w") as f:
        f.writelines(pred_cmap)
    os.system("python "+project_root+"/lib/conevainter_usingY_Labels.py "+project_root+name+"_true_cmap.rr "+project_root+name+"_pred_cmap.rr > "+project_root+name+"_temp_prec.txt")
    """
    with open (project_root+"temp_prec.txt","r") as f:
        for line in f:
            if line.strip().startswith("Name"): 
                line=f.readline()
                #print ("Prediction: "+name+"\t"+line)
                split=line.strip().split()
                prec_T5=float(split[2])
                prec_T10=float(split[3])
                prec_L30=float(split[4])
                prec_L20=float(split[5])
                prec_L10=float(split[6])
                prec_L5=float(split[7])
                break
            
    return (prec_T5,prec_T10,prec_L30,prec_L20,prec_L10,prec_L5)

def evaluate(LTR, model_arch, file_weights,pathX,pathY):
    
    list_acc_T5 =[]
    list_acc_T10 =[] 
    list_acc_l30 =[]
    list_acc_l20 =[]
    list_acc_l10 =[]
    list_acc_l5 =[]
    datacount=len(LTR)
    key_list=list(LTR.keys())
    #if datacount!=len(P): print ("Predictions and True Labels do not match!")
    for key in key_list:
        L=LTR[key]
        feat_file_name=pathX+"feat-"+key+".txt"
        label_file=pathY+"Y-"+key+".txt"
        print ("Getting Labels for "+key)
        Y=np.loadtxt(label_file)
        print ("Getting X-features for "+key)
        X=get_x_from_this_file(feat_file_name)
        print ("Making predictions for: "+key)
        P=make_prediction(model_arch, file_weights, X)
        (prec_T5,prec_T10,prec_L30,prec_L20,prec_L10,prec_L5)=calculateEvaluationStats(P, Y,key)
        list_acc_T5.append(prec_T5)
        list_acc_T10.append(prec_T10)
        list_acc_l30.append(prec_L30)
        list_acc_l20.append(prec_L20)
        list_acc_l10.append(prec_L10)
        list_acc_l5.append(prec_L5)
    return (list_acc_T5, list_acc_T10, list_acc_l30, list_acc_l20, list_acc_l10, list_acc_l5)

def print_detailed_accuracy_on_this_data(id_string, file_weights, LTR, XTR, YTR, pathX, pathY):
    print ('')
    #print (XTR1)
    all_list_acc_l5 = []
    all_list_acc_l10 = []
    all_list_acc_l20 = []
    all_list_acc_l30 = []
    all_list_acc_T10 = []
    all_list_acc_T5 = []
    XTR1=XTR[0]
    YTR1=YTR[0]
    LTR1=LTR[0]
    XTR2=XTR[1]
    YTR2=YTR[1]
    LTR2=LTR[1]
    XTR3=XTR[2]
    YTR3=YTR[2]
    LTR3=LTR[2]
    
    XTE1=XTR[6]
    YTE1=YTR[6]
    LTE1=LTR[6]
    XTE2=XTR[7]
    YTE2=YTR[7]
    LTE2=LTR[7]
    XTE3=XTR[8]
    YTE3=YTR[8]
    LTE3=LTR[8]
    for group in range(0, 3):
        #L = LTR[0]#LTR1
        #X = XTR[0]#XTR1
        #Y = YTR[0]#YTR1
        if 'TRAIN' in id_string:
            if 'VAL' in id_string:
                XTR1=XTR[3]
                YTR1=YTR[3]
                LTR1=LTR[3]
                XTR2=XTR[4]
                YTR2=YTR[4]
                LTR2=LTR[4]
                XTR3=XTR[5]
                YTR3=YTR[5]
                LTR3=LTR[5]
            print ('Printing detailed results for TRAIN group ' + str(group))
            if group == 0:
                #print ("X=",XTR1.shape)
                #print("L=",type(LTR1), len(LTR1))
                #print("Y=",YTR1.shape)
                #P = make_prediction(model_arch, file_weights, XTR1)
                print ("Evaluating for ",LTR1.keys())
                print ("Length is ", LTR1[list(LTR1.keys())[0]])
                (list_acc_T5, list_acc_T10, list_acc_l30, list_acc_l20, list_acc_l10, list_acc_l5) = evaluate(LTR1, model_arch, file_weights, pathX,pathY)#evaluate_prediction(LTR1, P, YTR1, 0)
                all_list_acc_l5.extend(list_acc_l5)
                all_list_acc_l10.extend(list_acc_l10)
                all_list_acc_l20.extend(list_acc_l20)
                all_list_acc_l30.extend(list_acc_l30)
                all_list_acc_T10.extend(list_acc_T10)
                all_list_acc_T5.extend(list_acc_T5)
            if group == 1:
                #P = make_prediction(model_arch, file_weights, XTR2)
                print ("Evaluating for ",LTR2.keys())
                print ("Length is ", LTR2[list(LTR2.keys())[0]])
                (list_acc_T5, list_acc_T10, list_acc_l30, list_acc_l20, list_acc_l10, list_acc_l5) = evaluate(LTR2,model_arch,file_weights,pathX,pathY) #evaluate_prediction(LTR2, P, YTR2, 0)
                all_list_acc_l5.extend(list_acc_l5)
                all_list_acc_l10.extend(list_acc_l10)
                all_list_acc_l20.extend(list_acc_l20)
                all_list_acc_l30.extend(list_acc_l30)
                all_list_acc_T10.extend(list_acc_T10)
                all_list_acc_T5.extend(list_acc_T5)
            if group == 2:
                #P = make_prediction(model_arch, file_weights, XTR3)
                print ("Evaluating for ",LTR3.keys())
                print ("Length is ", LTR3[list(LTR3.keys())[0]])
                (list_acc_T5, list_acc_T10, list_acc_l30, list_acc_l20, list_acc_l10, list_acc_l5) = evaluate(LTR3, model_arch,file_weights,pathX,pathY) #evaluate_prediction(LTR3, P, YTR3, 0)
                all_list_acc_l5.extend(list_acc_l5)
                all_list_acc_l10.extend(list_acc_l10)
                all_list_acc_l20.extend(list_acc_l20)
                all_list_acc_l30.extend(list_acc_l30)
                all_list_acc_T10.extend(list_acc_T10)
                all_list_acc_T5.extend(list_acc_T5)
        if 'TEST' in id_string:
            print ('Printing detailed results for TEST group ' + str(group))
            if group == 0:
                #P = make_prediction(model_arch, file_weights, XTE1)
                print ("Evaluating for ",LTE1.keys())
                print ("Length is ", LTE1[list(LTE1.keys())[0]])
                (list_acc_T5, list_acc_T10, list_acc_l30, list_acc_l20, list_acc_l10, list_acc_l5) = evaluate(LTE1, model_arch,file_weights,pathX,pathY) #evaluate_prediction(LTE1, P, YTE1, 0)
                all_list_acc_l5.extend(list_acc_l5)
                all_list_acc_l10.extend(list_acc_l10)
                all_list_acc_l20.extend(list_acc_l20)
                all_list_acc_l30.extend(list_acc_l30)
                all_list_acc_T10.extend(list_acc_T10)
                all_list_acc_T5.extend(list_acc_T5)
            if group == 1:
                #P = make_prediction(model_arch, file_weights, XTE2)
                print ("Evaluating for ",LTE2.keys())
                print ("Length is ", LTE2[list(LTE2.keys())[0]])
                (list_acc_T5, list_acc_T10, list_acc_l30, list_acc_l20, list_acc_l10, list_acc_l5) = evaluate(LTE2, model_arch,file_weights,pathX,pathY) #evaluate_prediction(LTE2, P, YTE2, 0)
                all_list_acc_l5.extend(list_acc_l5)
                all_list_acc_l10.extend(list_acc_l10)
                all_list_acc_l20.extend(list_acc_l20)
                all_list_acc_l30.extend(list_acc_l30)
                all_list_acc_T10.extend(list_acc_T10)
                all_list_acc_T5.extend(list_acc_T5)
            if group == 2:
                #P = make_prediction(model_arch, file_weights, XTE3)
                print ("Evaluating for ",LTE3.keys())
                print ("Length is ", LTE3[list(LTE3.keys())[0]])
                (list_acc_T5, list_acc_T10, list_acc_l30, list_acc_l20, list_acc_l10, list_acc_l5) = evaluate(LTE3, model_arch,file_weights,pathX,pathY) #evaluate_prediction(LTE3, P, YTE3, 0)
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
    acc_T10 = sum(all_list_acc_T10) / len(all_list_acc_T10)
    acc_T5 = sum(all_list_acc_T5) / len(all_list_acc_T5)
    print ('----------------------------------------------------------------------------------------------')
    print ('Cycle DataSet      Top-5  Top-10  Top-L/30  Top-L/20  Top-L/10  Top-L/5')
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

#dist_string = sys.argv[1]
dist_string=""
pathX = os.path.abspath(sys.argv[1])+"/" #/data/farhan/SoftwareTools/HomopolymerProject/data/homodimers/feat
pathY = os.path.abspath(sys.argv[2])+"/" #/data/farhan/SoftwareTools/HomopolymerProject/data/homodimers/scripts/Y-Labels
path_lists = os.path.abspath(sys.argv[3])+"/" #'/home/bap54/data/DNcon2-data/lists-test-train/'

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
print (max(all_l.values()))

LTR=[]
XTR=[]
YTR=[]

print ('Loading all Training data into memory..')
#Retrieve a dictionary of IDS to train: minL to maxL, count=1000, randomly or sequentially 
#Modify to select all data: maxL=maxLengthinDataset, count=len(tr_l)
LTR1 = subset_pdb_dict(train_l,   0, 175, 1, 'random')
LTR2 = subset_pdb_dict(train_l, 175, 250, 1, 'random')
LTR3 = subset_pdb_dict(train_l, 250, 300, 1, 'random')
LTR.append(LTR1)
LTR.append(LTR2)
LTR.append(LTR3)
#print("Typr of LTR1=",type(LTR1))
print ('Loading sets X1, X2, and X3..')
XTR1 = get_x_from_this_list(LTR1, pathX, 175)
XTR2 = get_x_from_this_list(LTR2, pathX, 250)
XTR3 = get_x_from_this_list(LTR3, pathX, 300)
XTR.append(XTR1)
XTR.append(XTR2)
XTR.append(XTR3)
#print("Typr of XTR1=",type(XTR1))
print ('Loading Y1, Y2, and Y3 ..')
YTR1 = get_y_from_this_list(LTR1, pathY, 0, 175, dist_string)
YTR2 = get_y_from_this_list(LTR2, pathY, 0, 250, dist_string)
YTR3 = get_y_from_this_list(LTR3, pathY, 0, 300, dist_string)
YTR.append(YTR1)
YTR.append(YTR2)
YTR.append(YTR3)
#print("Typr of YTR1=",type(YTR1))
sys.stdout.flush()

print ('Load Validation data into memory..')
LTV1 = subset_pdb_dict(val_l,   0, 175, 1, 'ordered')
LTV2 = subset_pdb_dict(val_l, 175, 250, 1, 'ordered')
LTV3 = subset_pdb_dict(val_l, 250, 300, 1, 'ordered')
LTR.append(LTV1)
LTR.append(LTV2)
LTR.append(LTV3)
print ('Loading sets X1, X2, and X3..')
XTV1 = get_x_from_this_list(LTV1, pathX, 175)
XTV2 = get_x_from_this_list(LTV2, pathX, 250)
XTV3 = get_x_from_this_list(LTV3, pathX, 300)
XTR.append(XTV1)
XTR.append(XTV2)
XTR.append(XTV3)
print ('Loading Y1, Y2, and Y3 ..')
YTV1 = get_y_from_this_list(LTV1, pathY, 24, 175, dist_string)
YTV2 = get_y_from_this_list(LTV2, pathY, 24, 250, dist_string)
YTV3 = get_y_from_this_list(LTV3, pathY, 24, 300, dist_string)
YTR.append(YTV1)
YTR.append(YTV2)
YTR.append(YTV3)
sys.stdout.flush()
print ('Load Test data into memory..')
LTE1 = subset_pdb_dict(test_l,   0, 175, 1, 'ordered')
LTE2 = subset_pdb_dict(test_l, 175, 250, 1, 'ordered')
LTE3 = subset_pdb_dict(test_l, 250, 300, 1, 'ordered')
LTR.append(LTE1)
LTR.append(LTE2)
LTR.append(LTE3)

print ('Loading sets X1, X2, and X3..')
XTE1 = get_x_from_this_list(LTE1, pathX, 175)
XTE2 = get_x_from_this_list(LTE2, pathX, 250)
XTE3 = get_x_from_this_list(LTE3, pathX, 300)
XTR.append(XTE1)
XTR.append(XTE2)
XTR.append(XTE3)
print ('Loading Y1, Y2, and Y3 ..')
YTE1 = get_y_from_this_list(LTE1, pathY, 24, 175, dist_string)
YTE2 = get_y_from_this_list(LTE2, pathY, 24, 250, dist_string)
YTE3 = get_y_from_this_list(LTE3, pathY, 24, 300, dist_string)
YTR.append(YTE1)
YTR.append(YTE2)
YTR.append(YTE3)

print ("Lengths of Train, Validation, Test = ",len(XTR1)+len(XTR2)+len(XTR3), len(XTV1)+len(XTV2)+len(XTV3), len(XTE1)+len(XTE2)+len(XTE3))

# cycle the training groups during training

#os.system('rm -f *.hdf5')
group = 0

hdf5_num = len(glob(project_root+'scripts/*.hdf5'))
rerun_epoch = hdf5_num
if (rerun_epoch>=1): print ("restarting from epoch:",rerun_epoch)
print (rerun_epoch)
#sys.exit()
#if rerun_epoch <= 0:
#    rerun_epoch = 0

#include script to save best weights
#for cyc in range (rerun_epoch, train_param['outer_epochs']):
for cyc in range (rerun_epoch, rerun_epoch+1):
    sys.stdout.flush()
    """
    if cyc % 40 == 0:
        if os.path.exists('./weights.hdf5'):
            print ('')
            print ('Reached 40 epochs, removing weights file to flush learning..')
            os.remove('./weights.hdf5')
    """
    if os.path.exists('./cycle-' + str(cyc) + '.hdf5'):
        print ('Skipping ' + 'cycle-' + str(cyc) + '.hdf5 ..')
        continue
    X = XTR1
    Y = YTR1
    #print ("@#@#@#@#@#@# Types = ",type(X), type(Y))
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
    print ('Epoch : ' + str(cyc) + ' of ' + str(train_param['outer_epochs']))
    print ("Total training data: ", len (X), "Shape: ", X.shape)
    print ("Total training labels: ", len (Y), "Shape: ", Y.shape)
    for item in LTR:
        print (item.keys())
    train_on_this_X_Y(model_arch, train_param, X, Y, './weights.hdf5')
    print ('')
    print ('Save the weights & model for this cycle..')
    shutil.copy2('./weights.hdf5', './cycle-' + str(cyc) + '.hdf5')
    group = next_group(group)
    print ('')
    cyc_id = str(cyc)
    cyc_id = cyc_id.rjust(5, '0')
    (acc_T5, acc_T10, acc_l30, acc_l20, acc_l10, acc_l5)=print_detailed_accuracy_on_this_data(cyc_id + ' SAMPLE-TRAIN', './cycle-' + str(cyc) + '.hdf5',LTR,XTR,YTR,pathX,pathY)
    with open ("training_acc.txt","a+") as f:
        epoch = cyc
        if (epoch == 0):
            f.write("Epoch\tSample_Size\tPrec-T5\tPrec-T10\tL/30\tL/20\tL/10\tL/5\n")
        f.write(str(epoch)+"\t"+str(len(LTR1)+len(LTR2)+len(LTR3))+"\t"+str(round(acc_T5,4))+"\t"+str(round(acc_T10,4))+"\t"+str(round(acc_l30,4))+"\t"+str(round(acc_l20,4))+"\t"+str(round(acc_l10,4))+"\t"+str(round(acc_l5,4))+"\n")
        
    print ('Evaluate on Validation data..')
    (acc_T5, acc_T10, acc_l30, acc_l20, acc_l10, acc_l5)=print_detailed_accuracy_on_this_data(cyc_id + ' VAL-TRAIN', './cycle-' + str(cyc) + '.hdf5',LTR,XTR,YTR,pathX,pathY)
    with open ("validation_acc.txt","a+") as f:
        epoch = cyc
        if (epoch == 0):
            f.write("Epoch\tSample_Size\tPrec-T5\tPrec-T10\tL/30\tL/20\tL/10\tL/5\n")
        f.write(str(epoch)+"\t"+str(len(LTR1)+len(LTR2)+len(LTR3))+"\t"+str(round(acc_T5,4))+"\t"+str(round(acc_T10,4))+"\t"+str(round(acc_l30,4))+"\t"+str(round(acc_l20,4))+"\t"+str(round(acc_l10,4))+"\t"+str(round(acc_l5,4))+"\n")
    print ('Evaluate on full Test data..')
    (acc_T5, acc_T10, acc_l30, acc_l20, acc_l10, acc_l5)=print_detailed_accuracy_on_this_data(cyc_id + ' ALL-TEST    ', './cycle-' + str(cyc) + '.hdf5',LTR,XTR,YTR,pathX,pathY)
    with open ("testing_acc.txt","a+") as f:
        epoch = cyc
        if (epoch == 0):
            f.write("Epoch\tSample_Size\tPrec-T5\tPrec-T10\tL/30\tL/20\tL/10\tL/5\n")
        f.write(str(epoch)+"\t"+str(len(LTR1)+len(LTR2)+len(LTR3))+"\t"+str(round(acc_T5,4))+"\t"+str(round(acc_T10,4))+"\t"+str(round(acc_l30,4))+"\t"+str(round(acc_l20,4))+"\t"+str(round(acc_l10,4))+"\t"+str(round(acc_l5,4))+"\n")

