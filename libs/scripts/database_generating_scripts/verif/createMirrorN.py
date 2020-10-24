#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 21 08:54:31 2020

@author: farhan
"""
from loadFastaDictionary import loadFastaDictionary
import os

def reverseDict(d):
    new_dict={}
    dup_key=[]
    for key, value in d.items():
        if value in new_dict.keys(): 
            #print ("Duplicate fasta for: "+key+"\n"+new_dict[value])
            dup_key.append(key)
            dup_key.append(new_dict[value])
        new_dict[value]=key
    return new_dict, dup_key

fasta_dict=loadFastaDictionary("fasta_dictionary.txt")
AB_rem_key_list=[]
BA_rem_key_list=[]

AB_file="hetero25_AB"
BA_file="hetero25_BA"
all_file="new_hetero25_all"

AB_dict={}
BA_dict={}
all_dict={}

with open (AB_file,"r") as f:
    for line in f:
        if (line.startswith(">")):
            fasta=f.readline().strip()
            AB_dict[line.strip()]=fasta

AB_key_list=list(AB_dict.keys())

print (AB_key_list[0].split("_"))
print (AB_key_list[0])
i=0
both_key_list=[]

key_A_2_key_B_dict={}
key_B_2_key_A_dict={}
all_keys_dict={}
for key in AB_key_list:
    pdb_A=key.split("_")[0].lstrip(">")
    chain_A=pdb_A[-1]
    pdb_B=key.split("_")[1].strip()
    chain_B=pdb_B[-1]
    #print (">"+pdb_B+"__"+pdb_A+"_"+str(i)+"; Chain: "+chain_B+","+chain_A+"; Lengths: "+str(len(fasta_dict[pdb_B]))+","+str(len(fasta_dict[pdb_A]))+"\n")
    k=">"+pdb_B+"__"+pdb_A+"_"+str(i)+"; Chain: "+chain_B+","+chain_A+"; Lengths: "+str(len(fasta_dict[pdb_B]))+","+str(len(fasta_dict[pdb_A]))
    #if k in list(BA_dict.keys()): print ("Duplicate keys found!!!!!\n"+k)
    BA_dict[k]=fasta_dict[pdb_B]+fasta_dict[pdb_A]
    both_key_list.append([key,k])
    key_A_2_key_B_dict[key]=k
    key_B_2_key_A_dict[k]=key
    i+=1
    #break
all_dict.update(AB_dict)
all_dict.update(BA_dict)
all_keys_dict.update(key_A_2_key_B_dict)
all_keys_dict.update(key_B_2_key_A_dict)
print ("Before:")
print (len(AB_dict))
print (len(BA_dict))
print (len(all_dict))


#i=0
for item in both_key_list:
    key=item[0]
    k=item[1]
    #print (AB_dict[key])
    #print (BA_dict[k])
    
    if AB_dict[key].strip()==BA_dict[k].strip():
        print("Here!")
        AB_dict.pop(key)
        BA_dict.pop(k)
    

#print ("##$#$#$#$#$#$")
#print (AB_dict[">3VEPH_3VEPJ_51857; Chain: H,J; Lengths: 69,47"])
pop_flag=False
"""
for key in list(AB_dict.keys()):
    for k in list(BA_dict.keys()):
        #print (key)
        #print (AB_dict[key])
        if AB_dict[key].strip()==BA_dict[k].strip():
            pop_flag=True
            #AB_dict.pop(key,"")
            #BA_dict.pop(all_keys_dict[key],"")
            BA_dict.pop(k,"")
            #AB_dict.pop(all_keys_dict[k],"")
    if pop_flag:
        AB_dict.pop(key,"")
        pop_flag=False
"""
reversed_BA,dupes_BA=reverseDict(BA_dict)
reverse_all_dict,all_dupes=reverseDict(all_dict)

for dupe_key in dupes_BA:
    BA_dict.pop(dupe_key,"")
    AB_dict.pop(all_keys_dict[dupe_key],"")

#Optional 
for dupe_key in all_dupes:
    BA_dict.pop(dupe_key,"")
    AB_dict.pop(all_keys_dict[dupe_key],"")


print ("After:")
print (len(AB_dict))
print (len(BA_dict))


with open ("new_"+AB_file,"w") as f:
    for key, fasta in AB_dict.items():
        f.write(key+"\n")
        f.write(fasta+"\n")

with open ("new_"+BA_file,"w") as f:
    for key, fasta in BA_dict.items():
        f.write(key+"\n")
        f.write(fasta+"\n")
#os.system("cat "+AB_file+" "+BA_file+" > "+all_file)
os.system("cat new_"+AB_file+" new_"+BA_file+" > "+all_file)