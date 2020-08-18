#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 27 19:34:38 2020

@author: farhan
"""
#this script processes the mismatched fastas individually from a list by calling the processMismatchedFastas.py
#Usage: python processMismatchedFastas_list.py <list_file.txt> <What=intra or leaveblank>

import os,sys

list_file=sys.argv[1]
what=sys.argv[2]

with open (list_file,"r") as f:
    for pdb_name in f:
        if (what.strip()=="intra"):
            os.system("python processMismatchedFastas_intra.py "+pdb_name.strip())
            pass
        else:
            os.system("python processMismatchedFastas.py "+pdb_name.strip())
        #break
