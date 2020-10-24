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
           'TYR':'Y','VAL':'V','MES':'M'}
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
            if (atom_A["chain"]==" " or atom_A["chain"]=="  " or atom_A["chain"]==""): atom_A["chain"]=chain_1
            if (atom_B["chain"]==" " or atom_B["chain"]=="  " or atom_B["chain"]==""): atom_B["chain"]=chain_2
            
            #if (atom_A["res_name"]=="GLY"):
            #    string+=atom_A["chain"]+" "+atom_A["serial"]+" "+atom_A["res_name"]+" "+atom_A["res_num"]+" "+atom_A["x"]+" "+atom_A["y"]+" "+atom_A["z"]+" "+atom_A["atom_name"]+" | "+ atom_B["atom_name"]+" "+atom_B["chain"]+" "+atom_B["serial"]+" "+atom_B["res_name"]+" "+atom_B["res_num"]+" "+atom_B["x"]+" "+atom_B["y"]+" "+atom_B["z"]+" | " + str(distance(getCoordinate(atom_A),getCoordinate(atom_B)))
            #    pass
            #if (atom_B["res_name"]=="GLY"):
            #    pass
            string+=atom_A["chain"]+" "+atom_A["serial"]+" "+atom_A["res_name"]+" "+atom_A["res_num"]+" "+atom_A["x"]+" "+atom_A["y"]+" "+atom_A["z"]+" "+atom_A["atom_name"]+" | "+ atom_B["atom_name"]+" "+atom_B["chain"]+" "+atom_B["serial"]+" "+atom_B["res_name"]+" "+atom_B["res_num"]+" "+atom_B["x"]+" "+atom_B["y"]+" "+atom_B["z"]+" | " + str(distance(getCoordinate(atom_A),getCoordinate(atom_B)))
            if (distance(getCoordinate(atom_A),getCoordinate(atom_B))<dist): result_list_string.append(string+"\n")
            #result_list_string.append(string+"\n")
    
    return result_list_string

def writeToFile(outfile,stuff):
    with open (outfile,"w") as f:
        f.writelines(stuff)
    return

#pdbfilename="/data/farhan/SoftwareTools/HomopolymerProject/data/pdb/5wvc.pdb"
atomfolder="/data/farhan/SoftwareTools/HomopolymerProject/data/homodimers/homodimers_files/outfolder/atom/"
pdb=sys.argv[1]
os.system("ls "+atomfolder+pdb+"* > atomfiles.txt")
pdbfile_list=[]
with open ("atomfiles.txt","r") as f:
    for line in f:
        pdbfile_list.append(line.strip())
#sys.exit()
os.system("rm -f atomfiles.txt")
pdbfile_A=pdbfile_list[0]#atomfolder+pdb+"A.atom"#sys.argv[1]
pdbfile_B=pdbfile_list[1]#atomfolder+pdb+"B.atom"#sys.argv[2]

#chain_1=sys.argv[2]
#chain_2=sys.argv[3]
dist=8.0#sys.argv[3]
#outfile=sys.argv[4]
#fasta=sys.argv[6]


split_contents_A=contents2Info(readPDB(pdbfile_A))
split_contents_B=contents2Info(readPDB(pdbfile_B))
chain_1=getChain(pdbfile_A)
chain_2=getChain(pdbfile_B)


atom_list_A=split_contents_A
atom_list_B=split_contents_B
fasta_A=pdb2FastaFromSplitContents(atom_list_A)
L_A=len(fasta_A)
fasta_B=pdb2FastaFromSplitContents(atom_list_B)
L_B=len(fasta_B)

if (fasta_A != fasta_B):
    print (pdb+" : Fasta sequences of both files are not same...")
    os.system("echo "+pdb+" "+": Fasta sequences of both files are not same... >> not_done_reason.txt")
    sys.exit()
    

"""
for items in cb_list_A:
    if (items["serial"].strip()=="376"): print (items["z"]+" "+items["res_num"]+" "+items["res_name"])
    if (items["serial"].strip()=="367"): print (items["z"]+" "+items["res_num"]+" "+items["res_name"])
    if (items["serial"].strip()=="343"): print (items["z"]+" "+items["res_num"]+" "+items["res_name"])

for items in cb_list_B:
    if (items["serial"].strip()=="423"): print (items["z"]+" "+items["res_num"]+" "+items["res_name"])
    if (items["serial"].strip()=="429"): print (items["z"]+" "+items["res_num"]+" "+items["res_name"])
    if (items["serial"].strip()=="435"): print (items["z"]+" "+items["res_num"]+" "+items["res_name"])
"""
#print (len(cb_list_A),len(cb_list_A))
pw_dist=createDistanceMapAllAtoms(atom_list_A,atom_list_B,8)

if (len(pw_dist)==0):
    print (pdb+" "+": No interchain contacts less than 8.0...")
    os.system("echo "+pdb+" "+": No interchain contacts less than 8.0... >> not_done_reason.txt")
    sys.exit()
ok_flag=False
for line in pw_dist:
    if ("GLY" in line):
        if ("CA  |  CA" in line or "CA  |  CB" in line or "CB  |  CA" in line): ok_flag=True
    else:
        if ("CB  |  CB" in line): ok_flag=True

if (not ok_flag):
    print (pdb+" : No CB-CB contacts found...")
    os.system("echo "+pdb+" "+": no CB-CB contacts found... >> not_done_reason.txt")
    
outfile_dist=getName(pdbfile_A)#outfile.replace(".txt","")+"_dist_"+chain_1+chain_2+".txt"
outfile=outfile_dist+"_"+chain_1+chain_2+".txt"
#print(outfile_dist)
#outfile_dist=outfile+"_dist_"+chain_1+chain_2+".txt"
write_flag=True

if (write_flag):
    writeToFile(outfile,pw_dist)
    #writeToFile(outfile.replace(".txt",".rr"),pw_rr)


