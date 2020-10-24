# this script calculates intrachain precision for a list of proteins
#Usage: python doAll_precision_intra.py <pdb_list> TODO: <intra_folder> <dncon2_rr_folder>

import os, sys, subprocess

def getPDBNames(protein_list):
    new_list=[]
    for items in protein_list:
        name=items.strip().split("/")[-1].replace(".pdb","")
        name=name.replace(".fasta","")
        name=name.replace(".atom","")
        name=name.replace(".seq","")
        name=name.replace(".dssp","")
        new_list.append(name)
    return new_list

def refineFolderEnd(folder):
    if (not folder.endswith("/")): folder+="/"
    return folder

print ("Running: "+sys.argv[0])
protein_list_file=sys.argv[1]
#intra_folder=sys.argv[2]
#dncon2_folder=sys.argv[3]
#outfolder=sys.argv[4]

intra_folder="/data/farhan/SoftwareTools/HomopolymerProject/data/homodimers/scripts/intrachains/"
dncon2_folder="/data/farhan/SoftwareTools/HomopolymerProject/data/homodimers/scripts/dncon2_rr/"
outfolder="/data/farhan/SoftwareTools/HomopolymerProject/data/homodimers/scripts/precisions/intra/"
if (not os.path.isdir(outfolder)): os.mkdir(outfolder)

intra_folder=refineFolderEnd(intra_folder)
dncon2_folder=refineFolderEnd(dncon2_folder)
outfolder=refineFolderEnd(outfolder)

protein_list=[]
with open (protein_list_file,"r") as f:
    for line in f:
        protein_list.append(line.strip())

protein_list=getPDBNames(protein_list)

#print (protein_list)

for protein_name in protein_list:
    exitcode=os.system("ls "+intra_folder+protein_name+"*.rr")
    if (exitcode!=0): 
        os.system("echo "+protein_name+" >> no_intra_contact_list_folder.txt")
        continue
    out = subprocess.check_output("ls "+intra_folder+protein_name+"*.rr",shell = True)
    out = out.rstrip()
    out = str(out)
    out = out[1:].strip("'").strip()
    if ("filtered" in out):
        print("Here")
        split=out.split("\\n")
        out = split[-1].strip()
        #if ("\\n" in out): print ("ADFADSF")
    print ("Processing: "+out)
    print ("system Command: python getPrecision_intra_v3.py "+out+" "+dncon2_folder+protein_name+".dncon2.rr")
    os.system("python getPrecision_intra_v3.py "+out+" "+dncon2_folder+protein_name+".dncon2.rr > "+outfolder+protein_name+"_intrachain_prec.txt")
    
