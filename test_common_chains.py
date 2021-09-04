#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 11 23:34:09 2020

@author: anes
"""
import os
import sys
import time

start_time = time.time()
file1=open("pairs2.txt")
Pairs_file=file1.readlines()
file1.close()
distance=6
#path=sys.argv[1]
path="/home/anes/Desktop/Cheng_new_project/"
for Pair in Pairs_file:
    
    Pair=Pair.strip()
    Pair_pdb=Pair.split(",")
    Pdb1=Pair_pdb[0]
    Pdb2=Pair_pdb[1]
    
    pdb1=Pair_pdb[0].split(".")[0]
    pdb2=Pair_pdb[1].split(".")[0]
    outfile=path+pdb1+"_"+pdb2+".txt"
    
    exit_code=os.system("python pdb2distance_inter_heavy_contact_test.py "+Pdb1+" "+Pdb2+" "+str(distance)+" "+outfile)
    print(exit_code)
    if exit_code== 0:
        print("in contact")
    else:
        print("not in contact")
print("--- %s seconds ---" % (time.time() - start_time))