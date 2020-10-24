#this script reads the Y-Labels and converts it to contact map in the rr format. 
#usage: python Label2cmap.py <Label_file> <cmap_file>
import os, sys
import numpy as np


def toCmap(arr):
    l=arr.shape[0]
    #print (l)
    cmap=[]
    for i in range(l):
        for j in range(l):
            if arr[i][j]==1:
                cmap.append(str(i+1)+" "+str(j+1)+" 0 6.0 1\n")
    cmap[-1]=cmap[-1].rstrip()
    return cmap

label_file=os.path.abspath(sys.argv[1])
cmap_file=os.path.abspath(sys.argv[2])

y=np.loadtxt(label_file)
#print (y.shape)
cmap=toCmap(y)
#print (cmap)
with open (cmap_file,"w") as f:
    f.writelines(cmap)    
