#this script reads the Y-Labels and converts it to contact map in the rr format. 
#usage: python Label2cmap.py <Label_file> <cmap_file> <fasta_file>
import os, sys
import numpy as np
#import subprocess

def toCmap(arr,fasta):
    l=arr.shape[0]
    if l!=len(fasta): sys.exit("Fasta lengths do not match with label file length!")
    print ("Shape[0]=",l)
    cmap=[]
    for i in range(l):
        for j in range(l):
            if arr[i][j]!=0:
                cmap.append(str(i+1)+" "+str(j+1)+" 0 6.0 "+str(arr[i][j])+"\n")
    cmap[-1]=cmap[-1].rstrip()
    cmap.insert(0,fasta.strip()+"\n")
    cmap[-1]=cmap[-1].strip()
    return cmap

label_file=os.path.abspath(sys.argv[1])
cmap_file=os.path.abspath(sys.argv[2])
fasta_file=os.path.abspath(sys.argv[3])
if (not os.path.exists(label_file)): print ("Label file: "+label_file+" not found!")
if (not os.path.exists(fasta_file)): sys.exit("Fasta file: "+fasta_file+" not found!")
print ("Reading Fasta file: "+fasta_file)
print ("Loading Label file: "+label_file)
print ("Writing cmap file: "+cmap_file)
y=np.loadtxt(label_file)
fasta=""
with open (fasta_file,"r") as f:
    for line in f:
        if line.startswith(">"): continue
        fasta+=line.strip()
#print (y.shape)
cmap=toCmap(y,fasta)
#print (cmap)
with open (cmap_file,"w") as f:
    f.writelines(cmap)    
