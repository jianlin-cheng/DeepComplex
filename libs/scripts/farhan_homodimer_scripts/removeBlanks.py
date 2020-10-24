import os,sys

infolder=os.path.abspath(sys.argv[1])
outfolder=os.path.abspath(sys.argv[2])

if not os.path.isdir(outfolder): os.makedirs(outfolder)

os.system("ls "+infolder+" > atom_file_list.txt")

import concurrent.futures
import os
import sys
import time

start_time = time.time()

flist=open("atom_file_list.txt")
file_list=flist.readlines()
flist.close()
for i in range(len(file_list)):
    file_list[i]=infolder+"/"+file_list[i].strip()
print("Total files:",len(file_list))
#print(infolder)
#print(outfolder)
#sys.exit()
def checkBlankFiles(file):
    #exit_code=os.system("python checknRemoveBlanks.py "+infolder+" "+outfolder)
    string="python checknRemoveBlanks.py "+file+" "+outfolder
    os.system(string)
    return 

with concurrent.futures.ProcessPoolExecutor() as executor:
    #for file in file_list):
    _result=executor.map(checkBlankFiles,file_list)
        





