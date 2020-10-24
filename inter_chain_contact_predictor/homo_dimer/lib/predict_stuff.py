#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 20 23:33:16 2020

@author: farhan
"""
#from Model_construct import *
import os, sys
from DNCON_lib import *
from readRR import readRRFile
import numpy as np
from keras.models import model_from_json, load_model
from training_strategy import *
from keras.utils import CustomObjectScope


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

def copyFiles(name,source,dest):
    if not os.path.exists(source+name+".dncon2.rr"):
        print (source+name+".dncon2.rr file not found!")
        return False
    
    os.system("scp "+source+name+".dncon2.rr "+dest)
    return True

dist_string = ""#'80'
limit =500
path_of_lists   = "../training_lists/same/"#GLOBAL_PATH+'/data/'+dataset+'/lists-test-train/'
reject_fea_file = "feature_to_use.txt"#"/lib/feature_txt/feature_to_use"+fea_file+".txt"#'/lib/feature_txt/feature_to_use_'+fea_file+'.txt'
############ Change here if necessary
path_of_X       = "/data/commons/DeepComplex_common/datasets/DNCON2_features_homodimers/feat/" #"/data/commons/DeepComplex_common/datasets/DNCON2_features_homodimers/feat"#feature_dir #feature_dir + '/features/' + dataset + '/'
path_of_Y       = "/data/commons/DeepComplex_common/datasets/DNCON2_features_homodimers/Y-Labels/" #"/data/commons/DeepComplex_common/datasets/DNCON2_features_homodimers/Y-Labels"#feature_dir 
model_dir="/data/commons/DeepComplex_common/DeepComplex/training/exp_model_saver/"
model="homo_stdb.json"
current_weights="model-train-weight-DNCON4_RESOTHER.h5"
best_weights="weights_64.h5"
outdir=model_dir+"predict_map/"
feature_num = load_sample_data_2D_intra(path_of_lists, path_of_X, path_of_Y,7000,0,dist_string, reject_fea_file)
#value=int(np.exp(featuredata[1][0][0])+0.5)
all_L=build_dataset_dictionaries_file(path_of_lists,"all_training_protein_list.txt")
all_subset=subset_pdb_dict(all_L,30,limit,10000,"ordered")
test_dict_L=build_dataset_dictionaries_file(path_of_lists,"test_.lst")
valid_dict_L=build_dataset_dictionaries_test(path_of_lists)
train_dict_L=build_dataset_dictionaries_train(path_of_lists)
test_dict=subset_pdb_dict(test_dict_L,30,limit,10000,"ordered")
valid_dict=subset_pdb_dict(valid_dict_L,30,limit,10000,"ordered")
train_dict=subset_pdb_dict(train_dict_L,30,limit,10000,"ordered")

#print (len(all_dict_L))
print (len(test_dict))
print (len(valid_dict))
print (len(train_dict))
print (len(all_L),len(all_subset))
#print (min(test_dict.values()))

test_name_dict=list(test_dict.keys())
valid_name_dict=list(valid_dict.keys())
train_name_dict=list(train_dict.keys())


with CustomObjectScope({'InstanceNormalization': InstanceNormalization, 'RowNormalization': RowNormalization, 'ColumNormalization': ColumNormalization, 'tf':tf}):
    json_file = open(model_dir+model, 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    model = model_from_json(loaded_model_json)
# load weights into new model
    model.load_weights(model_dir+best_weights)

#length=limit
source="/data/farhan/SoftwareTools/HomopolymerProject/data/homodimers/scripts/dncon2_combined/"
dest=path_of_X+"/intra/"
#for key in train_dict.keys():
#    copyFiles(key,source,dest)


#sys.exit()
for key in test_name_dict:
    #key="1GYO"
    #value=106
    p1={key:test_name_dict[key]}
    print (p1)
    #p1={key:value}
    value=test_name_dict[key]
    print (key,value)
    selected_list_2D = get_x_2D_from_this_list(p1, path_of_X, value, dist_string, reject_fea_file, value)
    if type(selected_list_2D) == bool: 
        print ("Problem with "+key)
        continue
    #print (type(selected_list_2D))
    #print (selected_list_2D.shape)
    #break
    label = get_y_from_this_list(p1, path_of_Y, 0, value, dist_string)
    prediction=model.predict([selected_list_2D],batch_size=1)
    prediction=prediction.reshape(value,value)
    label=label.reshape(value,value)
    #break
    #print (prediction.shape)
    filename=outdir+key+"_.rr"
    writeToRRFile(prediction,filename,L=value)
    filename=outdir+"Y-"+key+".txt"
    writeToRRFile(label,filename,L=value, label_flag=True)
    #break
    


"""
print(value)
length=limit
p1={'1GYO':value}

selected_list_2D = get_x_2D_from_this_list(p1, path_of_X, length, dist_string, reject_fea_file, value)
#selected_list_2D = get_x_2D_from_this_list(p1, path_of_X, value, dist_string, reject_fea_file, value)
with CustomObjectScope({'InstanceNormalization': InstanceNormalization, 'RowNormalization': RowNormalization, 'ColumNormalization': ColumNormalization, 'tf':tf}):
    json_file = open(model_dir+model, 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    model = model_from_json(loaded_model_json)
# load weights into new model
    model.load_weights(model_dir+best_weights)

print (selected_list_2D.shape)
prediction=model.predict([selected_list_2D],batch_size=1)
print (prediction.shape)

prediction=prediction.reshape(1,length*length)
#prediction=prediction.reshape(1,value*value)
#label = get_y_from_this_list(p1, path_of_Y, 0, length, dist_string).reshape(length,length)
label = get_y_from_this_list(p1, path_of_Y, 0, length, dist_string)
#label = get_y_from_this_list(p1, path_of_Y, 0, value, dist_string)
(avg_prec_l5, avg_prec_l2, avg_prec_1l, avg_mcc_l5, avg_mcc_l2, avg_mcc_1l, avg_recall_l5, avg_recall_l2, avg_recall_1l, avg_f1_l5, avg_f1_l2, avg_f1_1l)=evaluate_prediction_one(p1,prediction,label,0)
print (label.shape, label.sum())
print (prediction.shape)
print (avg_prec_l5*100)
print (avg_prec_l2*100)
print (avg_prec_1l*100)
#length=value
print (length,value)
prediction=prediction.reshape(length,length)
filename=model_dir+outdir+"1GYO_"+str(length)+".rr"
writeToRRFile(prediction,filename,length)

label = get_y_from_this_list(p1, path_of_Y, 0, length, dist_string).reshape(length,length)
filename=model_dir+outdir+"Y-1GYO_"+str(length)+".txt"
writeToRRFile(label,filename,length)

length=value
filename=model_dir+outdir+"1GYO_"+str(length)+".rr"
writeToRRFile(prediction,filename,length)
label = get_y_from_this_list(p1, path_of_Y, 0, length, dist_string).reshape(length,length)
filename=model_dir+outdir+"Y-1GYO_"+str(length)+".txt"
writeToRRFile(label,filename,length)
"""




