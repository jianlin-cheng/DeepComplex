#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan  5 22:35:30 2020

@author: farhan
"""

# this script creates a list of proteins that have same fasta sequences
#usage: python createSimilarFastaList.py <fasta_dictionary.txt>
import os,sys

fasta_dict={}

with open ("fasta_dictionary.txt","r") as f:
    for line in f:
        fasta_dict[line.split(":")[0].strip()]=line.split(":")[1].strip()

key_list=sorted(fasta_dict.keys())

print (len(key_list))
same_list=[]
different_list=[]

length=len(fasta_dict)
i=0
#while (i<length-1):
#[Modify the following code according to need]
for i in range(length-1):
    j=i+1
    while (j<length) :
        if (key_list[i][0:4]==key_list[j][0:4]):
            if (fasta_dict[key_list[i]]==fasta_dict[key_list[j]]):
                same_list.append(key_list[i][0:4]+"\n") #for multimers we can use pairs
                #break if needed
#                break
            else:
                different_list.append(key_list[i][0:4]+"\n") #for multimers ew can use pairs
                #break if needed
#                break
        else:
            break #moved to the next pdb
        j+=1

"""
for i in range(0,4,2):
    if (fasta_dict[key_list[i]]==fasta_dict[key_list[i+1]]):
        same_list.append(key_list[i]+"\n")
    else:
        different_list.append(key_list[i]+"\n")
"""

with open("same_fasta_list.txt","w") as f:
    f.writelines(same_list)

with open ("different_fasta_list.txt","w") as f:
    f.writelines(different_list)
