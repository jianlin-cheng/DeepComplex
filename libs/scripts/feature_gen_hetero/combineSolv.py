#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 06:13:13 2020

@author: farhan
"""

#this script combines the .solv feature from psipred prediction. Takes input a combined fasta_sequence, solv1, and solv2
#usage: python combineSolv.py <fasta> <solv1> <solv2> <output>

import sys,os

#fastafile=os.path.abspath(sys.argv[1])
solv_file1=os.path.abspath(sys.argv[1])
solv_file2=os.path.abspath(sys.argv[2])

if (len(sys.argv)==4):
    outfile=os.path.abspath(sys.argv[3])
else:
    outfile=os.path.dirname(solv_file1)+"/"+os.path.basename(solv_file1)[0:4]+"_"+solv_file1.split("/")[-1][4]+solv_file2.split("/")[-1][4]+".solv"
    
    #print (outfile)
    #sys.exit()

solv1=[]
with open (solv_file1,"r") as f:
    for line in f:
        solv1.append(line.rstrip())

last_num=int(solv1[-1].strip().split()[0])

solv2=[]
with open (solv_file2,"r") as f:
    for line in f:
        line=line.strip()
        split=line.split()
        last_num+=1
        last_num_string=str(last_num)
        last_num_string=" "*(4-len(last_num_string))+last_num_string
        solv2.append(last_num_string+" "+split[1]+"  "+split[2])


#print (last_num)
#print (solv1[-1])
#print (solv2[-1])
combined=solv1+solv2
#print (len(combined))
#print(combined[-1])
with open (outfile,"w") as f:
    for line in combined:
        f.write(line+"\n")