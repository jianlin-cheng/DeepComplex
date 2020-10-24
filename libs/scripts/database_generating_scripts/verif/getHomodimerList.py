
"""
homo_list=[]
with open ("/data/farhan/SoftwareTools/HomopolymerProject/DeepComplex/scripts/database_generating_scripts/verif/homo_cdhit/homo100","r") as f:
    for line in f:
        if line.startswith(">"):
            homo_list.append(line.strip().split(";")[0].lstrip(">"))

all_pairs=[]
with open ("all_homodimer_contact_pairs.txt","r") as f:
    for line in f:
        all_pairs.append(line.strip())

#print (homo_list[0])
print (len(all_pairs))
print (len(homo_list))
homo_keep=[]

for homo in homo_list:
    for pair in all_pairs:
        if homo in pair:
            homo_keep.append(pair+"\n")

print (len(homo_keep))
with open ("homo_keep_pairs.txt","w") as f:
    f.writelines(homo_keep)
"""
homo_keep=[]
with open ("homo_keep_pairs.txt","r") as f:
    for line in f:
        homo_keep.append(line)

print (len(homo_keep))
print(len(set(homo_keep)))
homo_keep=list((set(homo_keep)))

with open ("homo_keep_pairs_nr.txt","w") as f:
    f.writelines(homo_keep)

