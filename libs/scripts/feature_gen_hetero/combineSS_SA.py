#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 06:13:13 2020

@author: farhan
"""

#this script combines the .ss_sa feature. Takes input fasta_chain_1, fasta_chain_2, ss_sa_file1, and ss_sa_file2
#usage: python combineSS_SA.py <fasta1> <fasta2> <ss_sa_file1> <ss_sa_file2> <output>

import sys,os

def readFasta(file):
    l=""
    seq=""
    with open (file,"r") as f:
        l=f.readline().strip()
        #name=l.split()[0].replace(">","").strip()
        seq=f.readline().strip()
        ss=f.readline().strip()
        sa=f.readline().strip()
    
    #print (name)
    
    L=len(seq)
    return L,seq,ss,sa

#fastafile1=os.path.abspath(sys.argv[1])
#fastafile2=os.path.abspath(sys.argv[2])
ss_file1=os.path.abspath(sys.argv[1])
ss_file2=os.path.abspath(sys.argv[2])

name_1=os.path.basename(ss_file1).replace(".ss_sa","").replace(".fasta","")
name_2=os.path.basename(ss_file2).replace(".ss_sa","").replace(".fasta","")
chain_1=name_1.split("_")[-1][-1]
chain_2=name_2.split("_")[-1][-1]

L_1,seq_1,ss_1,sa_1=readFasta(ss_file1)
L_2,seq_2,ss_2,sa_2=readFasta(ss_file2)
new_name=name_1.split("_")[0]+"_"+chain_1+chain_2
print (name_1,chain_1,L_1,seq_1,ss_1,sa_1)
#sys.exit()


if (len(sys.argv)==4):
    outfile=os.path.abspath(sys.argv[3])
else:
    outfile=os.path.dirname(ss_file1)+"/"+os.path.basename(ss_file1)[0:4]+"_"+chain_1+chain_2+".ss_sa"
if not os.path.isdir(os.path.dirname(outfile)): os.makedirs(os.path.dirname(outfile))




ss1=[]  
ss1.append(">"+new_name)
ss1.append(seq_1+seq_2)
ss1.append(ss_1+ss_2)
ss1.append(sa_1+sa_2)

with open (outfile,"w") as f:
    for line in ss1:
        f.write(line+"\n")
        print (line)

with open (outfile.replace(".ss_sa",".ss"),"w") as f:
    f.write(ss1[0]+"\n")
    f.write(ss1[2]+"\n")
    print (line)

with open (outfile.replace(".ss_sa",".acc"),"w") as f:
    f.write(ss1[0]+"\n")
    f.write(ss1[3]+"\n")
    print (line)
