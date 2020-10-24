#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb  1 17:29:55 2020

@author: farhan
"""
#this script reads the aligned file and finds if any of the alignments have a gap. This is a testing script

from readRR import readRRFile
import os
alignment_folder="./aligned_seq_folder_different_01_29_2020/"
aln_list_file="aligned_seq_list.txt"
aln_file_list=[]

with open (aln_list_file,"r") as f:
    for line in f:
        aln_file_list.append(line.strip())

for file in aln_file_list:
    with open (alignment_folder+file+".aln.txt","r") as f:
        aln1=f.readline().strip()
        aln2=f.readline().strip()
    for i in range(len(aln1)):
        if (aln1[i]=="-" and aln2[i]=="-"):
            os.system("echo "+file+" >> gap_gap_list.txt")
    fasta,contents=readRRFile("./dncon2_rr/"+file+".dncon2.rr")
    if (fasta!=aln1):
        if (fasta!=aln2):
            os.system("echo "+file+" >> dncon2_fasta_mismatch.txt")
        
    #break

#print (aln1)
#print (aln2)
