#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  5 12:50:02 2019

@author: farhan
"""
#this script reads a distance.txt file and converts to sorted contact map file in .rr format
#usage: python dist2rr.py <dist_file> <outputfile>

import os,sys

dist_file=sys.argv[1]
sortedrr=sys.argv[2]
contents=[]
with open (dist_file,"r") as f:
    for line in f:
        contents.append(line)
#fasta=contens[0]
for i in range (1,len(contents)):
    split=contents[i].strip().split()
    d=float(split[-1])
    p=(1/d)+0.5
    #print (p)
    contents[i]=contents[i].replace(split[-1],str(p))
    #print (contents[i])

with open ("temp_rr.rr","w") as f:
    f.writelines(contents)

os.system("python sortrr.py temp_rr.rr True > "+sortedrr)
#os.system("python sortrr.py temp_rr.rr True")
