#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 21 14:47:28 2019

@author: farhan
"""

import numpy as np
import pandas as pd
import os,sys

def readPDB(pdb):
    df = pd.read_csv(pdb,header=None,index_col=False,delim_whitespace=True, names=["ATOM","Atom_Num","ATM","RES","RES_NUM","X","Y","Z","Val1","ATM_"])#,delimiter="\n")
    (rows,cols)=df.shape
    vals=cols-8
    nam=["ATOM","Atom_Num","ATM","RES","RES_NUM","X","Y","Z"]
    for i in range(vals):
        nam.append("Val"+str(i))
    df = pd.read_csv(pdb,header=None,index_col=False,delim_whitespace=True, names=["ATOM","Atom_Num","ATM","RES","RES_NUM","X","Y","Z","Val1","ATM_"])#,delimiter="\n")
    (rows,cols)=df.shape
    if (df.loc[(rows-1)][0])=="END": df = df.drop([rows-1])

    df=df.astype({"ATOM":'str',"ATM":'str',"RES":'str',"ATM_":'str','Atom_Num':'int','RES_NUM':'int'})
    #print(df.loc[0][0])
    return df

def readAtom(pdb):
    df = pd.read_csv(pdb,header=None,index_col=False,delim_whitespace=True)
    (rows,cols)=df.shape
    vals=cols-8
    #print(vals,cols)
    nam=["ATOM","Atom_Num","ATM","RES","RES_NUM","X","Y","Z"]
    for i in range(vals):
        nam.append("Val"+str(i))
    df = pd.read_csv(pdb,header=None,index_col=False,delim_whitespace=True, names=nam)
    (rows,cols)=df.shape
    #print (df.iloc[rows-2][0])
    if (df.loc[(rows-1)][0])=="END": df = df.drop([rows-1])
    #df=df.astype({"ATOM":'str',"ATM":'str',"RES":'str',"ATM_":'str','Atom_Num':'int','RES_NUM':'int'})
    df=df.astype({"ATOM":'str',"ATM":'str',"RES":'str','Atom_Num':'int','RES_NUM':'int'})
    df=df.round({"X":3,"Y":3,"Z":3})
    
    return df

def addColumn(df,name,val):
    rows=df.shape[0]
    l=[]
    for _ in range(rows):
        l.append(val)
    
    #df_add=pd.DataFrame(data=l,columns=[name])
    df.insert(4,name,l,True)
    return  df

def writedf2File(filename,dframe):
    dframe.to_csv(filename,sep="\t",index=False,header=False)
    return

def getChain(full_path):
    last=full_path.split("/")[len(full_path.split("/"))-1]
    chain=last.replace(".atom","")
    chain=chain[len(chain)-1]
    return chain

#pdb="/data/farhan/SoftwareTools/HomopolymerProject/working_scripts/pdb_folder_test/work_dir/atom/6BZEA.atom"
#pdb="/data/farhan/SoftwareTools/HomopolymerProject/working_scripts/pdb_folder_test/work_dir/atom/2MS7A.atom"
pdb="/data/farhan/SoftwareTools/HomopolymerProject/working_scripts/pdb_folder_test/work_dir/atom/3J6JB.atom"

#os.system("ls /data/farhan/SoftwareTools/HomopolymerProject/working_scripts/pdb_folder_test/work_dir/atom/*.atom > atom_list.lst")

atom_list=[]
with open ("atom_list.lst","r") as f:
    for line in f:
        atom_list.append(line.strip())

        #df = readPDB(line.strip())
        #print(line.strip())
        print (line.strip().split("/")[len(line.strip().split("/"))-1])
        df = readAtom(line.strip())
        #df = readAtom(pdb)
        df2 = addColumn(df,"Chain",getChain(line.strip()))
        file_name=line.strip().split("/")[len(line.strip().split("/"))-1].replace(".atom",".pdb")
        #print(file_name)
        writedf2File("/data/farhan/SoftwareTools/HomopolymerProject/working_scripts/pdb_folder_test/outfolder/pdb/"+file_name,df2)
        #break#


