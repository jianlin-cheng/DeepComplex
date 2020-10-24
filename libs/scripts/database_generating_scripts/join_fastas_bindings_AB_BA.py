#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  6 12:48:02 2020

@author: farhan
"""
#this script reads the heterodimer list and the fasta dictionary. Then it generates A+B and B+A fasta file
#Usage: python join_fastas_AB_BA.py <paired_list_file> <fasta_dictionary> <outfile>" 
import os, sys
from loadFastaDictionary import loadFastaDictionary
usage="Usage: python "+sys.argv[0]+" <paired_list_file> <fasta_dictionary> <outfile>"
fasta_list_file=os.path.abspath(sys.argv[1])
fasta_dict_file=os.path.abspath(sys.argv[2])
outfile=os.path.abspath(sys.argv[3])
outfile_AB=os.path.splitext(outfile)[0]+"_AB"+"."+os.path.splitext(outfile)[1]
outfile_BA=os.path.splitext(outfile)[0]+"_BA"+"."+os.path.splitext(outfile)[1]
fasta_dict=loadFastaDictionary(fasta_dict_file)
f=open(fasta_list_file)
fasta_pair_list=f.readlines()
f.close()

print (len(fasta_pair_list))
i=0
for pair in fasta_pair_list:
    first=pair.strip().split()[0]
    second=pair.strip().split()[1]
    #print (first)
    #print (second)
    fasta_A=fasta_dict[first]
    fasta_B=fasta_dict[second]
    #print (fasta_A)
    #print (fasta_B)
    name_AB=">"+first+"_"+second+"#"+str(i)#+"; Chain: "+first[-1]+","+second[-1]#+"; Lengths: "+str(len(fasta_A))+","+str(len(fasta_B))
    AB=fasta_A+fasta_B
    name_BA=">"+second+"__"+first+"#"+str(i)#+"; Chain: "+second[-1]+","+first[-1]#+"; Lengths: "+str(len(fasta_B))+","+str(len(fasta_A))
    BA=fasta_B+fasta_A
    os.system("echo '"+name_AB+"' >> "+outfile_AB)
    os.system("echo '"+AB+"' >> "+outfile_AB)
    os.system("echo '"+name_BA+"' >> "+outfile_BA)
    os.system("echo '"+BA+"' >> "+outfile_BA)
    i+=1
    #break

