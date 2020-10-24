#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 11:42:41 2020

@author: farhan
"""

#this script filters out the missing fastas from 
import os

fasta_folder="/data/farhan/SoftwareTools/HomopolymerProject/data/homodimers/scripts/final_training_set_04_13_2020/all_same_fastas/"
label_folder="/data/farhan/SoftwareTools/HomopolymerProject/data/homodimers/scripts/Y-Labels/Y-"
name_list=[]
missing_list=[]
list_file="/data/farhan/SoftwareTools/HomopolymerProject/DeepComplex/training/dncon2_model/training_lists/same/all_training_protein_list.txt"
with open (list_file,"r") as f:
    for line in f:
        name_list.append(line.strip())

for name in name_list:
    if not os.path.exists(fasta_folder+name+".fasta"): missing_list.append(name+"\n")
    #if not os.path.exists(label_folder+name+".txt"): missing_list.append(name+"\n")
print (len(name_list))
print (len(missing_list))
#print ("ls "+label_folder+name+".txt")
#print (os.system("ls "+label_folder+name+".txt"))
with open("missing_fastas.txt","w") as f:
    f.writelines(missing_list)
