#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  4 11:12:25 2020

@author: farhan
"""

#this script reads the agv_precision file and creates a distribution
#usage: createDistribution.py <file> <destination_folder>

import os
import sys

def writeDistributionFile(top_folder,top_dict):
    if not (os.path.isdir(top_folder)): os.mkdir(top_folder)
    with open (top_folder+"distribution.txt","w") as f:
        for key,value in top_dict.items():
            f.write(key+":"+value+"\n")
        
    
    

file=sys.argv[1].strip()
outfolder=sys.argv[2].strip()
if not (outfolder.endswith("/")): outfolder+="/"
top_5={}
top_10={}
top_Lb10={}
top_Lb5={}
top_Lb2={}
top_L={}
top_2L={}

with  open (file,"r") as f:
    for line in f:
        if (line.strip().startswith("Name")): continue
        if (line.strip().startswith("-")): continue
        if (line.strip().startswith("AVG")): continue
        split=line.strip().split()
        top_5[split[0]]=split[2]
        top_10[split[0]]=split[3]
        top_Lb10[split[0]]=split[4]
        top_Lb5[split[0]]=split[5]
        top_Lb2[split[0]]=split[6]
        top_L[split[0]]=split[7]
        top_2L[split[0]]=split[8]
Relax_Remove="Relax_Remove/"
if (Relax_Remove in outfolder): Relax_Remove=""
relaxrem=file.strip().split("_")[8]
relax=file.strip().split("_")[-1].replace(".txt","")
relax_removefolder=outfolder+Relax_Remove+relaxrem+"/"
relax_prec="Relax_Prec_"+relax+"/"

folder={}
folder["T5"]=relax_removefolder+relax_prec+"T5/"
folder["T10"]=relax_removefolder+relax_prec+"T10/"
folder["TLb10"]=relax_removefolder+relax_prec+"TLb10/"
folder["TLb5"]=relax_removefolder+relax_prec+"TLb5/"
folder["TLb2"]=relax_removefolder+relax_prec+"TLb2/"
folder["TL"]=relax_removefolder+relax_prec+"TL/"
folder["T2L"]=relax_removefolder+relax_prec+"T2L/"

#print(relaxrem)
#print(relax)
#print(file.split("_"))
#for key in folder.keys():
#    print (os.path.isdir(folder[key]))
#print (relax_removefolder)
writeDistributionFile(folder["T5"],top_5)    
writeDistributionFile(folder["T10"],top_10)    
writeDistributionFile(folder["TLb10"],top_Lb10)    
writeDistributionFile(folder["TLb5"],top_Lb5)    
writeDistributionFile(folder["TLb2"],top_Lb2)    
writeDistributionFile(folder["TL"],top_L)    
writeDistributionFile(folder["T2L"],top_2L)    

