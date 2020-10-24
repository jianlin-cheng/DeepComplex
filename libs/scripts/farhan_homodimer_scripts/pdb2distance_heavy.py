#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 17 13:28:19 2019

@author: farhan
"""

#this script creates a contact map text file for all atoms
#usage: python getContactAllAtoms.py <PDB>

import os,sys
from readPDBColumns import readPDB,readAtom,write2File,contents2Info,addColumn,reassembleLines,getChain,getName
import numpy as np

def pdb2FastaFromSplitContents(split_contents):
    fst=""
    letters = {'ALA':'A','ARG':'R','ASN':'N','ASP':'D','CYS':'C','GLU':'E','GLN':'Q','GLY':'G','HIS':'H',
           'ILE':'I','LEU':'L','LYS':'K','MET':'M','PHE':'F','PRO':'P','SER':'S','THR':'T','TRP':'W',
           'TYR':'Y','VAL':'V'}
    prev_res_num=split_contents[0]["res_num"]
    fst+=split_contents[0]["res_name"]
    for items in split_contents:
        if (items["res_num"]==prev_res_num): continue
        fst+=letters[items["res_name"]]
        prev_res_num=items["res_num"]
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

def createDistanceMapHeavyAtoms(atom_list_A,atom_list_B,dist=5.0):
    distance_list_string=[]
    for atom_A in atom_list_A:
        for atom_B in atom_list_B:
            string=""
            string+=atom_A["chain"]+" "+atom_A["serial"]+" "+atom_A["res_name"]+" "+atom_A["res_num"]+" "+atom_A["x"]+" "+atom_A["y"]+" "+atom_A["z"]+" "+atom_A["atom_name"]+" | "+ atom_B["atom_name"]+" "+atom_B["chain"]+" "+atom_B["serial"]+" "+atom_B["res_name"]+" "+atom_B["res_num"]+" "+atom_B["x"]+" "+atom_B["y"]+" "+atom_B["z"]+" | " + str(distance(getCoordinate(atom_A),getCoordinate(atom_B)))
            if (atom_A["atom_name"].strip()=="N" and atom_B["atom_name"].strip()=="O") or (atom_B["atom_name"].strip()=="N"and atom_A["atom_name"].strip()=="O"):
                    if (distance(getCoordinate(atom_A),getCoordinate(atom_B))<=dist): 
                        distance_string=atom_A["res_num"].strip()+" "+atom_B["res_num"].strip()+" 0 "+str(dist)+" "+ str(distance(getCoordinate(atom_A),getCoordinate(atom_B)))
                        
                        
    distance_list_string=removeRedundantContacts(distance_list_string)
    return distance_list_string

def writeToFile(outfile,stuff):
    with open (outfile,"w") as f:
        f.write(fasta+"\n")
        f.writelines(stuff)
    return

#atomfolder=sys.argv[2]# "/data/farhan/SoftwareTools/HomopolymerProject/data/homodimers/homodimers_files/outfolder/atom/"

pdbfile_A=sys.argv[1]
pdbfile_B=sys.argv[1]

#chain_1=sys.argv[2]
#chain_2=sys.argv[3]
dist=sys.argv[2] 
outfile=sys.argv[3]
pdb=getName(pdbfile_A)


split_contents_A=contents2Info(readPDB(pdbfile_A))
split_contents_B=contents2Info(readPDB(pdbfile_B))

atom_list_A=split_contents_A
atom_list_B=split_contents_B
fasta=pdb2FastaFromSplitContents(atom_list_A)
pw_dist=createDistanceMapHeavyAtoms(atom_list_A,atom_list_B,float(dist))

if (len(pw_dist)==0):
    print (pdb+" "+": No contacts less than "+dist+"...")
    os.system("echo "+pdb+" "+": No chain contacts less than "+dist+" ... >> not_done_reason_heavy.txt")
    sys.exit()

outfile_dist=outfile.replace(".txt","")+"_dist_.txt"
write_flag=True

if (write_flag):
    writeToFile(outfile_dist,pw_dist)



