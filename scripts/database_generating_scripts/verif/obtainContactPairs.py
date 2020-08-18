#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 21 12:51:25 2020

@author: farhan
"""
#this script reads the combined A+B fasta and creates a contact pair list between the chains
fasta_file="hetero100_red"
folder="./hetero_cdhit/"
output_file="hetero100_nr_contact_pairs_list.txt"
AB_dict={}

with open (folder+fasta_file,"r") as f:
    for line in f:
        if (line.startswith(">")):
            fasta=f.readline().strip()
            AB_dict[line.strip()]=fasta

key_list=list(AB_dict.keys())

print (len(key_list))

contact_pairs_list=[]
for key in key_list:
    pdb_A=key.split("_")[0].lstrip(">")
    if len(key.split("_"))==3: pdb_B=key.split("_")[1].strip()
    if len(key.split("_"))==4: pdb_B=key.split("_")[2].strip()
    contact_pairs_list.append(pdb_A+","+pdb_B+"\n")

with open (folder+output_file,"w") as f:
    f.writelines(contact_pairs_list)

"""
with open (folder+"redundant_"+output_file,"w") as f:
    f.writelines(contact_pairs_list)

print (len(contact_pairs_list))

redundant_list=[]

for i in range(len(contact_pairs_list)):
    for pair in contact_pairs_list:
        split=contact_pairs_list[i].strip().split(",")
        reverse_pair=split[1]+","+split[0]
        if reverse_pair.strip()==pair.strip():
            redundant_list.append([contact_pairs_list[i].strip(),pair.strip()])
            break

print (len(redundant_list))

with open (folder+"duplicates_in_"+output_file,"w") as f:
    for i in range(len(redundant_list)):
        f.write(redundant_list[i][0]+"\t\t"+redundant_list[i][1]+"\n")
#print (key_list[0])
"""