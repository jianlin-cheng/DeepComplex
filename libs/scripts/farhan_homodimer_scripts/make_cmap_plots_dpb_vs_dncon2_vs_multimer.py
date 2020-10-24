#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 19 15:03:35 2019

@author: farhan
"""
#this script plots the triple contact map
import os,sys
#monomer="/data/farhan/SoftwareTools/HomopolymerProject/scripts/inter_chain_results/Actin/coneva/actin_monomer.rr"
#directory="/data/farhan/SoftwareTools/HomopolymerProject/scripts/inter_chain_results/Actin/coneva/"
#outdirectory="/data/farhan/SoftwareTools/HomopolymerProject/scripts/inter_chain_results/Actin/coneva/"

#directory="/data/farhan/SoftwareTools/HomopolymerProject/scripts/inter_chain_results/ASC/coneva/"
#outdirectory="/data/farhan/SoftwareTools/HomopolymerProject/scripts/inter_chain_results/ASC/coneva/"

directory="/data/farhan/SoftwareTools/HomopolymerProject/scripts/4zuk_out/coneva/"
outdirectory="/data/farhan/SoftwareTools/HomopolymerProject/scripts/4zuk_out/coneva/graphs/"

script_dir="/data/farhan/SoftwareTools/HomopolymerProject/scripts/perl_scripts/"
#multimer=sys.argv[1]
file_list=[]
with open(directory+"rr_list.lst","r") as f:
    for line in f:
        file_list.append(line.strip())
        
monomer=file_list[0]
pdb=file_list[1]

for i in range(2,len(file_list)):
    #os.system("Rscript "+script_dir+"compare_rr_three.R "+directory+file_list[i]+" "+directory+monomer+" "+directory+pdb+" "+directory+file_list[i].replace(".rr",".png"))
    os.system("Rscript "+script_dir+"compare_rr_three_red_on_top.R "+directory+file_list[i]+" "+directory+monomer+" "+directory+pdb+" "+directory+file_list[i].replace(".rr","_red_on_top.png"))
    #print(directory+file_list[i].replace(".rr",".png"))
