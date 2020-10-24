#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  5 09:48:37 2019

@author: farhan
"""

#this script does the interchain contacts of the .atom files of a particular protein with the highest number of lines
#usage python doAll_interchain_protein.py <protein_name> <.atom folder> <dist> <out_dir>

import os,subprocess,sys

def getHighestLines(protein_name,atom_dir):
    os.system("ls "+protein_name+"_dist_*.txt > "+"interlist.lst")
    file_list=[]
    
    with open ("interlist.lst","r") as f:
        for line in f:
            file_list.append(line.strip())
    l=0
    best=""
    for file in file_list:
        
        if (not os.path.exists(file)): 
            print (file+ " not found")
            continue
        lnnum = subprocess.check_output("wc -l < "+file,shell = True)
        lnnum = lnnum.rstrip()
        lnnum = str(lnnum)
        lnnum = int(lnnum.strip("b").strip("'"))-1
        
        if (lnnum > l):
            best=file
            
            l=lnnum
        #print(best)
            
    #print(best)
    #delete the others
    file_list.remove(best)
    for file in file_list:
        os.remove(file)
    
    return best

protein_name=sys.argv[1]
atom_dir=sys.argv[2]
dist=sys.argv[3]
outdir=sys.argv[4]

if (not atom_dir.endswith("/")): atom_dir+="/"
os.system("ls "+atom_dir+protein_name+"*.atom > temp_atom_list_4_inter.lst")
atom_file_list=[]
with open ("temp_atom_list_4_inter.lst","r") as f:
    for line in f:
        atom_file_list.append(line.strip())
        #print(line.strip())
if len(atom_file_list)<2: sys.exit("No atom files found for "+protein_name+" in folder "+atom_dir+" . Skipping!")
print ("Running for protein "+protein_name)
chain_A_atom_file=atom_file_list[0]#atom_dir+protein_name+"A.atom"
atom_file_list.remove(chain_A_atom_file)
chain_A_atom_file=chain_A_atom_file.strip()
exit_flag=False
for atom_file in atom_file_list:
    exitcode=os.system("python pdb2distance_inter.py "+chain_A_atom_file+" "+atom_file+" "+dist+" "+protein_name)
    if (exitcode==-1): exit_flag=True
    #break
    #print(atom_file)
os.system("python getHighestContacts.py "+protein_name)
#Remove the temp_atom_list_4_inter.lst file
#os.system("rm -f temp_atom_list_4_inter.lst")

