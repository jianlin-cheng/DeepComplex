#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 14 18:50:14 2020

@author: farhan
"""

#this script reads the fasta_dictionary.txt file and creates a database/dictionary of PDB_Name and lengths
#Format: PDB   Chains(csv)  Lengths(csv)
#usage: python createFastaLength.py

def getMaxLength(length_tuple):
    if (length_tuple.endswith(",")):length_tuple=length_tuple[0:len(length_tuple)-1]
    
    split=length_tuple.split(",")
    for i in range(len(split)):
        split[i]=int(split[i])
    
    return max(split)

fasta_dict={}

with open ("fasta_dictionary.txt","r") as f:
    for line in f:
        #fasta_dict[line.split(":")[0].strip()]=line.split(":")[1].strip()+" "+len(line.split(":")[1].strip())
        fasta_dict[line.split(":")[0].strip()]=str(len(line.split(":")[1].strip()))

length_dict={}
max_length_dict={}
pdb_key_list=fasta_dict.keys()
pdb_list=[]

chain_dict={}

for k in pdb_key_list:
    chain_dict[k[0:4]]=""
    length_dict[k[0:4]]=""
    
for k in pdb_key_list:
    chain_dict[k[0:4]]+=k[4]+","
    length_dict[k[0:4]]+=fasta_dict[k]+","
all_8886_protein_list=[]
all_protein_length_list=[]
all_protein_length_list.append("Name\tChain\tLength\n")

with open ("all_8886_protein_list.txt","r") as f:
    for line in f:
        #print (line)
        all_8886_protein_list.append(line.strip())
        if (chain_dict[line.strip()].endswith(",")):chain_dict[line.strip()]=chain_dict[line.strip()][0:len(chain_dict[line.strip()])-1]
        if (length_dict[line.strip()].endswith(",")):length_dict[line.strip()]=length_dict[line.strip()][0:len(length_dict[line.strip()])-1]
        all_protein_length_list.append(line.strip()+"\t"+chain_dict[line.strip()]+"\t"+length_dict[line.strip()]+"\n")
        max_length_dict[line.strip()]=getMaxLength(length_dict[line.strip()])

with open ("all_8886_protein_chained_length.txt","w") as f:
    f.writelines(all_protein_length_list)

with open ("all_8886_protein_max_length.txt","w")as f:
    f.write("Name\tLength\n")
    for key,value in max_length_dict.items():
        f.write(key+"\t"+str(value)+"\n")

print (length_dict["3VKG"])
print (max_length_dict["3VKG"])
print (length_dict["4CSM"])
print (max_length_dict["4CSM"])

#print(chain_dict["1EK1"])
#print(length_dict["3VKG"])
#for key in pdb_key_list:
#    pdb_list.append(key[0:4])
#print (len(fasta_dict))