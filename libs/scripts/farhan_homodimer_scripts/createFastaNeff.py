#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 14 18:50:14 2020

@author: farhan
"""

#this script reads the fasta_dictionary.txt and dncon2.rr files and creates a database/dictionary of PDB_Name and Neff
#Format: PDB/Name   Neff
#usage: python createFastaLength.py

import numpy as np

all_8886_protein_list=[]
all_protein_Neff_list=[]
all_protein_Neff_list.append("Name\tNeff\tln(Neff)\n")
Neff_dict={}
with open ("all_8886_protein_list.txt","r") as f:
    for line in f:
        #print (line)
        all_8886_protein_list.append(line.strip())
for pdb in all_8886_protein_list:
    with open ("./dncon2_rr/"+pdb+".dncon2.rr","r") as f:
        for line in f:
            if ("REMARK Effective number of sequences in the alignment" in line):
                Neff_dict[pdb]=line.split("=")[1].strip()
                all_protein_Neff_list.append(pdb+"\t"+Neff_dict[pdb]+"\t"+str(np.log(float(Neff_dict[pdb])))+"\n")
                break

with open ("all_8886_protein_Neff.txt","w") as f:
    f.writelines(all_protein_Neff_list)

print (Neff_dict["3VKG"])