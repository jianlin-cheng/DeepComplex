#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 17 16:08:55 2019

@author: farhan
"""
import os,sys
import numpy as np
from readPDBColumns import readPDB,readAtom,write2File,contents2Info,addColumn,reassembleLines,getChain

#Module to read a pdb of multiple chains and find interchain contact regions:

#module1: Read the pdb (CB coordinates of chain X) Returns a dictionary or list
#filter out every atom except CB

def getCB(atom_list):
    new_list=[]
    #print(atom_list)
    prev_res_num=atom_list[0]["res_num"].strip()
    added=False
    keep={}
    for tup in atom_list:
        if (prev_res_num==tup["res_num"].strip() and added==True):
            keep={}
            continue       
        if (prev_res_num!=tup["res_num"].strip() and added==False): #No CB found. So add the CA
                new_list.append(keep)
                keep={}
                added=False
                prev_res_num=tup["res_num"].strip()
        if (prev_res_num!=tup["res_num"].strip() and added==True): #Reached the next residue
                keep={}
                added=False
                prev_res_num=tup["res_num"].strip()
        if (prev_res_num==tup["res_num"].strip() and added==False):

            if ("CA" in tup["atom_name"]):
                keep=tup
            if ("GLY" in tup["res_name"] and "CA" in tup["atom_name"]):
                new_list.append(tup)
                added=True
                prev_res_num=tup["res_num"].strip()
                continue
            else:
                if (tup["atom_name"].strip()=="CB"):
                    new_list.append(tup)
                    added=True
                    prev_res_num=tup["res_num"].strip()
                    continue
    if (added==False): new_list.append(keep)
    #print (new_list[-1])
    return new_list


def prob(e):
    return e[4]


#module2: Construct a distance distribution between each atom of chains X and Y.
def createDistanceMap(chainA,chainB):
    lenA=len(chainA)
    lenB=len(chainB)
    distmap=np.zeros((L+1,L+1))
    #print(distmap.shape)
    atom_list_A=[]
    atom_list_B=[]
    for i in range(lenA):
        infoA=chainA[i]
        chain_A=infoA["chain"]
        res_num_A=infoA["res_num"]
        atom_num_A=infoA["serial"]
        residue_A=infoA["res_name"]
        atom_A=infoA["atom_name"]
        fasta_res_num_A=infoA["res_num"]
        atom_list_A.append((chain_A,fasta_res_num_A,res_num_A,atom_num_A,residue_A,atom_A))
        x1=float(infoA["x"])
        y1=float(infoA["y"])
        z1=float(infoA["z"])
        for j in range(i,lenB):
            #print(j)
            infoB=chainB[j]
            chain_B=infoB["chain"]
            res_num_B=infoB["res_num"]
            atom_num_B=infoB["serial"]
            residue_B=infoB["res_name"]
            atom_B=infoB["atom_name"]
            fasta_res_num_B=infoB["res_num"]
            x2=float(infoB["x"])
            y2=float(infoB["y"])
            z2=float(infoB["z"])
            #atom_list_A.append((infoA[1],infoA[2]))
            
            atom_list_B.append((chain_B,fasta_res_num_B,res_num_B,atom_num_B,residue_B,atom_B))
            #atom_list_B.append((infoB[1],infoB[2]))
            #distmap[i][j]=np.sqrt((x1-x2)*(x1-x2)+(y1-y2)*(y1-y2)+(z1-z2)*(z1-z2))
            #distmap[j][i]=np.sqrt((x1-x2)*(x1-x2)+(y1-y2)*(y1-y2)+(z1-z2)*(z1-z2))
            distmap[int(res_num_A)][int(res_num_B)]=np.sqrt((x1-x2)*(x1-x2)+(y1-y2)*(y1-y2)+(z1-z2)*(z1-z2))
            distmap[int(res_num_B)][int(res_num_A)]=np.sqrt((x1-x2)*(x1-x2)+(y1-y2)*(y1-y2)+(z1-z2)*(z1-z2))
    return distmap

def filterDupes(pw): #not needed. Removes cross [(x,y),(y,x)] contacts if occuring consecutively
    new_pw=[]
    #for i in range(0,len(pw)-2,2):
    i=0
    while (i<len(pw)-1):
        x1=pw[i][0]
        y1=pw[i][1]
        x2=pw[i+1][0]
        y2=pw[i+1][1]
        if (x1==y2 and x2==y1):
            new_pw.append(pw[i])
        i+=1
            
        
    return new_pw


def createDistanceMapCB(chainA,chainB,threshold=6):
    lenA=len(chainA)
    lenB=len(chainB)
    #k=0
    #if (chain_1==chain_2): k=1
    #distmap=np.zeros((lenA,lenB))
    pw_dist=[]
    pw_rr=[]
    chn_A=""
    chn_B=""
    for i in range(lenA):
        infoA=chainA[i]
        res_num_A=infoA["res_num"]
        serial_A=infoA["serial"].strip()
        x1=float(infoA["x"])
        y1=float(infoA["y"])
        z1=float(infoA["z"])
        for j in range(lenB):
            infoB=chainB[j]
            res_num_B=infoB["res_num"]
            serial_B=infoB["serial"].strip()
            x2=float(infoB["x"])
            y2=float(infoB["y"])
            z2=float(infoB["z"])
            dist=np.sqrt((x1-x2)*(x1-x2)+(y1-y2)*(y1-y2)+(z1-z2)*(z1-z2))
            #print (dist)
            if (dist!=0 and dist<=threshold):
                pw_dist.append([int(res_num_A),int(res_num_B),0,threshold,dist])
                pw_rr.append([int(res_num_A),int(res_num_B),0,threshold,(1/dist)+0.5]) #adding 0.5 to increase coneva confidence interval
    pw_dist.sort(key=prob,reverse=False)
    pw_rr.sort(key=prob,reverse=True)
    #pw_dist=filterDupes(pw_dist)
    #pw_rr=filterDupes(pw_rr)

    return pw_dist,pw_rr#atom_list_A,atom_list_B,distmap

#module3: Use the output of module2 to find the docking region. Report the sequence of the docking region as well as the AA range

def writeToFile(filename,pw):
    if (len(pw)==0):
        print("No pairwise distances less than threshold found...")
        sys.exit(-1)
        return

    with open (filename,"w") as f:
        f.write(fasta+"\n")
        for item in pw:
            string=str(item[0])+" "+str(item[1])+" "+str(item[2])+" "+str(item[3])+" "+str(item[4])+"\n"
            f.write(string)
    return

def pdb2fasta(chain):
    #([chain,a_num,atom,residue,res_num,x,y,z,fasta_res_num])
    letters = {'ALA':'A','ARG':'R','ASN':'N','ASP':'D','CYS':'C','GLU':'E','GLN':'Q','GLY':'G','HIS':'H',
           'ILE':'I','LEU':'L','LYS':'K','MET':'M','PHE':'F','PRO':'P','SER':'S','THR':'T','TRP':'W',
           'TYR':'Y','VAL':'V'}
    fst=""
    #prev=""
    prev_res_num=0
    chain_CB=getCB(chain)
    for item in chain_CB:
        if (int(item[4])-prev_res_num==1):
            fst+=letters[item[3]]
            prev_res_num=int(item[4])
            
        else:
            fst+="-"*(int(item[4])-prev_res_num-1)
            fst+=letters[item[3]]
            prev_res_num=int(item[4])
            
    #print(len(fst))
    return fst

def pdb2FastaFromSplitContents(split_contents):
    fst=""
    letters = {'ALA':'A','ARG':'R','ASN':'N','ASP':'D','CYS':'C','GLU':'E','GLN':'Q','GLY':'G','HIS':'H',
           'ILE':'I','LEU':'L','LYS':'K','MET':'M','PHE':'F','PRO':'P','SER':'S','THR':'T','TRP':'W',
           'TYR':'Y','VAL':'V'}
    for items in split_contents:
        fst+=letters[items["res_name"]]
    return fst
        

#pdbfilename="/data/farhan/SoftwareTools/HomopolymerProject/data/pdb/5wvc.pdb"
pdbfile_A=sys.argv[1]
pdbfile_B=sys.argv[2]

#chain_1=sys.argv[2]
#chain_2=sys.argv[3]
dist=sys.argv[3]
outfile=sys.argv[4]
#fasta=sys.argv[6]

split_contents_A=contents2Info(readPDB(pdbfile_A))
split_contents_B=contents2Info(readPDB(pdbfile_B))
chain_1=getChain(pdbfile_A)
chain_2=getChain(pdbfile_B)


cb_list_A=getCB(split_contents_A)
cb_list_B=getCB(split_contents_B)
fasta_A=pdb2FastaFromSplitContents(cb_list_A)
L_A=len(fasta_A)
fasta_B=pdb2FastaFromSplitContents(cb_list_B)
L_B=len(fasta_B)
print (fasta_A)
if (fasta_A != fasta_B):
    print ("Fasta sequences of both files are not same...chosing the one with highest length")
    if (L_A > L_B):
        fasta=fasta_A
    else:
        fasta=fasta_B
else:
    fasta=fasta_A

"""
for items in cb_list_A:
    if (items["serial"].strip()=="376"): print (items["z"]+" "+items["res_num"]+" "+items["res_name"])
    if (items["serial"].strip()=="367"): print (items["z"]+" "+items["res_num"]+" "+items["res_name"])
    if (items["serial"].strip()=="343"): print (items["z"]+" "+items["res_num"]+" "+items["res_name"])

