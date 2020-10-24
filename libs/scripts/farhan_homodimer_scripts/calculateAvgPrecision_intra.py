#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 31 12:59:53 2019

@author: farhan
"""

#this  script reads a folder full of intrachain precision files and creates a merged file and calculates average precision
#usage: python calculateAvgPrecision_intra.py <folder or list_file.txt>

import os,sys

def splitValues(line):
    top={}
    split=line.split()
    if (len(split)!=9):
        return -1
    top["Name"]=split[0]
    top["Relax"]=int(split[1])
    top["5"]=float(split[2])
    top["10"]=float(split[3])
    top["L/10"]=float(split[4])
    top["L/5"]=float(split[5])
    top["L/2"]=float(split[6])
    top["L"]=float(split[7])
    top["2L"]=float(split[8])
    return top

list_file=sys.argv[1]

if (os.path.isdir(list_file)):
    if not (list_file.endswith("/")): list_file+="/"
    os.system("ls "+list_file+"* > intra_chain_precision_file_list.txt")
    list_file="intra_chain_precision_file_list.txt"

file_list=[]
with open (list_file,"r") as f:
    for line in f:
        file_list.append(line.strip())
        
num_proteins=len(file_list)
label=""
total_top={}
whole_list=[]
total_top["5"]=0
total_top["10"]=0
total_top["L/10"]=0
total_top["L/5"]=0
total_top["L/2"]=0
total_top["L"]=0
total_top["2L"]=0
for file in file_list:
    print ("Processing file: "+file)
    with open (file,"r") as f:
        for line in f:
            
            if (line.startswith("Name")):
                if label=="": 
                    label=line
                    whole_list.append(label)
                
                line=f.readline().strip()
                
                if line.strip()=="": 
                    num_proteins-=1
                    print ("Problem with "+file+" Skipping")
                    break
                
                top=splitValues(line)
                
                if (top=="" or top==-1):
                    num_proteins-=1
                    print ("Problem with "+file+" Skipping")
                    break
                whole_list.append(line+"\n")
                #print (top)
                #print(top["5"])
                #print(top["10"])
                #print(top["L/10"])
                #print(top["L/5"])
                #print(top["L/2"])
                #print(top["L"])
                #print(top["2L"])
                #break
                
                total_top["5"]+=top["5"]
                total_top["10"]+=top["10"]
                total_top["L/10"]+=top["L/10"]
                total_top["L/5"]+=top["L/5"]
                total_top["L/2"]+=top["L/2"]
                total_top["L"]+=top["L"]
                total_top["2L"]+=top["2L"]
                #print (line)
                
                break
        #break
dash="-"*len(whole_list[0])+"\n"
whole_list.append(dash)
avg_T5=str(round(total_top["5"]/num_proteins,2))
avg_T10=str(round(total_top["10"]/num_proteins,2))
avg_TLby10=str(round(total_top["L/10"]/num_proteins,2))
avg_TLby5=str(round(total_top["L/5"]/num_proteins,2))
avg_TLby2=str(round(total_top["L/2"]/num_proteins,2))
avg_TL=str(round(total_top["L"]/num_proteins,2))
avg_T2L=str(round(total_top["2L"]/num_proteins,2))

avg_T5=abs(5-len(avg_T5))*" "+avg_T5
avg_T10=" "+abs(6-len(avg_T10))*" "+avg_T10
avg_TLby10=" "+abs(8-len(avg_TLby10))*" "+avg_TLby10
avg_TLby5=" "+abs(7-len(avg_TLby5))*" "+avg_TLby5
avg_TLby2=" "+abs(7-len(avg_TLby2))*" "+avg_TLby2
avg_TL=" "+abs(5-len(avg_TL))*" "+avg_TL
avg_T2L=" "+abs(6-len(avg_T2L))*" "+avg_T2L

last_line="AVG      0  "+avg_T5+avg_T10+avg_TLby10+avg_TLby5+avg_TLby2+avg_TL+avg_T2L
whole_list.append(last_line)

with open ("avg_intra_chain_precision_01_06_2020.txt","w") as f:
    f.writelines(whole_list)