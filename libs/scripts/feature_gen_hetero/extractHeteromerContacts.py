#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  6 12:48:02 2020

@author: farhan
"""

#this script reads the dncon2 contact map and filters out heteromeric contacts
#usage: python extractHeteromerContacts.py <cmap_file in rr format> <original_dimeric_fasta> <chain_1> <chain_2> <outputfile>

import os, sys
from readRR import *
import numpy as np
from readHeterdimerFasta import *

#cmap_file=os.path.abspath(sys.argv[1])
#fasta_file=os.path.abspath(sys.argv[2])
#chain_1=sys.argv[3]
#chain_2=sys.argv[4]
#out_file=os.path.abspath(sys.argv[5])
chain_1="B"
chain_2="C"
fasta_file="/data/farhan/CASP14_multimers/targets/fastas/H1036/H1036.fasta"
cmap_file="/data/farhan/CASP14_multimers/results/H1036/H1036_BC.dncon2.rr"
name=os.path.basename(fasta_file).split(".")[0]
fasta_dict=readFastaFile(fasta_file)
#print (fasta_dict[name+chain_2])
len_A=len(fasta_dict[name+chain_1])
len_B=len(fasta_dict[name+chain_2])

cmap=np.zeros((len_A+len_B,len_A+len_B))
print (len_A, len_B)

fasta,rr,header=readRRFile(cmap_file)
for line in rr:
    i=int(line.strip().split()[0])-1
    j=int(line.strip().split()[1])-1
    value=float(line.strip().split()[-1])
    cmap[i][j]=value
    cmap[j][i]=value

slic=cmap[0:len_A,len_A:]
print (len_A,len_B)
print (slic.shape)

header.append(fasta)
for i in range(len_A):
    for j in range(len_B):
        header.append(str(i+1)+" "+str(j+1)+" 0 8 "+str(slic[i][j]))
out_file="/data/farhan/CASP14_multimers/results/H1036/H1036_BC.rr"
writeCASPRRFile(out_file,header)
