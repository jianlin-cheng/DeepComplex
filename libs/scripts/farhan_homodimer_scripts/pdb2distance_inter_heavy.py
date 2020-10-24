#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 17 13:28:19 2019

@author: farhan
"""

#this script creates a contact map text file for all atoms
#usage: python pdb2distance_inter_heavy.py <chainA.atom> <chainB.atom> <distance_threshold> <PDB_ID>

import os,sys
from readPDBColumns import readPDB,readAtom,write2File,contents2Info,addColumn,reassembleLines,getChain,getName
import numpy as np

def pdb2FastaFromSplitContents(split_contents):
    fst=""
    letters = {'ALA':'A','ARG':'R','ASN':'N','ASP':'D','CYS':'C','GLU':'E','GLN':'Q','GLY':'G','HIS':'H',
           'ILE':'I','LEU':'L','LYS':'K','MET':'M','PHE':'F','PRO':'P','SER':'S','THR':'T','TRP':'W',
           'TYR':'Y','VAL':'V'}
    prev_res_num=split_contents[0]["res_num"]
    fst+=letters[split_contents[0]["res_name"]]
    for items in split_contents:
        if (items["res_num"]==prev_res_num): continue
        fst+=letters[items["res_name"]]
        prev_res_num=items["res_num"]
    #fst+=letters[items["res_name"]]
    return fst
        
def getCoordinate(atom):
    coordinate={}
    coordinate["x"]=atom["x"]
    coordinate["y"]=atom["y"]
    coordinate["z"]=atom["z"]
    return coordinate

def distance(coord1, coord2):
    x1=float(coord1["x"])
    y1=float(coord1["y"])
    z1=float(coord1["z"])
    x2=float(coord2["x"])
    y2=float(coord2["y"])
    z2=float(coord2["z"])
    d=np.sqrt((x1-x2)**2+(y1-y2)**2+(z1-z2)**2)
    
    return d

def createDistanceMapAllAtoms(atom_list_A,atom_list_B,dist):
    result_list_string=[]
    
    for atom_A in atom_list_A:
        for atom_B in atom_list_B:
            string=""
            if (atom_A["chain"]==" " or atom_A["chain"]=="  " or atom_A["chain"]==""): atom_A["chain"]=chain_1
            if (atom_B["chain"]==" " or atom_B["chain"]=="  " or atom_B["chain"]==""): atom_B["chain"]=chain_2
            
            #if (atom_A["res_name"]=="GLY"):
            #    string+=atom_A["chain"]+" "+atom_A["serial"]+" "+atom_A["res_name"]+" "+atom_A["res_num"]+" "+atom_A["x"]+" "+atom_A["y"]+" "+atom_A["z"]+" "+atom_A["atom_name"]+" | "+ atom_B["atom_name"]+" "+atom_B["chain"]+" "+atom_B["serial"]+" "+atom_B["res_name"]+" "+atom_B["res_num"]+" "+atom_B["x"]+" "+atom_B["y"]+" "+atom_B["z"]+" | " + str(distance(getCoordinate(atom_A),getCoordinate(atom_B)))
            #    pass
            #if (atom_B["res_name"]=="GLY"):
            #    pass
            string+=atom_A["chain"]+" "+atom_A["serial"]+" "+atom_A["res_name"]+" "+atom_A["res_num"]+" "+atom_A["x"]+" "+atom_A["y"]+" "+atom_A["z"]+" "+atom_A["atom_name"]+" | "+ atom_B["atom_name"]+" "+atom_B["chain"]+" "+atom_B["serial"]+" "+atom_B["res_name"]+" "+atom_B["res_num"]+" "+atom_B["x"]+" "+atom_B["y"]+" "+atom_B["z"]+" | " + str(distance(getCoordinate(atom_A),getCoordinate(atom_B)))
            
                
            if (distance(getCoordinate(atom_A),getCoordinate(atom_B))<dist): result_list_string.append(string+"\n")
            #result_list_string.append(string+"\n")
    
    return result_list_string

def removeRedundantContacts(contact_list):
    new_list=[]
    contact_dict={}
    for contact in contact_list:
        x_y=contact.split()[0]+" "+contact.split()[1]
        contact_dict[x_y]=contact
    #contact_dict=dict(set(contact_dict))
    for key in contact_dict.keys():
        new_list.append(contact_dict[key])
    """
    prev_contact=contact_list[0]
    for contact in contact_list:
        prev_contact_vals=prev_contact.split()[0]+" "+prev_contact.split()[1]
        if (contact.startswith(prev_contact_vals)): #if contact matches move to next
            continue
            #pass
        else: #if it does not match then add previous to the list
            new_list.append(prev_contact)
            prev_contact=contact
            #pass
    """
    #new_list.append(prev_contact) #add the last value
    return new_list
"""
def createDistanceMapHeavyAtoms(atom_list_A,atom_list_B,dist=5.0):
    result_list_string=[]
    distance_list_string=[]
    rr_list_string=[]
    for atom_A in atom_list_A:
        for atom_B in atom_list_B:
            string=""
            if (atom_A["chain"]==" " or atom_A["chain"]=="  " or atom_A["chain"]==""): atom_A["chain"]=chain_1
            if (atom_B["chain"]==" " or atom_B["chain"]=="  " or atom_B["chain"]==""): atom_B["chain"]=chain_2
            
            #if (atom_A["res_name"]=="GLY"):
            #    string+=atom_A["chain"]+" "+atom_A["serial"]+" "+atom_A["res_name"]+" "+atom_A["res_num"]+" "+atom_A["x"]+" "+atom_A["y"]+" "+atom_A["z"]+" "+atom_A["atom_name"]+" | "+ atom_B["atom_name"]+" "+atom_B["chain"]+" "+atom_B["serial"]+" "+atom_B["res_name"]+" "+atom_B["res_num"]+" "+atom_B["x"]+" "+atom_B["y"]+" "+atom_B["z"]+" | " + str(distance(getCoordinate(atom_A),getCoordinate(atom_B)))
            #    pass
            #if (atom_B["res_name"]=="GLY"):
            #    pass
            string=atom_A["chain"]+" "+atom_A["serial"]+" "+atom_A["res_name"]+" "+atom_A["res_num"]+" "+atom_A["x"]+" "+atom_A["y"]+" "+atom_A["z"]+" "+atom_A["atom_name"]+" | "+ atom_B["atom_name"]+" "+atom_B["chain"]+" "+atom_B["serial"]+" "+atom_B["res_name"]+" "+atom_B["res_num"]+" "+atom_B["x"]+" "+atom_B["y"]+" "+atom_B["z"]+" | " + str(distance(getCoordinate(atom_A),getCoordinate(atom_B)))
            if (atom_A["atom_name"].strip()=="N" or atom_A["atom_name"].strip()=="CA" or atom_A["atom_name"].strip()=="C" or atom_A["atom_name"].strip()=="O"):
                if (atom_B["atom_name"].strip()=="N" or atom_B["atom_name"].strip()=="CA" or atom_B["atom_name"].strip()=="C" or atom_B["atom_name"].strip()=="O"):
                    if (distance(getCoordinate(atom_A),getCoordinate(atom_B))<=dist): 
                        distance_string=atom_A["res_num"].strip()+" "+atom_B["res_num"].strip()+" 0 8 "+ str(distance(getCoordinate(atom_A),getCoordinate(atom_B)))
                        rr_string=atom_A["res_num"].strip()+" "+atom_B["res_num"].strip()+" 0 8 "+ str(0.5+1/(distance(getCoordinate(atom_A),getCoordinate(atom_B))))
                        result_list_string.append(string+"\n")
                        distance_list_string.append(distance_string+"\n")
                        rr_list_string.append(rr_string+"\n")
