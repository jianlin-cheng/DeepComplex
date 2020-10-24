#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  7 13:07:33 2020

@author: farhan
"""

#this script is used to generate triple contact graphs for a list of proteins
#usage: generateContactGraphs.py <protein_list.txt or folder> <outfolder>

import os,sys

def getFileFromFolder(details):
    os.system("ls "+details+" > fileforgraphs.txt")
    file_list=[]
    with open ("fileforgraphs.txt","r") as f:
        for line in f:
            file_list.append(line.strip())
    if (len(file_list)>1): 
        print("chosing first file "+file_list[0])
        #sys.exit("Too many files for "+details)
    #print(file_list)
    return file_list[0]

list_file=sys.argv[1]
dncon2_folder="/data/farhan/SoftwareTools/HomopolymerProject/data/homodimers/scripts/dncon2_rr/"
intrafolder="/data/farhan/SoftwareTools/HomopolymerProject/data/homodimers/scripts/intrachains_/"
interfolder="/data/farhan/SoftwareTools/HomopolymerProject/data/homodimers/scripts/interchains_heavy/"
outfolder="/data/farhan/SoftwareTools/HomopolymerProject/data/homodimers/scripts/graphs/"

if (os.path.isdir(list_file)):
    if not (list_file.endswith("/")): list_file+="/"
    
    os.system("ls "+list_file+"*filtered* > inter_chain_precision_file_list_fake.txt")
    list_file="inter_chain_precision_file_list_fake.txt"

file_list=[]
with open (list_file,"r") as f:
    for line in f:
        file_list.append(line.strip())

for pdb in file_list:
    pdb=pdb.split("/")[-1][0:4]
    dncon2_file=dncon2_folder+pdb+".dncon2_sorted_filtered.rr"
    interfile=getFileFromFolder(interfolder+pdb+"*filtered.rr")
    intrafile=getFileFromFolder(intrafolder+pdb+"*filtered.rr")
    outfile=outfolder+pdb+"_2L.filtered.not_relaxed.png"
    #For not relaxed
    print("Running command 1: Rscript ./perl_scripts/compare_rr_three.R "+interfile+" "+dncon2_file+" "+intrafile+" "+outfile)
    os.system("Rscript ./perl_scripts/compare_rr_three.R "+interfile+" "+dncon2_file+" "+intrafile+" "+outfile)
    #For relaxed
    dncon2_file=dncon2_folder+pdb+".dncon2_sorted_inter_pred_2L.rr"
    for relax in range(3):
        #outfile=outfolder+pdb+"_2L.filtered.not_relaxed.png"
        dncon2_file=dncon2_folder+pdb+".dncon2_sorted_nointra_relax_"+str(relax)+".rr"
        outfile=outfolder+pdb+".dncon2_sorted_nointra_relax_"+str(relax)+".png"
        print("Running command 2: Rscript ./perl_scripts/compare_rr_three.R "+interfile+" "+dncon2_file+" "+intrafile+" "+outfile)
        os.system("Rscript ./perl_scripts/compare_rr_three.R "+interfile+" "+dncon2_file+" "+intrafile+" "+outfile)
    dncon2_file=dncon2_folder+pdb+".dncon2_sorted_inter_pred_2L.rr"
    outfile=outfolder+pdb+"_2L.filtered.relaxed.all.png"
    print("Running command 3: Rscript ./perl_scripts/compare_rr_three.R "+interfile+" "+dncon2_file+" "+intrafile+" "+outfile)
    os.system("Rscript ./perl_scripts/compare_rr_three.R "+interfile+" "+dncon2_file+" "+intrafile+" "+outfile)
