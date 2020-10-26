#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 25 12:07:26 2019

@author: farhan
"""

#this script filter outs alternate B residues from pdbs like BCYS and keeps the ACYS as CYS
#usage: python removeAlternatesFromPDB.py <in_pdb> <output_pdb>
import os, sys

def readFile(pdbfile):
    contents=[]
    original_contents=[]
    with open (pdbfile,"r") as f:
        for line in f:
            original_contents.append(line)
            if (line.startswith("ATOM")):
                #split=line.strip().split()
                
                aa=line[16:20]#split[3]
                if (len(aa.strip())==4):
                    if (aa.startswith("A")):
                        line=line.replace(aa," "+aa[1:4])
                        #print(line)
                        contents.append(line)
                        #line=f.readLine()
                        #continue
                    else:
                        continue
                else:
                    contents.append(line)
                        
            else:
                
                contents.append(line)
    return original_contents,contents
    
def write2file(file,contents):
    with open (file,"w") as f:
        f.writelines(contents)

#infile="/data/farhan/SoftwareTools/HomopolymerProject/data/4zuk/multimer/4zuk.pdb"
#outfile="/data/farhan/SoftwareTools/HomopolymerProject/data/4zuk/multimer/4zuk_mod.pdb"
infile=sys.argv[1]
outfile=sys.argv[2]

original_contents,contents=readFile(infile)
if (len(original_contents)>len(contents)): write2file(outfile,contents)

