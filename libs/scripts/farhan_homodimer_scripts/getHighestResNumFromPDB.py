#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 19:45:25 2020

@author: farhan
"""

#this script selects the pdb from the list that has the highest residue number.
#usage: python getHighestResNumFromPDB.py <pdb_name> <pdb_folder>

import os,sys
from readPDBColumns import readPDB,readAtom,write2File,contents2Info,addColumn,reassembleLines,getChain


def getMaxResNum(pdb_file):
    split_contents=contents2Info(readPDB(pdb_file))
    res_num_first=split_contents[0]["res_num"]
    res_num_last=split_contents[len(split_contents)-1]["res_num"]
    print (res_num_first,res_num_last)
    return (res_num_first,res_num_last)

pdb_name=sys.argv[1]
folder=sys.argv[2]
if not (folder.endswith("/")):folder+="/"
os.system("ls "+folder+pdb_name+"* > temp_pdb_folder_list.txt")
pdb_list=[]
with open ("temp_pdb_folder_list.txt","r") as f:
    for line in f:
        pdb_list.append(line.strip())

print (pdb_list)
for pdb_file in pdb_list:
    getMaxResNum(pdb_file)
    #sys.exit()
