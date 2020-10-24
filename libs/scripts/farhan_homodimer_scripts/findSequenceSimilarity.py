#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 20 19:38:36 2020

@author: farhan
"""

#this script will check aligned sequences to find % similarity. 
#usage: python findSequenceSimilarity.py 
#please change any folder paths below

import os,sys

def findNumOfGaps(seq):
    l=len(seq)
    gaps=0
    for i in range(l):
        if (seq[i]=="-"):
            gaps+=1
    return gaps

def calculatePercentageSimilarity(seq1,seq2):
    l = len(seq1)
    mismatch=0
    for i in range(l):
        if (seq1[i]!=seq2[i]): 
            mismatch+=1
            #print (i,seq1[i],seq2[i])
    
    return 100-(100*mismatch/l)

def getInclusionFlag(seq1,seq2,threshold=90):
    similarity=calculatePercentageSimilarity(seq1,seq2)
    if (similarity<threshold): return False
    return True

def seqDict2Fasta(seq_dict):
    fasta=""
    for key in seq_dict.keys():
        fasta+=seq_dict[key]
    return fasta

def writeMap(func,filename):
    with open (filename,"w") as f:
        for line in func:
            f.write(line+"\n")

def mapFunctionGenerator(seq1,seq2,unaligned_seq1,unaligned_seq2):#generates a mapping function old_fasta_sequence -> aligned_fasta_sequence
    l=len(seq1)
    seq1_dict={}
    seq1_list=[]
    seq2_dict={}
    seq2_list=[]
    for i in range(l):
        if (seq1[i]!="-"): 
            seq1_dict[str(i+1)]=seq1[i]
            seq1_list.append(str(i+1)+" : "+seq1[i])
        if (seq2[i]!="-"): 
            seq2_dict[str(i+1)]=seq2[i]
            seq2_list.append(str(i+1)+" : "+seq2[i])
    
    if (seqDict2Fasta(seq1_dict)!=unaligned_seq1): sys.exit("Unaligned sequences dont match!")
    if (seqDict2Fasta(seq2_dict)!=unaligned_seq2): sys.exit("Unaligned sequences dont match!")
    
    map_seq1_list=[]
    for i in range(len(unaligned_seq1)):
        map_seq1_list.append(str(i+1)+" : "+seq1_list[i])
    map_seq2_list=[]
    for i in range(len(unaligned_seq2)):
        map_seq2_list.append(str(i+1)+" : "+seq2_list[i])
    
    if (len(seq1_dict)==len(unaligned_seq1)): print ("Yes")
    if (len(seq2_dict)==len(unaligned_seq2)): print ("Yes")
    
    return map_seq1_list, map_seq2_list

def readFastaDict(fasta_dict_file):
    fasta_dict={}
    with open (fasta_dict_file,"r") as f:
        for line in f:
            fasta_dict[line.strip().split(":")[0].strip()]=line.strip().split(":")[1].strip()
    return fasta_dict

def getChain(filename):
    return filename.split("/")[-1][4]

#x="VVKFTKSEALHKEALEHIVGGVNSPSRSFKAVGGGAPIAERGKGAYFWDVDGNKYIDYLAAYGPIITGHAHPHITKAITTAAENGVLYGTPTALEVKFAKLKEAPALDKVRFVNSGTEAVTTIRVARAYTGRTKIKFAGCYHGHSDLVLVALGTPDSAGVPQSIAQEVITVPFNNVETLKEALDKWGHEVAAILVEPIVGNFGIVEPKPGFLEKVNELVHEAGALVIYDEVITAFRFYGGAQDLLGVTPDLTALGVIGGGLPIGAYGGKKEIEQVAPLGPAYQAGTAGNPASASGIACLEVLQQEGLYEKLDELGATLEKGILEQAAKHNIDITLNRLKGALTVYFTTNTIEDYDAAQDTDGEFGKFFKLLQEGVNLAPSKYEAWFLTTEHTKEDIEYTIEAVGRAFAALADN"
#y="VVKFTKSEALHKEALEHIVGGVNSPSRSFKAVGGGAPIAERGKGAYFWDVDGNKYIDYLAAYGPIITGHAHPHITKAITTAAENGVLYGTPTALEVKFAKLKEAPALDKVRFVNSGTEAVTTIRVARAYTGRTKIKFAGCYHGHSDLVLVAAGSGPSTLGTPDSAGVPQSIAQEVITVPFNNVETLKEALDKWGHEVAAILVEPIVGNFGIVEPKPGFLEKVNELVHEAGALVIYDEVITAFRFYGGAQDLLGVTPDLTALGVIGGGLPIGAYGGKKEIEQVAPLGPAYQAGTAGNPASASGIACLEVLQQEGLYEKLDELGATLEKGILEQAAKHNIDITLNRLKGALTVYFTTNTIEDYDAAQDTDGEFGKFFKLLQEGVNLAPSKYEAWFLTTEHTKEDIEYTIEAVGRAFAALADNK"
x=sys.argv[1]
y=sys.argv[2]
pdb_id=sys.argv[3]
key_x=sys.argv[4]
key_y=sys.argv[5]
mappingfolder="./reindexed_mapping_function/"#+pdb_id
if not(os.path.isdir(mappingfolder)): os.makedirs(mappingfolder)
if not(os.path.isdir("./aligned_seq_folder")): os.makedirs("./aligned_seq_folder")
print("Print Aligning sequences: ")
os.system("python sequenceAlign.py "+key_x+" "+x+" "+key_y+" "+y+" > aligned_seq.txt")
os.system("python sequenceAlign.py "+key_x+" "+x+" "+key_y+" "+y+" > ./aligned_seq_folder/"+pdb_id+"_"+getChain(key_x)+getChain(key_y)+".aln.txt")
"""
#Read the fasta_dictionary and get the atom file names of the chains
fasta_dict=readFastaDict("fasta_dictionary.txt")
key_list=fasta_dict.keys()
this_key_list=[]
for key in key_list:
    if pdb_id in key:
        this_key_list.append(key)
