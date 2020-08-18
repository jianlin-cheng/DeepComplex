#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 25 12:29:15 2019

@author: farhan
"""
#this script will do all the tasks sequentially to perform interchain analysis
#1. inputs are oiligomer.pdb, oligomer.fasta, monomer.dncon2.rr(intra_chain)
#2. Create monomer fasta from oligomer fasta (Need for dncon2 not now)
#3. Remove alternates using removeAlternatesFromPDB.py on oligomer.pdb
#4. Use splitpdb2chains.py to extract the chains from oiligomer.pdb > chain_A.pdb
#5. Use perform_chain_interaction.py on to get the interchain contacts
#6. Select file with highest number of contacts
#7. Use pdb2distancemonomer.py on chain_A.pdb to get true_intrachain contacts > monomer_intra_chain_native.txt
#8. Use mapfasta2pdb.py to obtain corrected fasta and mapping function.
#9. Use mapping function to translate the dncon2.rr
#10. Plot graphs for intra, inter and dncon2.rr and output intrachain precision
#11. Use getPrecision.py to get interchain precision
#

import os,sys
import subprocess

def getCBFromPDB(pdbfile):
    #print(atom_list[0])
    #print(len(atom_list))
    #sys.exit()
    atom_list =[]
    with open (pdbfile,"r") as f:
        for line in f:
            if (line.startswith("ATOM")): atom_list.append(line)
        
    new_list=[]
    #print(atom_list)
    prev_res=""
    for tupl in atom_list:
        #print(type(tup))
        tup=tupl.split()
        res=tup[5]
        if (tup[3]=="GLY" and tup[2]=="CA"):
            new_list.append(tupl)
            prev_res=res
            #print(tup[3]+tup[2])
            continue
        else:
            if (tup[2]=="CA"):
                keep=tupl
        #introduce a try patch here for missing CB
        if (tup[2]=="CB"):
            new_list.append(tupl)
            #print(tup[3]+tup[2])
            
        
    
    return new_list

#module1: Read the pdb (CB coordinates of chain X) Returns a dictionary or list
def readPDB(pdbfile):
    chain_dict={}
    with open (pdbfile) as f:
        prev_chain=""
        atom_num=0
        atom_list=[]
        fasta_res_num=0 #ignore this
        #count=0
        for line in f:
            #residue_list=[]
            #prev_residue=""
            #prev_carbon_atom=""
            #prev_res_num=-1
            if (line.startswith("ATOM")):
                #count+=1
                atom_num+=1
                fasta_res_num+=1
                line=line.strip()
                split=line.split()
                chain=split[4].strip()
                #print(atom_num)
                if (atom_num==0):
                    prev_chain=chain
                else:
                    if (prev_chain!=chain):
                        chain_dict[prev_chain]=atom_list
                        #print(len(atom_list))
                        #print(len(atom_list))
                        atom_list=[]
                        prev_chain=chain
                        fasta_res_num=1
                #if (count!=int(split[1])): 
                #    with open ("lost.txt","a") as f:
                #        f.write(split[1]+"\n")
                a_num=int(split[1])
                atom=split[2].strip()
                residue=split[3].strip()
                res_num=int(split[5].strip())
                x=float(split[6].strip())
                y=float(split[7].strip())
                z=float(split[8].strip())
                #atom_list.append([chain,atom_num,atom,residue,res_num,x,y,z,fasta_res_num])
                atom_list.append([chain,a_num,atom,residue,res_num,x,y,z,fasta_res_num])
            else:
                continue
    chain_dict[prev_chain]=atom_list
    
    return chain_dict

def getHighestContacts():
    os.system("ls "+temp_dir+interchain+"*.txt > "+temp_dir+"interlist.lst")
    file_list=[]
    
    with open (temp_dir+"interlist.lst","r") as f:
        for line in f:
            file_list.append(line.strip())
    l=0
    best=""
    for file in file_list:
        
        if (not os.path.exists(file)): 
            print (file+ " not found")
            continue
        lnnum = subprocess.check_output("wc -l < "+file,shell = True)
        lnnum = lnnum.rstrip()
        lnnum = str(lnnum)
        lnnum = int(lnnum.strip("b").strip("'"))-1
        
        if (lnnum > l):
            best=file
            
            l=lnnum
        #print(best)
            
    #print(best)
    return best

def getHighestAtoms():
    #os.system("ls "+temp_dir+pdb_mod+"*.pdb > "+temp_dir+"interlist.lst")
    file_list=[]
    
    with open (temp_dir+"chain_list.lst","r") as f:
        for line in f:
            file_list.append(line.strip())
    l=0
    best=""
    for file in file_list:
        
        if (not os.path.exists(file)): 
            print (file+ " not found")
            continue
        #lnnum = subprocess.check_output("wc -l < "+file,shell = True)
        #lnnum = lnnum.rstrip()
        #lnnum = str(lnnum)
        #lnnum = int(lnnum.strip("b").strip("'"))-1
        lnnum=len(getCBFromPDB(file))
        #print(lnnum)
        if (lnnum > l):
            best=file
            
            l=lnnum
        #print(best)
            
    #print(best)
    return best
"""
pdb="/data/farhan/SoftwareTools/HomopolymerProject/data/4zuk/multimer/4zuk.pdb"
fasta="/data/farhan/SoftwareTools/HomopolymerProject/data/4zuk/multimer/4zuk.fasta"
pred_rr="/data/farhan/SoftwareTools/HomopolymerProject/data/4zuk/monomer/4zuk.dncon2.rr"
outdir="/data/farhan/SoftwareTools/HomopolymerProject/working_scripts/4zuk_sample/"
"""
"""
pdb="/data/farhan/SoftwareTools/HomopolymerProject/data/halfmann_list/works/pdb/oligomer/3J6J.pdb"
fasta="/data/farhan/SoftwareTools/HomopolymerProject/data/halfmann_list/works/fastas/oligomers/3J6J.fasta"
pred_rr="/data/farhan/SoftwareTools/HomopolymerProject/data/halfmann_list/works/runlogs/dncon2_out/3J6J_monomer/3J6J_monomer.dncon2.rr"
outdir="/data/farhan/SoftwareTools/HomopolymerProject/working_scripts/3J6J_out/"
"""
"""
pdb="/data/farhan/SoftwareTools/HomopolymerProject/data/halfmann_list/works/pdb/oligomer/5FNA.pdb"
fasta="/data/farhan/SoftwareTools/HomopolymerProject/data/halfmann_list/works/fastas/oligomers/5FNA.fasta"
pred_rr="/data/farhan/SoftwareTools/HomopolymerProject/data/halfmann_list/works/runlogs/dncon2_out/5FNA_monomer/5FNA_monomer.dncon2.rr"
outdir="/data/farhan/SoftwareTools/HomopolymerProject/working_scripts/5FNA_out/"
"""

pdb="/data/farhan/SoftwareTools/HomopolymerProject/data/halfmann_list/nw/pdb/oligomer/2HM2.pdb"
fasta="/data/farhan/SoftwareTools/HomopolymerProject/data/halfmann_list/nw/fastas/oligomers/2HM2.fasta"
pred_rr="/data/farhan/SoftwareTools/HomopolymerProject/data/halfmann_list/nw/runlogs/dncon2_out/2HM2_monomer/2HM2_monomer.dncon2.rr"
outdir="/data/farhan/SoftwareTools/HomopolymerProject/working_scripts/2HM2_out/"

if (not outdir.endswith("/")): outdir+="/"

if (not os.path.isdir(outdir)):
    os.mkdir(outdir)
else:
    os.system("rm -rf "+outdir)
#####copy everything into a working temp directory
temp_dir=outdir+"temp/"
if (os.path.exists(temp_dir)): os.system("rm -rf "+temp_dir)
os.mkdir(temp_dir)
os.system("cp "+pdb+" "+temp_dir)
os.system("cp "+fasta+" "+temp_dir)
os.system("cp "+pred_rr+" "+temp_dir)
#os.system("cp "+pdb+" "+temp_dir)
pdb=pdb.split("/")[len(pdb.split("/"))-1]
fasta=fasta.split("/")[len(fasta.split("/"))-1]
pred_rr=pred_rr.split("/")[len(pred_rr.split("/"))-1]

os.system("python removeAlternatesFromPDB.py "+temp_dir+pdb+ " "+temp_dir+pdb.replace(".pdb","_mod.pdb"))
pdb_mod=pdb.replace(".pdb","_mod.pdb")

os.system("python getMonomerFasta.py "+temp_dir+fasta)
monomer_fasta=fasta.replace(".fasta","_monomer.fasta")

os.system("python splitpdb2chains.py "+temp_dir+pdb_mod+" > "+temp_dir+"chain_list.lst")
chainA=getHighestAtoms()
split=chainA.replace(".pdb","").split("_")
chain=split[len(split)-1]
print(chain)
#select chain that has highest atoms


#os.system("python perform_intrachain_interactions.py "+chainA+" A A 8 "+chainA.replace(".pdb","")+"_intrachain")
os.system("python perform_intrachain_interactions.py "+chainA+" "+chain+" "+chain+" 8 "+chainA.replace(".pdb","")+"_intrachain")
intrachain=chainA.replace(".pdb","")+"_intrachain_"+chain+chain+".txt"

#print("python perform_chain_interactions.py "+temp_dir+pdb_mod+" 8 "+temp_dir+pdb_mod.replace(".pdb","_interchain")+" "+temp_dir+fasta)
#sys.exit()

os.system("python perform_chain_interactions.py "+temp_dir+pdb_mod+" 8 "+temp_dir+pdb_mod.replace(".pdb","_interchain")+" "+temp_dir+monomer_fasta+ " "+chain)
interchain=pdb_mod.replace(".pdb","_interchain_dist")



#TODO: Put mapping function here. 

#select interchain interactions with highest contacts
high_cont=getHighestContacts()
#print("python getPrecision.py inter "+high_cont+" "+temp_dir+pred_rr+" "+temp_dir+intrachain)
os.system("python getPrecision.py inter "+high_cont+" "+temp_dir+pred_rr+" "+intrachain)

#works


#visualization script


