#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 23 20:34:36 2020

@author: farhan
"""

#this script copies the related files from a list from one folder to another
#usage: python copyFromList.py <list_file.txt> <source_folder> <destination_folder> <extension>

def readListFile(file):
    l=[]
    with open (file,"r") as f:
        for line in f:
            l.append(line.strip())
    return l

import os,sys

list_file=sys.argv[1]
source=sys.argv[2]
destination=sys.argv[3]
extension=sys.argv[4].strip()

if not (source.endswith("/")): source+="/"
if not (destination.endswith("/")): destination+="/"


if not (os.path.exists(list_file)): sys.exit("List file "+list_file+" does not exist. Quitting")
if not(os.path.isdir(source)): sys.exit("Source Directory "+source+" does not exist. Quitting")
if not(os.path.isdir(destination)): 
    print("Destination directory "+destination+" does not exist. Creating newdirectory called "+destination)
    os.makedirs(destination)

file_list=readListFile(list_file)
print (len(file_list))

for pdb_name in file_list:
    os.system("scp "+source+pdb_name+"*"+extension+" "+destination+" >> failed_copy.txt")
    #break
