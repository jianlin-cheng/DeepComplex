#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  6 13:13:27 2019

@author: farhan
"""

def readRRFile(file):
    contents=[]
    fasta=""
    line=""
#    ln=""
    #print ("Reading fasta sequence !!!!!!!!!!!!!!!!!1")
    with open (file,"r") as f:
        for line in f:
            #print (line)
            #ln=line.strip()
            #if (line.strip()=="END"):print ("END found!")            
            if (line.strip().startswith("0") or line.strip().startswith("1") or line.strip().startswith("2") or line.strip().startswith("3") or line.strip().startswith("4") or line.strip().startswith("5") or line.strip().startswith("6") or line.strip().startswith("7") or line.strip().startswith("8") or line.strip().startswith("9")):
                #split=line.strip().split()
                #i=int(split[0])
                #j=int(split[1])
                contents.append(line.strip())
                continue
            if (line.strip().startswith("PFRMAT") or line.strip().startswith("METHOD") or line.strip().startswith("MODEL") or line.strip().startswith("REMARK") or line.strip().startswith("TARGET") or line.strip().startswith("AUTHOR")):
                continue
            
            fasta+=line.strip()     
    if (line.strip()=="END"):
        fasta=fasta[0:len(fasta)-3]
#    print (len(fasta),"#!#!#!#!#!#!")
    return fasta,contents

def write2File(file,fasta,contents):
    with open (file,"w") as f:
        f.write(fasta.strip()+"\n")
        for line in contents:
            f.write(line.strip()+"\n")
        #f.writelines(contents)

#fasta,cont=readRRFile("./dncon2_rr/4X06.dncon2.rr")

#print (fasta)
#print (len(fasta))
