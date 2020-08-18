#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 16:38:30 2020

@author: farhan
"""

#this script reads a fasta_dictionary.txt files to generate the individual fasta files and outputs them into a folder
#usage createFastaFilesFromFastaDictionary.py <fasta_dictionary.txt> <outfolder> 

import sys, os
from loadFastaDictionary import loadFastaDictionary

fasta_dict_file=sys.argv[1].strip()
outfolder=sys.argv[2].strip()
outfolder=os.path.abspath(outfolder)

if not(os.path.exists(fasta_dict_file)): sys.exit("Unable to find "+fasta_dict_file+" file...quiting!")
if not (outfolder.endswith("/")): outfolder+="/"
if not (os.path.isdir(outfolder)): os.makedirs(outfolder)

fasta_dict=loadFastaDictionary(fasta_dict_file)
for key,fasta in fasta_dict.items():
    with open (outfolder+key+".fasta","w") as f:
        f.write("> "+key+", L="+str(len(fasta))+" :\n")
        f.write(fasta.strip())

print ("All fasta files are written in the folder "+outfolder)
#print (outfolder)