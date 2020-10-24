#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan  5 21:57:31 2020

@author: farhan
"""

#this script reads the .seq files and creates a fasta list
#usage: python createFastaDB.py <list_file.txt> <seq_folder>

import os,sys

seq_folder="/data/farhan/SoftwareTools/HomopolymerProject/data/homodimers/homodimers_files/work_dir/seq/"
seq_list="seq_list.txt"

pdb_list=[]
seq_fasta_dict={}
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
#Below is to write it to a file
#data_list=[]
#for key,value in seq_fasta_dict.items():
#    data_list.append(key+" : "+value+"\n")
#data_list[len(data_list)-1]=data_list[len(data_list)-1].strip()

#with open ("fasta_dictionary.txt","w") as f:
#    f.writelines(data_list)

key_list=sorted(seq_fasta_dict.keys())

similar_list=[]
different_list=[]

for i in range(0,len(key_list),2):
    if (key_list[i][0:4]==key_list[i+1][0:4]):
        if (seq_fasta_dict[key_list[i]].strip()==seq_fasta_dict[key_list[i+1]]):
            similar_list.append(key_list[i]+"\t"+key_list[i+1]+"\n")
            #similar_list.append(key_list[i+1])
            
        else:
            different_list.append(key_list[i][0:4]+"\n")
with open ("same_fasta_list.txt","w") as f:
    f.writelines(similar_list)

with open ("different_fasta_list.txt","w") as f:
    f.writelines(different_list)
        
    

    
        