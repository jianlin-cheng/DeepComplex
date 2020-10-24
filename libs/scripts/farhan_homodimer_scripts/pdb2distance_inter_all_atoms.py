#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 17 16:08:55 2019

@author: farhan
"""
import os,sys
import numpy as np
from readPDBColumns import readPDB,readAtom,write2File,contents2Info,addColumn,reassembleLines,getChain

#Module to read a pdb of multiple chains and find interchain contact regions between all atoms:

#module1: Read the pdb (CB coordinates of chain X) Returns a dictionary or list
#filter out every atom except CB

def getCB(atom_list):
    new_list=[]
    #print(atom_list)
    """
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
    """

    return atom_list #new_list

def getCBForFasta(atom_list):
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
    

    return new_list
def prob(e):
    return e[2]


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

def filterDupes(pw):
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
        atom_num_A=infoA["serial"]
        x1=float(infoA["x"])
        y1=float(infoA["y"])
        z1=float(infoA["z"])
        for j in range(lenB):
            infoB=chainB[j]
            atom_num_B=infoB["serial"]
            x2=float(infoB["x"])
            y2=float(infoB["y"])
            z2=float(infoB["z"])
            dist=np.sqrt((x1-x2)*(x1-x2)+(y1-y2)*(y1-y2)+(z1-z2)*(z1-z2))
            if (dist!=0 and dist<=threshold): 
                pw_dist.append([int(atom_num_A),int(atom_num_B),dist])
                pw_rr.append([int(atom_num_A),int(atom_num_B),(1/dist)+0.5]) #adding 0.5 to increase coneva confidence interval
    """
    with open ("sample_test_unsorted_ASC_"+chn_A+chn_B+".rr","w") as f:
        for line in pw_rr:
            f.write(str(line[0])+" "+str(line[1])+" 0 8 "+str(line[2])+"\n")
    """        
    pw_dist.sort(key=prob,reverse=False)
    pw_rr.sort(key=prob,reverse=True)
    #pw_dist=filterDupes(pw_dist)
    #pw_rr=filterDupes(pw_rr)
    #print(len(pw_dist),len(pw_rr))
    #sys.exit()
    return pw_dist,pw_rr#atom_list_A,atom_list_B,distmap

def serail2resNum(pw):
    
    return

def toStringList(lst):
    strlst=[]
    for items in lst:
        l=len(items)
        s=""
        for i in range(l):
            s+=str(items[i])+" "
        #s+="\n"
        strlst.append(s)
    return strlst

def createDistDistribution(distmap,atom_list_A,atom_list_B,threshold=0):
#creates a distance distribution of those atoms whose distances are less than the threshold distance   
    #print(threshold)
    (lA,lB)=distmap.shape
    distribution=[]
    distribution_list=[]
    atom_list_A_str=toStringList(atom_list_A)
    atom_list_B_str=toStringList(atom_list_B)
    for i in range (lA):
        for j in range (i,lB):
            if (threshold==0):
                #print(i)
                distribution.append(str(i)+" "+atom_list_A_str[i]+" "+str(j)+" "+atom_list_B_str[j]+" "+str(distmap[i][j])+"\n")
                distribution_list.append([i,atom_list_A_str[i],j,atom_list_B_str[j],distmap[i][j]])
            else:
                if (distmap[i][j]<=threshold):
                    distribution.append(str(i)+" "+atom_list_A_str[i]+" "+str(j)+" "+atom_list_B_str[j]+" "+str(distmap[i][j])+"\n")
                    distribution_list.append([i,atom_list_A_str[i],j,atom_list_B_str[j],distmap[i][j]])
      
    return distribution,distribution_list

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

def createNative(outfile):
    native=[]
    with open (outfile,"r") as f:
        for line in f:
            line=line.strip()
            split=line.split()
            i = split[3]+" "
            j = split[10]+" "
            dist=split[14]
            native.append(i+j+dist+"\n")
    with open (outfile.replace(".txt","")+".native.txt","w") as f:
        f.writelines(native)
    return

def writeToFile(filename,pw):
    if (len(pw)==0):
        print("Not pairwise distances less than threshold found...")
        return

    with open (filename,"w") as f:
        f.write(fasta+"\n")
        for item in pw:
            string=str(item[0])+" "+str(item[1])+" 0 8 "+str(item[2])+"\n"
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
fasta_A=pdb2FastaFromSplitContents(getCBForFasta(cb_list_A))
L_A=len(fasta_A)
fasta_B=pdb2FastaFromSplitContents(getCBForFasta(cb_list_B))
L_B=len(fasta_B)

print(fasta_A+"\n"+fasta_B)

if (fasta_A != fasta_B):
    print ("Fasta sequences of both files are not same...chosing the one with highest length")
    if (L_A > L_B):
        fasta=fasta_A
    else:
        fasta=fasta_B
else:
    fasta=fasta_A

#print("Boss!!!")

#atom_list_A,atom_list_B,distmap=createDistanceMap(chain_dict["D"],chain_dict["F"])
#This one
#atom_list_A,atom_list_B,distmap=createDistanceMap(getCB(chain_dict[chain_1]),getCB(chain_dict[chain_2]))

#print(len(chain_dict[chain_2]))

#print("A:",len(getCB(chain_dict[chain_1])))
#print("B:",len(getCB(chain_dict[chain_2])))

#x=getCB(chain_dict[chain_1])

#fasta=pdb2fasta(chain_dict[chain_1])

#print(type(x))
#with open ("CD_atomsonly.txt","w") as f:
#    for item in x:
        
    
#print(x[0])

pw_dist,pw_rr=createDistanceMapCB(cb_list_A,cb_list_B)
#distribution,distribution_list=createDistDistribution(distmap,atom_list_A,atom_list_B,8)
#This one
#distribution,distribution_list=createDistDistribution(distmap,atom_list_A,atom_list_B,int(dist))

#print(len(chain_dict[chain_1]))
#print(len(getCB(chain_dict[chain_1])))
#sys.exit()

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



#if (np.array_equal(np.zeros(distmap.shape),distmap)): #len(distribution)==0: 
#    sys.exit(chain_1+" and "+chain_2+"Has no interactions")
"""
with open (outfile,"w") as f:
    f.writelines(distribution)

s1=toStringList(atom_list_A)
s2=toStringList(atom_list_B)
refined_contents=refine(outfile)
os.remove(outfile)
if len(refined_contents)!=0:
    with open (outfile,"w") as f:
        f.writelines(refined_contents)
    createNative(outfile)
"""

#print(chain_dict["A"])

