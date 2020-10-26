#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  6 13:55:24 2019

@author: farhan
"""
#this script takes as an input an RR file and a map_dict.txt file generated using mapfasta2pdb.py script
#this script tries to patch the errors created due to mismatches between fasta sequence and the pdb fasta sequence.
import sys
from readRR import readRRFile, write2File

def readMapDict(mpd):
    map_dict={}
    with open (mpd,"r") as f:
        for line in f:
            split=line.strip().split(":")
            map_dict[split[0].strip()]=split[1].strip()
    return map_dict


def adjustRRFile(content_list, map_dict):
    contents=content_list
    new_contents=[]
    new_string=""
    for item in contents:
        split=item.split()
        
        if (split[0] in sorted(map_dict.keys()) and split[1] in sorted(map_dict.keys())): 
            split[0]=map_dict[split[0]]#str(int(split[0])-trim)
            split[1]=map_dict[split[1]]#str(int(split[1])-trim)
        else:
            continue #ignore the other stuff that are not found in the pdb but are present in RR file
        for i in range (len(split)):
            new_string+=split[i]+" "
        new_string+="\n"
        new_contents.append(new_string)
        new_string=""
    return new_contents

outdir="/data/farhan/SoftwareTools/HomopolymerProject/scripts/4zuk_out/"
file="4zuk_chainA.dncon2.rr"
#file=sys.argv[1]
#trim=int(sys.argv[2])

print(outdir+file)


fasta,contents=readRRFile(outdir+file)
map_dict=readMapDict(outdir+"mapdict.txt")
#print(map_dict)
#fasta=fasta[trim:len(fasta)]

new_contents= adjustRRFile(contents, map_dict)

write2File("trimmed_rr.rr",fasta,new_contents)

