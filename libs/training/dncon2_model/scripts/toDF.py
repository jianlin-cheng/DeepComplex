#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 29 23:15:08 2020

@author: farhan
"""

#reads the accuracy file and converts to dataframe

import pandas as pd
import os, sys

file = os.path.abspath(sys.argv[1])
#outfile = os.path.abspath(sys.argv[2])
#file="training_acc.txt"
outfile=file.replace(".txt","_df.txt")#"training_acc_df.txt"

df=pd.read_csv(file,sep="\t", index_col=None) #delimiter="\t"
print (df.to_string(index=False))
with open (outfile,"w") as f:
    f.write(df.to_string(index=False))
