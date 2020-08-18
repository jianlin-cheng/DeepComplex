#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  6 13:48:30 2020

@author: farhan
"""

#this script will read the homodimer pairs list and create a combined fasta file of all the individual proteins. 
#usage: python createCombinedHomodimerFastaFile.py <pairs_file> <fasta_dictionary> <outfile>

import os, sys
from loadFastaDictionary import loadFastaDictionary
usage="Usage: python "+sys.argv[0]+" <paired_list_file> <fasta_dictionary>"
fasta_list_file=os.path.abspath(sys.argv[1])
fasta_dict_file=os.path.abspath(sys.argv[2])
outputfile=os.path.abspath(sys.argv[3])
fasta_dict=loadFastaDictionary(fasta_dict_file)
f=open(fasta_list_file)
fasta_pair_list=f.readlines()
f.close()
fasta_list=[]
print (len(fasta_pair_list))
for pair in fasta_pair_list:
    first=os.path.splitext(pair.strip().split("_")[0])[0]
    second=os.path.splitext(pair.strip().split("_")[1])[0]
    fasta_list.append(first)
    fasta_list.append(second)
    #print (first)
    #print (second)
    #fasta_A=fasta_dict[first]
    #fasta_B=fasta_dict[second]

fasta_list=list(set(fasta_list))
fasta_whole_list=[]
problem_list=[]
for name in fasta_list:
    fasta=fasta_dict[">"+name]+"\n"
    #fasta=fasta_dict[name]+"\n"
    title=">"+name+"; Chain: "+name[-1]+"; Lengths: "+str(len(fasta.strip()))+"\n"
    if len(fasta.strip())<30:
#        print (len(fasta.strip()))
        problem_list.append(title)
        problem_list.append(fasta)
        continue
    fasta_whole_list.append(title)
    fasta_whole_list.append(fasta)
    #os.system("echo '"+title+"' >> heterodimer_fasta.txt")
    #os.system("echo '"+fasta+"' >> heterodimer_fasta.txt")
with open (outputfile,"w") as f:
    f.writelines(fasta_whole_list)

with open ("homomer95_fasta_length_30_or_less.txt","w") as f:
    f.writelines(problem_list)
