#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 24 03:52:57 2020

@author: farhan
"""

#this script will setup the paths according to the paths.txt file for DNCON2 feature generation.

import os, sys

def fixPaths(filename,path_dict,ofile):
    contents=[]
    #print (path_dict.keys())
    if not os.path.exists(filename):
        sys.exit(filename+" was not found! Quitting...unsuccessfull installation!")
    with open (filename,"r") as f:
        for line in f:
            if "use constant" in line:
                contents.append(line)
                for _ in range(len(path_dict)):
                    #print("i=",_)
                    line=f.readline()
                    for k in list(path_dict.keys()):
                        #print ("kk=",k)
                        if k == line.split("=>")[0].strip():
                            #print("k=",k)
                            #print("line:",line)
                            line=line.replace(line.split("=>")[1],"'"+path_dict[k]+"',\n")
                            #print ("new_line:",line)
                            contents.append(line)
                            break
                        #else:
                        #    contents.append(line)
            else:
                contents.append(line)
 
    with open (ofile,"w") as f:
        f.writelines(contents)
    os.system("mv "+ofile+" "+filename)
    return

paths_dict={}
feat_gen_dict={}
gen_aln_dict={}
feat_gen_list=["SCRATCH","FORMATDBPATH","BLASTPATH","BLASTNRDB","PSIPRED","ALNSTAT"]
gen_aln_list=["JACKHMMER","JACKHMMERDB","HHBLITS","HHBLITSDB"]
#with open ("paths.txt","r") as f:
with open (os.path.abspath(sys.argv[1]),"r") as f:
    for line in f:
        if line.strip()=="": continue
        split=line.strip().split("=")
        #print (split)
        if split[0].upper()=="NCBIBLASTPATH" or split[0].upper()=="NCBIPATH": split[0]="BLASTPATH"
        if split[0].upper()=="METAPSICOVPATH" or split[0].upper()=="METAPSICOV":
            if not split[1].strip().endswith("/"): split[1]=split[1].strip()+"/"
            paths_dict["PSIPRED"]=split[1]+"runpsipredandsolv"
            paths_dict["ALNSTAT"]=split[1]+"bin/alnstats"
            continue
            
        paths_dict[split[0]]=os.path.abspath(split[1].strip())
#print (paths_dict)
if len (paths_dict) != 9:
    sys.exit("Could not find all the paths in the paths.txt file! Quitting...unsuccessfull installation.")

print ("Checking if the softwares exist in the paths found...")
if "run_SCRATCH-1D_predictors.sh" not in paths_dict["SCRATCH"]:
    if "bin" in paths_dict["SCRATCH"]:
        paths_dict["SCRATCH"]+="/run_SCRATCH-1D_predictors.sh"
    else:
        paths_dict["SCRATCH"]+="/bin/run_SCRATCH-1D_predictors.sh"

paths_dict["FORMATDBPATH"]=paths_dict["SCRATCH"].split("bin/")[0]+"pkg/blast-2.2.26/bin/formatdb"

if not (paths_dict["BLASTPATH"].endswith("bin")):
    paths_dict["BLASTPATH"]+="/bin"

not_found=[]
for key,value in paths_dict.items():
    if not os.path.exists(value):
        print (value+" does not exits!")
        not_found.append(value)
if len (not_found)>0:
    sys.exit("One or more of the following paths could not be found:\n",not_found,"\nQuitting...unsuccessful installation!" )

for key in feat_gen_list:
    feat_gen_dict[key]=paths_dict[key]

for key in gen_aln_list:
    gen_aln_dict[key]=paths_dict[key]

package_dir=os.path.abspath(os.path.dirname(sys.argv[0]))

feature_gen_dir=package_dir+"/inter_chain_contact_predictor/homo_dimer/feature/feature_gen_dncon2/"

fixPaths(package_dir+"/feature_gen_dncon2.pl",feat_gen_dict,"new_file1.txt")
#print (feat_gen_dict)
fixPaths(package_dir+"/generate-alignments.pl",gen_aln_dict,"new_file2.txt")
#feature_gen_contents=[]
#align_gen_contents=[]
print ("All paths are set. Now you can proceed with feature generation and prediction! Successfull Installation!")



