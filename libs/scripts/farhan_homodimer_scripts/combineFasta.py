#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 29 22:00:16 2020

@author: farhan
"""

#this script reads the sequence alignment files and combines the sequences into one fasta sequence 
#this fills out the gaps in the sequences
#usage: python combineFasta.py <foldername>

import os,sys

def combine(aln_list):
    L=len(aln_list[0])
    fasta="-"*L
    #print(aln_list)
    print(":"+aln_list[0])
    print(":"+aln_list[1])
    print(fasta)
    for i in range(L):
        if (aln_list[0][i]=="-"):
            if (aln_list[1][i]=="-"):
                continue
            else:
                fasta=fasta[0:i]+aln_list[1][i]+fasta[i+1:]
        
        if (aln_list[1][i]=="-"):
            if (aln_list[0][i]=="-"):
                continue
            else:
                fasta=fasta[0:i]+aln_list[0][i]+fasta[i+1:]
        
        if (aln_list[0][i]==aln_list[1][i] and aln_list[0][i]!="-"):
            fasta=fasta[0:i]+aln_list[0][i]+fasta[i+1:]
    return fasta

folder=sys.argv[1] #/aligned_seq_folder/
#folder="/data/farhan/SoftwareTools/HomopolymerProject/data/homodimers/scripts/aligned_seq_folder/"
if not (folder.endswith("/")): folder+="/"

os.system("python makePDBList.py "+folder+" > temp_seq_folder_list.txt")

pdb_list=[]
with open ("temp_seq_folder_list.txt","r") as f:
    for line in f:
        pdb_list.append(line.strip().split("/")[-1])

for aln_file in pdb_list:
    aln_list=[]
    #aln_file="1GQP.aln.txt"
    with open (folder+aln_file+".aln.txt","r") as f:
        for line in f:
            aln_list.append(line.strip().split(":")[1])
    final_fasta=combine(aln_list)
    #print (final_fasta)
    #break
    os.system("echo "+aln_file[0:4]+":"+final_fasta+" >> final_combined_fasta_dictionary.txt")
