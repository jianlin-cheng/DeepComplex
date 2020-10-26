#this script creates a pdb name list from a directory that are not processed from the pdb_list
#Usage: python getNotDone.py <pdb_foldername> <pdb_list_file>
import os,sys

pdbfolder=sys.argv[1]
pdb_list_file=sys.argv[2]
pdb_list=[]

if not(os.path.isdir(pdbfolder)): sys.exit(pdbfolder+" not found!")
if not(pdbfolder.endswith("/")): pdbfolder+="/"

with open (pdb_list_file,"r") as f:
    for line in f:
        pdb_list.append(line.strip())

done_list=[]
not_found_list=[]
for pdb_name in pdb_list:
    exitcode=os.system("ls "+pdbfolder+pdb_name+"* > temp.txt")
    if (exitcode!=0): 
        not_found_list.append(pdb_name+"\n")
        continue
    file_list=[]
    #print (pdb_name)
    #break
    with open ("temp.txt","r") as f:
        for line in f:
            #print ("Here............"+line)
            #sys.exit()
            file_list.append(line.strip().split("/")[-1][0:4])
            #print (line)
    if len(file_list)!=0: done_list.append(pdb_name+"\n")
    #break
            
    
    
    
file_list_set=set(file_list)
file_list=list(file_list_set)

with open ("done_list_2.txt","w") as f:
    f.writelines(done_list)

with open ("not_done_list_2.txt","w") as f:
    f.writelines(not_found_list)

#print (len(not_found_list))
#print (len(done_list))
#for file in file_list:
#    print(file)

#print (len(pdb_list))
