#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  6 22:42:08 2020

@author: farhan
"""
#this script will create secondary structures using psipred.
#usage: python generatePSIPRED.py <paths.txt> <fasta> <outdir>


from readPathsFile import getToolPaths
import os, sys

paths_file=os.path.abspath(sys.argv[1])
fasta=os.path.abspath(sys.argv[2])
outfolder=os.path.abspath(sys.argv[3])+"/psipred/"
name=os.path.basename(fasta).split(".")[0]
if not os.path.isdir(outfolder): os.makedirs(outfolder)

paths_dict=getToolPaths(paths_file)
psipred_path=os.path.abspath(paths_dict["psipred"])
psipred_db=os.path.abspath(paths_dict["psipred_db"])
psipred_blast=os.path.abspath(paths_dict["psipred_blast"])
metapsicov_path=os.path.abspath(paths_dict["metapsicov"])
#formatdb=os.path.abspath(paths_dict["formatdb"])
command1="cp "+fasta+" "+outfolder
command2=" cd "+outfolder+" "
command3=" "+metapsicov_path+"/runpsipredandsolv "+outfolder+name+".fasta "+psipred_db+" "+psipred_blast+" "+psipred_path+"/bin/ "+metapsicov_path+"/bin/ "+psipred_path+"/data/ "+metapsicov_path+"/data/ "
os.system(command1+" && "+command2+" && "+command3)
