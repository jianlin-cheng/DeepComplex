#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  4 13:06:55 2020

@author: farhan
"""

#predictor script


import shutil
import sys, os
import numpy as np
from glob import glob
import time
import subprocess
import gc
import platform
from keras.optimizers import Adam, Adadelta, SGD, RMSprop, Adagrad, Adamax, Nadam
from DNCON_lib import *
from readRR import readRRFile
from keras.models import model_from_json, load_model
from training_strategy import *
from keras.utils import CustomObjectScope

project_root = os.path.dirname(os.path.abspath(sys.argv[0])).replace("scripts","")
print(project_root)
if not project_root.endswith("/"): project_root+="/"
sys.path.insert(0, project_root + "lib")
print ("Project Root Directory: ",project_root)

#from libtrain import *
#from libcommon import *

from Model_lib import *
from DNCON2_library import *
from training_strategy import *

def build_dataset_dictionaries(path_lists):
    length_dict = {}
#    n_dict = {}
#    neff_dict = {}
    with open(path_lists + 'all_training_protein_length.txt') as f:
        for line in f:
            cols = line.strip().split()
            length_dict[cols[0]] = int(cols[1])
    return length_dict

def writeToRRFile(pred,filename,L,label_flag=False):
    pred_new=np.zeros((L,L))
    pred_new=pred[0:L,0:L]
    np.savetxt(filename+".npy.txt",pred_new)
    fasta="A"*L
    with open (filename,"w") as f:
        f.write(fasta+"\n")
        for i in range(L):
            for j in range(L):
                if label_flag:
                    if pred[i][j]== 1.0: f.write(str(i+1)+" "+str(j+1)+" 0 6.0 "+str(pred[i][j])+"\n")
                else:
                    f.write(str(i+1)+" "+str(j+1)+" 0 6.0 "+str(pred[i][j])+"\n")

def read_file(_input):
    output_array=[]
    if os.path.isfile(_input):
        _file = open(_input, "r")
        if _file.mode == 'r':
            output_array = _file.read().strip().splitlines()
        _file.close()
    return output_array

def read_file(_input):
    output_array=[]
    if os.path.isfile(_input):
        _file = open(_input, "r")
        if _file.mode == 'r':
            output_array = _file.read().strip().splitlines()
        _file.close()
    return output_array

def calculateEvaluationStats(pred_cmap, true_cmap, name,L,epochs):
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
    # ll=int(np.sqrt(len(pred_cmap)))
    ll=370
    print("ll=",L)
    pred_cmap=pred_cmap.squeeze().reshape(ll,ll)
    if len(true_cmap.shape)==1: true_cmap=true_cmap.reshape(ll,ll)
    print("&&"*30)
    print (true_cmap.shape, pred_cmap.shape)
    if true_cmap.shape!=pred_cmap.shape: print ("True and predicted contact maps do not match in shape!")
    print("&&"*30)
    fasta_file="/storage/htc/bdm/farhan/DNCON2_features_homodimers/final_training_set_04_13_2020/all_same_fastas/"+name+".fasta"
    cmap_folder="/storage/htc/bdm/farhan/DeepComplex/training/dncon2_model/contact_maps/"
    #pred_cmap_list=toCmap(pred_cmap,fasta_file)
    #true_cmap_list=toCmap(true_cmap,fasta_file)
    
    max_Top=int((L/5)+0.5)
    if 50>max_Top: max_Top=50
    pred_cmap=pred_cmap[0:L,0:L]
    true_cmap=true_cmap[0:L,0:L]
    for i in range(1,max_Top+1):
        (x,y)=np.unravel_index(np.argmax(pred_cmap,axis=None),pred_cmap.shape)#coordinates of maximum value in 2d array
        pred_cmap[x][y]=0 #set that value to minimum so it is not picked in next turn
        if true_cmap[x][y]==1:
            con_num+=1

        if i==5:
            prec_T5=con_num*20
            if prec_T5>100: prec_T5=100
            print ("L=", L, "Val=",5,"Con_num=",con_num)
        if i==10:
            prec_T10=con_num*10
            if prec_T10>100: prec_T10=100
            print ("L=", L, "Val=",10,"Con_num=",con_num)
        if i==20:
            prec_T20=con_num*5
            if prec_T20>100: prec_T20=100
            print ("L=", L, "Val=",20,"Con_num=",con_num)
        if i==30:
            prec_T30=con_num*100/30
            if prec_T30>100: prec_T30=100
            print ("L=", L, "Val=",30,"Con_num=",con_num)
        if i==50:
            prec_T50=con_num*2
            if prec_T50>100: prec_T50=100
            print ("L=", L, "Val=",50,"Con_num=",con_num)
        if i==int((L/30)+0.5):
            prec_L30=con_num*100/i
            if prec_L30>100: prec_L30=100
            print ("L=", L, "Val=",i,"Con_num=",con_num)
        if i==int((L/20)+0.5):
            prec_L20=con_num*100/i
            if prec_L20>100: prec_L20=100
            print ("L=", L, "Val=",i,"Con_num=",con_num)
        if i==int((L/10)+0.5):
            prec_L10=con_num*100/i
            if prec_L10>100: prec_L10=100
            print ("L=", L, "Val=",i,"Con_num=",con_num)
        if i==int((L/5)+0.5):
            prec_L5=con_num*100/i
            if prec_L5>100: prec_L5=100
            print ("L=", L, "Val=",i,"Con_num=",con_num)
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



current_os_name = platform.platform()
print('%s' % current_os_name)
sysflag=""

if 'Ubuntu' in current_os_name.split('-'): #on local
  sysflag='local'
elif 'centos' in current_os_name.split('-'): #on lewis or multicom
  sysflag='lewis'
else:
  sysflag="local"
      

print ("sysflag=",sysflag)

gpu_mem = gpu_schedul_strategy(sysflag, gpu_mem_rate = 0.8, allow_growth = True)

global pathX, pathY, path_lists, min_len, max_len
pathY  = '/data/commons/DeepComplex_common/datasets/DNCON2_features_homodimers//Y-Labels/'
pathX = '/data/commons/DeepComplex_common/datasets/DNCON2_features_homodimers/feat/'
test_file_list='/data/commons/DeepComplex_common/DeepComplex/training/exp_model_saver/training_lists/same/test_list.txt'
model_dir="/data/commons/DeepComplex_common/DeepComplex/training/exp_model_saver/"
outdir=model_dir+"predict_map/"
model="homo_stdb_370.json"
# current_weights="model-train-weight-DNCON4_RESOTHER.h5"
best_weights="weights_80.hdf5"
len_dict = build_dataset_dictionaries('/data/commons/DeepComplex_common/DeepComplex/training/exp_model_saver/training_lists/same/')
json_file = open(model_dir+model, 'r')
loaded_model_json = json_file.read()
json_file.close()
model = model_from_json(loaded_model_json)
# load weights into new model
model.load_weights(model_dir+best_weights)


file_list = read_file(test_file_list)

for key in file_list:
    feat_file=pathX+'feat-'+key+'.txt'
    label=pathY+'Y-'+key+'.txt'
    # feat_file="/data/commons/DeepComplex_common/datasets/DNCON2_features_homodimers/feat/feat-5KEJ.txt"
    # label = "/data/commons/DeepComplex_common/datasets/DNCON2_features_homodimers/Y-Labels/Y-5KEJ.txt"
    # feat_file="/data/commons/DeepComplex_common/datasets/DNCON2_features_homodimers/feat/feat-3TFJ.txt"
    # label = "/data/commons/DeepComplex_common/datasets/DNCON2_features_homodimers/Y-Labels/Y-3TFJ.txt"

    # key=os.path.basename(feat_file).replace("feat-","").replace(".txt","")
    print ("Getting X-features for "+key)
    val = len_dict.get( key )
    if val <=370:
        X=get_x_from_this_file(feat_file,370)
    # Y = getY(label, 0, 500)
    # fea_len = X[0].shape[0]
    # X_reshape = np.zeros((500, 500, 56))
    # for m in range(0, fea_len):
    #     X_reshape[0:fea_len, 0:fea_len, m] = X[m]


        print ("Making predictions for: "+key)
        print ("X.shape=",X.shape)
        L=int(np.squeeze(X).shape[0])
        # model = DNCON2_tr_rosetta_ResNet(inputs=X,filters=32,residual_block_num=60,kernel_size=3)
        P=model.predict([X],batch_size=1)
        P=P.squeeze().reshape(L,L)
        value=get_x_from_this_file(feat_file).shape[1]
        filename=outdir+key+"_.rr"
        writeToRRFile(P,filename,L=value)
        Y=np.loadtxt(label)
        filename=outdir+"Y-"+key+".txt"
        writeToRRFile(Y,filename,L=value, label_flag=True)
    else:
        print('greater than 370 '+key)
    # P=P.squeeze()
    # Y=np.loadtxt(label)
    # print(Y)
    # print (Y.shape())
    # print (P.shape())
    # calculateEvaluationStats(P,Y,'test',get_x_from_this_file(feat_file).shape[1],0)