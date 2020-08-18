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

def toCmap(arr,fasta_file):
    l=arr.shape[0]
    print ("@$@$@$@$@$@$@$@$@$@$@$@$@$@$@  Original arr.shape=",arr.shape)
    if (l==1):
        arr=arr.squeeze()
        l=len(arr)
    l=int(np.sqrt(l))
    arr=arr.reshape(l,l)
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

def calculateEvaluationStats(pred_cmap, true_cmap, name):
    prec_T5=0
    prec_T10=0
    prec_T20=0
    prec_T30=0
    prec_T50=0
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
    print("&&"*30)
    print (true_cmap.shape, pred_cmap.shape)
    print (len(true_cmap), int(np.sqrt(len(pred_cmap))))
    print("&&"*30)
    np.savetxt(project_root+name+"_true_cmap.rr",true_cmap)
    pred_cmap=toCmap(pred_cmap,fasta_folder+name+".fasta")
    
    with open (project_root+name+"_pred_cmap.rr","w") as f:
        f.writelines(pred_cmap)
        f.close()
    cmap_folder="/data/farhan/SoftwareTools/HomopolymerProject/DeepComplex/training/dncon2_model/contact_maps/"
    #while not os.path.exists(project_root+name+"_pred_cmap.rr"):
    print ("Pred_cmap_list length=",len(pred_cmap))
    print ("Waiting for "+project_root+name+"_pred_cmap.rr to be created")
    while True:
        if os.path.exists(project_root+name+"_pred_cmap.rr"): break
        #print ("Still not created!")
    #shutil.copy2(project_root+name+"_pred_cmap.rr",cmap_folder+name+"_pred.rr")
    #time.sleep(30)
    if not os.path.exists(project_root+name+"_pred_cmap.rr"): print (project_root+name+"_pred_cmap.rr not found!")
    if os.path.exists(project_root+name+"_pred_cmap.rr"): print (project_root+name+"_pred_cmap.rr found!")
    lnnum = subprocess.check_output("wc -l < "+project_root+name+"_pred_cmap.rr",shell = True)
    lnnum = lnnum.rstrip()
    lnnum = str(lnnum)
    lnnum = int(lnnum.lstrip("b").strip("'"))-1
    print ("Line Numbers: ",lnnum,len(pred_cmap))
    print ("pred_cmap[0]:",pred_cmap[0])
    print ("pred_cmap[-1]:",pred_cmap[-1])
    print(subprocess.check_output("head -n 1 "+project_root+name+"_pred_cmap.rr",shell=True))
    print(subprocess.check_output("tail -n 1 "+project_root+name+"_pred_cmap.rr",shell=True))
    print ("Executing: "+ "cp "+project_root+name+"_pred_cmap.rr "+cmap_folder+name+"_pred.rr")
    #exit_code=os.system("cp "+project_root+name+"_pred_cmap.rr "+cmap_folder+name+"_pred.rr")
    #p=subprocess.Popen("cp "+project_root+name+"_pred_cmap.rr "+cmap_folder+name+"_pred.rr",shell=True)
    subprocess.check_call("cp "+project_root+name+"_pred_cmap.rr "+cmap_folder+name+"_pred.rr",shell=True)
    #print ("EC: ",exit_code)
    time.sleep(2)
    print ("Executing: "+ "python "+project_root+"/lib/sortrr.py "+cmap_folder+name+"_pred.rr True > "+cmap_folder+name+"_sorted_pred.rr")
    #exit_code=os.system("python "+project_root+"/lib/sortrr.py "+cmap_folder+name+"_pred.rr True > "+cmap_folder+name+"_sorted_pred.rr")
    subprocess.check_call("python "+project_root+"/lib/sortrr.py "+cmap_folder+name+"_pred.rr True > "+cmap_folder+name+"_sorted_pred.rr")
    #print ("EC: ",exit_code)
    #os.system("python "+project_root+"lib/conevainter_usingY_Labels.py "+project_root+"true_cmap.rr "+project_root+"pred_cmap.rr")
    #print ("python "+project_root+"lib/conevainter_usingY_Labels.py "+project_root+"true_cmap.rr "+project_root+"pred_cmap.rr > "+project_root+"temp_prec.txt")
    time.sleep(2)
    if not os.path.exists(project_root+name+"_true_cmap.rr"): print (project_root+name+"_true_cmap.rr not found!")
    if not os.path.exists(project_root+name+"_pred_cmap.rr"): print (project_root+name+"_pred_cmap.rr not found!")
    if not os.path.exists(cmap_folder+name+"_pred.rr"): print (cmap_folder+name+"_pred.rr not found!")
    if not os.path.exists(fasta_folder+name+".fasta"): print (fasta_folder+name+".fasta not found!")
    if not os.path.exists(project_root+"lib/conevainter_usingY_Labels.py"): print (project_root+"lib/conevainter_usingY_Labels.py not found!")
    #os.system("python "+project_root+"lib/conevainter_usingY_Labels.py "+project_root+name+"_true_cmap.rr "+project_root+name+"_pred_cmap.rr "+fasta_folder+name+".fasta")
    #os.system("python "+project_root+"lib/conevainter_usingY_Labels.py "+project_root+name+"_true_cmap.rr "+project_root+name+"_pred_cmap.rr "+fasta_folder+name+".fasta")
    gc.collect()
    #exit_code=os.system("python "+project_root+"lib/conevainter_usingY_Labels.py "+project_root+name+"_true_cmap.rr "+project_root+name+"_pred_cmap.rr "+fasta_folder+name+".fasta")
    print(subprocess.check_output("python "+project_root+"lib/conevainter_usingY_Labels.py "+project_root+name+"_true_cmap.rr "+project_root+name+"_pred_cmap.rr "+fasta_folder+name+".fasta",shell=True))
    time.sleep(2)
    
    #print ("EC: ",exit_code)
    print ("Command...:\n"+"python "+project_root+"lib/conevainter_usingY_Labels.py "+project_root+name+"_true_cmap.rr "+project_root+name+"_pred_cmap.rr "+fasta_folder+name+".fasta > "+project_root+name+"_temp_prec.txt")
    #exit_code=os.system("python "+project_root+"lib/conevainter_usingY_Labels.py "+project_root+name+"_true_cmap.rr "+project_root+name+"_pred_cmap.rr "+fasta_folder+name+".fasta > "+project_root+name+"_temp_prec.txt")
    print(subprocess.check_output("python "+project_root+"lib/conevainter_usingY_Labels.py "+project_root+name+"_true_cmap.rr "+project_root+name+"_pred_cmap.rr "+fasta_folder+name+".fasta > "+project_root+name+"_temp_prec.txt",shell=True))
    time.sleep(2)
    #print ("EC: ",exit_code)
    #time.sleep(20)
    #with open (project_root+"temp_prec.txt","r") as f:
    #shutil.copy2(project_root+"lib/"+name+"_temp_rr.rr",cmap_folder+name+"_true.rr")
    #os.system("cp "+project_root+"lib/"+name+"_temp_rr.rr "+cmap_folder+name+"_true.rr")
    subprocess.check_call("cp "+project_root+"lib/"+name+"_temp_rr.rr "+cmap_folder+name+"_true.rr",shell=True)
    time.sleep(2)
    """
    #np.savetxt(project_root+name+"_true_cmap.rr",true_cmap)
    np.savetxt(project_root+name+"_true_cmap.rr",true_cmap)
    pred_cmap=toCmap(pred_cmap)
    #pred_cmap=toCmap(true_cmap.flatten())
    with open (project_root+name+"_pred_cmap.rr","w") as f:
        f.writelines(pred_cmap)
    os.system("python "+project_root+"/lib/conevainter_usingY_Labels.py "+project_root+name+"_true_cmap.rr "+project_root+name+"_pred_cmap.rr > "+project_root+name+"_temp_prec.txt")
    """
    while True:
        if (os.path.exists(project_root+name+"_temp_prec.txt")):break
    with open (project_root+name+"_temp_prec.txt","r") as f:
        for line in f:
            if line.strip().startswith("Name"): 
                line=f.readline()
                print ("Prediction: "+name+"\t"+line)
                split=line.strip().split()
                prec_T5=float(split[2])
                prec_T10=float(split[3])
                prec_T20=float(split[4])
                prec_T30=float(split[5])
                prec_T50=float(split[6])
                prec_L30=float(split[7])
                prec_L20=float(split[8])
                prec_L10=float(split[9])
                prec_L5=float(split[10])
                break
            
    return (prec_T5,prec_T10,prec_T20,prec_T30,prec_T50,prec_L30,prec_L20,prec_L10,prec_L5)

