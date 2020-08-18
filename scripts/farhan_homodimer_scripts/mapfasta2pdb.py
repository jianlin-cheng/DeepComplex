# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
#this script does a few things:
#1. Takes a pdb and an rr file. Then maps the sequence in the fasta section of the rr file to the respective residue positions in pdb
#2. Corrects the input fasta by using the pdb file.

import os,sys

def readPDB(file):
    contents=[]
    with open (file,"r") as f:
        for line in f:
            if (line.startswith("ATOM")):
                contents.append(line)
    return contents

def getChain(contents,chain): #gets the coordinates and other information of a particular chain from multimer pdb
    chain_list=[]
    prev_chain=""

    for line in contents:
        split=line.strip().split()
        #print(chain+" "+split[4])
        if (chain==split[4]):
            chain_list.append(line)
        else:
            continue
    return chain_list
 
def pdb2dict(pdb_file): #creates a dictionary and list for the residues and their positions in the pdb
    pdb_dict={}
    pdb_list=[]
    prev_res_num=""
    res_num=""
    with open (pdb_file,"r") as f:
        for line in f:
            if (line.startswith("ATOM")):
                split=line.strip().split()
                aa=letters[split[3]]
                res_num=split[5]
                atom=split[2]
            if (prev_res_num!=res_num):
                pdb_dict[int(res_num)]=aa
                pdb_list.append((res_num,aa))
                prev_res_num=res_num
    
    return pdb_dict, pdb_list

           
def writePDB(filename,chain_list): #writes the list to a file
    with open(filename,"w") as f:
        f.writelines(chain_list)
"""
def map2dict(fasta,pdb_dict): #Maps the residues in the fasta to the respective positions in the pdb. 
    #This is used later to correct the rr files
    map_dict={}
    L = len(fasta)
    max_val=max(pdb_dict.keys())
    print(L,max_val)
    i=0
    
    for key in sorted(pdb_dict.keys()):
        pdb_res_num=str(key)
        aa_pdb=pdb_dict[key]
        while (i<L):
            if (fasta[i]==aa_pdb):
                map_dict[str(i+1)]=pdb_res_num
                i+=1
                break
            i+=1
    
    return map_dict
"""
#modify the following: may not be this case
def map2dict(fasta,pdb_dict): #Maps the residues in the fasta to the respective positions in the pdb. 
    #This is used later to correct the rr files
    map_dict={}
    L = len(fasta)
    fasta=fasta.strip()
    max_val=max(pdb_dict.keys())
    #print(L,max_val)
    i=0
    j=0
    string=""
    #string_L="-"*L
    #res_num_key=sorted(pdb_dict.keys())
    key=sorted(pdb_dict.keys())
    start_i=0
    while (j<len(key)):
        
        pdb_res_num=str(key[j])
        aa_pdb=pdb_dict[key[j]].strip()
        
        while (i<L):
            if (fasta[i]==aa_pdb): #if equal no need to change
                string=string.strip()+(aa_pdb).strip()
                map_dict[str(i+1)]=pdb_res_num
                i+=1
                break
            else:
                
                if (j==0): diff=1
                if (j!=0): diff=abs(key[j]-key[j-1])
                if (diff==1):
                    
                    start_i+=1 #move to next position in original fasta
                    i=start_i #restart from next position in original fasta
                    j=-1 #start aligning from beginning of pdb_fasta
                    string=""
                    map_dict={}
                    for k in range (start_i):#add this many gaps
                        string+="-"
                    string=string.strip()
                    break
                    
                else:
                    i+=diff #missing in pdb. Move to next location by inserting gaps
                    for k in range (diff):
                        string=string.strip()+"-"
                    string=string.strip()
                    break
            
            i+=1
        j+=1
        
    if (len(fasta)==len(string)): print ("Ok")
    print(fasta)
    print(string)
    #with open ("temp.txt","w") as f:
    #    f.write(string)
    #print (len(string))
    
    return map_dict

def readFastaFile(file): #reads the fasta sequence from the fasta file
    string=""
    with open (file,"r") as f:
        for line in f:
            if line.startswith(">"): continue
            string+=line.strip()
    return string

def writeMapFile(file,map_string): #writes the output of the map2dict to a file
    map_string=str(map_dict)
    map_string=map_string.strip("{").strip("}").replace("'","")
    
    #if ("," in map_string): print(map_string)
    split=map_string.split(",")
    
    with open(file,"w") as f:
        for items in split:
            f.write(items.strip()+"\n")

def getMissingAA(fasta,pdb_dict): #gets the list and position of the missing residues or disorders
    
    return

