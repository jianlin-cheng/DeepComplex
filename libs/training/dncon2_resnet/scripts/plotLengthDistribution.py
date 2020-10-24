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

length_list_file="/data/farhan/SoftwareTools/HomopolymerProject/DeepComplex/training/dncon2_model/training_lists/same/all_training_protein_length.txt"
#length_list_file="/data/farhan/SoftwareTools/HomopolymerProject/DeepComplex/training/dncon2_model/training_lists/all_training_protein_length.txt"
range_gap=100
range_gap_list=[]
all_dict={}
with open (length_list_file,"r") as f:
    for line in f:
        all_dict[line.strip().split()[0]]=int(line.strip().split()[1])

maxLength=max(all_dict.values())

sets=int(maxLength/range_gap)

last_limit=int(sets*range_gap)

print (len(all_dict))
print (maxLength)
print (sets)

df = pd.read_csv(length_list_file,sep="\t",index_col=None,header=None)
#df = df.astype({1:"int32"})
df.astype({1:"int32"})
#print (len(df))
#print (df.describe())
#print (df[1])
#cut=pd.qcut(df[1],q=4)
#cut_bins=[]
#cut_bins=pd.interval_range(start=0, freq=range_gap, end=maxLength, closed="right")
cut_bins=pd.interval_range(start=0, freq=range_gap, end=range_gap*(sets+1), closed="right")
cut_labels=[]
print (cut_labels)
"""
for sts in range(sets+1):
    cut_bins.append(sts*range_gap)
    #if sts!=0: cut_labels.append(str((sts-1)*range_gap))
    #print(sts)
if len(cut_bins)==sets+1:
    cut_bins.append(maxLength)
    #cut_labels.append(str(maxLength))
"""
print (cut_bins)    
#val_cut=pd.cut(df[1],bins=cut_bins,labels=cut_labels)
val_cut=pd.cut(df[1],bins=cut_bins)

val_cut=val_cut.value_counts()

keys=sorted(val_cut.index)
val_cut=val_cut.sort_index()
val_cut.plot.bar(grid=True)
#dictionary = plt.figure()
#xticks(labels=list(D.keys()))
#plt.bar(D.keys(),D.values(),color="g")
plt.hist(val_cut)
plt.title("Length frequency distribution")
plt.xlabel("Length Range")
plt.ylabel("Frequency")


#print (type(val_cut))
#print (type(val_cut.index))
#print (val_cut.)
#print (val_cut[0].to_string())
os.system("echo '"+val_cut.to_string()+"' > data_same_distr_"+str(range_gap)+".txt")


    