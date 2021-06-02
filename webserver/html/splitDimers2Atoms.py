#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 20 08:51:24 2021

@author: farhan
"""
import os
targetid="LCI1"
pdbfile="./LCI1_GD.pdb"
chain_A=""
chain_B=""
with open (pdbfile) as f:
    for line in f:
        if line.startswith("ATOM"):
            #print (line[21])
            chain_A=line[21].strip()
            break
#print ("A=",chain_A)
atom_list_A=[]
atom_list_B=[]

with open (pdbfile) as f:
    for line in f:
        if line.startswith("TER"): continue
        if line.startswith("ATOM"):
            if line[21].strip() == chain_A:
                atom_list_A.append(line)
            if line[21].strip()!="" and line[21].strip()!=chain_A:
                chain_B=line[21].strip()
                break

with open (pdbfile) as f:
    for line in f:
        if line.startswith("ATOM"):
            if line[21].strip() == chain_B:
                atom_list_B.append(line)
atomfileA=targetid+chain_A+".atom" #os.path.basename(pdbfile).split("_")[0]
atomfileB=targetid+chain_B +".atom"

print ("A=",chain_A)
print ("B=",chain_B)


with open (os.path.dirname(pdbfile)+"/"+atomfileA,"w") as f:
    f.writelines(atom_list_A)

with open (os.path.dirname(pdbfile)+"/"+atomfileB,"w") as f:
    f.writelines(atom_list_B)
