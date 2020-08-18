#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 19:38:32 2019

@author: farhan
"""

#this script will find reasons using the getContactAllAtoms.py script as to why something went wrong

#usage: python findReason.py <not_done_list>

import os, sys
pdb_list=[]
with open ("not_done_list_2.txt","r") as f:
    for line in f:
        pdb_list.append(line.strip())

for pdb in pdb_list:
    os.system("python getContactAllAtoms.py "+pdb)