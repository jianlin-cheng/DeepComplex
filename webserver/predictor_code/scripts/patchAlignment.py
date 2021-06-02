#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  3 21:27:28 2020

@author: farhan
"""

#this script checks the alignments folder for any incomplete alignment files and renames them to WXYZ.aln
#checks for # of alignments >= L * 5 and minimum e-value
import os, sys, subprocess,shutil

fastafolder=os.path.abspath(sys.argv[2]) #"/storage/htc/bdm/farhan/HomopolymerProject/HomopolymerProject/data/homooligomer/fastas/different_fastas/"
outputfolder=os.path.abspath(sys.argv[3])+"/" #"/storage/htc/bdm/farhan/HomopolymerProject/HomopolymerProject/data/homooligomer/diff_dncon2_output/"
fasta_list_file=os.path.abspath(sys.argv[1])
fasta_file=fasta_list_file
fasta_list=[]
length_dict={}
found=[]
failure=[]
fasta_list.append(os.path.basename(fasta_file).replace(".fasta",""))

#with open (fasta_list_file,"r") as f:
#    for line in f:
#        fasta_list.append(line.strip())

with open (fasta_file) as f2:
    fasta=""
    for ln in f2:
        if ln.startswith(">"): continue
        fasta+=ln.strip()
    length_dict[fasta_list[-1]]=int(len(fasta))

samefile=[]

for file in fasta_list:
    print ("Working on file: "+file)
    #if os.path.exists(outputfolder+file+".aln"): continue
    L=length_dict[file]
    os.system("ls "+outputfolder+"*.aln > "+file+"_aln_list.txt")
    lnnum = subprocess.check_output("wc -l < "+file+"_aln_list.txt",shell = True)
    lnnum = lnnum.rstrip()
    lnnum = str(lnnum)
    lnnum = int(lnnum.strip("b").strip("'"))-1
    if lnnum==0:
        pass
    aln_file_list=[]
    with open (file+"_aln_list.txt","r") as f:
        for line in f:
            line=line.strip()
            if "/" in line:
                aln_file_list.append(line)
    aln_file_list=sorted(aln_file_list)
    idx=0
    alnnum={}
    for aln_file in aln_file_list:
        aln_file=os.path.basename(aln_file)
        #print (aln_file)
        alnnum [aln_file] = subprocess.check_output("wc -l < "+outputfolder+aln_file, shell = True)
        alnnum [aln_file] = alnnum[aln_file].rstrip()
        alnnum [aln_file] = str(alnnum[aln_file])
        alnnum [aln_file] = int(alnnum[aln_file].strip("b").strip("'"))-1
#    e_val_key=["hhb-cov60.aln","jhm-1e-20.aln","jhm-1e-10.aln","jhm-1e-4.aln","jhm-1e-3.aln","jhm-e-0.aln"]
    e_val_key=["prot-1e-20.aln","prot-1e-10.aln","prot-1e-4.aln","prot-1e-3.aln","prot-e-0.aln"]
    keep_file=""
    for i in range(len(e_val_key)):
        if (e_val_key[i] not in alnnum.keys()): continue
        if alnnum[e_val_key[i]] >= 5 * L:
            keep_file=e_val_key[i]
            shutil.copy2(outputfolder+e_val_key[i],outputfolder+file+".aln")
            shutil.copy2(outputfolder+e_val_key[i].replace(".aln",".a3m"),outputfolder+file+".a3m")
            found.append(file+"\n")
            break
    if keep_file=="":
        keymax = max(alnnum, key=alnnum.get)
        if outputfolder+keymax==outputfolder+file+".aln":
            samefile.append(outputfolder+file+".aln\n")
            continue
#           os.system(outputfolder+file+".aln")
        shutil.copy2(outputfolder+keymax,outputfolder+file+".aln")
        shutil.copy2(outputfolder+keymax.replace(".aln",".a3m"),outputfolder+file+".a3m")
        
    os.remove(file+"_aln_list.txt")
#with open ("alignment_fixed.txt","w") as f:
#    f.writelines(found)
    
with open ("samealntempfilelist.txt","w") as ff:
    ff.writelines(samefile)
            



    
