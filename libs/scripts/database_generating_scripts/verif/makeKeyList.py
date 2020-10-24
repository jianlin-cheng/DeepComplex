#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 22 08:49:06 2020

@author: farhan
"""
fasta_file="hetero100"
folder="./hetero_cdhit/"
#folder="./hetero_mmseqs/"
output_file="hetero100_red"
AB_dict={}
key_list=[]
with open (folder+fasta_file,"r") as f:
    for line in f:
        if line.startswith(">"):
            key_list.append(line.strip())
            fasta=f.readline().strip()
            AB_dict[line.strip()]=fasta
            
#with open (folder+"key_list.txt","w") as f:
#    f.writelines(key_list)
contact_key_dict={}
contact_pair_list=[]

for key in key_list:
    pdb_A=key.split("_")[0].lstrip(">")
    if len(key.split("_"))==3: pdb_B=key.split("_")[1].strip()
    if len(key.split("_"))==4: pdb_B=key.split("_")[2].strip()
    contact_pair_list.append(pdb_A+","+pdb_B+"\n")
    contact_key_dict[pdb_A+","+pdb_B]=key
#print (contact_key_dict)
#print (len(contact_key_dict))


pair_key_list=list(contact_key_dict.keys())
#xy=pair_key_list[-1]
#print(xy)

dupe_list=[]
#print(yx)
for xy in pair_key_list:
    split=xy.split(",")
    yx=split[1]+","+split[0]
    if (yx in pair_key_list):
        #print(xy)
        #print(yx)
        AB_dict.pop(contact_key_dict[yx].strip())
        dupe_list.append(contact_key_dict[xy]+"\t\t"+contact_key_dict[yx]+"\n")
        pair_key_list.remove(yx)
print (len(AB_dict))
print("Dupes: ",len(dupe_list))

with open (folder+output_file,"w") as f:
    for key, value in AB_dict.items():
        f.write(key+"\n")
        f.write(value+"\n")

with open (folder+"dupes_list.txt","w") as f:
    f.writelines(dupe_list)

