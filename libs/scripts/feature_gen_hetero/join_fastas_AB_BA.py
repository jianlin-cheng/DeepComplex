#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  6 12:48:02 2020

@author: farhan
"""
#this script reads the heterodimer list and the fasta dictionary. Then it generates A+B and B+A fasta file
#Usage: python join_fastas_AB_BA.py <paired_list_file> <fasta_dictionary>"
import os, sys
from loadFastaDictionary import loadFastaDictionary
usage="Usage: python "+sys.argv[0]+" <paired_list_file> <fasta_dictionary>"
fasta_list_file=os.path.abspath(sys.argv[1])
fasta_dict_file=os.path.abspath(sys.argv[2])
fasta_dict=loadFastaDictionary(fasta_dict_file)
f=open(fasta_list_file)
fasta_pair_list=f.readlines()
f.close()

print (len(fasta_pair_list))
i=0
for pair in fasta_pair_list:
    first=os.path.splitext(pair.strip().split(",")[0])[0]
    second=os.path.splitext(pair.strip().split(",")[1])[0]
    #print (first)
    #print (second)
    fasta_A=fasta_dict[first]
    fasta_B=fasta_dict[second]
    #print (fasta_A)
    #print (fasta_B)
    name_AB=">"+first+"_"+second+"_"+str(i)+"; Chain: "+first[-1]+","+second[-1]+"; Lengths: "+str(len(fasta_A))+","+str(len(fasta_B))
    AB=fasta_A+fasta_B
    name_BA=">"+second+"__"+first+"_"+str(i)+"; Chain: "+second[-1]+","+first[-1]+"; Lengths: "+str(len(fasta_B))+","+str(len(fasta_A))
    BA=fasta_B+fasta_A
    os.system("echo '"+name_AB+"' >> combined_fasta_AB.txt")
    os.system("echo '"+AB+"' >> combined_fasta_AB.txt")
    os.system("echo '"+name_BA+"' >> combined_fasta_BA.txt")
    os.system("echo '"+BA+"' >> combined_fasta_BA.txt")
    i+=1
    #break