#            string=""            
            #result_list_string.append(string+"\n")
    distance_list_string=removeRedundantContacts(distance_list_string)
    rr_list_string=removeRedundantContacts(rr_list_string)
    return result_list_string,distance_list_string,rr_list_string
"""

def createDistanceMapHeavyAtoms(atom_list_A,atom_list_B,dist=6.0): #new version. Chose all atoms but the hydrogens
    result_list_string=[]
    distance_list_string=[]
    rr_list_string=[]
    for atom_A in atom_list_A:
        for atom_B in atom_list_B:
            string=""
            if (atom_A["chain"]==" " or atom_A["chain"]=="  " or atom_A["chain"]==""): atom_A["chain"]=chain_1
            if (atom_B["chain"]==" " or atom_B["chain"]=="  " or atom_B["chain"]==""): atom_B["chain"]=chain_2
            
            #if (atom_A["res_name"]=="GLY"):
            #    string+=atom_A["chain"]+" "+atom_A["serial"]+" "+atom_A["res_name"]+" "+atom_A["res_num"]+" "+atom_A["x"]+" "+atom_A["y"]+" "+atom_A["z"]+" "+atom_A["atom_name"]+" | "+ atom_B["atom_name"]+" "+atom_B["chain"]+" "+atom_B["serial"]+" "+atom_B["res_name"]+" "+atom_B["res_num"]+" "+atom_B["x"]+" "+atom_B["y"]+" "+atom_B["z"]+" | " + str(distance(getCoordinate(atom_A),getCoordinate(atom_B)))
            #    pass
            #if (atom_B["res_name"]=="GLY"):
            #    pass
            string=atom_A["chain"]+" "+atom_A["serial"]+" "+atom_A["res_name"]+" "+atom_A["res_num"]+" "+atom_A["x"]+" "+atom_A["y"]+" "+atom_A["z"]+" "+atom_A["atom_name"]+" | "+ atom_B["atom_name"]+" "+atom_B["chain"]+" "+atom_B["serial"]+" "+atom_B["res_name"]+" "+atom_B["res_num"]+" "+atom_B["x"]+" "+atom_B["y"]+" "+atom_B["z"]+" | " + str(distance(getCoordinate(atom_A),getCoordinate(atom_B)))
            if (atom_A["element"].strip()=="H" or atom_A["element"].strip()=="D"): continue
            if (atom_B["element"].strip()=="H" or atom_A["element"].strip()=="D"): continue
            if (distance(getCoordinate(atom_A),getCoordinate(atom_B))<=dist): 
                distance_string=atom_A["res_num"].strip()+" "+atom_B["res_num"].strip()+" 0 "+str(dist)+" "+ str(distance(getCoordinate(atom_A),getCoordinate(atom_B)))
                rr_string=atom_A["res_num"].strip()+" "+atom_B["res_num"].strip()+" 0 "+str(dist)+" "+ str(0.5+1/(distance(getCoordinate(atom_A),getCoordinate(atom_B))))
                result_list_string.append(string+"\n")
                distance_list_string.append(distance_string+"\n")
                rr_list_string.append(rr_string+"\n")
#            string=""            
            #result_list_string.append(string+"\n")
    distance_list_string=removeRedundantContacts(distance_list_string)
    rr_list_string=removeRedundantContacts(rr_list_string)
    return result_list_string,distance_list_string,rr_list_string

def writeToFile(outfile,stuff,fasta):
    with open (outfile,"w") as f:
        if (fasta.strip()!=""): f.write(fasta+"\n")
        f.writelines(stuff)
    return

def readFastaDict(fasta_dict_file="fasta_dictionary.txt"):
    fasta_dict={}
    if not (os.path.exists(fasta_dict_file)): 
        print(fasta_dict_file+" fasta dictionary file not found. Exiting")
        sys.exit(-6)
    with open (fasta_dict_file,"r") as f:
        for line in f:
            name=line.strip().split(":")[0].strip()
            fast=line.strip().split(":")[1].strip()
            fasta_dict[name]=fast
    return fasta_dict

def getFastaFromDictionary(pdbfile,fasta_dict):
    #fasta_dict=readFastaDict(fasta_dict_file)
    name=pdbfile.split("/")[-1][0:5]
    return fasta_dict[name]

#pdbfilename="/data/farhan/SoftwareTools/HomopolymerProject/data/pdb/5wvc.pdb"
atomfolder="/data/farhan/SoftwareTools/HomopolymerProject/data/homodimers/homodimers_files/outfolder/atom/"
#pdb=sys.argv[1]
#os.system("ls "+atomfolder+pdb+"* > atomfiles.txt")
#pdbfile_list=[]
"""
with open ("atomfiles.txt","r") as f:
    for line in f:
        pdbfile_list.append(line.strip())
