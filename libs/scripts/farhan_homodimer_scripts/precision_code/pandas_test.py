#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 30 01:41:06 2020

@author: farhan
"""
import pandas as pd
file="pd_df_0_0.txt"
#names=["Name","Relax","Top-5","Top-10","Top-L/10","Top-L/5","Top-L/2","Top-L","Top-2L"]
names=[0,1,2,3,4,5,6,7,8]
nam=[2,3,4,5,6,7,8]
df=pd.read_csv(file,header="infer",names=names,index_col=0,usecols=nam)#, index_col=0)
print (df)
#print (df["Top-5"].mean())
#print(df[8].)
#print(df.mean(axis=1))