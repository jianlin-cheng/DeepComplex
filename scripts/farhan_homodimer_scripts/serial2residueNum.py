#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  4 12:50:39 2019

@author: farhan
"""

#converts a serial number rr file to res_num rr file
#from readPDBColumns import readPDB,readAtom,write2File,contents2Info,addColumn,reassembleLines,getChain

def readPDB(pdb):
    contents=[]
    with open (pdb,"r") as f:
        for line in f:
            #if (line.startswith("ATOM")):
            #    pass
            contents.append(line)
    return contents

def splitLine2Tuple(line):
    atom=line[0:6]
    serial=line[6:12]
    atom_name=line[12:16]
    alt_loc=line[16]
    res_name=line[17:20]
    chain=line[20:22]
    res_num=line[22:26]
    icode=line[26:30]
    x=line[30:38]
    y=line[38:46]
    z=line[46:54]
    occupancy=line[54:60]
    temp_fact=line[60:76]
    element=line[76:78]
    charge=line[78:80]
    
    return {"atom":atom,"serial":serial,"atom_name":atom_name,"alt_loc":alt_loc,"res_name":res_name,"chain":chain,
            "res_num":res_num,"icode":icode,"x":x,"y":y,"z":z,"occupancy":occupancy,"temp_fact":temp_fact,"element":element,
            "charge":charge}

def contents2Info(contents): #reads the ATOM line. Then splits the info into respective frames and returns the data
    split_contents={}
    for lines in contents:
        if (lines.startswith("ATOM")):
            tupl_dict=splitLine2Tuple(lines.strip())
            #print (tupl_dict)
            #split_contents.append(tupl_dict)
            split_contents[tupl_dict["serial"].strip()]=tupl_dict
    return split_contents

pdbA="/data/farhan/SoftwareTools/HomopolymerProject/working_scripts/pdb_folder_test/work_dir/atom/6BZEA.atom"
pdbB="/data/farhan/SoftwareTools/HomopolymerProject/working_scripts/pdb_folder_test/work_dir/atom/6BZEB.atom"
rrfile="6BZE_dist_AB.txt"
res_contents=[]
res_rr=[]
split_contents_A=contents2Info(readPDB(pdbA))
split_contents_B=contents2Info(readPDB(pdbB))

with open (rrfile,"r") as f:
    line=f.readline()
    for line in f:
        #print (line)
        split=line.strip().split()
        i=split[0]
        j=split[1]
        atom_i=split_contents_A[i]["atom_name"].strip()
        res_num_i=split_contents_A[i]["res_num"].strip()
        res_name_i=split_contents_A[i]["res_name"].strip()
        atom_j=split_contents_B[j]["atom_name"].strip()
        res_num_j=split_contents_B[j]["res_num"].strip()
        res_name_j=split_contents_B[j]["res_name"].strip()
        if (atom_i=="CB" and atom_j=="CB"):
            res_contents.append(i+" "+atom_i+" "+atom_j+" "+j+"\n")
            res_rr.append(res_num_i+" "+res_num_j+" 0 8.0 "+split[4]+"\n")
        #res_contents.append(i+" "+atom_i+" "+atom_j+" "+j+"\n")
#print (res_contents)

with open ("atoms_AB_CB.txt","w") as f:
    f.writelines(res_contents)

with open ("atoms_AB_CB.rr","w") as f:
    f.writelines(res_rr)
