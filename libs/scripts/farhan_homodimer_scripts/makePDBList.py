#this script creates a pdb name list from a directory of .atom or .pdb or .seq, etc files
#Usage: python makePDBList.py <foldername> <start_position> <num_of_chars> 
import os,sys

pdbfolder=sys.argv[1]
start=int(sys.argv[2])
char_num=int(sys.argv[3])
if (os.path.isdir(pdbfolder)):os.system("ls "+pdbfolder+" > temp.txt")

file_list=[]
with open ("temp.txt","r") as f:
    for line in f:
#        file_list.append(line.strip().split("/")[-1][0:4])
        file_list.append(line.strip().split("/")[-1][start:start+char_num])


file_list_set=set(file_list)
file_list=list(file_list_set)
for file in file_list:
    print(file)
os.system("rm -f temp.txt")
#print (len(file_list))
