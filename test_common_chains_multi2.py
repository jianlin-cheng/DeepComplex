#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 18 22:49:26 2020

@author: anes
"""

import concurrent.futures
import os
import sys
import copy
import time

start_time = time.time()

file1=open("pairs.txt")
Pairs_file=file1.readlines()
file1.close()

start_part=int(sys.argv[1])
distance=6
part_range=1000
 
def in_contact(Pr):
    Pair=copy.copy(Pr)
    Pair=Pair.strip()
    Pair_pdb=Pair.split(",")
    Pdb1="pdb_atom/"+Pair_pdb[0]
    Pdb2="pdb_atom/"+Pair_pdb[1]
    Dt=6
    
    Rxt_cd=os.system("python pdb2distance_inter_heavy_contact_test.py "+Pdb1+" "+Pdb2+" "+str(Dt))
    line=[Pair,Rxt_cd]

    return line
    
with concurrent.futures.ProcessPoolExecutor() as executor:
    for lists in list(range(10)):
        print("part: ",start_part+lists)
        start_pair=(start_part+lists)*part_range
        end_pair=start_pair+part_range
        
        if end_pair>=len(Pairs_file):
            end_pair=Pairs_file
            
        list_part=Pairs_file[start_pair:end_pair]
        
        fout1=open("pairs_in_contact_"+str(start_part)+".txt","w")
        fout2=open("pairs_not_in_contact_"+str(start_part)+".txt","w")
    
        line_result=executor.map(in_contact,list_part)
        for result in line_result:
            if result[1]== 0:
                fout1.write(result[0]+"\n")
            else:
                fout2.write(result[0]+"\n")                
        
    fout1.close()
    fout2.close()


print("--- %s seconds ---" % (time.time() - start_time))

