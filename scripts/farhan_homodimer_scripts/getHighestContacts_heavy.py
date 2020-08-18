#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  5 09:32:53 2019

@author: farhan
"""

#this script browses through all the distance files in the interchain contacts and choses the file with the highest number 
#of contacts. Also moves the required files to the ./interchains_heavy folder

#usage: python getHighestContacts.py protein_name

import os,subprocess,sys

def getHighestContacts(protein_name):
    os.system("ls "+protein_name+"_dist*.txt > "+"interlist.lst")
    file_list=[]
    
    with open ("interlist.lst","r") as f:
        for line in f:
            file_list.append(line.strip())
    if (len(file_list)==0): sys.exit("No "+protein_name+"_dist_*.txt distance file found. Exiting!")
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
    #delete the others
    file_list.remove(best)
    for file in file_list: #keep the best. Remove the rest
        #rr_file=file.replace("_dist_","")
        rr_file=file.replace("_dist","")
        rr_file=rr_file.replace(".txt",".rr")
        os.remove(file)
        os.remove(rr_file)
    return best

if (not os.path.isdir("interchains_heavy")): os.mkdir("interchains_heavy")
 
protein_name=sys.argv[1]
file_name=getHighestContacts(protein_name)
rr_file_name=file_name.replace("_dist","")
#rr_file_name=file_name.replace("_dist","")
rr_file_name=rr_file_name.replace(".txt",".rr")
#print (rr_file_name)
if (os.path.exists(file_name)): os.system("mv "+file_name+" interchains_heavy")

if (os.path.exists(rr_file_name)): os.system("mv "+rr_file_name+" interchains_heavy")
#print(file_name)