for items in cb_list_B:
    if (items["serial"].strip()=="423"): print (items["z"]+" "+items["res_num"]+" "+items["res_name"])
    if (items["serial"].strip()=="429"): print (items["z"]+" "+items["res_num"]+" "+items["res_name"])
    if (items["serial"].strip()=="435"): print (items["z"]+" "+items["res_num"]+" "+items["res_name"])
"""
#print (len(cb_list_A),len(cb_list_A))
pw_dist,pw_rr=createDistanceMapCB(cb_list_A,cb_list_B,8)

#print (len(pw_dist))
print ([chain_1,chain_2])
for items in pw_dist:
    print (items)
    #if (items[0]==45 and items[1]==51): print (items)
    #if (items[0]==44 and items[1]==51): print (items)
    #if (items[0]==41 and items[1]==51): print (items)
    #if (items[0]==41 and items[1]==53): print (items)
    #if (items[0]==44 and items[1]==52): print (items)
    #if (items[0]==45): print (items)


#np.savetxt("distmap_DF.txt",distmap)


outfile_dist=outfile.replace(".txt","")+"_dist_"+chain_1+chain_2+".txt"
outfile=outfile+"_"+chain_1+chain_2+".txt"
#print(outfile_dist)
#outfile_dist=outfile+"_dist_"+chain_1+chain_2+".txt"
write_flag=True
for item in pw_dist:
    if (item[2]<8):
        write_flag=True
        break

if (write_flag):
    writeToFile(outfile_dist,pw_dist)
    writeToFile(outfile.replace(".txt",".rr"),pw_rr)



