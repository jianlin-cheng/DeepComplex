#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  7 12:34:44 2020

@author: farhan
"""

#this script creates an average precision list from a list of files or a folder or files for INTER chains
#usage: python calculateAveragePrecision_inter.py <list_file or folder>

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
    #print ("Top:\n")
    #print (top)
    return top

list_file=sys.argv[1]

if (os.path.isdir(list_file)):
    if not (list_file.endswith("/")): list_file+="/"
    os.system("ls "+list_file+"* > inter_chain_precision_file_list_fake.txt")
    list_file="inter_chain_precision_file_list_fake.txt"

file_list=[]
with open (list_file,"r") as f:
    for line in f:
        file_list.append(os.path.abspath(line.strip()))
        
num_proteins=len(file_list)
label=""
total_top={}
whole_list=[]
whole_list_dict={}
for relax_rem in range(3):
    for relax in range(3):
        total_top[str(relax_rem)+"_"+str(relax)+" 5"]=0
        total_top[str(relax_rem)+"_"+str(relax)+" 10"]=0
        total_top[str(relax_rem)+"_"+str(relax)+" L/10"]=0
        total_top[str(relax_rem)+"_"+str(relax)+" L/5"]=0
        total_top[str(relax_rem)+"_"+str(relax)+" L/2"]=0
        total_top[str(relax_rem)+"_"+str(relax)+" L"]=0
        total_top[str(relax_rem)+"_"+str(relax)+" 2L"]=0
        whole_list_dict[str(relax_rem)+"_"+str(relax)]=[]

    
"""
total_top["5"]=0
total_top["10"]=0
total_top["L/10"]=0
total_top["L/5"]=0
total_top["L/2"]=0
total_top["L"]=0
total_top["2L"]=0
"""
for file in file_list:
    print ("Processing file: "+file)
    with open (file,"r") as f:
        for line in f:
            #print (line)
            if "Name" in line:#if (line.strip().startswith("Name")):
                #print ("Here!!!!!")
                if label=="": 
                    label=line.strip()+"\n"
                    #whole_list.append(label)
                for relax_rem in range(3):
                    for relax in range(3):
                        line=f.readline().strip()
                        #print ("Line:\n"+line)
                        if line.strip()=="": 
                            continue
                            num_proteins-=1
                            print ("Stripped line:\n"+line)
                            print("Here@#@#@#@")
                            print ("Problem with "+file+" Skipping")
                            break
                        
                        top=splitValues(line)
                        #print ("Top:\n",top)
                        if (top=="" or top==-1):
                            num_proteins-=1
                            print ("Problem with "+file+" Skipping")
                            break
                        whole_list_dict[str(relax_rem)+"_"+str(relax)].append(line+"\n")
                        #print ("Whole list dict:\n",whole_list_dict)
                        #print (top)
                        #print(top["5"])
                        #print(top["10"])
                        #print(top["L/10"])
                        #print(top["L/5"])
                        #print(top["L/2"])
                        #print(top["L"])
                        #print(top["2L"])
                        #break
                        
                        total_top[str(relax_rem)+"_"+str(relax)+" 5"]+=top["5"]
                        total_top[str(relax_rem)+"_"+str(relax)+" 10"]+=top["10"]
                        total_top[str(relax_rem)+"_"+str(relax)+" L/10"]+=top["L/10"]
                        total_top[str(relax_rem)+"_"+str(relax)+" L/5"]+=top["L/5"]
                        total_top[str(relax_rem)+"_"+str(relax)+" L/2"]+=top["L/2"]
                        total_top[str(relax_rem)+"_"+str(relax)+" L"]+=top["L"]
                        total_top[str(relax_rem)+"_"+str(relax)+" 2L"]+=top["2L"]
                        #print (line)
                        
                        #break
        #break
#dash="-"*len(whole_list[0])+"\n"
print (num_proteins)
dash="-"*len(label)+"\n"
for relax_rem in range(3):
    for relax in range(3):
        whole_list_dict[str(relax_rem)+"_"+str(relax)].insert(0,dash)
        whole_list_dict[str(relax_rem)+"_"+str(relax)].insert(0,label)
        
        avg_T5=str(round(total_top[str(relax_rem)+"_"+str(relax)+" 5"]/num_proteins,2))
        avg_T10=str(round(total_top[str(relax_rem)+"_"+str(relax)+" 10"]/num_proteins,2))
        avg_TLby10=str(round(total_top[str(relax_rem)+"_"+str(relax)+" L/10"]/num_proteins,2))
        avg_TLby5=str(round(total_top[str(relax_rem)+"_"+str(relax)+" L/5"]/num_proteins,2))
        avg_TLby2=str(round(total_top[str(relax_rem)+"_"+str(relax)+" L/2"]/num_proteins,2))
        avg_TL=str(round(total_top[str(relax_rem)+"_"+str(relax)+" L"]/num_proteins,2))
        avg_T2L=str(round(total_top[str(relax_rem)+"_"+str(relax)+" 2L"]/num_proteins,2))
        
        avg_T5=abs(5-len(avg_T5))*" "+avg_T5
        avg_T10=" "+abs(6-len(avg_T10))*" "+avg_T10
        avg_TLby10=" "+abs(8-len(avg_TLby10))*" "+avg_TLby10
        avg_TLby5=" "+abs(7-len(avg_TLby5))*" "+avg_TLby5
        avg_TLby2=" "+abs(7-len(avg_TLby2))*" "+avg_TLby2
        avg_TL=" "+abs(5-len(avg_TL))*" "+avg_TL
        avg_T2L=" "+abs(6-len(avg_T2L))*" "+avg_T2L
        
        last_line="AVG      "+str(relax)+"  "+avg_T5+avg_T10+avg_TLby10+avg_TLby5+avg_TLby2+avg_TL+avg_T2L
        whole_list_dict[str(relax_rem)+"_"+str(relax)].append(dash)
        whole_list_dict[str(relax_rem)+"_"+str(relax)].append(last_line)
    
        with open ("avg_inter_chain_random_precision_07_28_2020_relaxrem_"+str(relax_rem)+"_relax_"+str(relax)+".txt","w") as f:
            f.writelines(whole_list_dict[str(relax_rem)+"_"+str(relax)])
