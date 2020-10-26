#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 22:30:54 2020

@author: farhan
"""

#this script will read the contact map .rr file and convert it to a symmetric matrix
#usage: python makeSymmetry.py <input_file> <output_file>

import os,sys
from readRR import readRRFile, write2File
import numpy as np

infile=sys.argv[1]
outfile=sys.argv[2]
dirnm=sys.argv[3]

if not (os.path.exists(infile)): sys.exit("Input file "+infile+" was not found!")
fasta,rr_contents=readRRFile(infile)
L=len(fasta)+1
mat=np.zeros((L,L))

for line in rr_contents:
    i=int(line.split()[0])
    j=int(line.split()[1])
    val=float(line.split()[-1])
    mat[i][j]=val
    mat[j][i]=val
new_rr=[]
for i in range(L):
    for j in range(i,L):
        if (mat[i][j] !=0):
            new_rr.append(str(i)+" "+str(j)+" 0 8 "+str(mat[i][j]))
            new_rr.append(str(j)+" "+str(i)+" 0 8 "+str(mat[j][i]))
            pass
write2File(outfile,fasta,new_rr)
os.system("python "+dirnm+"casp14structure_prediction_tool/scripts/sortrr.py "+outfile+" True > "+outfile+".txt")
os.system("mv "+outfile+".txt "+outfile)
#print (rr_contents, L)
