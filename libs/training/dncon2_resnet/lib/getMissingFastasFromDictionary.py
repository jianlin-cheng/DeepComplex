#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 12:16:56 2020

@author: farhan
"""
#gets the missing list from missing_fastas.txt and creates a folder and writes new fasta files
#getMissingFastasFromDictionary.py

from loadFastaDictionary import *
import os
fasta_dict=loadFastaDictionary("fasta_dictionary.txt")
print (len(fasta_dict))

missing_list=[]
with open ("missing_fastas.txt","r")as f:
    for line in f:
        missing_list.append(line.strip())

print (len(missing_list))
new_fasta_dict={}

key_list=list(fasta_dict.keys())

for name in missing_list:
    for key in key_list:
        if name in key:  
            new_fasta_dict[name]=fasta_dict[key]
print (len(new_fasta_dict))

if not os.path.isdir("missing_fasta_dir"): os.makedirs("missing_fasta_dir")
for key,value in new_fasta_dict.items():
    with open ("missing_fasta_dir/"+key+".fasta","w")as f:
        f.write(">"+key+"\n")
        f.write(value)