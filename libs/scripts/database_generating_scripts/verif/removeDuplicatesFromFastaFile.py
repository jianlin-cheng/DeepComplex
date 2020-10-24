#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 22 07:58:11 2020

@author: farhan
"""
fasta_file="hetero100"
folder="./hetero_cdhit/"
duplicate_file="duplicates_in_hetero100_pairs_list.txt"
output_file="hetero100_red"
AB_dict={}
dupes_list=[]

with open (folder+duplicate_file,"r") as f:
    for line in f:
        split=line.strip().split("\t\t")
        dupes_list.append(split[0].strip())
        
print (len(dupes_list))
print (len(set(dupes_list)))

with open (folder+fasta_file,"r") as f:
    for line in f:
        if (line.startswith(">")):
            fasta=f.readline().strip()
            AB_dict[line.strip()]=fasta
key_list=list(AB_dict.keys())


for dupe in dupes_list:
    dupe_string=dupe.split(",")[0]+"_"+dupe.split(",")[1]
    other_dupe_string=dupe.split(",")[0]+"__"+dupe.split(",")[1]
    for key in key_list:
        if dupe_string in key:
            AB_dict.pop(key)
            print ("Removing: "+dupe_string)
            break
        if other_dupe_string in key:
            AB_dict.pop(key)
            print ("Removing: "+other_dupe_string)
            break

print ("Final size= ",len (AB_dict))
#print (AB_dict)
final_list=[]

for key,fasta in AB_dict.items():
    final_list.append(key+"\n")
    final_list.append(fasta.strip()+"\n")

with open (folder+output_file,"w") as f:
    f.writelines(final_list)


