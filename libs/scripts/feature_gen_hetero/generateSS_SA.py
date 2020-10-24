#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  6 22:42:08 2020

@author: farhan
"""
#this script will create secondary structures and solvent accessibility using SCRATCH
#usage: python generateSS_SA.py <paths.txt> <fasta> <outdir>


from readPathsFile import getToolPaths
import os, sys

paths_file=os.path.abspath(sys.argv[1])
fasta=os.path.abspath(sys.argv[2])
outfolder=os.path.abspath(sys.argv[3])+"/ss_sa/"
name=os.path.basename(fasta).split(".")[0]
if not os.path.isdir(outfolder): os.makedirs(outfolder)

paths_dict=getToolPaths(paths_file)
scratch_path=os.path.abspath(paths_dict["scratch"])
#metapsicov_path=os.path.abspath(paths_dict["metapsicov"])
print ("Predicting secondary structure and solvent accessibility using SCRATCH...")
command1="cp "+fasta+" "+outfolder
command2=" cd "+outfolder+" "
os.system(command1+" && "+command2+" && "+scratch_path+"/run_SCRATCH-1D_predictors.sh "+outfolder+name+".fasta "+outfolder+name)
#print ("1 Command: "+command1)
cmd1="cp "+fasta +" "+outfolder+name+".ss_sa"
#cmd2="echo >"+name+" > $outdir/ss_sa/$id.ss_sa"
#cmd3="echo \"".seq_fasta($fasta)."\" >> $outdir/ss_sa/$id.ss_sa"
cmd4="tail -n 1 "+outfolder+name+".ss >> "+outfolder+name+".ss_sa"
cmd5="tail -n 1 "+outfolder+name+".acc >> "+outfolder+name+".ss_sa"
cmd6="sed -i 's/-/b/g' "+outfolder+name+".ss_sa"
print ("Predicted SS and SA:\n")

os.system (cmd1+" && "+command2+" && "+cmd4+" && "+cmd5+" && "+cmd6+" && "+"cat "+outfolder+name+".ss_sa")