#this will make a fasta sequence from the pdb file with '-' for missing residues
def pdb2fasta(pdb_file,chain="A"):
    file_contents=readPDB(pdb_file)
    chain_X=getChain(file_contents,chain)
    writePDB("temp.pdb",chain_X)
    pdb_dict_X,pdb_list_X=pdb2dict("temp.pdb")
    os.remove("temp.pdb")
    #string=makeFastaPDBDict(pdb_dict_X)
    string=makePDBFasta(pdb_dict_X)
    print(string)
    return string

#this will make a fasta sequence from the pdb_dict with '-' for missing residues
def makeFastaPDBDict(pdb_dict):
    string=""
    keys= sorted(pdb_dict.keys())
    curr_pos=1
    
    for key in keys:
        if (curr_pos<key):
            for i in range (key-curr_pos-1):
                string+="-"
            string+=pdb_dict[key]
            curr_pos=key+1
        elif (curr_pos==key):
            string+=pdb_dict[key]
            curr_pos=key+1
        else:
            print("Something wrong!")
            
    return string

def makePDBFasta(pdb_dict,fasta=""): #reads the pdb and generates a fasta sequence with gaps if applicable
    l=len(fasta)
    if (max(pdb_dict.keys())>l): l=max(pdb_dict.keys())
    string=""
    for i in range(l):
        string+="-"
    string_new=""
    for key in sorted(pdb_dict.keys()):
        string_new=string[:key-1]+pdb_dict[key]+string[key:]
        string=string_new
    print(string_new)
    #print (len(fasta),len(string_new))
    return string_new

def alignFastas(fasta,fasta_pdb,pdb_dict): 
    s=fasta_pdb
    l=len(fasta)
    i=0
    max_val=max(pdb_dict.keys())
    #string=""
    if (l>len(s)):
        while (i<l):
            if (s[i]=="-" or s[i]==fasta[i]):
                i+=1
                continue
            if (s[i]!=fasta[i]):
                #string=s[:i-1]+"-"+s[i:] #insert a gap at the beginning
                s="-"+s #insert a gap at the beginning
                i=0
    
    
    
    return s
    

# one letter code for AA
letters = {'ALA':'A','ARG':'R','ASN':'N','ASP':'D','CYS':'C','GLU':'E','GLN':'Q','GLY':'G','HIS':'H',
           'ILE':'I','LEU':'L','LYS':'K','MET':'M','PHE':'F','PRO':'P','SER':'S','THR':'T','TRP':'W',
           'TYR':'Y','VAL':'V'}


#print("A")
#contents=readPDB("4zuk.pdb")                
#chain_A=getChain(contents,"A")
#chain_B=getChain(contents,"B")

#writePDB("4zuk_chain_A.pdb",chain_A)
#writePDB("4zuk_chain_B.pdb",chain_B)

#folder_out="/data/farhan/SoftwareTools/HomopolymerProject/scripts/4zuk_out/"
"""
chainA_pdb=sys.argv[1]
fastafile=sys.argv[2]
outdir=sys.argv[3]

if (not outdir.endswith("/")): outdir+="/"
pdb_dict,pdb_list=pdb2dict(chainA_pdb)
fasta=readFastaFile(fastafile)
map_dict=map2dict(fasta,pdb_dict)
writeMapFile(outdir+"mapdict.txt",str(map_dict))
"""
#print(makeFastaPDBDict(pdb_dict))
#print(len(makeFastaPDBDict(pdb_dict)))


"""
folder="/data/farhan/SoftwareTools/HomopolymerProject/data/4zuk/monomer/"
outdir="/data/farhan/SoftwareTools/HomopolymerProject/scripts/4zuk_out/"

pdb_dict,pdb_list=pdb2dict(folder+"4zuk_chainA.pdb")
fasta=readFastaFile(folder+"4zuk_chainA.fasta")
map_dict=map2dict(fasta,pdb_dict)
writeMapFile(outdir+"mapdict.txt",str(map_dict))
print(makeFastaPDBDict(pdb_dict))
print(len(makeFastaPDBDict(pdb_dict)))
"""
"""
folder="/data/farhan/SoftwareTools/HomopolymerProject/data/4zuk/monomer/"
outdir="/data/farhan/SoftwareTools/HomopolymerProject/scripts/4zuk_out/"

pdb_dict,pdb_list=pdb2dict(folder+"4zuk_chainA_mock.pdb")
fasta=readFastaFile(folder+"4zuk_chainA.fasta")
pdb_fasta=makePDBFasta(pdb_dict,fasta)
map_dict=map2dict(fasta,pdb_dict)
"""
#writeMapFile(outdir+"mapdict.txt",str(map_dict))

#print(makeFastaPDBDict(pdb_dict))
#print(len(makeFastaPDBDict(pdb_dict)))

#for i in sorted(pdb_dict.keys()):
#    print(i,pdb_dict[i])