#this script does the interchain precision of two cmaps (true and predicted) given a list of pdb codes
#usge: doAllPrecision_inter_twocmaps <listfile> <true_interchain_folder> <predicted_interchain_folder>

import os, sys

listfile=os.path.abspath("all_training_protein_list.txt")
true_interchain_folder=os.path.abspath("/data/farhan/SoftwareTools/HomopolymerProject/data/homodimers/scripts/interchains")+"/" #true interchain
outfolder="./rand_precision_outputs/"
pred_interchain_folder=os.path.abspath("/data/farhan/SoftwareTools/HomopolymerProject/DeepComplex/training/dncon2_model/scripts/random_precisions")+"/" #dncon2 folder
if not os.path.isdir(outfolder): os.makedirs(outfolder)
full_list=[]
with open (listfile,"r") as f:
    for line in f:
        full_list.append(line.strip())

rand_file_dict={}
with open ("random_precision_filelist.txt","r") as f:
    for line in f:
        name=line.strip().split("_")[0]
        rand_file_dict[name]=line.strip()

true_file_dict={}
with open ("true_inter_list.txt","r") as f:
    for line in f:
        name=line.strip().split("_")[0]
        true_file_dict[name]=line.strip()

print (len(full_list))
print (len(rand_file_dict))
print(len(true_file_dict))

for pdb in full_list:
    print ("now processing: "+pdb)
    print ("Running command: "+"python getPrecision_inter_twocmaps_v2.py "+true_interchain_folder+true_file_dict[pdb]+" "+pred_interchain_folder+rand_file_dict[pdb]+" > "+outfolder+pdb+"_inter_prec.txt")
    exit_code=os.system("python getPrecision_inter_twocmaps_v2.py "+true_interchain_folder+true_file_dict[pdb]+" "+pred_interchain_folder+rand_file_dict[pdb]+" > "+outfolder+pdb+"_inter_prec.txt")
    if (exit_code!=0):os.system("echo '"+pdb+"' >> problems.txt")
    #break

#sys.exit()