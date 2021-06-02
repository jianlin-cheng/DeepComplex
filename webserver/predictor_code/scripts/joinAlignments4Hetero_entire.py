#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 14 03:13:59 2020

@author: farhan
"""

#this script reads the two heteromeric alignments in .a3m format
#creates respectie dictionaries and indices
#searches the PPI dictionary for interacting pairs
#then creates the concatenated alignment file in .a3m format

import os, sys, shutil
import numpy as np

def getName(file):
    return os.path.basename(file.strip()).split(".")[0]

def createDictFromA3m(file,name):
    aln_dict={}
    with open (file) as f:
        for line in f:
            if line.startswith(">"):
                idx=line.strip().replace(">","")
                #idx=idx.split("/")[0]
                if name in idx: idx=name
                line=f.readline()
                aln_dict[idx]=line.strip()            
    return aln_dict

def saveFastaDictionary(filename,dict):
    with open (filename,"w") as f:
        for k,v in dict.items():
            f.write(k+":"+v+"\n")

def loadFastaDictionary(filename):
    d={}
    with open (filename) as f:
        for line in f:
            idx=line.strip().split(":")[0].strip()
            fasta=line.strip().split(":")[1].strip()
            d[idx]=fasta
    return d


list_file=os.path.abspath(sys.argv[1])
aln_folder=os.path.abspath(sys.argv[2])
ppi_file=os.path.abspath(sys.argv[3])
outdir=os.path.abspath(sys.argv[4])+"/"
missing_dir=outdir+"missing/"
print ("Output will be stored in "+outdir)
if not os.path.isdir(outdir): os.makedirs(outdir)
if not os.path.isdir(missing_dir): os.makedirs(missing_dir)
#loading the ppi_dict can fail. This file is very big. So loading it only once is logical
ppi_dict = np.load(ppi_file, allow_pickle='TRUE').item()


with open ("DoneFile.txt","w") as donefile:
    with open (list_file) as lsf:
        for line in lsf:
            if "__" in line: line=line.replace("__","_")
            aln_A=aln_folder+"/"+line.strip().split("_")[0]+".a3m"
            aln_B=aln_folder+"/"+line.strip().split("_")[1]+".a3m"
            #extract the names
            name_A=getName(aln_A)
            name_B=getName(aln_B)
            #create the fasta dictionaries from the .a3m files
            dict_A=createDictFromA3m(aln_A,name_A)
            dict_B=createDictFromA3m(aln_B,name_B)
            #temporary working directory
            tmpdir=outdir+"tmpdir"+name_A+"_"+name_B+"/"
            #save the dictionaries as .txt files
            if not os.path.isdir(tmpdir): os.makedirs(tmpdir)
            dictfile_A=tmpdir+name_A+"_dict.txt"
            dictfile_B=tmpdir+name_B+"_dict.txt"
            saveFastaDictionary(dictfile_A,dict_A)
            saveFastaDictionary(dictfile_B,dict_B)
            
            keys_A=list(dict_A.keys())
            keys_B=list(dict_B.keys())
            keys_A.remove(name_A)
            keys_B.remove(name_B)
            pairs_AB=[]
            pairs_AB.append([name_A,name_B])
            #here comes the big search. This is the longest step. Needs to be optimized.
            
#$#$#$#$#$#$#$            
            print ("Len (A)",len(keys_A))
            print ("Len (B)",len(keys_B))
            #here comes the big search. This is the longest step. Needs to be optimized.
            if os.path.exists(missing_dir+name_A+"_"+name_B+"_missing.txt"): os.remove(missing_dir+name_A+"_"+name_B+"_missing.txt")
            for idx_A in keys_A:
                print ("Processing idx_A: "+idx_A)
                #get the interacting proteins for this idx
                if ppi_dict.get(idx_A.split("/")[0])!=None:
                    #print ("Here!@!@!@!@!@!@!@!@!@!@")
                    #interactions_with_idx_A=ppi_dict[idx_A]
                    interactions_with_idx_A=ppi_dict.get(idx_A.split("/")[0])
                    ##### Uncomment the following if we want to keep phylogeny-based integrated.
                    interactions_with_idx_A.insert(0,idx_A.split("/")[0])
                    interactions_with_idx_A=list(set(interactions_with_idx_A))
                    print ("Found interactions for:\n"+idx_A+":"+str(ppi_dict[idx_A.split("/")[0]]))
                else:
                    print (idx_A + " interactions were not found. Possibly these are chemical interactions and not physical or homomeric. Adding to missing list!")
                    ##### Uncomment the following if we want to keep phylogeny-based integrated. Comment out the 'continue'
                    interactions_with_idx_A.insert(0,idx_A.split("/")[0])
                    with open (missing_dir+name_A+"_"+name_B+"_missing.txt","a+") as missing:
                        missing.write(idx_A+"\n")
                    #continue
                print (len(interactions_with_idx_A),"possible interactions found!")
                if len(interactions_with_idx_A)==0: continue
                for inner_idx_key_A in interactions_with_idx_A:
                    for idx_B in keys_B:
                        if inner_idx_key_A in idx_B.split("/")[0]:
                            pairs_AB.append([idx_A,idx_B])
                        
            if os.path.exists(tmpdir+"pairs_AB.a3m"): os.remove(tmpdir+"pairs_AB.a3m")
            
            print ("Total of ",len(pairs_AB),"alignments found!")
            
            with open (tmpdir+"pairs_AB.txt","w") as f:
                for pair in pairs_AB:
                    f.write(pair[0]+","+pair[1]+"\n")
            
            with open (tmpdir+"pairs_AB.a3m","w") as fa3m:
                for pair in pairs_AB:
                    fa3m.write(">"+pair[0]+"_"+pair[1]+"\n")
                    fa3m.write(dict_A[pair[0]].strip()+dict_B[pair[1]].strip()+"\n")
            
            shutil.copy2(tmpdir+"pairs_AB.a3m",outdir+name_A+"_"+name_B+".a3m")

#$#$#$#$#$#$#$            
            """
            for idx_A in keys_A:
                #get the interacting proteins for this idx
                interactions_with_idx_A=ppi_dict[idx_A]
                for inner_idx_key_A in interactions_with_idx_A:
                    if inner_idx_key_A in keys_B:
                        pairs_AB.append([idx_A,inner_idx_key_A])
                        
            
            with open (tmpdir+"pairs_AB.txt","w") as f:
                for pair in pairs_AB:
                    f.write(pair[0]+","+pair[1]+"\n")
                    with open (tmpdir+"pairs_AB.a3m","w") as fa3m:
                        fa3m.write(">"+pair[0]+"_"+pair[1]+"\n")
                        fa3m.write(dict_A[pair[0]].strip()+dict_B[pair[1]].strip()+"\n")
            
            shutil.copy2(tmpdir+"pairs_AB.a3m",outdir+name_A+"_"+name_B+".a3m")
            """
            os.system("grep -v ^> "+outdir+name_A+"_"+name_B+".a3m"+" | sed 's/[a-z]//g' > "+outdir+name_A+"_"+name_B+".aln")
        donefile.write(line)
        os.system("rm -rf "+tmpdir)

#print ()
    











