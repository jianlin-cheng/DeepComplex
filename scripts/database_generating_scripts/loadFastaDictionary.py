#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 24 16:00:58 2020

@author: farhan
"""

#this script loads the fasta_dictionary.txt file into a dictionary
#usage: python loadFastaDictionary.txt <fasta_dictionary.txt>

def loadFastaDictionary(dict_file):
    fasta_dict={}
#    i=0
    with open(dict_file,"r") as f:
        for line in f:
#            i+=1
            fasta_dict[line.strip().split(":")[0].strip()]=line.strip().split(":")[1].strip()

#    print (len(fasta_dict.keys()),i)
    return fasta_dict
