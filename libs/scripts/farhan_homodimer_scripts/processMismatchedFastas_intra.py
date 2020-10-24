#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 24 17:32:42 2020

@author: farhan
"""

#this script processes the mismatched fasta sequence atom files by:
#1. Searching the fasta_dictionary.txt to find the fasta sequences of the respective .atom files
#2. Aligns the sequences and finds sequence similarity using findSequenceSimilarity.py script
#3. Reindexes the respective .atom files to a selected destination "reindexed_atom"

import os,sys

def readFastaDict(fasta_dict_file):
    fasta_dict={}
    with open (fasta_dict_file,"r") as f:
        for line in f:
            fasta_dict[line.strip().split(":")[0].strip()]=line.strip().split(":")[1].strip()
    return fasta_dict


pdb_name=sys.argv[1]#"2HXR"#"2EHP"#"4I24"#"1BFT"#"1UZY"#"5IZV"#"11AS"
print("Processing fasta mismatches in chains for: "+pdb_name)
print("Reading fasta_dictionary...")
fasta_dict=readFastaDict("fasta_dictionary.txt") #reads the fasta_dictionary.txt file as a dictionary
key_list=list(fasta_dict.keys()) #get the keys of the dictionary
this_key_list=[] #stores the list of keys for pdb_name
print("Done!")

for key in key_list:
    if pdb_name in key:
        this_key_list.append(key)

print ("Atom file list found: ",this_key_list)
#the following arranges the fasta lengthwise. x=lower length, y= higher length
if len(fasta_dict[this_key_list[0]]) > len(fasta_dict[this_key_list[1]]):
    y=fasta_dict[this_key_list[0]]
    key_y=this_key_list[0]
    x=fasta_dict[this_key_list[1]]
    key_x=this_key_list[1]
    print("y > x", len(y),len(x))
else:
    y=fasta_dict[this_key_list[1]]
    key_y=this_key_list[1]
    x=fasta_dict[this_key_list[0]]
    key_x=this_key_list[0]
    print("x > y", len(x),len(y))
#No need if chain sequences are similary
if x==y: sys.exit("All fasta sequences are similar. Quitting!")
#2. and #3.
exit_code=os.system("python findSequenceSimilarity.py "+x+" "+y+" "+pdb_name+" "+key_x+" "+key_y)
if (exit_code!=0):
    sys.exit("Some thing went wrong for "+pdb_name+". Quitting!")
