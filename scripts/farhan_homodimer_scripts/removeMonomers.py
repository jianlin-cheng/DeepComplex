import os,sys

#pdb_list_file=os.path.abspath(sys.argv[1])
folder=os.path.abspath(sys.argv[1])+"/"
abspath=os.path.dirname((os.path.abspath(sys.argv[0])))+"/"
os.system("python "+abspath+"makePDBList.py "+folder+" 0 4 > "+abspath+"temp_pdb_list.txt")
f=open(abspath+"temp_pdb_list.txt")
pdb_list=f.readlines()
f.close()

#print (len())
#sys.exit()
#for pdb_name in pdb_list:
#    os.system("ls "+folder+pdb_name.strip()+"*.atom > "+abspath+pdb_name+"_temp_atom_list.txt")
    


import concurrent.futures
import os
import sys
import time

start_time = time.time()

#flist=open("atom_file_list.txt")
#file_list=flist.readlines()
#flist.close()
for i in range(len(pdb_list)):
    pdb_list[i]=pdb_list[i].strip()
print("Total files:",len(pdb_list))
#print(infolder)
#print(outfolder)
#sys.exit()
def removeMonomers(pdb_name):
#for pdb_name in pdb_list:
    os.system("ls "+folder+pdb_name.strip()+"*.atom > "+abspath+pdb_name.strip()+"_temp_atom_list.txt")
    f=open(abspath+pdb_name+"_temp_atom_list.txt")
    atom_list=f.readlines()
    f.close()
    if (len(atom_list)==1):os.system("rm -f "+folder+pdb_name.strip()+"*.atom")

    os.system("rm -f "+abspath+pdb_name.strip()+"_temp_atom_list.txt")
    #exit_code=os.system("python checknRemoveBlanks.py "+infolder+" "+outfolder)
    #string="python checknRemoveBlanks.py "+file+" "+outfolder
    #os.system(string)
    
    return

with concurrent.futures.ProcessPoolExecutor() as executor:
    #for file in file_list):
    _result=executor.map(removeMonomers,pdb_list)


