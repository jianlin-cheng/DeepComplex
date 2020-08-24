#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  6 22:42:08 2020

@author: farhan
"""
#this script will read the heterodimer fasta and return a fasta_dictionary

def readFastaFile(file):
    import string
    fasta_dict={}
    fasta_list=[]
    key=""
    i = 0
    alphabet_string = string.ascii_uppercase
    with open (file,"r") as f:
        for line in f:
            if line.startswith(">"):
                key=line.strip().split()[0].replace(">","")+alphabet_string[i]
                fasta_dict[key]=""
                i+=1
            else:
                fasta_dict[key]+=line.strip()
            
    return fasta_dict

