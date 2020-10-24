#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 16:33:35 2020

@author: farhan
"""


#this script reads the WXYZ_inter_prec.txt precision files and creates a database of PDB_Name and respective number of interchain contacts
#Format: PDB/Name  Length  Relax_removal   Relaxation   Top-5   Top-10  Top-L/10  Top-L/5  Top-L/2  Top-L  Top-2L
#usage: python createContactTable.py

#import numpy as np
import pandas as pd

def loadLengthDictionary(file):
    l_dict={}
    with open (file,"r") as f:
        for line in f:
            if line.startswith("Name"): continue
            l_dict[line.strip().split()[0]]=line.strip().split()[1]
        
    return l_dict

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

#mini_list= all_8886_protein_list[0:2]
mini_list=all_8886_protein_list
#mini_list=["1A0F"]
for pdb in mini_list:
#for pdb in all_8886_protein_list:
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
                    kk=0 
                    for i in range(8):
                        line=f.readline().strip()
                        #print ("ASDFASDFADSFASDFASDFADSF:::::"+line)
                        if ("Relaxation =" in line): 
                            relax=line.split("=")[1].strip()
                            row_list.append(relax)
                            density_row_list.append(relax)
                        #the following is meant to ensure contact numbers for diagonals don't exceed threshold
                        if ("con_num=" in line):
                            con_num=line.split("=")[1].strip()
                            #print (kk)
                            if (kk==0):
                                if (int(con_num)>5):con_num="5"
                            if (kk==1):
                                if (int(con_num)>10):con_num="10"
                            if (kk==2):
                                if (int(con_num)>int(length_dict[pdb])/10):con_num=int((int(length_dict[pdb])/10)+0.5)
                            if (kk==3):
                                if (int(con_num)>int(length_dict[pdb])/5):con_num=int((int(length_dict[pdb])/5)+0.5)
                            if (kk==4):
                                if (int(con_num)>int(length_dict[pdb])/2):con_num=int((int(length_dict[pdb])/2)+0.5)
                            if (kk==5):
                                if (int(con_num)>int(length_dict[pdb])):con_num=int(int(length_dict[pdb]))
                            if (kk==6):
                                if (int(con_num)>int(length_dict[pdb])*2):con_num=int(int(length_dict[pdb])*2)
                            row_list.append(str(con_num))
                            density_row_list.append(str(round((int(con_num)/int(length_dict[pdb])),5)))
                            kk+=1
                    #if (pdb=="1D2C"): break
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
#print (df_density.to_string(index=False))
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
