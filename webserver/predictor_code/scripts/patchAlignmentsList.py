#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  3 21:27:28 2020

@author: farhan
"""
#thi script runs the patchAlignment.py for every file in the list
#this script checks the alignments folder for any incomplete alignment files and renames them to WXYZ.aln
#checks for # of alignments >= L * 5 and minimum e-value
import os, sys, subprocess,shutil

fastafolder=os.path.abspath(sys.argv[2])+"/" #"/storage/htc/bdm/farhan/HomopolymerProject/HomopolymerProject/data/homooligomer/fastas/different_fastas/"
outfolder=os.path.abspath(sys.argv[3])+"/" #"/storage/htc/bdm/farhan/HomopolymerProject/HomopolymerProject/data/homooligomer/diff_dncon2_output/"
list_file=os.path.abspath(sys.argv[1])
pdblist=[]

with open (list_file) as f:
   for line in f:
      pdblist.append(line.strip().replace(".fasta",""))
problem=[]
for fasta_name in pdblist:
   print ("Working on :",fasta_name)
   exitcode=os.system("python /storage/htc/bdm/farhan/string_db/hetero30_aln_run/patchAlignment.py "+fastafolder+fasta_name+".fasta "+outfolder+"/tmpdir"+fasta_name+" "+outfolder+"/tmpdir"+fasta_name)
   if (exitcode!=0):
      print("problem with "+fasta_name)
      problem.append(fasta_name+"\n")
      continue
   shutil.copy2(outfolder+"/tmpdir"+fasta_name+"/"+fasta_name+".a3m",outfolder+fasta_name+".a3m")
   shutil.copy2(outfolder+"/tmpdir"+fasta_name+"/"+fasta_name+".aln",outfolder+fasta_name+".aln")

if len(problem)!=0:
   with open ("patch_problem.txt","w") as f:
      f.writelines(problem)



