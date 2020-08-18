#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 16:33:35 2020

@author: farhan
"""


#this script reads the WXYZ_inter_prec.txt precision files and creates a database of PDB_Name and respective number of interchain contacts
#Format: PDB/Name   Relax_removal   Relaxation   Top-5   Top-10  Top-L/10  Top-L/5  Top-L/2  Top-L  Top-2L
#usage: python readnPrintInterPrecisionOnly.py

#import numpy as np
import pandas as pd

all_8886_protein_list=[]
top_list=[]
all_protein_prec_list=[]
all_protein_prec_list.append("Name   Relax_removal   Relaxation   Top-5   Top-10  Top-L/10  Top-L/5  Top-L/2  Top-L  Top-2L")
connum_dict={}
df_list=[]
key_list=list(("Name","Relax_removal","Relaxation","Top-5","Top-10","Top-L/10","Top-L/5","Top-L/2","Top-L","Top-2L"))
#df = pd.DataFrame([top_list],columns=key_list,index=None)
with open ("all_8886_protein_list.txt","r") as f:
    for line in f:
        #print (line)
        all_8886_protein_list.append(line.strip())
mini_list=all_8886_protein_list[0:4]
#print (mini_list)
for pdb in mini_list:
    with open ("./precisions/inter/"+pdb+"_inter_prec.txt","r") as f:
    #with open ("./precisions/inter/1A0F_inter_prec.txt","r") as f:
        #print (len(df_list))
        
        for line in f:
            if ("Name" in line):
                top_list.append(line.strip())
                for i in range(3):
                    for j in range(3):
                        line=f.readline().strip()
                        row_list=line.split()
                        row_list.insert(1,str(i))
                        df=pd.DataFrame([row_list],columns=key_list,index=None)
                        df_list.append(df)
                        #top_list.append(line)
                
                #break
    #break
                



#df_list.append(df)
df=pd.concat(df_list)
print (df.to_string(index=False))
print (len(df_list))
"""
with open ("all_8886_protein_prec.txt","w") as f:
    f.writelines(all_protein_prec_list)
"""
