#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 31 12:59:53 2019

@author: farhan
"""

#this  script reads a folder full of intrachain precision files and creates a merged file and calculates average precision
#usage: python calculateAvgPrecision_intra.py <folder or list_file.txt> <dncon2_rr_folder> <pdb or atomfolder> <coneva_output_folder>

import os,sys

list_file=sys.argv[1]
dncon2_dir=sys.argv[2]
atomfolder=sys.argv[3]
coneva_prec_dir=sys.argv[4]

def getDir(file):
    
    return os.path.dirname(os.path.abspath(file))

def getName(file):
    return file.split("/")[-1][0:4]

def getChain(file):
    return file.split("/")[-1].split("_")[-1][0:1]
    
def getFileChainFromDir(file,folder):
    if not(folder.endswith("/")):folder+="/"
    os.system("ls "+folder+getName(file)+"* > name_list.txt")
    chain=""
    #print ("ASDFADSFADSF")
    with open ("name_list.txt","r") as f:
        for line in f:
            if (getName(file) in line):
                chain=getChain(line)
                break
    os.system("rm -f name_list.txt")
    return chain

def doConeva(file,smin=24):
    two_lines=[]
    coneva_prec_dir=sys.argv[4]
    os.system("./perl_scripts/coneva.pl -rr ./dncon2_rr/"+getName(file)+".dncon2.rr -pdb ./new_atom/"+getName(file)+getFileChainFromDir(file,"./intrachains_12_31_2019/")+".atom -smin "+str(smin)+" > coneva_temp.txt")
    print ("./perl_scripts/coneva.pl -rr ./dncon2_rr/"+getName(file)+".dncon2.rr -pdb ./new_atom/"+getName(file)+getFileChainFromDir(file,"./intrachains_12_31_2019/")+".atom -smin "+str(smin)+" > coneva_temp.txt")
    #sys.exit()
    with open ("coneva_temp.txt","r") as f:
        for line in f:
            if (line.startswith("PRECISION")):
                two_lines.append(line)
                line=f.readline()
                if (".dncon2.rr" in line):
                    two_lines.append(line.strip())
                    break
    os.system("rm -f coneva_temp.txt")
    if not(os.path.isdir(coneva_prec_dir)): os.mkdir(coneva_prec_dir)
    if not(coneva_prec_dir.endswith("/")): coneva_prec_dir+="/"
    with open (coneva_prec_dir+getName(file)+"_coneva.txt","w") as f:
        f.writelines(two_lines)
                
    return

def splitValues(line):
    top={}
    split=line.split()
    if (len(split)!=8):
        return -1
    top["Name"]=split[0]+" "+split[1]
    top["5"]=float(split[2])
    #top["10"]=float(split[3])
    top["L/10"]=float(split[3])
    top["L/5"]=float(split[4])
    top["L/2"]=float(split[5])
    top["L"]=float(split[6])
    top["2L"]=float(split[7])
    return top

###############################################################################

if (os.path.isdir(list_file)):
    if not (list_file.endswith("/")): list_file+="/"
    os.system("ls "+list_file+"* > intra_chain_precision_file_list.txt")
    list_file="intra_chain_precision_file_list.txt"
if not (coneva_prec_dir.endswith("/")): coneva_prec_dir+="/"
file_list=[]
with open (list_file,"r") as f:
    for line in f:
        file_list.append(line.strip())
"""
for file in file_list:
    doConeva(file,6)

"""

num_proteins=len(file_list)
label=""
total_top={}
whole_list=[]
total_top["5"]=0
#total_top["10"]=0
total_top["L/10"]=0
total_top["L/5"]=0
total_top["L/2"]=0
total_top["L"]=0
total_top["2L"]=0
for file in file_list:
    file=coneva_prec_dir+getName(file)+"_coneva.txt"
    print ("Processing file: "+file)
    if not(os.path.exists(file)): 
        print (file+" not found. Skipping!")
        os.system("echo "+file+" not found. Skipping >> coneva_problem.txt")
        continue
    with open (file,"r") as f:
        for line in f:
            
            if (line.startswith("PRECISION")):
                if label=="": 
                    label=line.replace("PRECISION","NAME     ")
                    whole_list.append(label)
                
                line=f.readline().strip()
                
                if line.strip()=="": 
                    num_proteins-=1
                    print ("Problem with "+file+" Skipping")
                    os.system("echo Problem with "+file+" Skipping >> coneva_problem.txt")
                    break
                
                top=splitValues(line)
                
                if (top=="" or top==-1):
                    num_proteins-=1
                    print ("Problem with "+file+" Skipping")
                    os.system("echo Problem with "+file+" Skipping >> coneva_problem.txt")
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
                #total_top["10"]+=top["10"]
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
#avg_T10=str(round(total_top["10"]/num_proteins,2))
avg_TLby10=str(round(total_top["L/10"]/num_proteins,2))
avg_TLby5=str(round(total_top["L/5"]/num_proteins,2))
avg_TLby2=str(round(total_top["L/2"]/num_proteins,2))
avg_TL=str(round(total_top["L"]/num_proteins,2))
avg_T2L=str(round(total_top["2L"]/num_proteins,2))

avg_T5=abs(5-len(avg_T5))*" "+avg_T5
#avg_T10=" "+abs(6-len(avg_T10))*" "+avg_T10
avg_TLby10="  "+abs(8-len(avg_TLby10))*" "+avg_TLby10
avg_TLby5="   "+abs(7-len(avg_TLby5))*" "+avg_TLby5
avg_TLby2="   "+abs(7-len(avg_TLby2))*" "+avg_TLby2
avg_TL="     "+abs(5-len(avg_TL))*" "+avg_TL
avg_T2L="    "+abs(6-len(avg_T2L))*" "+avg_T2L

last_line="AVG                           "+avg_T5+avg_TLby10+avg_TLby5+avg_TLby2+avg_TL+avg_T2L
whole_list.append(last_line)

with open ("avg_intra_chain_precision_coneva.txt","w") as f:
    f.writelines(whole_list)
