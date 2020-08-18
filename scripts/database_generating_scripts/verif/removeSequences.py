#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 21 08:01:52 2020

@author: farhan
"""

def reverseDict(d):
    new_dict={}
    for key, value in d.items():
        new_dict[value]=key
    return new_dict


AB_rem_key_list=[]
BA_rem_key_list=[]
with open ("same_seq.txt","r") as f:
    for line in f:
        AB_rem_key_list.append(line.strip().split("\t")[0])
        BA_rem_key_list.append(line.strip().split("\t")[-1])
        #break
print (len(AB_rem_key_list))
print (len(BA_rem_key_list))
AB_rem_key_list=list(set(AB_rem_key_list))
BA_rem_key_list=list(set(BA_rem_key_list))


AB_dict={}
BA_dict={}
all_dict={}

"""
with open ("hetero100_AB","r") as f:
    for line in f:
        if (line.startswith(">")):
            if line.strip() in AB_rem_key_list: 
                f.readline()
                continue
            fasta=f.readline().strip()
            AB_dict[line.strip()]=fasta
"""
with open ("hetero100_AB","r") as f:
    for line in f:
        if (line.startswith(">")):
            fasta=f.readline().strip()
            AB_dict[line.strip()]=fasta

with open ("hetero100_BA","r") as f:
    for line in f:
        if (line.startswith(">")):
            if line.strip() in BA_rem_key_list: 
                f.readline()
                continue
            fasta=f.readline().strip()
            BA_dict[line.strip()]=fasta


reversed_AB_dict=reverseDict(AB_dict)
reversed_BA_dict=reverseDict(BA_dict)

print(len(reversed_AB_dict))
print(len(reversed_BA_dict))

key_list_AB=list(reversed_AB_dict.keys())
key_list_BA=list(reversed_BA_dict.keys())

similar_list=[]

for key_i in key_list_AB:
    for key_j in key_list_BA:
        if key_i == key_j:  
            similar_list.append(reversed_AB_dict[key_i]+"\t\t"+reversed_BA_dict[key_j]+"\n")
            similar_list.append(key_i+"\n")
            similar_list.append(key_j+"\n")

with open ("same_seq_still_found.txt","w") as f:
    f.writelines(similar_list)

"""
with open ("hetero_all_100","r") as f:
    for line in f:
        if (line.startswith(">")):
            if (line.strip() in AB_rem_key_list) or (line.strip() in BA_rem_key_list): 
                print (line.strip())
                f.readline()
                continue
            fasta=f.readline().strip()
            all_dict[line.strip()]=fasta
"""

print (len(AB_dict))
print (len(BA_dict))
print (len(all_dict))


