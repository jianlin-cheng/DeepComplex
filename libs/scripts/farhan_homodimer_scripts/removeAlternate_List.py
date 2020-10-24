#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 30 21:20:40 2019

@author: farhan
"""
#calls removeAlternatesFromPDB.py for each PDB in the list
import os

#atomfolder="/data/farhan/SoftwareTools/HomopolymerProject/data/homodimers/homodimers_files/outfolder/atom/"
atomfolder="/data/farhan/SoftwareTools/HomopolymerProject/data/homodimers/scripts/new_atom/"
os.system("python makePDBListAllFiles.py "+atomfolder+" > atomfolder_list.txt")

with open ("atomfolder_list.txt","r") as f:
    for atomfile in f:
        print (atomfile.strip())
        #break
        os.system("python removeAlternatesFromPDB.py "+atomfolder+atomfile.strip()+" "+atomfolder+atomfile.strip())

