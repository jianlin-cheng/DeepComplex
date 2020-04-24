#this script will create the labels from the list of interchain.rr files
#usage: python createLabels.py <folder or list_file>

import os, sys
import numpy as np
from readRR import readRRFile
fl=sys.argv[1]
outfolder=sys.argv[2]
folder="./interchains/"
if (os.path.isdir(fl)):
    os.system("python makePDBList.py "+fl+" > for_label_list.txt")
    folder=fl
    fl="for_label_list.txt"

if not(folder.endswith("/")): folder+="/"
if not(outfolder.endswith("/")): outfolder+="/"

if not(os.path.exists(fl)): sys.exit("List file "+fl+" not found!")

if not(os.path.isdir(outfolder)): os.mkdir(outfolder)

pdb_list=[]
with open (fl,"r") as f:
    for line in f:
        pdb_list.append(line.strip())
        

for pdb in pdb_list:
    os.system("ls "+folder+pdb+"*.rr > temp_rr_list_4_label.txt")
    with open ("temp_rr_list_4_label.txt","r") as f:
        for line in f:
            pdb=line.split("/")[-1].strip()[0:7]
            break
    print (pdb)
    fasta,rr_contents=readRRFile(folder+pdb+".rr")
    L=len(fasta)
    mat=np.zeros((L,L),dtype=np.int8)
    for rr_line in rr_contents:
        i=int(rr_line.split()[0])-1
        j=int(rr_line.split()[1])-1
        mat[i][j]=1
    np.savetxt(outfolder+"Y-"+pdb[0:4]+".txt",mat,delimiter=" ",fmt="%i")
os.remove("temp_rr_list_4_label.txt")
#print (type(mat[0][0]))
#print (mat[0][0])
    
        

