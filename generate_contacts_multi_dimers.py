#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 20 22:56:26 2020

@author: anes
"""

import concurrent.futures
import os
import sys
import copy
import time

#time.sleep(30)
start_time = time.time()

file1=open("homodimers_missing.txt")
Pairs_file=file1.readlines()
file1.close()

start_part=int(sys.argv[1])
distance=6
part_range=10
 
def in_contact(Pr):
    Pair=copy.copy(Pr)
    Pair=Pair.strip()
    Pair_pdb=Pair.split(",")
    Pdb1="reindexed_pdb/"+Pair_pdb[0]+".pdb"
    Pdb2="reindexed_pdb/"+Pair_pdb[1]+".pdb"
    Dt=6
    Pdb1_out=Pair_pdb[0]#.split(".")[0]
    Pdb2_out=Pair_pdb[1]#.split(".")[0]
    outfile="contacts_homodimers_952/"+Pdb1_out+"_"+Pdb2_out+"_contact"
    
    Rxt_cd=os.system("python pdb2distance_inter_heavy.py "+Pdb1+" "+Pdb2+" "+str(Dt)+" "+outfile)
    line=[Pair,Rxt_cd]

    return line
    
with concurrent.futures.ProcessPoolExecutor() as executor:
    for lists in list(range(1)):
        print("part: ",start_part+lists)
        start_pair=(start_part+lists)*part_range
        end_pair=start_pair+part_range
        
        if end_pair>=len(Pairs_file):
            end_pair=Pairs_file
            
        list_part=Pairs_file[start_pair:end_pair]
    
        line_result=executor.map(in_contact,list_part)
        


print("--- %s seconds ---" % (time.time() - start_time))
