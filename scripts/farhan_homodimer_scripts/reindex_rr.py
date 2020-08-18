#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  3 14:25:00 2020

@author: farhan
"""

#this script will reindex the .rr files eg: dncon2.rr and intrachain.rr
#usage: python reindex_rr.py <>

from readRR import readRRFile, write2File
import os

def readFastaDict(fasta_dict_file):
    fasta_dict={}
    with open (fasta_dict_file,"r") as f:
        for line in f:
            fasta_dict[line.strip().split(":")[0].strip()]=line.strip().split(":")[1].strip()
    return fasta_dict

def mapList2Dict(map_list):
    map_dict={}
    for val in map_list:
        split=val.split(":")
        map_dict[split[0].strip()]=split[1].strip()
    return map_dict

def readSeqAlnFile(aln_file):
    aln_dict={}
    key_list=[]
    with open (aln_file,"r") as f:
        for line in f:
            key=line.strip().split(":")[0].strip()
            aln_dict[key]=line.strip().split(":")[1].strip()
            key_list.append(key)
    return key_list,aln_dict

def reindex_rr(dncon2_rr,map_dict):
    new_rr_list=[]
    for line in dncon2_rr:
        split=line.strip().split()
        split[0]=map_dict[split[0]]
        split[1]=map_dict[split[1]]
        new_rr_list.append(split[0]+" "+split[1]+" "+split[2]+" "+split[3]+" "+split[4])
    return new_rr_list

fasta_dict=readFastaDict("fasta_dictionary.txt")
dncon2_reindex_file_list="reindex_different_fasta_list.txt"#"fake_reindex_list.txt"#"reindex_different_fasta_list.txt"
with open (dncon2_reindex_file_list,"r") as f:
    for fl in f:
        
        pdb_file=fl.strip()
        dncon2_rr_file="./dncon2_rr/"+pdb_file+".dncon2.rr"
        intrachain_rr="./intrachains_12_31_2019/"
        seq_aln_file="./aligned_seq_folder/"+pdb_file+".aln.txt"
        map_file="./reindexed_mapping_function/"
        dncon2_reindexed="./dncon2_reindexed/"
        outfile=dncon2_reindexed+pdb_file+".dncon2.rr"
        outfile_rr="./reindexed_intrachains/"
        if not (os.path.isdir(dncon2_reindexed)): os.mkdir(dncon2_reindexed)
        print("Processing reindexing of: "+pdb_file)
        if (os.path.exists(dncon2_rr_file)):
            print("Copying "+dncon2_rr_file+" to the folder ./dncon2_reindexed/")
            exit_code=os.system("cp "+dncon2_rr_file+" "+dncon2_reindexed+pdb_file+".dncon2.rr")
            if (exit_code==0): 
                print("copy done. Moving to reindexing.")
            else:
                os.system("echo "+pdb_file+": Unable to copy "+dncon2_rr_file+" Skipping! >> reindexing_problems_not_done.txt")
        else:
            print("The file "+dncon2_rr_file+" was not found! Skipping")
            os.system("echo "+pdb_file+": "+dncon2_rr_file+" was not found! Skipping >> reindexing_problems_not_done.txt")
        
        selected_key=""
        selected_fasta=""
        selected_chain=""
        
        dncon_fasta,dncon2_rr=readRRFile(dncon2_rr_file)
        key_list,seq_aln_dict=readSeqAlnFile(seq_aln_file)
        skip_flag=False
        for key in key_list:
            if (dncon_fasta==seq_aln_dict[key]):
                print("The fasta sequence in dncon2 matches one of the atom files. Skipping reindexing!")
                os.system("echo "+pdb_file+": The fasta sequence in dncon2 matches one of the atom files. Skipping! >> reindexing_problems_not_done.txt")
                skip_flag=True
        #print ("skip_flag=",skip_flag)
        if skip_flag: continue
        
        for key in key_list: #search and match fasta_dict fasta sequence with the one in the rr file
            if (dncon_fasta==fasta_dict[key]):
                #print("Here")
                selected_fasta=dncon_fasta
                selected_key=key
                selected_chain=key[4]
                #print ("selected_key=",selected_key)
                break
        #print ("selected_key=",selected_key)
        map_file+=selected_key+"_map.txt"
        intrachain_rr+=pdb_file+"_"+selected_chain+selected_chain+".rr"
        print (map_file,"Map file found status: ",os.path.exists(map_file))
        print (intrachain_rr,"Intrachian_rr file found status: ",os.path.exists(intrachain_rr))
        if not (os.path.exists(map_file)): 
            print ("Map file: "+map_file+" not found! Skipping")
            os.system("echo "+pdb_file+": "+map_file+" not found. Skipping! >> reindexing_problems_not_done.txt")
            continue
        #print (type(dncon2_rr[0]))
        map_list=[]
        with open (map_file,"r") as f:
            for line in f:
                map_list.append(line.strip())
        map_dict=mapList2Dict(map_list)
        reindexed_dncon2_rr=reindex_rr(dncon2_rr,map_dict)
        write2File(outfile,seq_aln_dict[selected_key],reindexed_dncon2_rr)
        print("Done with this one!")



