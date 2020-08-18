#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 17 16:08:55 2019

@author: farhan
"""
import os,sys
import numpy as np
from readPDBColumns import readPDB,readAtom,write2File,contents2Info,addColumn,reassembleLines,getChain

#Module to read a .atom file and find intrachain contacts:

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


#module1: Read the pdb (CB coordinates of chain X) Returns a dictionary or list
def thisReadPDB(pdbfile):
    chain_dict={}
    with open (pdbfile) as f:
        prev_chain=""
        atom_num=-1
        atom_list=[]
        fasta_res_num=0
        for line in f:
            #residue_list=[]
            #prev_residue=""
            #prev_carbon_atom=""
            #prev_res_num=-1
            if (line.startswith("ATOM")):
                atom_num+=1
                fasta_res_num+=1
                line=line.strip()
                split=line.split()
                chain=split[4].strip()
                #print(atom_num)
                if (atom_num==0):
                    prev_chain=chain
                else:
                    if (prev_chain!=chain):
                        chain_dict[prev_chain]=atom_list
                        #print(len(atom_list))
                        atom_list=[]
                        prev_chain=chain
                        fasta_res_num=1
                
                atom=split[2].strip()
                residue=split[3].strip()
                res_num=int(split[5].strip())
                x=float(split[6].strip())
                y=float(split[7].strip())
                z=float(split[8].strip())
                atom_list.append([chain,atom_num,atom,residue,res_num,x,y,z,fasta_res_num])
            else:
                continue
    chain_dict[prev_chain]=atom_list
    return chain_dict



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

def toStringList(lst): #takes the components and combines them into a single string
    strlst=[]
    for items in lst:
        l=len(items)
        s=""
        for i in range(l):
            s+=str(items[i])+" "
        #s+="\n"
        strlst.append(s)
    return strlst
"""
def createDistDistribution(distmap,atom_list_A,atom_list_B,threshold=0):
#creates a distance distribution of those atoms whose distances are less than the threshold distance    
    (lA,lB)=distmap.shape
    #print(distmap.shape)
    #print(distmap[509][510])
    distribution=[]
    distribution_list=[]
    atom_list_A_str=toStringList(atom_list_A)
    atom_list_B_str=toStringList(atom_list_B)
    for i in range (1,lA): #changed from 0 to 1
        for j in range (i+1,lB):
            #if (i==j): continue
            if (threshold==0):
                distribution.append(str(i)+" "+atom_list_A_str[i]+" "+str(j)+" "+atom_list_B_str[j]+" "+str(distmap[i][j])+"\n")
                distribution_list.append([i,atom_list_A_str[i],j,atom_list_B_str[j],distmap[i][j]])
            else:
                if (distmap[i][j]<=threshold and distmap[i][j]!=0):
                    print(i,j)
                    distribution.append(str(i)+" "+atom_list_A_str[i]+" "+str(j)+" "+atom_list_B_str[j]+" "+str(distmap[i][j])+"\n")
                    distribution_list.append([i,atom_list_A_str[i],j,atom_list_B_str[j],distmap[i][j]])
      
    return distribution,distribution_list
