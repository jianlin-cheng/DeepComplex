#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 01:10:42 2020

@author: farhan
"""

import shutil
import sys, os
import numpy as np
from glob import glob
import time
import subprocess
import gc

project_root = os.path.abspath(sys.argv[0]).rstrip(sys.argv[0]).rstrip("scripts/")
if not project_root.endswith("/"): project_root+="/"
sys.path.insert(0, project_root + "lib")
print ("Project Root Directory: ",project_root)

from libtrain import *
from libcommon import *

def prob(e):
    return e[-1]



def toCmap(arr,fasta_file):
    l=arr.shape[0]
    print ("@$@$@$@$@$@$@$@$@$@$@$@$@$@$@  Original arr.shape=",arr.shape)
    if (l==1):
        arr=arr.squeeze()
        l=len(arr)
    #l=int(np.sqrt(l))
    #arr=arr.reshape(l,l)
    #print ("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$  toCmap_length=",l)
    print ("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ Length = ",l, "Shape=",arr.shape)
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
    cmap[-1]=cmap[-1].strip()
    return cmap

def calculateEvaluationStats(pred_cmap, true_cmap, name,epochs):
    prec_T5=0
    prec_T10=0
    prec_T20=0
    prec_T30=0
    prec_T50=0
    prec_L30=0
    prec_L20=0
    prec_L10=0
    prec_L5=0
    con_num=0
    #print ("Name: ", name, " True_shape=",true_cmap.shape," Pred_shape=",pred_cmap.shape)
    pred_cmap=pred_cmap.squeeze()
    ll=int(np.sqrt(len(pred_cmap)))
    pred_cmap=pred_cmap.squeeze().reshape(ll,ll)
    print("&&"*30)
    print (true_cmap.shape, pred_cmap.shape)
    if true_cmap.shape!=pred_cmap.shape: print ("True and predicted contact maps do not match in shape!")
    print("&&"*30)
    fasta_file="/storage/htc/bdm/farhan/DNCON2_features_homodimers/final_training_set_04_13_2020/all_same_fastas/"+name+".fasta"
    cmap_folder="/storage/htc/bdm/farhan/DeepComplex/training/dncon2_model/contact_maps/"
    #pred_cmap_list=toCmap(pred_cmap,fasta_file)
    #true_cmap_list=toCmap(true_cmap,fasta_file)
    
    max_Top=int((ll/5)+0.5)
    if 50>max_Top: max_Top=50
    
    for i in range(1,max_Top+1):
        (x,y)=np.unravel_index(np.argmax(pred_cmap,axis=None),pred_cmap.shape)
        pred_cmap[x][y]=0
        if true_cmap[x][y]==1:
            con_num+=1
        if i==5:
            prec_T5=con_num*20
            if prec_T5>100: prec_T5=100
            print ("L=", ll, "Val=",5,"Con_num=",con_num)
        if i==10:
            prec_T10=con_num*10
            if prec_T10>100: prec_T10=100
            print ("L=", ll, "Val=",10,"Con_num=",con_num)
        if i==20:
            prec_T20=con_num*5
            if prec_T20>100: prec_T20=100
            print ("L=", ll, "Val=",20,"Con_num=",con_num)
        if i==30:
            prec_T30=con_num*100/30
            if prec_T30>100: prec_T30=100
            print ("L=", ll, "Val=",30,"Con_num=",con_num)
        if i==50:
            prec_T50=con_num*2
            if prec_T50>100: prec_T50=100
            print ("L=", ll, "Val=",50,"Con_num=",con_num)
        if i==int((ll/30)+0.5):
            prec_L30=con_num*100/i
            if prec_L30>100: prec_L30=100
            print ("L=", ll, "Val=",i,"Con_num=",con_num)
        if i==int((ll/20)+0.5):
            prec_L20=con_num*100/i
            if prec_L20>100: prec_L20=100
            print ("L=", ll, "Val=",i,"Con_num=",con_num)
        if i==int((ll/10)+0.5):
            prec_L10=con_num*100/i
            if prec_L10>100: prec_L10=100
            print ("L=", ll, "Val=",i,"Con_num=",con_num)
        if i==int((ll/5)+0.5):
            prec_L5=con_num*100/i
            if prec_L5>100: prec_L5=100
            print ("L=", ll, "Val=",i,"Con_num=",con_num)
    """
    if prec_L5>0:
        with open (cmap_folder+name+"_pred_cmap_"+str(epochs)+".rr","w") as f:
            f.writelines(pred_cmap_list)
        with open (cmap_folder+name+"_true_cmap_"+str(epochs)+".rr","w") as f:
            f.writelines(true_cmap_list)
        del true_cmap_list, pred_cmap_list, pred_cmap, true_cmap
        """
    del pred_cmap, true_cmap
    gc.collect()
        #subprocess.check_call("python "+project_root+"lib/sortrr.py "+cmap_folder+name+"_pred_cmap_"+str(epochs)+".rr True > "+cmap_folder+name+"_pred_cmap_"+str(epochs)+".sorted.rr",shell=True)
    return (prec_T5,prec_T10,prec_T20,prec_T30,prec_T50,prec_L30,prec_L20,prec_L10,prec_L5)

def evaluate(LTR, model_arch, file_weights,pathX,pathY,epochs):
    
    list_acc_T5 =[]
    list_acc_T10 =[] 
    list_acc_l30 =[]
    list_acc_l20 =[]
    list_acc_l10 =[]
    list_acc_l5 =[]
    list_acc_T20 =[]
    list_acc_T30 =[]
    list_acc_T50 =[]
    #datacount=len(LTR)
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
        print ("Prediction output shape:",P.shape," to " ,P.squeeze().reshape(len(Y),len(Y)).shape)
        print ("True Labels shape:",Y.shape)
        print ("Length in dict: ",L)
        (prec_T5,prec_T10,prec_T20,prec_T30,prec_T50,prec_L30,prec_L20,prec_L10,prec_L5)=calculateEvaluationStats(P, Y,key,epochs)
        list_acc_T5.append(prec_T5)
        list_acc_T10.append(prec_T10)
        list_acc_T20.append(prec_T20)
        list_acc_T30.append(prec_T30)
        list_acc_T50.append(prec_T50)
        list_acc_l30.append(prec_L30)
        list_acc_l20.append(prec_L20)
        list_acc_l10.append(prec_L10)
        list_acc_l5.append(prec_L5)
    return (list_acc_T5, list_acc_T10, list_acc_T20, list_acc_T30, list_acc_T50, list_acc_l30, list_acc_l20, list_acc_l10, list_acc_l5)

def print_detailed_accuracy_on_this_data(id_string, file_weights, LT, XT, YT, pathX, pathY, epochs):
    print ('')
    #print (XTR1)
    all_list_acc_l5 = []
    all_list_acc_l10 = []
    all_list_acc_l20 = []
    all_list_acc_l30 = []
    all_list_acc_T10 = []
    all_list_acc_T5 = []
    all_list_acc_T20 = []
    all_list_acc_T30 = []
    all_list_acc_T50 = []
    
    if 'TRAIN' in id_string:
            if 'VAL' in id_string:
               print ('Printing detailed results for VALIDATION dataset ')
            else:
                print ('Printing detailed results for TRAIN dataset ')
    if "TEST" in id_string:
        print ('Printing detailed results for TEST dataset ')
    
    print ("Evaluating for ",LT.keys())
    print ("Total number of data in this set is ",len(LT.keys()))
    print ("Length is ", LT[list(LT.keys())[0]])
    (list_acc_T5, list_acc_T10, list_acc_T20, list_acc_T30, list_acc_T50, list_acc_l30, list_acc_l20, list_acc_l10, list_acc_l5) = evaluate(LT, model_arch, file_weights, pathX,pathY,epochs)#evaluate_prediction(LTR1, P, YTR1, 0)
    all_list_acc_l5.extend(list_acc_l5)
    all_list_acc_l10.extend(list_acc_l10)
    all_list_acc_l20.extend(list_acc_l20)
    all_list_acc_l30.extend(list_acc_l30)
    all_list_acc_T10.extend(list_acc_T10)
    all_list_acc_T5.extend(list_acc_T5)
    all_list_acc_T20.extend(list_acc_T20)
    all_list_acc_T30.extend(list_acc_T30)
    all_list_acc_T50.extend(list_acc_T50)
    
    
    acc_l5 = sum(all_list_acc_l5) / len(all_list_acc_l5)
    acc_l10 = sum(all_list_acc_l10) / len(all_list_acc_l10)
    acc_l20 = sum(all_list_acc_l20) / len(all_list_acc_l20)
    acc_l30 = sum(all_list_acc_l30) / len(all_list_acc_l30)
    acc_T10 = sum(all_list_acc_T10) / len(all_list_acc_T10)
    acc_T5 = sum(all_list_acc_T5) / len(all_list_acc_T5)
    acc_T20 = sum(all_list_acc_T20) / len(all_list_acc_T20)
    acc_T30 = sum(all_list_acc_T30) / len(all_list_acc_T30)
    acc_T50 = sum(all_list_acc_T50) / len(all_list_acc_T50)
    print ('----------------------------------------------------------------------------------------------')
    print ('Cycle DataSet      Top-5  Top-10  Top-20  Top-30  Top-50  Top-L/30  Top-L/20  Top-L/10  Top-L/5')
    print ('' + id_string + ' %.3f  %.3f   %.3f   %.3f   %.3f   %.3f   %.3f   %.3f   %.3f' %(acc_T5, acc_T10,acc_T20,acc_T30,acc_T50, acc_l30, acc_l20, acc_l10, acc_l5))
    print ('----------------------------------------------------------------------------------------------')
    return (acc_T5, acc_T10, acc_T20, acc_T30, acc_T50, acc_l30, acc_l20, acc_l10, acc_l5)

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

#The following loads the training data in groups:
data_distribution=[]
with open (project_root+"scripts/data_distr_100.txt","r") as f:
    for line in f:
        for line in f:
            freq=int(line.strip().split()[-1])
            low_limit=int(line.strip().split()[0].strip("(").strip("[").strip(")").strip("]").strip(","))
            up_limit=int(line.strip().split()[1].strip("(").strip("[").strip(")").strip("]").strip(","))
    


print ('Loading all Training data into memory..')
#Retrieve a dictionary of IDS to train: minL to maxL, count=1000, randomly or sequentially 
#Modify to select all data: maxL=maxLengthinDataset, count=len(tr_l)
#LTR1 = subset_pdb_dict(train_l, 0, maxLengthinDataset, len(train_l), 'random')
LTR1 = subset_pdb_dict(train_l, low_limit, up_limit, freq, 'random')
LTR.append(LTR1)
#print("Typr of LTR1=",type(LTR1))
print ('Loading sets input feature matrix X..')
XTR1 = get_x_from_this_list(LTR1, pathX, freq)
XTR.append(XTR1)
#print("Typr of XTR1=",type(XTR1))
print ('Loading label matrix Y ..')
YTR1 = get_y_from_this_list(LTR1, pathY, 0, freq, dist_string)
YTR.append(YTR1)
#print("Typr of YTR1=",type(YTR1))
sys.stdout.flush()

print ('Load Validation data into memory..')
LTV1 = subset_pdb_dict(val_l,   low_limit, up_limit, len(val_l), 'ordered')
LTR.append(LTV1)
print ('Loading validation data sets input feature matrix X..')
XTV1 = get_x_from_this_list(LTV1, pathX, len(val_l))
XTR.append(XTV1)
print ('Loading label matrix Y ..')
YTV1 = get_y_from_this_list(LTV1, pathY, 24, len(val_l), dist_string)
YTR.append(YTV1)
sys.stdout.flush()
print ('Load Test data into memory..')
LTE1 = subset_pdb_dict(test_l,   0, maxLengthinDataset, len(test_l), 'ordered')
LTR.append(LTE1)
print ('Loading test data sets input feature matrix X..')
XTE1 = get_x_from_this_list(LTE1, pathX, maxLengthinDataset)
XTR.append(XTE1)
print ('Loading label matrix Y ..')
YTE1 = get_y_from_this_list(LTE1, pathY, 24, maxLengthinDataset, dist_string)
YTR.append(YTE1)

print ("Lengths of Train, Validation, Test = ",len(XTR1), len(XTV1), len(XTE1))

# cycle the training groups during training

#os.system('rm -f *.hdf5')
group = 0
if (os.path.exists(project_root+"scripts/weights.hdf5")): os.remove(project_root+"scripts/weights.hdf5")
hdf5_num = len(glob(project_root+'scripts/*.hdf5'))
rerun_epoch = hdf5_num-1
if rerun_epoch==-1: rerun_epoch = 0
if (rerun_epoch>=1): print ("restarting from epoch:",rerun_epoch)
print (rerun_epoch)
#sys.exit()
#if rerun_epoch <= 0:
#    rerun_epoch = 0

#include script to save best weights
for cyc in range (rerun_epoch, train_param['outer_epochs']):
#for cyc in range (rerun_epoch, rerun_epoch+1):
#for cyc in range (rerun_epoch, 21):
    sys.stdout.flush()
    
    if cyc % 40 == 0:
        if os.path.exists('./weights.hdf5'):
            print ('')
            print ('Reached 40 epochs, removing weights file to flush learning..')
            os.remove('./weights.hdf5')
    
    if os.path.exists('./cycle-' + str(cyc) + '.hdf5'):
        print ('Found previous checkpoint weights ' + 'cycle-' + str(cyc) + '.hdf5 ..')
        #continue
    X = XTR1
    Y = YTR1
    #print ("@#@#@#@#@#@# Types = ",type(X), type(Y))
    XTR = XTR1
    YTR = YTR1
    LTR = LTR1 
    LTV = LTV1
    XTV = XTV1
    YTV = YTV1
    LTE = LTE1
    XTE = XTE1
    YTE = YTE1
    
    if cyc == 0:
        print_feature_summary(X)
    print ('')
    #print ('Group : ' + str(group))
    print ('Epoch : ' + str(cyc) + ' of ' + str(train_param['outer_epochs']))
    print ("Total training data: ", len (X), "Shape: ", X.shape)
    print ("Total training labels: ", len (Y), "Shape: ", Y.shape)
    for item in LTR:
        print (item+":",all_l[item])
    print ("Training sample is: ")
    print (list(LTR.keys()))
    train_on_this_X_Y(model_arch, train_param, X, Y, project_root+"scripts/weights.hdf5")
    print ('')
    print ('Save the weights & model for this cycle..')
    shutil.copy2(project_root+"scripts/weights.hdf5", project_root+"scripts/"+'cycle-' + str(cyc) + '.hdf5')
    #group = next_group(group)
    print ('')
    cyc_id = str(cyc)
    cyc_id = cyc_id.rjust(5, '0')
    print ("Evaluating on training data:")
    (acc_T5, acc_T10, acc_T20, acc_T30, acc_T50, acc_l30, acc_l20, acc_l10, acc_l5)=print_detailed_accuracy_on_this_data(cyc_id + ' SAMPLE-TRAIN', './cycle-' + str(cyc) + '.hdf5',LTR,XTR,YTR,pathX,pathY,epochs=cyc)
    with open ("training_acc_"+str(group)+".txt","a+") as f:
        epoch = cyc
        if (epoch == 0):
            f.write("Epoch\tSample_Size\tPrec-T5\tPrec-T10\tPrec-T20\tPrec-T30\tPrec-T50\tL/30\tL/20\tL/10\tL/5\n")
        f.write(str(epoch)+"\t"+str(len(LTR1)+len(LTR2)+len(LTR3))+"\t"+str(round(acc_T5,4))+"\t"+str(round(acc_T10,4))+"\t"+str(round(acc_T20,4))+"\t"+str(round(acc_T30,4))+"\t"+str(round(acc_T50,4))+"\t"+str(round(acc_l30,4))+"\t"+str(round(acc_l20,4))+"\t"+str(round(acc_l10,4))+"\t"+str(round(acc_l5,4))+"\n")
        print("Train Accuracies: \n"+str(epoch)+"\t"+str(len(LTR1)+len(LTR2)+len(LTR3))+"\t"+str(round(acc_T5,4))+"\t"+str(round(acc_T10,4))+"\t"+str(round(acc_T20,4))+"\t"+str(round(acc_T30,4))+"\t"+str(round(acc_T50,4))+"\t"+str(round(acc_l30,4))+"\t"+str(round(acc_l20,4))+"\t"+str(round(acc_l10,4))+"\t"+str(round(acc_l5,4))+"\n")
        
    print ('Evaluate on Validation data..')
    (acc_T5, acc_T10, acc_T20, acc_T30, acc_T50, acc_l30, acc_l20, acc_l10, acc_l5)=print_detailed_accuracy_on_this_data(cyc_id + ' VAL-TRAIN', './cycle-' + str(cyc) + '.hdf5',LTV,XTV,YTV,pathX,pathY,epochs=cyc)
    with open ("validation_acc_"+str(group)+".txt","a+") as f:
        epoch = cyc
        if (epoch == 0):
            f.write("Epoch\tSample_Size\tPrec-T5\tPrec-T10\tPrec-T20\tPrec-T30\tPrec-T50\tL/30\tL/20\tL/10\tL/5\n")
        f.write(str(epoch)+"\t"+str(len(LTR1)+len(LTR2)+len(LTR3))+"\t"+str(round(acc_T5,4))+"\t"+str(round(acc_T10,4))+"\t"+str(round(acc_T20,4))+"\t"+str(round(acc_T30,4))+"\t"+str(round(acc_T50,4))+"\t"+str(round(acc_l30,4))+"\t"+str(round(acc_l20,4))+"\t"+str(round(acc_l10,4))+"\t"+str(round(acc_l5,4))+"\n")
        print("Validation Accuracies: \n"+str(epoch)+"\t"+str(len(LTR1)+len(LTR2)+len(LTR3))+"\t"+str(round(acc_T5,4))+"\t"+str(round(acc_T10,4))+"\t"+str(round(acc_T20,4))+"\t"+str(round(acc_T30,4))+"\t"+str(round(acc_T50,4))+"\t"+str(round(acc_l30,4))+"\t"+str(round(acc_l20,4))+"\t"+str(round(acc_l10,4))+"\t"+str(round(acc_l5,4))+"\n")
    
    print ('Evaluate on full Test data..')
    (acc_T5, acc_T10, acc_T20, acc_T30, acc_T50, acc_l30, acc_l20, acc_l10, acc_l5)=print_detailed_accuracy_on_this_data(cyc_id + ' ALL-TEST    ', './cycle-' + str(cyc) + '.hdf5',LTE,XTE,YTE,pathX,pathY,epochs=cyc)
    with open ("testing_acc_"+str(group)+".txt","a+") as f:
        epoch = cyc
        if (epoch == 0):
            f.write("Epoch\tSample_Size\tPrec-T5\tPrec-T10\tPrec-T20\tPrec-T30\tPrec-T50\tL/30\tL/20\tL/10\tL/5\n")
        f.write(str(epoch)+"\t"+str(len(LTR1)+len(LTR2)+len(LTR3))+"\t"+str(round(acc_T5,4))+"\t"+str(round(acc_T10,4))+"\t"+str(round(acc_T20,4))+"\t"+str(round(acc_T30,4))+"\t"+str(round(acc_T50,4))+"\t"+str(round(acc_l30,4))+"\t"+str(round(acc_l20,4))+"\t"+str(round(acc_l10,4))+"\t"+str(round(acc_l5,4))+"\n")
        print("Testing Accuracies: \n"+str(epoch)+"\t"+str(len(LTR1)+len(LTR2)+len(LTR3))+"\t"+str(round(acc_T5,4))+"\t"+str(round(acc_T10,4))+"\t"+str(round(acc_T20,4))+"\t"+str(round(acc_T30,4))+"\t"+str(round(acc_T50,4))+"\t"+str(round(acc_l30,4))+"\t"+str(round(acc_l20,4))+"\t"+str(round(acc_l10,4))+"\t"+str(round(acc_l5,4))+"\n")



