#this script creates a file list from a directory of .atom or .pdb or .seq, etc files
#Usage: python makePDBList.py <foldername>
import os,sys

pdbfolder=sys.argv[1]

if (os.path.isdir(pdbfolder)):os.system("ls "+pdbfolder+" > temp.txt")

file_list=[]
with open ("temp.txt","r") as f:
    for line in f:
        print(line.strip())#file_list.append(line.strip().split("/")[-1][0:4])
"""
file_list_set=set(file_list)
file_list=list(file_list_set)
for file in file_list:
    print(file)
"""
os.system("rm -f temp.txt")
#print (len(file_list))
