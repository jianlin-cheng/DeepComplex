#this scripts calls the update_database.pl script to perform a clean up

#usage:
#python cleanUpPDB.py option.txt

import os,sys,subprocess
from readPDBColumns import readPDB,readAtom,write2File,contents2Info,addColumn,reassembleLines,getChain
import pandas as pd

def getName(file):
    split=file.split("/")
    file=split[len(split)-1].replace(".pdb","")
    file=file.replace(".atom","")
    file=file.replace(".seq","")
    return file


def removeBlankFiles(pdb_list):
    for pdb in pdb_list:
        pdb=getName(pdb)
        if (os.path.exists(atomfolder+pdb+".atom")):
            print("Removing blank files: "+atomfolder+pdb+".atom")
            os.system("rm -f "+atomfolder+pdb+".atom")
    return

option_file=sys.argv[1]
#outfolder=sys.argv[2]
#run clean up to generate .seq, .atom and .dssp files
"""
update_dataset="/data/farhan/SoftwareTools/multicom/src/prosys/script/update_dataset.pl "
os.system("perl "+update_dataset+option_file)

os.system("rm *.dssp")
os.system("rm *.tmp")
"""
#take the files and then generate seperate .pdb files by adding the chain info
#outfolder="/data/farhan/SoftwareTools/HomopolymerProject/working_scripts/pdb_folder_test/outfolder/"
#atomfolder="/data/farhan/SoftwareTools/HomopolymerProject/working_scripts/pdb_folder_test/work_dir/atom/"
#pdbfolder="/data/farhan/SoftwareTools/HomopolymerProject/working_scripts/pdb_folder_test/work_dir/pdb/"
#seqfolder="/data/farhan/SoftwareTools/HomopolymerProject/working_scripts/pdb_folder_test/work_dir/seq/"

outfolder="/data/farhan/SoftwareTools/HomopolymerProject/data/homodimers/homodimers_files/outfolder/"
atomfolder="/data/farhan/SoftwareTools/HomopolymerProject/data/homodimers/homodimers_files/work_dir/atom/"
pdbfolder="/data/farhan/SoftwareTools/HomopolymerProject/data/homodimers/homodimers_files/work_dir/pdb/"
seqfolder="/data/farhan/SoftwareTools/HomopolymerProject/data/homodimers/homodimers_files/work_dir/seq/"


os.system("ls "+pdbfolder+"*.pdb > pdb_list.lst")
pdb_list=[]
with open ("pdb_list.lst","r") as f:
    for line in f:
        pdb_list.append(line.strip())
#print (pdb_list)

if (not os.path.exists(outfolder)): os.mkdir(outfolder)
if (not os.path.exists(outfolder+"pdb")): os.mkdir(outfolder+"pdb")
if (not os.path.exists(outfolder+"pdb_whole")): os.mkdir(outfolder+"pdb_whole")
if (not os.path.exists(outfolder+"fastas")): os.mkdir(outfolder+"fastas")

removeBlankFiles(pdb_list)

#1. make pdb with chains from .atom files
updated_pdb_list=[]
for pdb in pdb_list:
    pdb_name=getName(pdb).upper()
    #print("@#@#@#"+pdb_name)
    if (os.path.exists(atomfolder+pdb_name+".atom")): os.system("rm "+atomfolder+pdb_name+".atom")
    if not (os.system("ls "+atomfolder+pdb_name+"*.atom > atom_list.lst")==0): continue
    #check if file is blank
    lnnum = subprocess.check_output("wc -l < atom_list.lst",shell = True)
    lnnum = lnnum.rstrip()
    lnnum = str(lnnum)
    lnnum = int(lnnum.strip("b").strip("'"))-1
    if (lnnum==0):continue
    updated_pdb_list.append(pdb+"\n") #the proper .atom files selected
    atom_file_list=[]
    with open ("atom_list.lst","r") as f:
        for line in f:
            atom_file=line.strip()
            atom_file_name=getName(atom_file)
            chain=atom_file_name.replace(pdb_name,"")
            contents=readAtom(atom_file)
            split_contents=contents2Info(contents)
            split_contents = addColumn(split_contents,"chain",getChain(line.strip()))
            #writedf2File("/data/farhan/SoftwareTools/HomopolymerProject/working_scripts/pdb_folder_test/work_dir/atom/6BZEA.txt",df2)
            write2File(outfolder+"pdb/"+atom_file_name+".pdb",reassembleLines(split_contents))
            atom_file_list.append(outfolder+"pdb/"+atom_file_name+".pdb")
            #writedf2File(outfolder+pdb_name+"_chain_"+chain+".pdb",df2)
            #print(chain)
    if (len(atom_file_list)==0): 
        print ("#############Zero!!!!!")
        print (atom_file_list)
        continue#print ("#############Zero!!!!!")
    super_list=[]
    for atm_file in atom_file_list:
        with open (atm_file,"r")as f:
            for line in f:
                if not line.endswith("\n"): line+="\n"
                super_list.append(line)
    super_list[len(super_list)-1]=super_list[len(super_list)-1].strip()
    with open (outfolder+"pdb_whole/"+pdb_name+".pdb","w") as f:
        f.writelines(super_list)
    
#os.remove("atom_list.lst")

#2. make fasta files from the .seq files
pdb_list=updated_pdb_list
updated_pdb_list=[]
for pdb in pdb_list:
    pdb_name=getName(pdb).upper()
    #print("@#@#@#"+pdb_name)
    if not (os.system("ls "+seqfolder+pdb_name+"*.seq > seq_list.lst")==0): continue
    lnnum = subprocess.check_output("wc -l < seq_list.lst",shell = True)
    lnnum = lnnum.rstrip()
    lnnum = str(lnnum)
    lnnum = int(lnnum.strip("b").strip("'"))-1
    if (lnnum==0):continue

    seq_file_list=[]
    L=0
    fasta=""
    best_name=""
    all_seqs_of_this_pdb=[]
    with open ("seq_list.lst","r") as f:
        for line in f:
            seq_file=line.strip()
            seq_file_name=getName(seq_file)
            chain=seq_file_name.replace(pdb_name,"")
            contents=[]
            
            with open (seq_file,"r") as f:
                for line in f:
                    contents.append(line.strip().replace(" ",""))
            #Add code to filter out pdbs whose fasta sequences do not match
            #if fasta sequences dont match: break out

            if (contents[4]!=fasta): #compare the fasta length of all .seq files and take the max one
                l1=len(contents[4])
                l2=len(fasta)
                if (l1>l2): 
                    fasta=contents[4]
                    L=int(contents[3])
                    seq_file_list=[]
                    seq_file_list.append(outfolder+"fastas/"+pdb_name+".fasta")
                    seq_file_list.append(">"+pdb_name+", Chain: "+chain+", Length: "+str(L)+"\n")
                    seq_file_list.append(fasta)

    if (len(seq_file_list)==0): 
        print ("#############Zero!!!!!")
        print (atom_file_list)
        continue#print ("#############Zero!!!!!")
    with open (seq_file_list[0],"w") as f:
        f.write(seq_file_list[1])
        f.write(seq_file_list[2])
with open ("updated_pdb_list.lst","w") as f:
    f.writelines(updated_pdb_list)
#os.system("rm *.tmp")
#os.system("rm *.dssp")


#if we want we can join the pdbs to one pdb



#os.system("rm "+pdb+"*.tmp ")
