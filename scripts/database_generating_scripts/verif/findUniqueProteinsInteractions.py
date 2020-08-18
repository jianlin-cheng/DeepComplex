#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 22 10:08:04 2020

@author: farhan
"""

fasta_file="hetero100_nr_contact_pairs_list.txt"
folder="./hetero_cdhit/"
#folder="./hetero_mmseqs/"
output_file="hetero100_red"
AB_dict={}
plist=[]
pdb_list=[]
with open (folder+fasta_file,"r") as f:
    for line in f:
        plist.append(line.split(",")[0])
        pdb_list.append(line.split(",")[0][0:4])

print (len(plist))
plist=list(set(plist))
print (len(plist))

print (len(list(set(pdb_list))))