"""
def createDistDistribution(distmap,threshold=5):
#creates a distance distribution of those atoms whose distances are less than the threshold distance    
    (lA,lB)=distmap.shape
    distribution=[]
    rr_distribution=[]
    for i in range (1,lA): #changed from 0 to 1
        for j in range (i+1,lB):
            #if (i==j): continue
            if (threshold==0):
                distribution.append(str(i)+" "+str(j)+" 0 "+str(threshold)+" "+str(distmap[i][j])+"\n")
                rr_distribution.append(str(i)+" "+str(j)+" 0 "+str(threshold)+" "+str((1/distmap[i][j])+0.5)+"\n")
            else:
                if (distmap[i][j]<=threshold and distmap[i][j]!=0):
                    distribution.append(str(i)+" "+str(j)+" 0 "+str(threshold)+" "+str(distmap[i][j])+"\n")
                    rr_distribution.append(str(i)+" "+str(j)+" 0 "+str(threshold)+" "+str((1/distmap[i][j])+0.5)+"\n")

      
    return distribution,rr_distribution#,distribution_list

#module3: Use the output of module2 to find the docking region. Report the sequence of the docking region as well as the AA range

def refine(filename):
    contents=[]
    with open (filename,"r") as f:
        for line in f:
            split=line.strip().split()
            if (split[5]=="GLY" and split[12]=="GLY"):
                if (split[6]=="CA" and split[13]=="CA"):
                    contents.append(line.strip()+"\n")
                
            if (split[5]=="GLY" and split[12]!="GLY"):
                if (split[6]=="CA" and split[13]=="CB"):
                    contents.append(line.strip()+"\n")
                #if (split[6]=="CA" and split[13]=="CA"):
                #    backup=line.strip()
                    
                
            if (split[5]!="GLY" and split[12]=="GLY"):
                if (split[6]=="CB" and split[13]=="CA"):
                    contents.append(line.strip()+"\n")
                #if (split[6]=="CA" and split[13]=="CA"):
                #    backup=line.strip()
            
            if (split[5]!="GLY" and split[12]!="GLY"):
                #print(split[5] +" "+split[12])
                if (split[6]=="CB" and split[13]=="CB"):
                    #print(split[5] +" "+split[12])
                    contents.append(line.strip()+"\n")
                #if (split[6]=="CA" and split[13]=="CA"):
                #    backup=line.strip()
            
            #if (split[6]=="CA" or split[13]=="CB"):
            #    contents.append(line.strip())
    #for item in contents:
    #    print(item)
    return contents

def pdb2fasta(chain):
    #([chain,a_num,atom,residue,res_num,x,y,z,fasta_res_num])
    letters = {'ALA':'A','ARG':'R','ASN':'N','ASP':'D','CYS':'C','GLU':'E','GLN':'Q','GLY':'G','HIS':'H',
           'ILE':'I','LEU':'L','LYS':'K','MET':'M','PHE':'F','PRO':'P','SER':'S','THR':'T','TRP':'W',
           'TYR':'Y','VAL':'V','MSE':'M'}
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
           'TYR':'Y','VAL':'V','MSE':'M'}
    for items in split_contents:
        fst+=letters[items["res_name"]]
    return fst

def createNative(outfile):
    native=[]
    with open (outfile,"r") as f:
        for line in f:
            line=line.strip()
            split=line.split()
            i = split[3]+" "
            j = split[10]+" "
            dist=split[14]
            if (float(dist)<8): native.append(i+j+"0 8 "+dist+"\n")
    with open (outfile.replace(".txt","")+".native.txt","w") as f:
        f.write(fasta+"\n")
        f.writelines(native)
    return

def readFastaDict(fasta_dict_file="fasta_dictionary.txt"):
    fasta_dict={}
    if not (os.path.exists(fasta_dict_file)): 
        print(fasta_dict_file+" fasta dictionary file not found. Exiting")
        sys.exit(-6)
    with open (fasta_dict_file,"r") as f:
        for line in f:
            name=line.strip().split(":")[0].strip()
            fast=line.strip().split(":")[1].strip()
            fasta_dict[name]=fast
    return fasta_dict

def getFastaFromDictionary(pdbfile,fasta_dict):
    #fasta_dict=readFastaDict(fasta_dict_file)
    name=pdbfile.split("/")[-1][0:5]
    return fasta_dict[name]

#pdbfilename="/data/farhan/SoftwareTools/HomopolymerProject/data/pdb/5wvc.pdb"
pdbfilename=sys.argv[1]
#chain_1=sys.argv[2]
#chain_2=sys.argv[3]
#dist=sys.argv[4]
outfile=sys.argv[2]

#pdbfilename="/data/farhan/SoftwareTools/HomopolymerProject/data/Actin/monomer/1j6z.pdb"
#chain_1="A"
#chain_2="A"
dist=8
#outfile="Actin_out/Actin_monomer"


chain_dict=readPDB(pdbfilename)
split_contents_A=contents2Info(readPDB(pdbfilename))
split_contents_B=contents2Info(readPDB(pdbfilename))
chain_1=getChain(pdbfilename)
chain_2=getChain(pdbfilename)


cb_list=getCB(split_contents_A)
#Read fasta from fasta_dictionary.txt
#fasta=pdb2FastaFromSplitContents(cb_list)
fasta_dict_file="fasta_dictionary.txt"
fasta_dict=readFastaDict(fasta_dict_file)
fasta=getFastaFromDictionary(pdbfilename,fasta_dict)
L=len(fasta)
#print (L)
#print (fasta)

distmap=createDistanceMap(getCB(split_contents_A),getCB(split_contents_B))

distribution,rr_distribution=createDistDistribution(distmap,float(dist))

outfile_dist=outfile+"_"+chain_1+chain_2+".txt"
outfile_rr=outfile+"_"+chain_1+chain_2+".rr"
distribution.insert(0,fasta+"\n")
rr_distribution.insert(0,fasta+"\n")
with open (outfile_dist,"w") as f:
    f.writelines(distribution)

with open (outfile_rr,"w") as f:
    f.writelines(rr_distribution)

if (not os.path.isdir("intrachains")): os.mkdir("intrachains")
os.system("mv "+outfile_dist+" intrachains")
os.system("mv "+outfile_rr+" intrachains")

#np.savetxt("distmap_DF.txt",distmap)
#if len(distribution)==0: sys.exit()

#s1=toStringList(atom_list_A)
#s2=toStringList(atom_list_B)
#refined_contents=refine(outfile)
#os.remove(outfile)

#with open (outfile,"w") as f:
#    f.writelines(refined_contents)

#createNative(outfile)

#print(len(chain_dict))


#print(chain_dict["A"])

