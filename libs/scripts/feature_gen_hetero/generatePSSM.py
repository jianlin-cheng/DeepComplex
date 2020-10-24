#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  6 22:42:08 2020

@author: farhan
"""
#this script will generate the psiblast homologue alignment and then the pssm protein profile matrix
#usage: python generatePSSM.py <paths.txt> <fasta> <outfolder>

from readPathsFile import getToolPaths
import os, sys

paths_file=os.path.abspath(sys.argv[1])
fasta=os.path.abspath(sys.argv[2])
outfolder=os.path.abspath(sys.argv[3])+"/pssm/"
name=os.path.basename(fasta).split(".")[0]
if not os.path.isdir(outfolder): os.makedirs(outfolder)

paths_dict=getToolPaths(paths_file)
psiblast_path=os.path.abspath(paths_dict["psiblast"])
psiblast_db=os.path.abspath(paths_dict["blast_db"])
formatdb=os.path.abspath(paths_dict["formatdb"])

print("Running PSI-BLAST on fasta_file: "+fasta+" using database "+psiblast_db)
exit_code=os.system(psiblast_path+"/psiblast -query "+fasta+" -evalue 0.001 -inclusion_ethresh 0.002 -db "+psiblast_db+" -num_iterations 3 -outfmt 0 -out "+outfolder+name+".psiblast -seg yes -out_ascii_pssm "+outfolder+name+".pssm")
#Run with different arguments incase fails
#print ("Seccond try failed. Running custom db version with formated fasta...")
#exit_code=os.system(formatdb+"/formatdb -i "+fasta)
#exit_code=os.system(psiblast_path+"/psiblast -query "+fasta+" -evalue 0.001 -inclusion_ethresh 0.002 -db "+fasta+" -num_iterations 3 -outfmt 0 -out "+outfolder+name+".psiblast -seg yes -out_ascii_pssm "+outfolder+name+".pssm")

if exit_code!=0 or not os.path.exists(outfolder+name+".pssm"):
    print ("First try failed. Running less stringent version ...")
    exit_code=os.system(psiblast_path+"/psiblast -query "+fasta+" -evalue 10 -inclusion_ethresh 10 -db "+psiblast_db+" -num_iterations 3 -outfmt 0 -out "+outfolder+name+".psiblast -num_alignments 2000 -out_ascii_pssm "+outfolder+name+".pssm")

if exit_code!=0 or not os.path.exists(outfolder+name+".pssm"):
    print ("Seccond try failed. Running custom db version with formated fasta...")
    exit_code=os.system(formatdb+"/formatdb -i "+fasta)
    exit_code=os.system(psiblast_path+"/psiblast -query "+fasta+" -evalue 0.001 -inclusion_ethresh 0.002 -db "+fasta+" -num_iterations 3 -outfmt 0 -out "+outfolder+name+".psiblast -seg yes -out_ascii_pssm "+outfolder+name+".pssm")
