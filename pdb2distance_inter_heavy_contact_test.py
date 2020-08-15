#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 17 13:28:19 2019

@author: farhan
"""

#this script creates a contact map text file for all atoms
#usage: python pdb2distance_inter_heavy.py <chainA.atom> <chainB.atom> <distance_threshold> <PDB_ID>

import os,sys
from readPDBColumns import readPDB,readAtom,write2File,contents2Info,addColumn,reassembleLines,getChain,getName
import numpy as np

#%%

def pdb2FastaFromSplitContents(split_contents):
    fst=""
    letters = {'ALA':'A','ARG':'R','ASN':'N','ASP':'D','CYS':'C','GLU':'E','GLN':'Q','GLY':'G','HIS':'H',
           'ILE':'I','LEU':'L','LYS':'K','MET':'M','PHE':'F','PRO':'P','SER':'S','THR':'T','TRP':'W',
           'TYR':'Y','VAL':'V'}
    prev_res_num=split_contents[0]["res_num"]
    fst+=letters[split_contents[0]["res_name"]]
    for items in split_contents:
        if (items["res_num"]==prev_res_num): continue
        fst+=letters[items["res_name"]]
        prev_res_num=items["res_num"]
    #fst+=letters[items["res_name"]]
    return fst
        
def getCoordinate(atom):
    coordinate={}
    coordinate["x"]=atom["x"]
    coordinate["y"]=atom["y"]
    coordinate["z"]=atom["z"]
    return coordinate

def distance(coord1, coord2):
    x1=float(coord1["x"])
    y1=float(coord1["y"])
    z1=float(coord1["z"])
    x2=float(coord2["x"])
    y2=float(coord2["y"])
    z2=float(coord2["z"])
    d=np.sqrt((x1-x2)**2+(y1-y2)**2+(z1-z2)**2)
    
    return d

def createDistanceMapAllAtoms(atom_list_A,atom_list_B,dist):
    result_list_string=[]
    
    for atom_A in atom_list_A:
        for atom_B in atom_list_B:
            string=""
            if (atom_A["chain"]==" " or atom_A["chain"]=="  " or atom_A["chain"]==""): atom_A["chain"]=chain_1
            if (atom_B["chain"]==" " or atom_B["chain"]=="  " or atom_B["chain"]==""): atom_B["chain"]=chain_2
            
            string+=atom_A["chain"]+" "+atom_A["serial"]+" "+atom_A["res_name"]+" "+atom_A["res_num"]+" "+atom_A["x"]+" "+atom_A["y"]+" "+atom_A["z"]+" "+atom_A["atom_name"]+" | "+ atom_B["atom_name"]+" "+atom_B["chain"]+" "+atom_B["serial"]+" "+atom_B["res_name"]+" "+atom_B["res_num"]+" "+atom_B["x"]+" "+atom_B["y"]+" "+atom_B["z"]+" | " + str(distance(getCoordinate(atom_A),getCoordinate(atom_B)))
            
                
            if (distance(getCoordinate(atom_A),getCoordinate(atom_B))<dist): result_list_string.append(string+"\n")
    
    return result_list_string

def removeRedundantContacts(contact_list):
    new_list=[]
    contact_dict={}
    for contact in contact_list:
        x_y=contact.split()[0]+" "+contact.split()[1]
        contact_dict[x_y]=contact
    #contact_dict=dict(set(contact_dict))
    for key in contact_dict.keys():
        new_list.append(contact_dict[key])

    return new_list

def createDistanceMapHeavyAtoms(atom_list_A,atom_list_B,dist=6.0): #new version. Chose all atoms but the hydrogens
    result_list_string=[]
    distance_list_string=[]
    rr_list_string=[]
    for atom_A in atom_list_A:
        for atom_B in atom_list_B:
            string=""

            if (atom_A["element"].strip()=="H" or atom_A["element"].strip()=="D"): continue
            if (atom_B["element"].strip()=="H" or atom_A["element"].strip()=="D"): continue
            if (distance(getCoordinate(atom_A),getCoordinate(atom_B))<=dist): 
                sys.exit(0)

    distance_list_string=removeRedundantContacts(distance_list_string)
    rr_list_string=removeRedundantContacts(rr_list_string)
    return result_list_string,distance_list_string,rr_list_string

#%%
    
pdbfile_A=sys.argv[1]

pdbfile_B=sys.argv[2]

dist=sys.argv[3] 

pdb=getName(pdbfile_A)

fasta_dict_file="fasta_dictionary.txt"

split_contents_A=contents2Info(readPDB(pdbfile_A))
split_contents_B=contents2Info(readPDB(pdbfile_B))
chain_1=getChain(pdbfile_A)
chain_2=getChain(pdbfile_B)


atom_list_A=split_contents_A
atom_list_B=split_contents_B


result_list,pw_dist,pw_rr=createDistanceMapHeavyAtoms(atom_list_A,atom_list_B,float(dist))

if (len(pw_dist)==0):

    sys.exit("-2")
