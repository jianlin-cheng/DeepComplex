#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 24 10:57:22 2019

@author: farhan
"""

#this script calculates intrachain percision and keeps them in the mentioned folder
#usage: python doAll_precision_intrachain.py <interchain_list_done.txt> <intrachain_folder> <rr_folder> <output_folder>

import os,sys

def updateList(filelist,directory): #checks the folder for missing files and updates the list accordingly
    newlist=[]
    for file in filelist:
        if not (os.path.exists(directory+file)): newlist.append(file)
        #print(file)
    return newlist

def getName(file):
    name=file.split("/")[-1].strip()
    name=name[0:4]
    return name

def file2Name(file_list): #converts the list of files info to list of pdb names
    newlist=[]
    for file in file_list:
        newlist.append(getName(file))
    
    return newlist

list_file=sys.argv[1]
folder=sys.argv[2]
dncon_rr_folder=sys.argv[3]
outfolder=sys.argv[4]
if not (folder.endswith("/")): folder+="/"
if not (outfolder.endswith("/")): outfolder+="/"
if not (dncon_rr_folder.endswith("/")): dncon_rr_folder+="/"

file_list=[]
if not (os.path.exists(list_file)): sys.exit("List file "+list_file+" not found. Quitting!")
if not (os.path.isdir(folder)): sys.exit("Folder name "+folder+" not found. Quitting!")

with open (list_file,"r") as f:
    for line in f:
        file_list.append(line.strip())
pdb_list=file2Name(file_list)

#os.system("python makePDBList.py "+folder+" > my_intrafolder_list.txt")
os.system("python makePDBListAllFiles.py "+folder+" > my_intrafolder_list.txt")
intra_file_list=[]
with open ("my_intrafolder_list.txt","r") as f:
    for line in f:
        intra_file_list.append(line.strip())
#os.system("rm -f my_intrafolder_list.txt")

#intra_file_list=updateList(intra_file_list,folder)
#print (intra_file_list)
do_precision_list=[]
#check which files from input lists are present in the intrachain_folder
for pdb_name in pdb_list:
    for intra_file in intra_file_list:
        if (pdb_name in intra_file and ".rr" in intra_file): 
            print(pdb_name+"\t"+intra_file)
            do_precision_list.append(intra_file)
            
#do_precision_name_list=file2Name(do_precision_list)

print ("Performing intrachain_precision calculation in total:",len(do_precision_list),"files")
if not(os.path.isdir(outfolder)): os.mkdir(outfolder)
for intrachain_file in do_precision_list:
    print("Running command: python getPrecision_intra_v3.py "+folder+intrachain_file+" "+dncon_rr_folder+getName(intrachain_file)+".dncon2.rr > "+outfolder+getName(intrachain_file)+"_intra.txt")
    os.system("python getPrecision_intra_v3.py "+folder+intrachain_file+" "+dncon_rr_folder+getName(intrachain_file)+".dncon2.rr > "+outfolder+getName(intrachain_file)+"_intra.txt")

