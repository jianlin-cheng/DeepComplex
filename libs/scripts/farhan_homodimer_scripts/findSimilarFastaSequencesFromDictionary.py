#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 15:32:42 2020

@author: farhan
"""

#this script looks at a fasta_dictionary.txt and reports the pdb ids with similar fasta Sequences. output: common_fasta_keys.txt
#usage: python findSimilarFastaSequencesFromDictionary.py <dataset_fasta_dictionary.txt>
from loadFastaDictionary import loadFastaDictionary

import sys
file=sys.argv[1]#"dataset_fasta_dictionary.txt"
fasta_dict=loadFastaDictionary(file)
key_list_a=list(fasta_dict.keys())
key_list_b=list(fasta_dict.keys())

reverse_dict={}
for key in key_list_a:
    reverse_dict[fasta_dict[key]]=key

reversed_reverse_dict={}
for key,value in reverse_dict.items():
    reversed_reverse_dict[value]=key

new_key_list=list(reversed_reverse_dict.keys())

set_a=set(key_list_a)
set_b=set(new_key_list)

diff_set=set_a - set_b

print (len(reverse_dict))
print(len(diff_set))

common_keys=[]
diff_list=list(diff_set)
remaining_list=list(set_a - diff_set)
for key in diff_list:
    for k in remaining_list:
        if (fasta_dict[key]==fasta_dict[k]): common_keys.append(key+" , "+k+"\n")

with open("common_fasta_keys.txt","w") as f:
    f.writelines(common_keys)
    #for line in common_keys:
    



#filelist=[]
#with open (file,"r") as f:
#    for line in f:
#        filelist.append(line.strip())
