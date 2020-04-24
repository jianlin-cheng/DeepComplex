#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan  5 21:57:31 2020

@author: farhan
"""

#this script reads the .seq files and creates a fasta list for similar fasta sequences vs differenct fasta sequences
#usage: python createFastaDB.py <list_file.txt> <seq_folder>

import os,sys


def getChainSubset(pdb_name, all_keys):
    subset_chain_list=[]
    for key in all_keys:
        if pdb_name in all_keys:
            subset_chain_list.append(key)
    return subset_chain_list

def writeListToFile(list_name,filename):
    with open (filename,"w") as f:
        f.writelines(list_name)

#seq_folder="/data/farhan/SoftwareTools/HomopolymerProject/data/homodimers/homodimers_files/work_dir/seq/"
seq_folder="/data/farhan/SoftwareTools/HomopolymerProject/data/homooligomers/original_pdbs_7400/work_dir/seq/"
seq_list="seq_list.txt"

pdb_list=[]
seq_fasta_dict={}
#Since we have the fasta_dictionary.txt now we don't need the following code:
"""
with open (seq_list,"r") as f:
    for pdb in f:
        pdb=pdb.strip()
        os.system("ls "+seq_folder+pdb+"* > temp_seq.txt")
        
        with open ("temp_seq.txt","r") as fseq:
            for seqfile in fseq:
                fasta=""
                with open (seqfile.strip(),"r") as seq:
                    for _ in range (5):
                        line=seq.readline().strip()
                    for i in range(len(line)):
                        fasta+=line[i].strip()
                    seq_fasta_dict[seqfile.strip().split("/")[-1].replace(".seq","")]=fasta
        #break
"""
#Below is to write it to a file
#data_list=[]
#for key,value in seq_fasta_dict.items():
#    data_list.append(key+" : "+value+"\n")
#data_list[len(data_list)-1]=data_list[len(data_list)-1].strip()

#with open ("fasta_dictionary.txt","w") as f:
#    f.writelines(data_list)

with open("fasta_dictionary.txt","r") as f:
#with open("fake_fasta_dictionary.txt","r") as f:
    for line in f:
        seq_fasta_dict[line.strip().split(":")[0].strip()]=line.strip().split(":")[1].strip()

key_list=sorted(seq_fasta_dict.keys())

similar_list=[]
different_list=[]

#Older code:
"""
for i in range(0,len(key_list),2):
    if (key_list[i][0:4]==key_list[i+1][0:4]):
        if (seq_fasta_dict[key_list[i]].strip()==seq_fasta_dict[key_list[i+1]]):
            similar_list.append(key_list[i]+"\t"+key_list[i+1]+"\n")
            #similar_list.append(key_list[i+1])
            
        else:
            different_list.append(key_list[i][0:4]+"\n")
"""


#Replace the following code with while loop since now oligomer/multimer
pdb_list=[]
for key in key_list:
    pdb_list.append(key[0:4])

pdb_list=list(set(pdb_list))

"""
for pdb_name in pdb_list:
    subset=getChainSubset(pdb_name,key_list)
    match_flag=True
    for pdb_subset in subset:
        for k in range(len(subset)):
            if seq_fasta_dict[pdb_subset]!=seq_fasta_dict[subset[k]]:
                match_flag=False
                break
        if (match_flag==False): break
    if match_flag:
        similar_list.append(pdb_name+"\n")
    else:
        different_list.append(pdb_name+"\n")

writeListToFile(similar_list,"similar_list.txt")
writeListToFile(different_list,"different_list.txt")
#sys.exit()
print (different_list)
"""
similar_list=[]
different_list=[]

i=0
match_flag=False
done_flag=False
while (i<len(key_list)):
    if (i+1==len(key_list)):
        #print (i)
        if (match_flag): similar_list.append(key_list[i][0:4])
        if not (match_flag): different_list.append(key_list[i][0:4])
        break
        #pass
    #print (i,key_list[i])
    if (key_list[i][0:4]==key_list[i+1][0:4]):
        if (seq_fasta_dict[key_list[i]].strip()==seq_fasta_dict[key_list[i+1]]):
            i+=1
            if (done_flag==False):match_flag=True
            #continue
            #similar_list.append(key_list[i]+"\t"+key_list[i+1]+"\n")
            #similar_list.append(key_list[i+1])
            
        else:
            match_flag=False
            if (done_flag==False):different_list.append(key_list[i][0:4]+"\n")
            done_flag=True
            i+=1
    else:
        if (match_flag==True):
            similar_list.append(key_list[i][0:4]+"\n")
        i+=1
        match_flag=False
        done_flag=False
        #pass#if ()
#print (i,match_flag,done_flag)
with open ("same_fasta_list.txt","w") as f:
    f.writelines(similar_list)

with open ("different_fasta_list.txt","w") as f:
    f.writelines(different_list)
        
#print (different_list)
#print (similar_list)

print ("similar fasta sequences= ",len(similar_list))
print ("different fasta sequences= ",len(different_list))
print("whole list length= ",len(pdb_list))
#print (pdb_list)
#print ("1AM7" in pdb_list)
