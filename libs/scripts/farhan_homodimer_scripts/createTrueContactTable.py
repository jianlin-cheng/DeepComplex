#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 16:33:35 2020

@author: farhan
"""


#this script reads the WXYZ_inter_prec.txt precision files and creates a database of PDB_Name and respective number of interchain contacts
#Format: PDB/Name  Length  Relax_removal   Relaxation   Top-5   Top-10  Top-L/10  Top-L/5  Top-L/2  Top-L  Top-2L
#usage: python createFastaLength.py

#import numpy as np
import pandas as pd
import os
import subprocess

def loadLengthDictionary(file):
    l_dict={}
    with open (file,"r") as f:
        for line in f:
            if line.startswith("Name"): continue
            l_dict[line.strip().split()[0]]=line.strip().split()[1]
        
    return l_dict

def getTrueInterContactFile(pdb_name):
    os.system("ls ./interchains/"+pdb_name+"*.rr > xyz.temp.txt")
    file_names=""
    with open ("xyz.temp.txt","r") as f:
        for line in f:
            if ("filtered" in line.strip()): continue
            if ("inter" in line.strip()): continue
            if ("all" in line.strip()): continue
            file_names=line.strip()
    return file_names

def getNumberofTrueContactsFromFile(file_name):
    os.system("wc -l "+file_name+" > line_num.txt")
    num=0
    with open ("line_num.txt","r") as f:
        for line in f:
            num=int(line.strip().split()[0])
            break
    return num
    

all_8886_protein_list=[]
top_list=[]
all_protein_prec_list=[]
all_protein_prec_list.append("Name   Relax_removal   Relaxation   Top-5   Top-10  Top-L/10  Top-L/5  Top-L/2  Top-L  Top-2L")
length_dict=loadLengthDictionary("all_8886_protein_max_length.txt")
df_list=[]
df_density_list=[]
key_list=list(("Name","Length","Relax_removal","Relaxation","Top-5","Top-10","Top-L/10","Top-L/5","Top-L/2","Top-L","Top-2L"))
#df = pd.DataFrame([top_list],columns=key_list,index=None)


with open ("all_8886_protein_list.txt","r") as f:
    for line in f:
        #print (line)
        all_8886_protein_list.append(line.strip())

mini_list= all_8886_protein_list[0:2]
#mini_list=all_8886_protein_list
mini_list=["1A0F"]
for pdb in mini_list:
#for pdb in all_8886_protein_list:
    inter_rr_file=getTrueInterContactFile(pdb)
    true_contacts=getNumberofTrueContactsFromFile(inter_rr_file)
    
    with open ("./precisions/inter/"+pdb+"_inter_prec.txt","r") as f:
    #with open ("./precisions/inter/1A0F_inter_prec.txt","r") as f:
        for line in f:
            
            #print (line)
            if ("Relaxation Removal =" in line):
                top_list.append(line.strip())
                rel_rem=line.split("=")[1].strip()
                for j in range(3):
                    row_list=[]
                    density_row_list=[]
                    row_list.append(pdb)
                    density_row_list.append(pdb)
                    row_list.append(length_dict[pdb])
                    density_row_list.append(length_dict[pdb])
                    row_list.append(rel_rem)
                    density_row_list.append(rel_rem)
                    for i in range(8):
                        line=f.readline().strip()
                        #print ("ASDFASDFADSFASDFASDFADSF:::::"+line)
                        if ("Relaxation =" in line): 
                            relax=line.split("=")[1].strip()
                            row_list.append(relax)
                            density_row_list.append(relax)
                        if ("con_num=" in line):
                            con_num=line.split("=")[1].strip()
                            row_list.append(con_num)
                            density_row_list.append(str(round((int(con_num)/int(length_dict[pdb])),5)))

                    #print(row_list)
                    df=pd.DataFrame([row_list],columns=key_list,index=None)
                    df_density=pd.DataFrame([density_row_list],columns=key_list,index=None)
                    df_list.append(df)
                    df_density_list.append(df_density)
                    #top_list.append(line)
                #break
    #break
                



#df_list.append(df)
df=pd.concat(df_list)
df_density=pd.concat(df_density_list)
#print (df.to_string(index=False))
print (df_density.to_string(index=False))
with open ("contact_table.txt","w") as f:
    f.writelines(df.to_string(index=False))
with open ("contact_density_table.txt","w") as f:
    f.writelines(df_density.to_string(index=False))
#print (type(df.to_string(index=False)))
#import os
#os.system("echo "+df.to_string(index=False)+" > contact_table.txt")
#df.to_csv("contact_table.txt",sep=" ",index=False,header=True)
#print (top_list)
"""
with open ("all_8886_protein_prec.txt","w") as f:
    f.writelines(all_protein_prec_list)
"""
