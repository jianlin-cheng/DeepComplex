#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 21 14:47:28 2019

@author: farhan
"""
#this script is used to read a pdb file according to columns convention

import numpy as np
import pandas as pd
import os,sys

def getName(file):
    return file.split("/")[-1][0:4]

def readPDB(pdb):
    contents=[]
    with open (pdb,"r") as f:
        for line in f:
            #if (line.startswith("ATOM")):
            #    pass
            contents.append(line)
    return contents

def splitLine2Tuple(line):
    atom=line[0:6]
    serial=line[6:12]
    atom_name=line[12:16]
    alt_loc=line[16]
    res_name=line[17:20]
    chain=line[20:22]
    res_num=line[22:26]
    icode=line[26:30]
    x=line[30:38]
    y=line[38:46]
    z=line[46:54]
    occupancy=line[54:60]
    temp_fact=line[60:76]
    element=line[76:78]
    charge=line[78:80]
    
    return {"atom":atom,"serial":serial,"atom_name":atom_name,"alt_loc":alt_loc,"res_name":res_name,"chain":chain,
            "res_num":res_num,"icode":icode,"x":x,"y":y,"z":z,"occupancy":occupancy,"temp_fact":temp_fact,"element":element,
            "charge":charge}

def contents2Info(contents): #reads the ATOM line. Then splits the info into respective frames and returns the data
    split_contents=[]
    for lines in contents:
        if (lines.startswith("ATOM")):
            tupl_dict=splitLine2Tuple(lines.strip())
            #print (tupl_dict)
            split_contents.append(tupl_dict)
    return split_contents

def reassembleLines(split_contents): #reassembles the split contents dictionary into one line string
    contents=[]
    for split_line in split_contents:
        line = ""
        for key in split_line:
            line+=split_line[key]
        contents.append(line+"\n")
    return contents

def readAtom(pdb):
    contents=[]
    with open (pdb,"r") as f:
        for line in f:
            #if (line.startswith("ATOM")):
            #    pass
            contents.append(line)
    return contents
    
def addChain(line,value):
    line=line[0:21]+value+line[22:]
    return line

def addColumn(split_contents,name,val):
    new_contents=[]
    for split_line in split_contents:
        split_line[name.lower()]=(len(split_line[name.lower()])-len(val))*" "+val
            #pass
        new_contents.append(split_line)
    return new_contents 

def replaceColumn(split_contents,name,val,by):
    new_contents=[]
    for split_line in split_contents:
        if (split_line[name.lower()].strip()==val): split_line[name.lower()]=(len(split_line[name.lower()])-len(val))*" "+by
            #pass
        new_contents.append(split_line)
    return new_contents 

def addColumnLine(contents,name,val):
    new_contents=[]
    for line in contents:
        if (line.startswith("ATOM")):
            if (name.lower()=="chain"):
                line=addChain(line,val)
            #pass
        new_contents.append(line)
    return new_contents 

def write2File(filename,cont):
    #dframe.to_csv(filename,sep="\t",index=False,header=False)
    with open (filename,"w") as f:
        f.writelines(cont)
        if (cont[len(cont)-1].strip()!="END"):
            f.write("END")
    return

def getChain(full_path): #returns the chain from the name of the .atom file
    last=full_path.split("/")[len(full_path.split("/"))-1]
    chain=last.replace(".atom","")
    chain=chain[len(chain)-1]
    return chain


pdb="/data/farhan/SoftwareTools/HomopolymerProject/working_scripts/pdb_folder_test/work_dir/atom/6BZEA.atom"
#pdb="/data/farhan/SoftwareTools/HomopolymerProject/working_scripts/pdb_folder_test/work_dir/atom/2MS7A.atom"
#pdb="/data/farhan/SoftwareTools/HomopolymerProject/working_scripts/pdb_folder_test/work_dir/atom/3J6JB.atom"

#os.system("ls /data/farhan/SoftwareTools/HomopolymerProject/working_scripts/pdb_folder_test/work_dir/atom/*.atom > atom_list.lst")

#main code to insert the chain info
"""
atom_list=[]
with open ("atom_list.lst","r") as f:
    for line in f:
        atom_list.append(line.strip())

        #df = readPDB(line.strip())
        #print(line.strip())
        print (line.strip().split("/")[len(line.strip().split("/"))-1])
        #contents = readAtom(line.strip())
        contents = readAtom(pdb)
        split_contents=contents2Info(contents)
        #Remark line below to reproduce file
        split_contents = addColumn(split_contents,"Chain",getChain(line.strip()))
        
        #file_name=line.strip().split("/")[len(line.strip().split("/"))-1].replace(".atom",".pdb")
        
        file_name=pdb.strip().split("/")[len(pdb.strip().split("/"))-1].replace(".atom",".pdb")
        #print(file_name)
        write2File("/data/farhan/SoftwareTools/HomopolymerProject/working_scripts/pdb_folder_test/outfolder/pdb/"+file_name,reassembleLines(split_contents))
        #break#

"""
