#this script creates a training fasta dictionary for the final dataset
#it reads the all_8886_protein.txt list and searches the final_fasta_dictionary.txt and the fasta_dictionary.txt
#creates a fasta_dictionary

from loadFastaDictionary import loadFastaDictionary

def checkIfInList(name,lst):
    name_list=[]
    for item in lst:
        if name in item:
            name_list.append(item)
    name_dict={}
    name_dict[name]=name_list
    return name_dict

def checkFastaSimilarity(lst,fasta_dict):
    for i in range(1,len(lst)):
        if (fasta_dict[lst[0]]!=fasta_dict[lst[i]]): return False
    return True

all_list_file="all_8886_protein_list.txt"
all_list=[]

with open (all_list_file,"r") as f:
    for line in f:
        all_list.append(line.strip())

final_fasta_dictionary_file="final_combined_fasta_dictionary.txt" #slight different fasta seq in chains
final_fasta_dict=loadFastaDictionary(final_fasta_dictionary_file)
final_dict_keys=list(final_fasta_dict.keys())

fasta_dict_file="fasta_dictionary.txt"
fasta_dict=loadFastaDictionary(fasta_dict_file)
fasta_dict_keys=list(fasta_dict.keys())

dataset_fasta_dict={}

for pdb in all_list:
    if (pdb in final_dict_keys):
        dataset_fasta_dict[pdb]=final_fasta_dict[pdb]
        
    else:
        chain_fasta_dict=checkIfInList(pdb,fasta_dict_keys) #same fasta seq in chains
        if checkFastaSimilarity(chain_fasta_dict[pdb],fasta_dict):
            dataset_fasta_dict[pdb]=fasta_dict[chain_fasta_dict[pdb][0]]
        else:
            continue
        
with open ("dataset_fasta_dictionary.txt","w") as f:
    for key,items in dataset_fasta_dict.items():
        f.write(key+":"+items+"\n")

dataset_keys=list(dataset_fasta_dict.keys())
with open ("dataset_names.txt","w") as f:
    for key in dataset_keys:
        f.write(key+"\n")
