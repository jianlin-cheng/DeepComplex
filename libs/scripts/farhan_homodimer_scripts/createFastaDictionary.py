#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan  5 21:57:31 2020

@author: farhan
"""

#this script reads the .seq files and creates a fasta dictionary
#usage: python createFastaDictionary.py <seq_folder>

import os,sys

#seq_folder="/data/farhan/SoftwareTools/HomopolymerProject/data/homodimers/homodimers_files/work_dir/seq/"
seq_folder=sys.argv[1]#"/data/farhan/SoftwareTools/HomopolymerProject/data/homooligomers/original_pdbs_7400/work_dir/seq/"
seq_list="seq_list.txt"
os.system("python makePDBListAllFiles.py "+seq_folder+" > seq_list.txt")
pdb_list=[]
seq_fasta_dict={}
"""
with open (seq_list,"r") as f:
    for pdb in f:
        pdb=pdb.strip()
        os.system("ls "+seq_folder+pdb+"* > temp_seq.txt")
        
        with open ("temp_seq.txt","r") as fseq:
            for seqfile in fseq:
                fasta=""
                with open (seqfile.strip(),"r") as seq:
                    for _ in range (5):
                        line=seq.readline().strip()
                    for i in range(len(line)):
                        fasta+=line[i].strip()
                    seq_fasta_dict[seqfile.strip().split("/")[-1].replace(".seq","")]=fasta
        #break
"""
#New code without the need of temporary file
with open (seq_list,"r") as f:
    for pdb in f:
        seqfile=pdb.strip()

        fasta=""
        with open (seq_folder+seqfile.strip(),"r") as seq:
            for _ in range (5):
                line=seq.readline().strip()
            for i in range(len(line)):
                fasta+=line[i].strip()
            seq_fasta_dict[seqfile.strip().split("/")[-1].replace(".seq","")]=fasta


#Below is to write it to a file
data_list=[]
for key,value in seq_fasta_dict.items():
    data_list.append(key+" : "+value.strip()+"\n")
data_list[len(data_list)-1]=data_list[len(data_list)-1].strip()

with open ("fasta_dictionary.txt","w") as f:
    f.writelines(data_list)

