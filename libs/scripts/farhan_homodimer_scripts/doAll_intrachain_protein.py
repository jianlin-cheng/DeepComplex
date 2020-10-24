#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  5 09:48:37 2019

@author: farhan
"""

#this script does the intrachain contacts of the .atom files of a particular protein with the highest number of lines
#usage python doAll_interchain_protein.py <protein_name> <.atom folder> <out_dir>

import os,subprocess,sys

def getHighestLines(protein_name,atom_dir): #Modify: Select the file with the highest residue number
    """
    os.system("ls "+atom_dir+protein_name+"*.atom > "+"intra_atom_list.lst")
    file_list=[]
    
    with open ("intra_atom_list.lst","r") as f:
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
    #file_list.remove(best)
    #for file in file_list:
    #    os.remove(file)
    """
    os.system("ls "+atom_dir+protein_name+"*.atom > "+"intra_atom_list.lst")
    file_list=[]
    
    with open ("intra_atom_list.lst","r") as f:
        for line in f:
            file_list.append(line.strip())
    l=0
    best=""
    for file in file_list:
        
        if (not os.path.exists(file)): 
            print (file+ " not found")
            continue
        res_list=[]
        with open (file,"r") as f:
            for line in f:
                #print (line[22:26])
                if (line.startswith("ATOM")): res_list.append(int(line[22:26]))
        res_num=max(res_list)
        if (res_num > l):
            best=file
            l=res_num

    return best
protein_name=sys.argv[1]
atom_dir=sys.argv[2]
dist=sys.argv[3]
outdir=sys.argv[4]

if (not atom_dir.endswith("/")): atom_dir+="/"

file_name=getHighestLines(protein_name,atom_dir)
print (file_name)

os.system("python pdb2distancemonomer.py "+file_name+" "+protein_name)


