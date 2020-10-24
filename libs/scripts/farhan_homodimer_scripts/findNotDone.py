#this script will read the two list files and find what has not been done
#usage: python FindNotDone.py <list_file1.txt> <list_file2.txt>

import os,sys

def readFile(file):
    file_list=[]
    with open (file,"r") as f:
        for line in f:
            file_list.append(line.strip())
    return file_list

file1=sys.argv[1]
file2=sys.argv[2]

if (os.path.isdir(file1)): 
    os.system("python makePDBList.py "+file1+"> list_file1.txt")
    file1="list_file1.txt"

if (os.path.isdir(file2)): 
    os.system("python makePDBList.py "+file2+"> list_file2.txt")
    file1="list_file2.txt"

file_list_1=readFile(file1)
file_list_2=readFile(file2)

file_list_1=set(file_list_1)
file_list_2=set(file_list_2)

if (len(file_list_1)>=len(file_list_2)): remaining=file_list_1-file_list_2
if (len(file_list_2)>=len(file_list_1)): remaining=file_list_2-file_list_1

remaining=list(remaining)

for item in remaining:
    print (remaining)