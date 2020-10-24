#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  7 11:40:21 2020

@author: farhan
"""
#this script calculates the interchain precision given the following folders and files
#usage: python doAll_precision_inter_v2.py
import os,sys

intrafolder="/data/farhan/SoftwareTools/HomopolymerProject/data/homodimers/scripts/intrachains_12_31_2019/"
interfolder="/data/farhan/SoftwareTools/HomopolymerProject/data/homodimers/scripts/interchains_heavy/"
dncon2_folder="/data/farhan/SoftwareTools/HomopolymerProject/data/homodimers/scripts/dncon2_combined/"
outfolder="/data/farhan/SoftwareTools/HomopolymerProject/data/homodimers/scripts/precisions/inter/"
list_file="/data/farhan/SoftwareTools/HomopolymerProject/data/homodimers/scripts/all_8886_protein_list.txt"

file_list=[]
dncon2_dict={}
with open (list_file,"r") as f:
    for line in f:
        if (os.path.exists(dncon2_folder+line.strip()+".dncon2.rr")): 
            file_list.append(line.strip())
            dncon2_dict[line.strip().split("/")[-1][0:4]]=line.strip()+".dncon2.rr"

os.system("python makePDBListAllFiles.py "+intrafolder+" > temp_intra_folder_list.txt")

intra_folder_list=[]
with open ("temp_intra_folder_list.txt","r") as f:
    for line in f:
        if ("filtered" in line or ".txt" in line or "dist" in line): continue
        intra_folder_list.append(line.strip()+"\n")

os.system("python makePDBListAllFiles.py "+interfolder+" > temp_inter_folder_list.txt")

inter_folder_list=[]
with open ("temp_inter_folder_list.txt","r") as f:
    for line in f:
        if ("filtered" in line or ".txt" in line or "dist" in line): continue
        inter_folder_list.append(line.strip()+"\n")

with open ("temp_intra_folder_list.txt","w") as f:
    f.writelines(intra_folder_list)
    
with open ("temp_inter_folder_list.txt","w") as f:
    f.writelines(inter_folder_list)

pdb_list=[]
for fil in file_list:
    pdb_list.append(fil.split("/")[-1][0:4])
    #print (fil)

exists_intra_dict={}
exists_inter_dict={}
#print (pdb_list)
#the following checks if the relevant .dncon2.rr, intrachain.rr and interchain.rr files the same pdb exists. if all 3 does, then execute
for pdb in pdb_list:
    exist_flag=False
    for intra_file in intra_folder_list:
        if (pdb in intra_file):
            exist_flag=True
            
            break
    if (exist_flag):
        exist_flag=False
        for inter_file in inter_folder_list:
            if (pdb in inter_file):
                exist_flag=True
                break
        if (exist_flag):
            exists_intra_dict[pdb]=intra_file
            exists_inter_dict[pdb]=inter_file
            
pdb_list=exists_intra_dict.keys()
#print(pdb_list)
#print(exists_intra_dict["4RUE"])
#print(exists_inter_dict["4RUE"])


for pdb in pdb_list:
    print ("Processing interchain precision for: "+pdb)
    print("Running commapnd...")
#    print("python getPrecision_inter.py "+interfolder+exists_inter_dict[pdb]+" "+dncon2_folder+dncon2_dict[pdb]+" "+intrafolder+exists_intra_dict[pdb] +" > "+outfolder+pdb+"_inter_prec.txt")
    print("python getPrecision_inter_v3.py "+interfolder+exists_inter_dict[pdb]+" "+dncon2_folder+dncon2_dict[pdb]+" "+intrafolder+exists_intra_dict[pdb] +" > "+outfolder+pdb+"_inter_prec.txt")
#    os.system("python getPrecision_inter.py "+interfolder+exists_inter_dict[pdb].strip()+" "+dncon2_folder+dncon2_dict[pdb].strip()+" "+intrafolder+exists_intra_dict[pdb].strip() +" > "+outfolder+pdb.strip()+"_inter_prec.txt")
    os.system("python getPrecision_inter_v3.py "+interfolder+exists_inter_dict[pdb].strip()+" "+dncon2_folder+dncon2_dict[pdb].strip()+" "+intrafolder+exists_intra_dict[pdb].strip() +" > "+outfolder+pdb.strip()+"_inter_prec.txt")
   
    
        
