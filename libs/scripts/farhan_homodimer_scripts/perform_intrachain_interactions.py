#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  5 11:01:54 2019

@author: farhan
"""
#this script performs an intra chain chain interaction in a pdb containing single chain and records the distance into a file
import os,sys

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


pdbfilename=sys.argv[1]
chain_1=sys.argv[2]
chain_2=sys.argv[3]
dist=sys.argv[4]
outfile=sys.argv[5]
#pdbfilename="/data/farhan/SoftwareTools/HomopolymerProject/data/Actin/monomer/1j6z.pdb"
dist=8
#outfile="Actin_out/Actin_monomer"
#if (not os.path.isdir(outfile)):
#    os.mkdir(outfile)
    
#chain_1="A"
#chain_2="A"
chain_list=getChainList(pdbfilename)
#print(chain_list)
os.system("python pdb2distancemonomer.py "+pdbfilename+" "+chain_1+" "+chain_2+" "+str(dist)+" "+outfile)
#os.system("python pdb2distancemonomer.py "+pdbfilename+" "+chain_list[0]+" "+chain_list[0]+" "+str(dist)+" "+outfile)
#os.system("python pdb2distanceallchains.py "+pdbfilename+" "+chain_list[0]+" "+chain_list[0]+" "+str(dist)+" "+outfile)
#os.system("python pdb2distanceallchains.py "+pdbfilename+" A C "+str(dist)+" "+outfile)

#for i in range(1,len(chain_list)-1):
#    print(chain_list[i])
    #    os.system("python pdb2distanceallchains.py "+pdbfilename+" "+chain_list[0]+" "+chain_list[i]+" "+str(dist)+" "+outfile)
    
    


