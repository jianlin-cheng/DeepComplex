#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 06:13:13 2020

@author: farhan
"""

#this script combines the .ss2 feature from psipred prediction. Takes input a combined fasta_sequence, ss2_file1, and ss2_file2
#usage: python combineSS2.py <fasta> <ss2_file1> <ss2_file2> <output>

import sys,os

#fastafile=os.path.abspath(sys.argv[1])
ss_file1=os.path.abspath(sys.argv[1])
ss_file2=os.path.abspath(sys.argv[2])

if (len(sys.argv)==4):
    outfile=os.path.abspath(sys.argv[3])
else:
    outfile=os.path.dirname(ss_file1)+"/"+os.path.basename(ss_file1)[0:4]+"_"+ss_file1.split("/")[-1][4]+ss_file2.split("/")[-1][4]+".ss2"
label=""
ss1=[]
with open (ss_file1,"r") as f:
    for line in f:
        if (line.startswith("#") or line.strip()==""):
            if (line.startswith("#")):label=line.strip()
            continue
        ss1.append(line.rstrip())

last_num=int(ss1[-1].strip().split()[0])

ss2=[]
with open (ss_file2,"r") as f:
    for line in f:
        if (line.startswith("#") or line.strip()==""):continue
        line=line.strip()
        split=line.split()
        #print (split)
        last_num+=1
        last_num_string=str(last_num)
        last_num_string=" "*(4-len(last_num_string))+last_num_string
        ss2.append(last_num_string+" "+split[1]+" "+split[2]+"   "+split[3]+"  "+split[4]+"  "+split[5])


#print (last_num)
#print (ss1[-1])
#print (ss2[-1])
combined=ss1+ss2
#print (len(combined))
#print (label)
combined.insert(0,label+"\n")
#print(combined[-1])
with open (outfile,"w") as f:
    for line in combined:
        f.write(line+"\n")
