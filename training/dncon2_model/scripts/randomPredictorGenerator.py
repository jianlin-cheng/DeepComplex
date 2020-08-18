#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 21 06:11:21 2020

@author: farhan
"""
import os
import numpy as np

outfolder=os.path.abspath("./random_precisions/")+"/"
if not os.path.isdir(outfolder):os.makedirs(outfolder)

length_list_file="/data/farhan/SoftwareTools/HomopolymerProject/DeepComplex/training/dncon2_model/training_lists/all_training_protein_length.txt"
all_dict={}
with open (length_list_file,"r") as f:
    for line in f:
        all_dict[line.strip().split()[0]]=int(line.strip().split()[1])

key_list=all_dict.keys()
#all_dict={}
#all_dict["2CU3"]=61
for key,L in all_dict.items():
    print("Processing: ",key)
    filename=outfolder+key+"_rand.rr"
    fasta_file="/data/farhan/SoftwareTools/HomopolymerProject/data/homodimers/scripts/final_training_set_04_13_2020/fastas/"+key+".fasta"
    fasta=""
    rr_list=[]
    with open (fasta_file,"r") as f:
        for line in f:
            if line.startswith(">"): continue
            fasta+=line.strip()
    arr=np.random.rand(L,L)
    for i in range(L-1):
        for j in range(i+1,L):
            rr_list.append(str(i+1)+" "+str(j+1)+" 0 6 "+str(arr[i][j])+"\n")
    with open (filename,"w") as f:
        f.write(fasta+"\n")
        f.writelines(rr_list)