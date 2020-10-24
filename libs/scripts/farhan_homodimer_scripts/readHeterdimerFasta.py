#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  6 22:42:08 2020

@author: farhan
"""
#this script will read the heterodimer fasta and return a fasta_dictionary

def readFastaFile(file):
    fasta_dict={}
    fasta_list=[]
    key=""
    with open (file,"r") as f:
        for line in f:
            if line.startswith(">"):
                key=line.strip().split()[0].replace(">","")
                fasta_dict[key]=""
            else:
                fasta_dict[key]+=line.strip()
    return fasta_dict

