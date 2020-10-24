#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  6 22:42:08 2020

@author: farhan
"""
#this script will create a database in the psiblast format
#usage: python createPSIBLASTDB.py <fasta>

from readPathsFile import getToolPaths
import os, sys

paths_file=os.path.abspath(sys.argv[1])
fasta=os.path.abspath(sys.argv[2])
paths_dict=getToolPaths(paths_file)
psiblast_path=os.path.abspath(paths_dict["psiblast"])

if not os.path.exists(psiblast_path+"/formatdb"):
    #sys.exit("Error! "+psiblast_path+"/makeblastdb not found. Quitting!")
    sys.exit("Error! "+psiblast_path+"/formatdb not found. Quitting!")
#exit_code=os.system(psiblast_path+"/makeblastdb -in "+fasta+" -dbtype prot -parse_seqids")
exit_code=os.system(psiblast_path+"/formatdb -i "+fasta)
if (exit_code!=0):
    print ("Oops! Something went wront. Quitting!")