def evaluate(LTR, model_arch, file_weights,pathX,pathY):
    
    list_acc_T5 =[]
    list_acc_T10 =[] 
    list_acc_l30 =[]
    list_acc_l20 =[]
    list_acc_l10 =[]
    list_acc_l5 =[]
    list_acc_T20 =[]
    list_acc_T30 =[]
    list_acc_T50 =[]
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
        print ("Prediction output shape:",P.shape," to " ,P.squeeze().reshape(len(Y),len(Y)).shape)
        print ("True Labels shape:",Y.shape)
        print ("Length in dict: ",L)
        (prec_T5,prec_T10,prec_T20,prec_T30,prec_T50,prec_L30,prec_L20,prec_L10,prec_L5)=calculateEvaluationStats(P, Y,key)
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

def print_detailed_accuracy_on_this_data(id_string, file_weights, LT, XT, YT, pathX, pathY):
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
    (list_acc_T5, list_acc_T10, list_acc_T20, list_acc_T30, list_acc_T50, list_acc_l30, list_acc_l20, list_acc_l10, list_acc_l5) = evaluate(LT, model_arch, file_weights, pathX,pathY)#evaluate_prediction(LTR1, P, YTR1, 0)
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
#for cyc in range (rerun_epoch, train_param['outer_epochs']):
for cyc in range (rerun_epoch, rerun_epoch+1):
#for cyc in range (rerun_epoch, 21):
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
        #continue
    X = XTR1
    Y = YTR1
    #print ("@#@#@#@#@#@# Types = ",type(X), type(Y))
    for group in range(3): 
        if group == 0:
            X= XTR1
            Y= YTR1
            XTR = XTR1
            YTR = YTR1
            LTR = LTR1 
            LTV = LTV1
            XTV = XTV1
            YTV = YTV1
            LTE = LTE1
            XTE = XTE1
            YTE = YTE1
        if group == 1:
            X = XTR2
            Y = YTR2
            XTR = XTR2
            YTR = YTR2
            LTR = LTR2 
            LTV = LTV2
            XTV = XTV2
            YTV = YTV2
            LTE = LTE2
            XTE = XTE2
            YTE = YTE2
        if group == 2:
            X = XTR3
            Y = YTR3
            XTR = XTR3
            YTR = YTR3
            LTR = LTR3 
            LTV = LTV3
            XTV = XTV3
            YTV = YTV3
            LTE = LTE3
            XTE = XTE3
            YTE = YTE3
        if cyc == 0:
            print_feature_summary(X)
        print ('')
        print ('Group : ' + str(group))
        print ('Epoch : ' + str(cyc) + ' of ' + str(train_param['outer_epochs']))
        print ("Total training data: ", len (X), "Shape: ", X.shape)
        print ("Total training labels: ", len (Y), "Shape: ", Y.shape)
        for item in LTR:
            print (item+":",all_l[item])
        train_on_this_X_Y(model_arch, train_param, X, Y, project_root+"scripts/weights.hdf5")
        print ('')
        print ('Save the weights & model for this cycle..')
        shutil.copy2(project_root+"scripts/weights.hdf5", project_root+"scripts/"+'cycle-' + str(cyc) + '.hdf5')
        group = next_group(group)
        print ('')
        cyc_id = str(cyc)
        cyc_id = cyc_id.rjust(5, '0')
        print ("Evaluating on training data:")
        (acc_T5, acc_T10, acc_T20, acc_T30, acc_T50, acc_l30, acc_l20, acc_l10, acc_l5)=print_detailed_accuracy_on_this_data(cyc_id + ' SAMPLE-TRAIN', './cycle-' + str(cyc) + '.hdf5',LTR,XTR,YTR,pathX,pathY)
        with open ("training_acc.txt","a+") as f:
            epoch = cyc
            if (epoch == 0):
                f.write("Epoch\tSample_Size\tPrec-T5\tPrec-T10\tPrec-T20\tPrec-T30\tPrec-T50\tL/30\tL/20\tL/10\tL/5\n")
            f.write(str(epoch)+"\t"+str(len(LTR1)+len(LTR2)+len(LTR3))+"\t"+str(round(acc_T5,4))+"\t"+str(round(acc_T10,4))+"\t"+str(round(acc_T20,4))+"\t"+str(round(acc_T30,4))+"\t"+str(round(acc_T50,4))+"\t"+str(round(acc_l30,4))+"\t"+str(round(acc_l20,4))+"\t"+str(round(acc_l10,4))+"\t"+str(round(acc_l5,4))+"\n")
            print("Train Accuracies: \n"+str(epoch)+"\t"+str(len(LTR1)+len(LTR2)+len(LTR3))+"\t"+str(round(acc_T5,4))+"\t"+str(round(acc_T10,4))+"\t"+str(round(acc_T20,4))+"\t"+str(round(acc_T30,4))+"\t"+str(round(acc_T50,4))+"\t"+str(round(acc_l30,4))+"\t"+str(round(acc_l20,4))+"\t"+str(round(acc_l10,4))+"\t"+str(round(acc_l5,4))+"\n")
            
        print ('Evaluate on Validation data..')
        (acc_T5, acc_T10, acc_T20, acc_T30, acc_T50, acc_l30, acc_l20, acc_l10, acc_l5)=print_detailed_accuracy_on_this_data(cyc_id + ' VAL-TRAIN', './cycle-' + str(cyc) + '.hdf5',LTV,XTV,YTV,pathX,pathY)
        with open ("validation_acc.txt","a+") as f:
            epoch = cyc
            if (epoch == 0):
                f.write("Epoch\tSample_Size\tPrec-T5\tPrec-T10\tPrec-T20\tPrec-T30\tPrec-T50\tL/30\tL/20\tL/10\tL/5\n")
            f.write(str(epoch)+"\t"+str(len(LTR1)+len(LTR2)+len(LTR3))+"\t"+str(round(acc_T5,4))+"\t"+str(round(acc_T10,4))+"\t"+str(round(acc_T20,4))+"\t"+str(round(acc_T30,4))+"\t"+str(round(acc_T50,4))+"\t"+str(round(acc_l30,4))+"\t"+str(round(acc_l20,4))+"\t"+str(round(acc_l10,4))+"\t"+str(round(acc_l5,4))+"\n")
            print("Validation Accuracies: \n"+str(epoch)+"\t"+str(len(LTR1)+len(LTR2)+len(LTR3))+"\t"+str(round(acc_T5,4))+"\t"+str(round(acc_T10,4))+"\t"+str(round(acc_T20,4))+"\t"+str(round(acc_T30,4))+"\t"+str(round(acc_T50,4))+"\t"+str(round(acc_l30,4))+"\t"+str(round(acc_l20,4))+"\t"+str(round(acc_l10,4))+"\t"+str(round(acc_l5,4))+"\n")
        
        print ('Evaluate on full Test data..')
        (acc_T5, acc_T10, acc_T20, acc_T30, acc_T50, acc_l30, acc_l20, acc_l10, acc_l5)=print_detailed_accuracy_on_this_data(cyc_id + ' ALL-TEST    ', './cycle-' + str(cyc) + '.hdf5',LTE,XTE,YTE,pathX,pathY)
        with open ("testing_acc.txt","a+") as f:
            epoch = cyc
            if (epoch == 0):
                f.write("Epoch\tSample_Size\tPrec-T5\tPrec-T10\tPrec-T20\tPrec-T30\tPrec-T50\tL/30\tL/20\tL/10\tL/5\n")
            f.write(str(epoch)+"\t"+str(len(LTR1)+len(LTR2)+len(LTR3))+"\t"+str(round(acc_T5,4))+"\t"+str(round(acc_T10,4))+"\t"+str(round(acc_T20,4))+"\t"+str(round(acc_T30,4))+"\t"+str(round(acc_T50,4))+"\t"+str(round(acc_l30,4))+"\t"+str(round(acc_l20,4))+"\t"+str(round(acc_l10,4))+"\t"+str(round(acc_l5,4))+"\n")
            print("Testing Accuracies: \n"+str(epoch)+"\t"+str(len(LTR1)+len(LTR2)+len(LTR3))+"\t"+str(round(acc_T5,4))+"\t"+str(round(acc_T10,4))+"\t"+str(round(acc_T20,4))+"\t"+str(round(acc_T30,4))+"\t"+str(round(acc_T50,4))+"\t"+str(round(acc_l30,4))+"\t"+str(round(acc_l20,4))+"\t"+str(round(acc_l10,4))+"\t"+str(round(acc_l5,4))+"\n")


