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

length_list_file="/data/farhan/SoftwareTools/HomopolymerProject/DeepComplex/training/dncon2_model/training_lists/all_training_protein_length.txt"
#length_list_file="/data/farhan/SoftwareTools/HomopolymerProject/DeepComplex/training/dncon2_model/training_lists/all_training_protein_length.txt"
range_gap=100
range_gap_list=[]
all_dict={}
with open (length_list_file,"r") as f:
    for line in f:
        #all_dict[line.strip().split()[0]]=int(line.strip().split()[1])
        if (int(line.strip().split()[1])>=30):all_dict[line.strip().split()[0]]=int(line.strip().split()[1])

print (len(all_dict))