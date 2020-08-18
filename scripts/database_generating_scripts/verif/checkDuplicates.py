#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 21 10:03:04 2020

@author: farhan
"""

def reverseDict(d):
    new_dict={}
    dup_key=[]
    for key, value in d.items():
        if value in new_dict.keys(): 
            print ("Duplicate fasta for: "+key+"\n"+new_dict[value])
            dup_key.append((new_dict[value],key))
            #print(value)
        new_dict[value]=key
    return new_dict, dup_key


AB_dict={}
#fasta=""
with open ("./hetero_cdhit/hetero30","r") as f:
#with open ("./hetero_mmseqs/hetero25","r") as f:
#with open ("homo100_mmseqs","r") as f:
    for line in f:
        if (line.startswith(">")):
            #fasta=""
            fasta=f.readline().strip()
            AB_dict[line.strip()]=fasta

print (len(AB_dict))

reversed_AB_dict, dup=reverseDict(AB_dict)
print(len(reversed_AB_dict))

#for keys in list(AB_dict.keys()):
    