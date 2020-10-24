#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 13 00:56:56 2019

@author: farhan
"""

#this script will calculate the precision (intrachain) by comparing two rr files. according to the requirement like Top-5, Top-10, etc.

from readRR import *
import numpy as np
import os,sys
from mapfasta2pdb import pdb2fasta

def trimRR(rr,val):
    new_rr=[]
    if (len(rr)<val):val=len(rr)
    for i in range(val):
        new_rr.append(rr[i])
    return new_rr

def filterContacts(rr,min_sep,max_sep):
    new_rr=[]
    
    for line in rr:
        split=line.strip().split()
        #unremark if calculating intrachain
        """
        if (int(split[0]) > int(split[1])):
            t=split[0]
            split[0]=split[1]
            split[1]=t
            line=""
            for l in split:
                line+=l+" "
        """    
        if (abs(int(split[0])-int(split[1])) < min_sep): continue
        if (abs(int(split[0])-int(split[1])) > max_sep): continue
        new_rr.append(line)
    
    return new_rr

def findMax(rr):
    num=[]
    for item in rr:
        split=item.split()
        num.append(int(split[0]))
        num.append(int(split[1]))
    
    return max(num)

def findContact(rr1,rr2,fasta,relax=0): #usually cmap1 is the pdb_rr, cmap2 is the predicted rr
    contact_num=0
    if (relax==0):
        for rr2_item in rr2:
            split=rr2_item.split()
            i2=split[0]#int(split[0])
            j2=split[1]#int(split[1])
            select=i2+" "+j2
            for rr1_item in rr1:
                #split2=rr1_item.split()
                #i1=int(split2[0])
                #j1=int(split2[1])
                #if (i1==i2 and j1==j2): 
                if (select in rr1_item):
                    contact_num+=1
                    break
    """
    else:
        L=len(fasta)
        cmap1=np.zeros((L,L))
        cmap2=np.zeros((L,L))
        for rr1_item in rr1:
            split=rr1_item.split()
            i1=int(split[0])
            j1=int(split[1])
            cmap1[i1][j1]=1
            cmap1[j1][i1]=1
        for rr2_item in rr2:
            split2=rr2_item.split()
            i2=int(split2[0])
            j2=int(split2[1])
            cmap2[i2][j2]=1
            cmap2[j2][i2]=1
        for i in range(L):
            for j in range(i,L):
                if (cmap1[i][j]==0 and cmap2[i][j]==0):
                    continue
                    
                if (cmap1[i][j]==1 and cmap2[i][j]==1):
                    contact_num+=1
                    continue
                if (cmap1[i][j]==0 and cmap2[i][j]==1):
                    for k in range(relax):
                        kk=k+1
                        if ((i-kk >= 0) and (j-kk >= 0) and (i+kk < L) and (j+kk < L)):
                            if (cmap1[i-kk][j-kk]==1 and cmap2[i-kk][j-kk]!=1):
                                contact_num+=1
                                break
                        #if ((i-kk >= 0) and (j-kk >= 0) and (i+kk < L) and (j+kk < L)):
                            if (cmap1[i-kk][j]==1 and cmap2[i-kk][j]!=1):
                                contact_num+=1
                                break
                        #if ((i-kk >= 0) and (j-kk >= 0) and (i+kk < L) and (j+kk < L)):
                            if (cmap1[i][j-kk]==1 and cmap2[i][j-kk]!=1):
                                contact_num+=1
                                break
                        #if ((i-kk >= 0) and (j-kk >= 0) and (i+kk < L) and (j+kk < L)):
                            if (cmap1[i+kk][j+kk]==1 and cmap2[i+kk][j+kk]!=1):
                                contact_num+=1
                                break
                        #if ((i-kk >= 0) and (j-kk >= 0) and (i+kk < L) and (j+kk < L)):
                            if (cmap1[i+kk][j]==1 and cmap2[i+kk][j]!=1):
                                contact_num+=1
                                break
                        #if ((i-kk >= 0) and (j-kk >= 0) and (i+kk < L) and (j+kk < L)):
                            if (cmap1[i][j+kk]==1 and cmap2[i][j+kk]!=1):
                                contact_num+=1
                                break
                        #if ((i-kk >= 0) and (j-kk >= 0) and (i+kk < L) and (j+kk < L)):
                            if (cmap1[i-kk][j+kk]==1 and cmap2[i-kk][j+kk]!=1):
                                contact_num+=1
                                break
                        #if ((i-kk >= 0) and (j-kk >= 0) and (i+kk < L) and (j+kk < L)):
                            if (cmap1[i+kk][j-kk]==1 and cmap2[i+kk][j-kk]!=1):
                                contact_num+=1
                                break
                        continue
       """         
    #print ("CNUM=",contact_num)
    return contact_num

def makeRelaxed(rr,L,filename,relax=0):
    new_rr=[]
    if relax==0: return rr
    
    for item in rr:
        split=item.strip().split()
        i=int(split[0])
        j=int(split[1])
        ii=[]
        jj=[]
        new_rr.append(item)
        val=split[len(split)-1]
        for k in reversed(range(1,relax+1)):
            if (i-k>=0):ii.append(i-k)
            if (j-k>=0):jj.append(j-k)
            if (i+k<L):ii.append(i+k)
            if (j+k<L):jj.append(j+k)
        for x in ii:
            for y in jj:
                string=str(x)+""+str(y)+" 0 8 "+val
                if (y>x): new_rr.append(string)
            
    return new_rr

def fillArea(rr_pred,i,j,v): # fills a square matrix of v+1 size centered at (i,j) 
    l=len(rr_pred)
    cp=np.copy(rr_pred)
    for x in list(reversed(range(v+1))):
        if (i-x>=0):
            ii_min=i-x
            break
    
    for x in list(reversed(range(v+1))):
        if (j-x>=0):
            jj_min=j-x
            break
    
    for x in list(reversed(range(v+1))):
        if (i+x<l):
            ii_max=i+x
            break
    
    
    for x in list(reversed(range(v+1))):
        if (j+x<l):
            jj_max=j+x
            break
    
    for x in range(ii_min,ii_max+1,1):
        for y in range(jj_min,jj_max+1,1):
            cp[x][y]=1
        
    return cp

def checkArea(rr_pred,i,j,v): # checks a square matrix of v+1 size centered at (i,j) for a 1
    l=len(rr_pred)
    cp=np.copy(rr_pred)
    for x in list(reversed(range(v+1))):
        if (i-x>=0):
            ii_min=i-x
            break
    
    for x in list(reversed(range(v+1))):
        if (j-x>=0):
            jj_min=j-x
            break
    
    for x in list(reversed(range(v+1))):
        if (i+x<l):
            ii_max=i+x
            break
    
    
    for x in list(reversed(range(v+1))):
        if (j+x<l):
            jj_max=j+x
            break
    
    for x in range(ii_min,ii_max+1,1):
        for y in range(jj_min,jj_max+1,1):
            if cp[x][y]==1: return 1 #True
        
    return 0 #False

def findContactInter(rr1,rr2,fasta,relax=0): #usually cmap1 is the pdb_rr, cmap2 is the predicted rr
    contact_num=0
    if (relax==0):
        for rr2_item in rr2:
            split=rr2_item.split()
            i2=split[0]#int(split[0])
            j2=split[1]#int(split[1])
            select=i2+" "+j2
            select_rev=j2+" "+i2
            for rr1_item in rr1:
                #split2=rr1_item.split()
                #i1=int(split2[0])
                #j1=int(split2[1])
                #if (i1==i2 and j1==j2): 
                if (select in rr1_item or select_rev in rr1_item):
                    contact_num+=1
                    break
    #else do relaxation
    else:
        L=len(fasta)
        cmap1=np.zeros((L,L)) #pdb 
        cmap2=np.zeros((L,L)) #predicted rr
        for rr1_item in rr1:
            split=rr1_item.split()
            i1=int(split[0])-1
            j1=int(split[1])-1
            cmap1[i1][j1]=1
            cmap1[j1][i1]=1
        for rr2_item in rr2:
            split2=rr2_item.split()
            i2=int(split2[0])-1
            j2=int(split2[1])-1
            cmap2[i2][j2]=1
            cmap2[j2][i2]=1
        for i in range(L):
            for j in range(i,L):
                if (cmap1[i][j]==0 and cmap2[i][j]==0):
                    continue
                    
                if (cmap1[i][j]==1 and cmap2[i][j]==1):
                    contact_num+=1
                    continue
                if (cmap1[i][j]==0 and cmap2[i][j]==1):
                    #temp_cmap=fillArea(cmap1,i,j,relax)
                    contact_num+=checkArea(cmap1,i,j,relax)
                    
                    
       
    #print ("CNUM=",contact_num)
    return contact_num


def analyze(file1,rr):
    for item in rr:
        split=item.split()
        select=split[0]+" "+split[1]
        #print(select)
        #break
        with open (file1,"r") as f:
            for line in f:
                
                if ("PDB" in line):
                    
                    if (select in line):
                        pass
                    else:
                        print (select+" "+line)

def getPrecisionInter(rr1,rr2,fasta,top="All",relax=0):
    L=len(fasta)
    if (len(rr2)<2*L):  
 
        val = len (rr1)
    else:
        val=2*L
    if (top=="All" or top=="all" or top ==""): val=100000
    if (top=="5"): val=5
    if (top=="10"): val=10
    if (top=="L/10" or top=="l/10"): val=int(L/10)
    if (top=="L/5" or top=="l/5"): val=int(L/5)
    if (top=="L/2" or top=="l/2"): val=int(L/2)
    if (top=="L" or top=="l"): val=int(L)
    if (top=="2L" or top=="2l"): val=int(2*L)
    
    #rr1=trimRR(rr1,val)
    rr2=trimRR(rr2,val)
    write2File(outfile_inter,fasta1,rr1)
    write2File(outfile_pred,fasta2,rr2)
    con_num=findContactInter(rr1,rr2,fasta,relax)
    #analyze("temp(1).rr",rr1)
    
    
    return 100*con_num/val

def getPrecision(rr1,rr2,fasta,top="All",relax=0):
    L=len(fasta)
    if (len(rr2)<2*L):  
 
        val = len (rr1)
    else:
        val=2*L
    if (top=="All" or top=="all" or top ==""): val=100000
    if (top=="5"): val=5
    if (top=="10"): val=10
    if (top=="L/10" or top=="l/10"): val=int(round((L/10),0))
    if (top=="L/5" or top=="l/5"): val=int(round((L/5),0))
    if (top=="L/2" or top=="l/2"): val=int(round((L/2),0))
    if (top=="L" or top=="l"): val=int(L)
    if (top=="2L" or top=="2l"): val=int(2*L)
    
    #rr1=trimRR(rr1,val)
    rr2=trimRR(rr2,val)

#    write2File(outfile_inter,fasta1,rr1)
#    write2File(outfile_pred,fasta2,rr2)
    con_num=findContact(rr1,rr2,fasta,0)
    #analyze("temp(1).rr",rr1)
    
    #if (top=="L/10"):print (rr2)#("%L/10=",100*con_num/(11))
    return 100*con_num/val

def makeOutputFile(file,ext):
    #split=file.split()
    #basename=split[len(split)-1]
    basename=os.path.splitext(os.path.basename(file))[0]
    dirname=os.path.dirname(file)+"/"
    return dirname+basename+ext

def makeDiagonalOne(mat): #makes the diagonals of matrix one
    for i in range(len(mat)):
        mat[i][i]=1
    return mat

def rr2mat(mat,rr,triangle_equal=True): #converts an rr_list to its equivalent matrix
    matt=np.copy(mat)
    #print("Mat_Len=",len(matt))
    for item in rr:
        split=item.split()
        i= int (split[0])-1
        j= int (split[1])-1
        val = float(split[len(split)-1])
        matt[i][j]=val
        if (triangle_equal): matt[j][i]=val
        
    return matt

def clearArea(rr_pred,i,j,v): # clears a square matrix of v+1 size centered at (i,j) 
    l=len(rr_pred)
    cp=np.copy(rr_pred)
    for x in list(reversed(range(v+1))):
        if (i-x>=0):
            ii_min=i-x
            break
    
    for x in list(reversed(range(v+1))):
        if (j-x>=0):
            jj_min=j-x
            break
    
    for x in list(reversed(range(v+1))):
        if (i+x<l):
            ii_max=i+x
            break
    
    
    for x in list(reversed(range(v+1))):
        if (j+x<l):
            jj_max=j+x
            break
    
    for x in range(ii_min,ii_max+1,1):
        for y in range(jj_min,jj_max+1,1):
            cp[x][y]=0
        
    return cp

def removeIntraContactsVicinity(l,rr,rr_intra,v=0):
    print("Len=",len(rr))
    new_rr=[]
    common=[]
    #l+=1
    result=np.zeros((l,l))
    rr_pred=np.zeros((l,l))
    rr_act=np.zeros((l,l))
    #rr_pred=makeDiagonalOne(rr_pred)
    
    rr_pred=rr2mat(rr_pred,rr)
    rr_act=rr2mat(rr_act,rr_intra,False)
    count=0
    for i in range(len(rr_act)):
        for j in range(len(rr_act)):
            if (rr_act[i][j]!=0): 
                #print("Zero")
                count+=1
    print (count)
    
    for i in range(l):
        for j in range(l):
            if (rr_act[i][j]!=0):
                #remove from rr_pred 3x3 if v=1, 5x5 if v=2
                rr_pred[i][j]=0
                rr_pred[j][i]=0
                rr_pred=clearArea(rr_pred,i,j,v)
                """
                if (v==1):
                    if (i-1>=0):
                        rr_pred[i-1][j]=0
                        if (j-1>=0): rr_pred[i-1][j-1]=0
                        if (j+1<l): rr_pred[i-1][j+1]=0
                    if (j-1>=0):
                        if (i+1<l): rr_pred[i+1][j-1]=0
                        rr_pred[i][j-1]=0
                    if (i+1<l):
                        if (j+1<l): rr_pred[i+1][j+1]=0
                        rr_pred[i+1][j]=0
                    if (j+1<l):
                        rr_pred[i][j+1]=0
                if (v==2):
                    rr_pred=clearArea(rr_pred,i,j,v)
                """
    for i in range(l):
          for j in range(i+1,l):
              if (rr_pred[i][j]!=0):
                  string=str(i+1)+" "+str(j+1)+" 0 8 "+str(rr_pred[i][j])
                  new_rr.append(string)
                        
            
                
                
    """
    for item in rr:
        split=item.split()
        selected=split[0]+" "+split[1]
        selected_rev=split[1]+" "+split[0]
        k=0
        while (k < len(rr_intra)):
            intra_item=rr_intra[k]
            if (selected in intra_item):
                
                break
            k+=1
        if (k==len(rr_intra)): 
            new_rr.append(item)
            #print ("NE")
    print("Len_new=",len(rr))
    """
    #temp_file=makeOutputFile(rr_file2,"_temp_rr.txt")
    #print(temp_file)
    #sys.exit()
    #print(os.path.abspath(temp_file))
    #write2File(temp_file,fasta2,new_rr)
    write2File("temp_rr.txt",fasta2,new_rr)
    print("New_rr=",len(new_rr))
    #for i in range(10):
    #    print(new_rr[i])
    #for i in range (len(new_rr)):
    #    if (new_rr[i]!=rr[i]):
    #        print("NE")
    return new_rr

def removeIntraContacts(rr,rr_intra):
    print("Len=",len(rr))
    new_rr=[]
    common=[]
    for item in rr:
        split=item.split()
        selected=split[0]+" "+split[1]
        selected_rev=split[1]+" "+split[0]
        k=0
        while (k < len(rr_intra)):
            intra_item=rr_intra[k]
            if (selected in intra_item):
                
                break
            k+=1
        if (k==len(rr_intra)): 
            new_rr.append(item)
            #print ("NE")
    print("Len_new=",len(rr))
    #temp_file=makeOutputFile(rr_file2,"_temp_rr.txt")
    #print(temp_file)
    #sys.exit()
    #print(os.path.abspath(temp_file))
    #write2File(temp_file,fasta2,new_rr)
    write2File("temp_rr.txt",fasta2,new_rr)
    #for i in range(10):
    #    print(new_rr[i])rr1,rr2,fasta,top="All",relax=0
    #for i in range (len(new_rr)):
    #    if (new_rr[i]!=rr[i]):
    #        print("NE")
    return new_rr

def getPrecisionMyWay(rr1,rr2,fasta,top="All",relax=0):
    #rr1 = interchain from pdb
    #rr2 = predicted rr with intrachains removed trimmed to 2L
    L=len(fasta)
    if (len(rr2)<2*L):  
        val = len (rr1)
    else:
        val=2*L
    if (top=="All" or top=="all" or top ==""): val=100000
    if (top=="5"): val=5
    if (top=="10"): val=10
    if (top=="L/10" or top=="l/10"): val=int(L/10)
    if (top=="L/5" or top=="l/5"): val=int(L/5)
    if (top=="L/2" or top=="l/2"): val=int(L/2)
    if (top=="L" or top=="l"): val=int(L)
    if (top=="2L" or top=="2l"): val=int(2*L)
    
    #rr1=trimRR(rr1,val)
    rr2=trimRR(rr2,val)
    #write2File(outfile_inter,fasta1,rr1)
    #write2File(outfile_pred,fasta2,rr2)
    con_num = 0
    for intercxy in rr1:
        split= intercxy.strip().split()
        selected = split[0]+" "+split[1]
        selected_rev = split[1]+" "+split[0]
        for intra_pred in rr2:
            if (selected in intra_pred or selected_rev in intra_pred):
                con_num+=1
                break
    
    return con_num*100/len(rr1) #con_num*100/val

def filterConfidence(rr_list, conf=0.5):
    new_rr=[]
    for item in rr_list:
        split=item.strip().split()
        if (float(split[len(split)-1])>=conf):
            new_rr.append(item)
    
    return new_rr

def printFromConeva():
    s=""
    return s

def getName(name):
    split=name.split("/")
    name=split[len(split)-1]
    name=name.split(".")[0] #modified
    name=name.split("_")[0] 
    return name

#rr_file1="./4zuk_out/4zuk_monomer_distance_next_AA.native.txt" #always the native file
#rr_file2="./sorted_4zuk.rr" #the prediction file
#intrachain below

#rr_file1="./4zuk_out/4zuk_monomer_distance_next_AA.native.txt" #always the native file
#rr_file2="./sorted_4zuk.rr" #the prediction file

rr_file1=sys.argv[1] #calculated intra_chain file
rr_file2=sys.argv[2] #predicted dncon2.rr file

#fasta2,rr2=readRRFile(rr_file2)
#rr2=filterContacts(rr2,6,10000)
#write2File(rr_file2.replace(".rr","_filtered_unsorted.rr"),fasta2,rr2)

#sort the dncon2.rr file
os.system("python sortrr.py "+rr_file2+" > "+rr_file2.replace(".rr","_sorted.rr")+" True")
rr_file2=rr_file2.replace(".rr","_sorted.rr")

fasta1,rr1=readRRFile(rr_file1) #multimer PDB interchain rr
fasta2,rr2=readRRFile(rr_file2) #prediction rr

#print (len(rr1),len(rr2))

rr1=filterContacts(rr1,6,10000) #not needed for multimer PDB
write2File(rr_file1.replace(".rr","_filtered.rr"),fasta1,rr1)
#rr2=filterConfidence(rr2)
rr2=filterContacts(rr2,6,10000)
#rr2=filterConfidence(rr2) #Not needed
#save the filtered .rr dncon2 file
write2File(rr_file2.replace(".rr","_filtered.rr"),fasta2,rr2)

name=getName(rr_file1)
#print (len(fasta2),len(fasta1))

print("Top-5=",round(getPrecision(rr1,rr2,fasta2,"5",0),2))
print("Top-10=",round(getPrecision(rr1,rr2,fasta2,"10",0),2))
print("Top-L/10=",round(getPrecision(rr1,rr2,fasta2,"L/10",0),2))
print("Top-L/5=",round(getPrecision(rr1,rr2,fasta2,"L/5",0),2))
print("Top-L/2=",round(getPrecision(rr1,rr2,fasta2,"L/2",0),2))
print("Top-L=",round(getPrecision(rr1,rr2,fasta2,"L",0),2))
print("Top-2L=",round(getPrecision(rr1,rr2,fasta2,"2L",0),2))
top={}
string1="Name        Top-5        Top-10        Top-L/10        Top-L/5        Top-L/2        Top-L        Top-2L"
string2="---------------------------------------------------------------------------------------------------------"
print(string1)
print(string2)
#print("Relaxation = "+str(relax_prec))
relax_prec=0

top["Name"]=name
top["Relax"]=str(relax_prec)
top["Top-5"]=str(round(getPrecision(rr1,rr2,fasta2,"5",relax_prec),2))
top["Top-10"]=str(round(getPrecision(rr1,rr2,fasta2,"10",relax_prec),2))
top["Top-L/10"]=str(round(getPrecision(rr1,rr2,fasta2,"L/10",relax_prec),2))
top["Top-L/5"]=str(round(getPrecision(rr1,rr2,fasta2,"L/5",relax_prec),2))
top["Top-L/2"]=str(round(getPrecision(rr1,rr2,fasta2,"L/2",relax_prec),2))
top["Top-L"]=str(round(getPrecision(rr1,rr2,fasta2,"L",relax_prec),2))
top["Top-2L"]=str(round(getPrecision(rr1,rr2,fasta2,"2L",relax_prec),2))
"""
top["Name"]=[name]
top["Top-5"]=[str(round(getPrecision(rr1,rr2,fasta2,"5",relax_prec),2))]
top["Top-10"]=[str(round(getPrecision(rr1,rr2,fasta2,"10",relax_prec),2))]
top["Top-L/10"]=[str(round(getPrecision(rr1,rr2,fasta2,"L/10",relax_prec),2))]
top["Top-L/5"]=[str(round(getPrecision(rr1,rr2,fasta2,"L/5",relax_prec),2))]
top["Top-L/2"]=[str(round(getPrecision(rr1,rr2,fasta2,"L/2",relax_prec),2))]
top["Top-L"]=[str(round(getPrecision(rr1,rr2,fasta2,"L",relax_prec),2))]
top["Top-2L"]=[str(round(getPrecision(rr1,rr2,fasta2,"2L",relax_prec),2))]
"""
#string3=name+"        "+top["5"]+"          "+top["10"]+"            "+top["L/10"]+"          "+top["L/5"]+"          "+top["L/2"]+"        "+top["L"]+"         "+top["2L"]
import pandas as pd
top_list=[]
for key in top.keys():
    top_list.append(top[key])
#top_list.insert(0,name)
key_list=list(top.keys())
#print(type(key_list))
#key_list.insert(0,"Name")
df = pd.DataFrame([top_list],columns=key_list,index=None)
#df=pd.DataFrame.from_dict(top)
print (df.to_string(index=False))
#print (df.to_csv(sep="\t",index=False))
#pd.write_csv(df,)
#print(string3)
#print(string2)


