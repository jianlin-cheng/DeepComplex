#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan  5 21:57:31 2020

@author: farhan
"""

#this script reads the .seq files and creates a fasta dictionary
#usage: python createFastaDictionaryFromCombinedFasta.py <combined_fasta> <output_file>

import os,sys
from readHeterdimerFasta import readFastaFile

fasta_file=os.path.abspath(sys.argv[1])
outfile=os.path.abspath(sys.argv[2])

seq_fasta_dict={}

seq_fasta_dict=readFastaFile(fasta_file)        

#Below is to write it to a file
data_list=[]
for key,value in seq_fasta_dict.items():
    data_list.append(key+" : "+value.strip()+"\n")
#data_list[-1]=data_list[-1].strip()

with open (outfile,"w") as f:
    f.writelines(data_list)

