#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  6 22:42:08 2020

@author: farhan
"""

#this script browses the timeout.txt files in lewis to find those proteins that failed. Creates a new list to run on longer time
#usage: python createTimedOutList.py <timeout.txt> <outputfile>

import os, sys
timeout_job_list=[]
failed_protein_list=[]
if (os.path.exists("timedout_protein_list.txt")):
    f=open("timedout_protein_list.txt")
    failed_protein_list=f.readlines()
    f.close()
    

with open (os.path.abspath(sys.argv[1].strip()),"r") as f:
    for line in f:
        if ("TIMEOUT" in line):
            timeout_job_list.append("result-"+line.split()[0].strip()+".out")
timeout_job_list=list(set(timeout_job_list))



for file in timeout_job_list:
    with open (file,"r") as f:
        for line in f:
            if line.startswith("Running"):
                name=line.split("/")[-1].split(".")[0]
                failed_protein_list.append(name+"\n")
failed_protein_list=list(set(failed_protein_list))
failed_protein_list[-1]=failed_protein_list[-1].strip()
with open ("timedout_protein_list.txt","w") as f:
    f.writelines(failed_protein_list)

