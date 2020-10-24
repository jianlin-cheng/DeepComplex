import os

def reverseDict(d):
    new_dict={}
    for key, value in d.items():
        new_dict[value]=key
    return new_dict


AB_dict={}
BA_dict={}

with open ("new_hetero100_AB","r") as f:
    for line in f:
        if (line.startswith(">")):
            fasta=f.readline().strip()
            AB_dict[line.strip()]=fasta

with open ("new_hetero100_BA","r") as f:
    for line in f:
        if (line.startswith(">")):
            fasta=f.readline().strip()
            BA_dict[line.strip()]=fasta

print (len(AB_dict))
print (len(BA_dict))

reversed_AB_dict=reverseDict(AB_dict)
reversed_BA_dict=reverseDict(BA_dict)

print(len(reversed_AB_dict))
print(len(reversed_BA_dict))

key_list_AB=list(reversed_AB_dict.keys())
key_list_BA=list(reversed_BA_dict.keys())

similar_list=[]

for key_i in key_list_AB:
    for key_j in key_list_BA:
        if key_i == key_j:  
            similar_list.append(reversed_AB_dict[key_i]+"\t\t"+reversed_BA_dict[key_j]+"\n")
            similar_list.append(key_i+"\n")
            similar_list.append(key_j+"\n")

with open ("same_seq_found_new.txt","w") as f:
    f.writelines(similar_list)