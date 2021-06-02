#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  6 22:42:08 2020

@author: farhan
"""
#this script will generate the pssm protein profile matrix using psiblast and already made alignments
#usage: python generatePSSM.py <paths.txt> <fasta> <msa> <outfolder>

from readPathsFile import getToolPaths
import os, sys

paths_file=os.path.abspath(sys.argv[1])
fasta=os.path.abspath(sys.argv[2])
msa=os.path.abspath(sys.argv[3])#
outfolder=os.path.abspath(sys.argv[4])+"/pssm/"
name=os.path.basename(fasta).split(".")[0]
if not os.path.isdir(outfolder): os.makedirs(outfolder)
#os.system("cp "+msa+" "+outfolder)
os.system("sed 's/[a-z]//g' "+msa+" > "+outfolder+name+".a3m")
paths_dict=getToolPaths(paths_file)
psiblast_path=os.path.abspath(paths_dict["psiblast"])
psiblast_db=os.path.abspath(paths_dict["blast_db"])
formatdb=os.path.abspath(paths_dict["formatdb"])

print("Running PSI-BLAST on fasta_file: "+fasta+" using MSA "+msa)
exit_code=os.system(psiblast_path+"/psiblast -subject "+fasta+" -in_msa "+outfolder+name+".a3m -out "+outfolder+name+".psiblast -seg yes -out_ascii_pssm "+outfolder+name+".pssm")