#sys.exit()
os.system("rm -f atomfiles.txt")
"""
pdbfile_A=sys.argv[1]
pdbfile_B=sys.argv[2]

#chain_1=sys.argv[2]
#chain_2=sys.argv[3]
dist=sys.argv[3] 
outfile=sys.argv[4]
pdb=getName(pdbfile_A)

fasta_dict_file="fasta_dictionary.txt"
fasta_dict=readFastaDict(fasta_dict_file)

split_contents_A=contents2Info(readPDB(pdbfile_A))
split_contents_B=contents2Info(readPDB(pdbfile_B))
chain_1=getChain(pdbfile_A)
chain_2=getChain(pdbfile_B)


atom_list_A=split_contents_A
atom_list_B=split_contents_B
#Get fasta from fasta_dictionary.txt
#fasta_A=pdb2FastaFromSplitContents(atom_list_A)
fasta_A=getFastaFromDictionary(pdbfile_A,fasta_dict)
L_A=len(fasta_A)
#fasta_B=pdb2FastaFromSplitContents(atom_list_B)
fasta_B=getFastaFromDictionary(pdbfile_B,fasta_dict)
L_B=len(fasta_B)
###########################################################
#remark the following segment to allow calculations for mismatched fasta
###########################################################
"""
if (fasta_A != fasta_B):
    print (pdb+" : Fasta sequences of both files are not same...")
    os.system("echo "+pdb+" "+": Fasta sequences of both files are not same... >> not_done_reason_heavy.txt")
    #print ("Check!!!!!")
    print (fasta_A)
    print (fasta_B)
    sys.exit("-3")
