#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  5 11:01:54 2019

@author: farhan
"""
#this script performs a chain chain interaction in a pdb containing multiple chains and records the distance into a file
import os,sys
from mapfasta2pdb import pdb2fasta

def getChainList(pdb):
    with open (pdb,"r") as f:
        prev_chain="-1"
        chain_list=[]
        for line in f:
            if line.startswith("ATOM"):
                split=line.strip().split()
                chain=split[4]
                if (prev_chain==chain): 
                    continue
                else:
                    chain_list.append(chain)
                    prev_chain=chain
            else:
                continue
    return chain_list

def getLength(fastafile):
    l=0
    s=""
    with open (fastafile,"r") as f:
        for line in f:
            if line.strip().startswith(">"): continue
            s+=line.strip()
            l+=len(line.strip())
            
    return s,l

fold="/data/farhan/SoftwareTools/HomopolymerProject/scripts/3J6J_out/temp"

pdbfilename=sys.argv[1]
#chain_1=sys.argv[2]# not needed
#chain_2=sys.argv[3]# not needed
dist=sys.argv[2]
outfile=sys.argv[3]
fastafile=sys.argv[4]
chn=sys.argv[5]

#Actin
#pdbfilename="/data/farhan/SoftwareTools/HomopolymerProject/data/Actin/multimer/5jlf.pdb"
#fastafile="/data/farhan/SoftwareTools/HomopolymerProject/data/Actin/monomer/1j6z.fasta.txt"

#ASC
#pdbfilename="/data/farhan/SoftwareTools/HomopolymerProject/data/ASC/multimer/3j63.pdb"
#fastafile="/data/farhan/SoftwareTools/HomopolymerProject/data/ASC/monomer/1ucp.fasta.txt"

#4zuk
#pdbfilename="/data/farhan/SoftwareTools/HomopolymerProject/data/4zuk/multimer/4zuk.pdb"
#fastafile="/data/farhan/SoftwareTools/HomopolymerProject/data/4zuk/monomer/4zuk_chainA.fasta"

#3J6J
#pdbfilename="/data/farhan/SoftwareTools/HomopolymerProject/scripts/3J6J_out/temp/3J6J_mod.pdb"
#fastafile="/data/farhan/SoftwareTools/HomopolymerProject/scripts/3J6J_out/temp/3J6J.fasta"


fasta=pdb2fasta(pdbfilename,chn)

#dist=8
#outfile="Actin_out/Actin_multimer_dist_8"
#outfile="4zuk_out/4zuk_multimer_dist_8"
#if (not os.path.isdir(outfile)):
#    os.mkdir(outfile)
    
chain_1="A"
chain_2="B"
chain_list=getChainList(pdbfilename)
ffasta,ll=getLength(fastafile)
l=len(fasta)
#print(l,ll)
if (l!=ll): print("Fasta length not similar!")
#os.system("python pdb2distanceallchains.py "+pdbfilename+" A C "+str(dist)+" "+outfile)
#print(chain_list)
for i in range(0,len(chain_list)):
    #print(chain_list[i])
    if (chn==chain_list[i]): continue
    os.system("python pdb2distanceallchains.py "+pdbfilename+" "+chn+" "+chain_list[i]+" "+str(dist)+" "+outfile+" "+fasta)
    print("python pdb2distanceallchains.py "+pdbfilename+" "+chn+" "+chain_list[i]+" "+str(dist)+" "+outfile+" "+fasta)
    #sys.exit()
    #print("Boss!!!")
    
    


