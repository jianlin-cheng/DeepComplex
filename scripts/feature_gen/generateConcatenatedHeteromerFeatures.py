#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  6 22:42:08 2020

@author: farhan
"""
#this script will create some features that need to be concatenated.
#usage: python generateConcatenatedHeteromerFeatures.py <paths.txt> <heterodimer_fasta> <outdir>

from readPathsFile import getToolPaths
from readHeterdimerFasta import readFastaFile
import os, sys
import string


def runFeatureGeneration(file):
    if not os.path.exists(file): sys.exit("File "+file+" was not found. Quitting!")
    dirnm=os.path.dirname(file)+"/"
    command_psipred="python generatePSIPRED.py paths.txt "+file+" "+dirnm
    #command_pssm="python generatePSSM.py paths.txt "+file+" "+dirnm
    command_ss_sa="python generateSS_SA.py paths.txt "+file+" "+dirnm
    #command_deepmsa=""
    #os.system(command_psipred+" & "+command_pssm+" & "+command_ss_sa)
    os.system(command_psipred+" & "+command_ss_sa)
    return

#paths_file=os.path.abspath(sys.argv[1])
fasta_file=os.path.abspath(sys.argv[1])
outfolder=os.path.abspath(sys.argv[2])+"/"
name=os.path.basename(fasta_file).split(".")[0]
temp_work_dir=outfolder+name+"/temp/"

if not os.path.isdir(outfolder): os.makedirs(outfolder)
if not os.path.isdir(temp_work_dir): os.makedirs(temp_work_dir)
#paths_dict=getToolPaths(paths_file)

fasta_dict=readFastaFile(fasta_file)
chains=len(fasta_dict)
key_list=list(fasta_dict.keys())
alphabet_string = string.ascii_uppercase
i=0
file_list=[]
for key in key_list:
    file_name=key.split()[0].replace(">","")+alphabet_string[i]+".fasta"
    dir_name=temp_work_dir+key.split()[0].replace(">","")+alphabet_string[i]+"/"
    if not os.path.isdir(dir_name):os.makedirs(dir_name)
    file_list.append(dir_name+file_name)
    with open (dir_name+file_name,"w") as f:
        f.write(key.split()[0]+alphabet_string[i]+"\n")
        f.write(fasta_dict[key]+"\n")
    i+=1

for i in range(len(file_list)):
    runFeatureGeneration(file_list[i])

combined_dir=outfolder+name+"/"
if not os.path.isdir(combined_dir+"pssm/"): os.makedirs(combined_dir+"pssm/")
if not os.path.isdir(combined_dir+"psipred/"): os.makedirs(combined_dir+"psipred/")
if not os.path.isdir(combined_dir+"ss_sa/"): os.makedirs(combined_dir+"ss_sa/")

if len (file_list)==2:
    concat_fasta_file=combined_dir+name+"_AB.fasta"
    with open (concat_fasta_file,"w") as f:
        f.write(">"+name+"_AB; Chains: A, B; Lengths: "+str(len(fasta_dict[key_list[0]]))+str(len(fasta_dict[key_list[1]]))+"\n")
        f.write(fasta_dict[key_list[0]]+fasta_dict[key_list[1]])
    dirnm_A=os.path.dirname(file_list[0])+"/"
    file_A=os.path.basename(file_list[0]).split(".")[0]
    dirnm_B=os.path.dirname(file_list[1])+"/"
    file_B=os.path.basename(file_list[1]).split(".")[0]
    os.system("python combineSS2.py "+dirnm_A+"psipred/"+file_A+".ss2 "+dirnm_B+"psipred/"+file_B+".ss2 "+combined_dir+"psipred/"+name+".ss2")
    os.system("python combineSolv.py "+dirnm_A+"psipred/"+file_A+".solv "+dirnm_B+"psipred/"+file_B+".solv "+combined_dir+"psipred/"+name+".ss2")
    #os.system("python combineSS_SA.py "+file_list[0]+" "+dirnm_A+"ss_sa/"+file_A+".ss_sa "+file_list[1]+" "+dirnm_B+"ss_sa/"+file_B+".ss_sa "+combined_dir+"ss_sa/"+name+".ss_sa")
    os.system("python combineSS_SA.py "+dirnm_A+"ss_sa/"+file_A+".ss_sa "+dirnm_B+"ss_sa/"+file_B+".ss_sa "+combined_dir+"ss_sa/"+name+".ss_sa")
    os.system("python generatePSIPRED.py paths.txt "+concat_fasta_file+" "+combined_dir)

#os.system("rm -rf "+temp_work_dir)
#print (fasta_dict)

