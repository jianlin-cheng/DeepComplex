#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  5 14:23:22 2020

@author: farhan
"""

#this script reads the fasta_file
def readFastaFile(file):
    import os,sys
    if not (os.path.exists(file)): sys.exit("Fasta file "+file+" not found!")
    header=""
    fasta=""
    with open (file,"r") as f:
        for line in f:
            if line.startswith(">"):
                header=line.strip()
                continue
            fasta+=line.strip()
    return header,fasta