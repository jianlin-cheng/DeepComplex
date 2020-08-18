#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 30 14:04:18 2019

@author: farhan
"""

#this script will reindex the residue numbers in the pdb/atom file according to a mapping function
#usage: python reindex.py <pdb_file> <mapping_function.txt> <outputfile>

import sys

def mapList2Dict(map_list):
    map_dict={}
    for val in map_list:
        split=val.split(":")
        map_dict[split[0].strip()]=split[1].strip()
    return map_dict

#pdb_file="./reindex_test/3L44A.atom"
#mapfile="map_A.txt"
#outputfile="./reindex_test/3L44A_reindexed.atom"

letters = {'ALA':'A','ARG':'R','ASN':'N','ASP':'D','CYS':'C','GLU':'E','GLN':'Q','GLY':'G','HIS':'H',
           'ILE':'I','LEU':'L','LYS':'K','MET':'M','PHE':'F','PRO':'P','SER':'S','THR':'T','TRP':'W',
           'TYR':'Y','VAL':'V','ASX':'B','GLX':'Z','MSE':'M'}

reversed_letters={'A':'ALA','R':'ARG','N':'ASN','D':'ASP','C':'CYS','E':'GLU','Q':'GLN','G':'GLY','H':'HIS',
           'I':'ILE','L':'LEU','K':'LYS','M':'MET','F':'PHE','P':'PRO','S':'SER','T':'THR','W':'TRP',
           'Y':'TYR','V':'VAL','B':'ASX','Z':'GLX'}

pdb_file=sys.argv[1]
mapfile=sys.argv[2]
outputfile=sys.argv[3]

map_list=[]
atom_file_list=[]
with open (mapfile,"r") as f:
    for line in f:
        map_list.append(line.strip())

with open (pdb_file,"r") as f:
    for line in f:
        atom_file_list.append(line)

map_dict=mapList2Dict(map_list)
new_atom_list=[]
for atom_lines in atom_file_list:
    #print (len(atom_lines[17:21]))#res_name
    #print (len(atom_lines[22:26]))#res_name
    #print (atom_lines[22:26])#res_num
    if atom_lines.startswith("ATOM"):
        res_num=atom_lines[22:26]
        #print (atom_lines)
        new_res_num=" "*(4-len(map_dict[res_num.strip()]))+map_dict[res_num.strip()]
        new_atom_line=atom_lines[0:22]+new_res_num+atom_lines[26:]
        new_atom_list.append(new_atom_line)
        #print(new_atom_line)
    else:
        new_atom_list.append(atom_lines)
    
    #break



with open (outputfile,"w") as f:
    f.writelines(new_atom_list)
