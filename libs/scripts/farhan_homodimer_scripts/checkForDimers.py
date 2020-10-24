#checks to see if .atom files for each pdb is a dimer. selects the dimers only and moves to desired directory
#usage: python checker.py <pdb_list> <>
import os

pdb_list_file="pdb_list.lst"
pdb_list=[]
atom_list_file="check_atom_list_file.txt"

atomfolder="/data/farhan/SoftwareTools/HomopolymerProject/data/homodimers/homodimers_files/work_dir/atom/"
outfolder_atom="/data/farhan/SoftwareTools/HomopolymerProject/data/homodimers/homodimers_files/outfolder/atom/"

with open (pdb_list_file,"r") as f:
    for line in f:
        line=line.split("/")[-1]
        pdb_list.append(line.strip().replace(".pdb",""))

#print (len(pdb_list))
#os.system("ls "+atomfolder+pdb_list[0]+"* >> /dev/null")

#print (pdb_list[100])
#if (os.system("ls "+atomfolder+pdb_list[0]+"*")==0): 
#    print ("lslslslsls")
not_present_list=[]
present_list=[]
for i in range(len(pdb_list)):
    atom_list=[]
    if (os.system("ls "+atomfolder+pdb_list[i]+"* >> /dev/null")==0):
        os.system("ls "+atomfolder+pdb_list[i]+"* > "+atom_list_file)
        
        with open (atom_list_file,"r") as f:
            for line in f:
                atom_list.append(line)
        if (len(atom_list)!=2):
            #print(pdb_list[i])
            print(atom_list)
            not_present_list.append(pdb_list[i])
            continue
        present_list.append(pdb_list[i])
    else:
        print (pdb_list[i])
        not_present_list.append(pdb_list[i])
 
print (len(pdb_list))
print (len(present_list))
print (len(not_present_list))
true_pdb_list=[]
for pdb in present_list:
    if ((os.system("mv "+atomfolder+pdb+"*.atom "+outfolder_atom))==0):
        true_pdb_list.append(pdb+".pdb\n")

with open ("true_pdb_list.txt","w") as f:
    f.writelines(true_pdb_list)
with open ("not_present_pdb_list.txt","w") as f:
    for pdb in not_present_list:
        f.write(pdb+".pdb\n")
