#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 14 03:13:59 2020

@author: farhan
"""

#this script reads the two heteromeric alignments in .a3m format
#creates respectie dictionaries and indices
#searches the PPI dictionary for interacting pairs
#then creates the concatenated alignment file in .a3m format

import os, sys, shutil
import numpy as np

def getName(file):
    return os.path.basename(file.strip()).split(".")[0]

def createDictFromA3m(file,name):
    aln_dict={}
    with open (file) as f:
        for line in f:
            if line.startswith(">"):
                idx=line.strip().replace(">","")
                if name in idx: idx=name
                line=f.readline()
                aln_dict[idx]=line.strip()            
                
    return aln_dict

def saveFastaDictionary(filename,dict):
    with open (filename,"w") as f:
        for k,v in dict.items():
            f.write(k+":"+v+"\n")

def loadFastaDictionary(filename):
    d={}
    with open (filename) as f:
        for line in f:
            idx=line.strip().split(":")[0].strip()
            fasta=line.strip().split(":")[1].strip()
            d[idx]=fasta
    return d


aln_A=os.path.abspath(sys.argv[1])
aln_B=os.path.abspath(sys.argv[2])
ppi_file=os.path.abspath(sys.argv[3])
outdir=os.path.abspath(sys.argv[4])+"/"

if not os.path.isdir(outdir): os.makedirs(outdir)
#loading the ppi_dict can fail. This file is very big
ppi_dict = np.load(ppi_file, allow_pickle='TRUE').item()
print ("PPI_DICT_LEN=",len(ppi_dict))
print (type(ppi_dict))
with open ("ppi_dict_temp.txt","w") as f:
    f.write(str(ppi_dict))
    
keys=str(ppi_dict.keys())

with open ("ppi_dict_keys.txt","w") as f:
    f.write(keys)

del keys

#extract the names
name_A=getName(aln_A)
name_B=getName(aln_B)
#create the fasta dictionaries from the .a3m files
dict_A=createDictFromA3m(aln_A,name_A)
dict_B=createDictFromA3m(aln_B,name_B)
#temporary working directory
tmpdir=outdir+"tmpdir"+name_A+"_"+name_B+"/"
#save the dictionaries as .txt files
if not os.path.isdir(tmpdir): os.makedirs(tmpdir)
dictfile_A=tmpdir+name_A+"_dict.txt"
dictfile_B=tmpdir+name_B+"_dict.txt"
saveFastaDictionary(dictfile_A,dict_A)
saveFastaDictionary(dictfile_B,dict_B)

keys_A=list(dict_A.keys())
keys_B=list(dict_B.keys())
keys_A.remove(name_A)
keys_B.remove(name_B)
pairs_AB=[]
pairs_AB.append([name_A,name_B])

#here comes the big search. This is the longest step. Needs to be optimized.
for idx_A in keys_A:
    #get the interacting proteins for this idx
    if ppi_dict.get(idx_A)!=None:
        interactions_with_idx_A=ppi_dict[idx_A]
    else:
        continue
    for inner_idx_key_A in interactions_with_idx_A:
        if inner_idx_key_A in keys_B:
            pairs_AB.append([idx_A,inner_idx_key_A])
            

with open (tmpdir+"pairs_AB.txt","w") as f:
    for pair in pairs_AB:
        f.write(pair[0]+","+pair[1]+"\n")
        with open (tmpdir+"pairs_AB.a3m","w") as fa3m:
            fa3m.write(">"+pair[0]+"_"+pair[1]+"\n")
            fa3m.write(dict_A[pair[0]].strip()+dict_B[pair[1]].strip()+"\n")

shutil.copy2(tmpdir+"pairs_AB.a3m",outdir+name_A+"_"+name_B+".a3m")

#print ()
    