"""
if (fasta_A=="" or fasta_B==""): 
    print("No fasta for "+pdb)
    os.system("echo '"+pdb+"' >> no_fasta.txt")
    sys.exit("No fasta found for "+pdb)
"""
for items in cb_list_A:
    if (items["serial"].strip()=="376"): print (items["z"]+" "+items["res_num"]+" "+items["res_name"])
    if (items["serial"].strip()=="367"): print (items["z"]+" "+items["res_num"]+" "+items["res_name"])
    if (items["serial"].strip()=="343"): print (items["z"]+" "+items["res_num"]+" "+items["res_name"])

for items in cb_list_B:
    if (items["serial"].strip()=="423"): print (items["z"]+" "+items["res_num"]+" "+items["res_name"])
    if (items["serial"].strip()=="429"): print (items["z"]+" "+items["res_num"]+" "+items["res_name"])
    if (items["serial"].strip()=="435"): print (items["z"]+" "+items["res_num"]+" "+items["res_name"])
3R31_dist_AB.rr_AB.rr
"""
#print (len(cb_list_A),len(cb_list_A))
#pw_dist_all=createDistanceMapAllAtoms(atom_list_A,atom_list_B,5.0)
#writeToFile("3R31_heavy.txt",pw_dist_all)
result_list,pw_dist,pw_rr=createDistanceMapHeavyAtoms(atom_list_A,atom_list_B,float(dist))
print (len(pw_dist),len(pw_rr), len(result_list))
if (len(pw_dist)==0):
    print (pdb+" "+": No interchain contacts less than "+dist+"...")
    os.system("echo "+pdb+" "+": No interchain contacts less than "+dist+" ... >> not_done_reason_heavy.txt")
    sys.exit("-2")
"""
ok_flag=False
for line in pw_dist:
    if ("GLY" in line):
        if ("CA  |  CA" in line or "CA  |  CB" in line or "CB  |  CA" in line): ok_flag=True
    else:
        if ("CB  |  CB" in line): ok_flag=True

if (not ok_flag):
    print (pdb+" : No CB-CB contacts found...")
    os.system("echo "+pdb+" "+": no CB-CB contacts found... >> not_done_reason_heavy.txt")
"""    
outfile_dist=outfile.replace(".txt","")+"_dist_"+chain_1+chain_2+".txt"
outfile=outfile+"_"+chain_1+chain_2+".txt"
#print(outfile_dist)
#outfile_dist=outfile+"_dist_"+chain_1+chain_2+".txt"
write_flag=True
if (L_B>L_A): fasta_A=fasta_B
if (write_flag):
    writeToFile(outfile_dist,pw_dist,fasta_A)
    writeToFile(outfile.replace(".txt",".rr"),pw_rr,fasta_A)
    #writeToFile(outfile.replace(".txt","_whole.txt"),result_list,"")

if not(os.path.exists(outfile_dist)):
    sys.exit("-4")



