reject_list=[]
#with open ("homomer_fasta_length_30_or_less.txt","r") as f:
with open ("homomer95_fasta_length_30_or_less.txt","r") as f:
    for line in f:
        if line.startswith(">"):
            name=line.split(";")[0].strip(">").strip()
            reject_list.append(name)
print (reject_list[-1])
print (len(reject_list))

new_pairs=[]
reject_flag=False
#with open ("contacts_list_txt_contacts_perfectdimers.txt","r") as f:
with open ("contacts_list_txt_contacts_homodimers_95.txt","r") as f:
    for line in f:
        for rej in reject_list:
            if rej in line.strip():
                #print (":"+line.strip())
                reject_flag=True
                break
        if reject_flag==True:
            reject_flag=False
            continue
        new_pairs.append(line)

print (len(new_pairs))
with open ("new_homodimer95_pairs.txt","w") as f:
    f.writelines(new_pairs)