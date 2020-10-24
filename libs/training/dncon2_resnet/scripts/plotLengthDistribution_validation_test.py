#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul  4 01:25:01 2020

@author: farhan
"""

#this script reads the length.txt file and plots a distribution of frequency vs range of lengths
import pandas as pd
import matplotlib.pyplot as plt
import os

def getCut(d, cut_bins):
    df_dict=pd.DataFrame.from_dict(d,orient="index")
    df_dict=df_dict.astype({0:"int32"})
    val_cut=pd.cut(df_dict[0],bins=cut_bins)
    val_cut=val_cut.value_counts()
    val_cut=val_cut.sort_index()
    val_cut.plot.bar(grid=True)
    
    return val_cut

length_list_file="/data/farhan/SoftwareTools/HomopolymerProject/DeepComplex/training/dncon2_model/training_lists/same/all_training_protein_length.txt"
train_list_file="/data/farhan/SoftwareTools/HomopolymerProject/DeepComplex/training/dncon2_model/training_lists/same/train_list.txt"
val_list_file="/data/farhan/SoftwareTools/HomopolymerProject/DeepComplex/training/dncon2_model/training_lists/same/validation_list.txt"
test_list_file="/data/farhan/SoftwareTools/HomopolymerProject/DeepComplex/training/dncon2_model/training_lists/same/test_list.txt"
range_gap=100
range_gap_list=[]
all_dict={}
train_dict={}
test_dict={}
val_dict={}

with open (length_list_file,"r") as f:
    for line in f:
        all_dict[line.strip().split()[0]]=int(line.strip().split()[1])

with open (train_list_file,"r") as f:
    for line in f:
        train_dict[line.strip()]=all_dict[line.strip()]

with open (test_list_file,"r") as f:
    for line in f:
        test_dict[line.strip()]=all_dict[line.strip()]

with open (val_list_file,"r") as f:
    for line in f:
        val_dict[line.strip()]=all_dict[line.strip()]

maxLength=max(all_dict.values())

sets=int(maxLength/range_gap)

last_limit=int(sets*range_gap)

print (len(all_dict))
print (maxLength)
print (sets)

df = pd.read_csv(length_list_file,sep="\t",index_col=None,header=None)
df=df.astype({1:"int32"})
cut_bins=pd.interval_range(start=0, freq=range_gap, end=range_gap*(sets+1), closed="right")

print (cut_bins)    
all_cut=pd.cut(df[1],bins=cut_bins)
all_cut=all_cut.value_counts()
#keys=sorted(all_cut.index)
all_cut=all_cut.sort_index()
#Plot bars
all_cut.plot.bar(grid=True)
plt.title("Length frequency distribution")
plt.xlabel("Length Range")
plt.ylabel("Frequency")
os.system("echo '"+all_cut.to_string()+"' > data_distr_"+str(range_gap)+".txt")

#print (len(train_dict))
#print (len(val_dict))
#print (len(test_dict))
#print (test_dict)
df_train=getCut(train_dict,cut_bins)
df_val=getCut(val_dict,cut_bins)
df_test=getCut(test_dict,cut_bins)

os.system("echo '"+df_train.to_string()+"' > train_distr_"+str(range_gap)+".txt")
os.system("echo '"+df_val.to_string()+"' > val_distr_"+str(range_gap)+".txt")
os.system("echo '"+df_test.to_string()+"' > test_distr_"+str(range_gap)+".txt")


    