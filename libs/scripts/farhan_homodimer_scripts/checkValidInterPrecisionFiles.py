#this script checks the ./precisions/inter/ folder and sees if there are 14 lines in it

#usage: python checkValidInterPrecisionFiles.py <interprecisionfolder or listfile.txt>

import os, sys

def readFile(file):
    file_list=[]
    with open (file,"r") as f:
        for line in f:
            file_list.append(line.strip())
    return file_list

file=sys.argv[1]


if (os.path.isdir(file)): 
    os.system("ls "+file+"> temp_list_file.txt")
    file="temp_list_file.txt"

file_list=readFile(file)

for file in file_list:
    #print (file)
    #break
    line_list=[]
    with open (sys.argv[1]+file,"r") as f:
        for line in f:
            line_list.append(line.strip())
        
    if (len(line_list)==14): os.system("echo "+file+" >> valid_inter_precision_list.txt")
    if (len(line_list)!=14): os.system("echo "+file+" >> invalid_inter_precision_list.txt")
    

if (os.path.exists("temp_list_file.txt")):os.system("rm -f temp_list_file.txt")