"""

"""
os.system("ls ./new_atom/"+pdb_id+"/* > reindex_atom_list.txt")
atom_file_list=[]
with open ("reindex_atom_list.txt","r") as f:
    for line in f:
        atom_file_list.append(line.strip())
"""
#Change the folders below accordingly
atom_folder="./new_atom/" #folder for atom files
output_folder="./reindexed_atom/" #output for atom files after reindexing
atom_file_x=atom_folder+key_x+".atom"
atom_file_y=atom_folder+key_y+".atom"
outputfile_x=output_folder+key_x+".atom"
outputfile_y=output_folder+key_y+".atom"
thres=90

alignment=[]
with open ("aligned_seq.txt","r") as f:
    for line in f:
        alignment.append(line.strip().split(":")[-1].strip())
print("Aligned sequences are:")
print (alignment[0])
print (alignment[1])
if (len(alignment[0])!=len(alignment[1])): 
    os.system("echo "+pdb_id+" > mismatch_fasta_aligned_length_different.txt")
    sys.exit("Aligned Sequence lengths dont match")

#print (findNumOfGaps(alignment[0]))
#print (findNumOfGaps(alignment[1]))

#print (calculatePercentageSimilarity(alignment[0],alignment[1]))
#print (getInclusionFlag(alignment[0],alignment[1]))
print("Calculating percentage similarity...")
include=getInclusionFlag(alignment[0],alignment[1],threshold=thres)

if (include):
    print("Done!")
    print("Creating mapping function for both alignments...")
    mapFunc_A,mapFunc_B=mapFunctionGenerator(alignment[0],alignment[1],x,y)
    print("Done!")
    print("Writing to file...")
    writeMap(mapFunc_A,mappingfolder+key_x+"_map.txt") 
    writeMap(mapFunc_B,mappingfolder+key_y+"_map.txt")
else:
    os.system("echo "+pdb_id+" >> exclusion_list_not_"+str(thres)+".txt")
    sys.exit("Sequence similarity is < 90%. Excluding "+pdb_id+" "+str(include))
print("Done!")
mapfile_A=mappingfolder+key_x+"_map.txt"
mapfile_B=mappingfolder+key_y+"_map.txt"
#print (atom_file_x)
#print (atom_file_y)
#print (mapfile_A)
#print (mapfile_B)
#print (outputfile_x)
#print (outputfile_y)
###########################
#Here the .atom files are reindexed if needed
#Unremark the following if you want to reindex the .atom files
"""
print("Reindexing the atom files...")
exit_code=os.system("python reindex.py "+atom_file_x+" "+mapfile_A+" "+outputfile_x)
exit_code=os.system("python reindex.py "+atom_file_y+" "+mapfile_B+" "+outputfile_y)
print("Finished!")
"""
