#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 21 12:51:25 2020

@author: farhan
"""
#this script reads the combined A+B fasta and creates a contact pair list between the chains
fasta_file="redundant_hetero100_pairs_list.txt"
folder="./hetero_cdhit/"
output_file="hetero100_red_pairs_list.txt"
AB_dict={}

with open (folder+fasta_file,"r") as f:
    
