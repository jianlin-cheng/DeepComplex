#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  5 10:21:24 2019

@author: farhan
"""

#this script does the intrachain contacts of the .atom files of a particular protein with the highest number of lines
#usage python doAll_interchain_protein_list.py <protein_name> <.atom folder> <out_dir>


import os,sys

def getPDBNames(protein_list):
    new_list=[]
    for items in protein_list:
        name=items.strip().split("/")[-1][0:4]#.replace(".pdb","")
        name=name.replace(".fasta","")
        name=name.replace(".atom","")
        name=name.replace(".seq","")
        name=name.replace(".dssp","")
        new_list.append(name)
    return new_list


protein_list_file=sys.argv[1]
atom_folder=sys.argv[2]
dist=sys.argv[3]
outdir=sys.argv[4]
protein_list=[]
with open (protein_list_file,"r") as f:
    for line in f:
        protein_list.append(line.strip())

protein_list=getPDBNames(protein_list)

#print (protein_list)

for protein_name in protein_list:
    print("Processing interchain contact for heavy atoms for: "+protein_name)
    os.system("python doAll_interchain_protein_heavy.py "+protein_name+" "+atom_folder+" "+dist+" "+outdir)
    #break
