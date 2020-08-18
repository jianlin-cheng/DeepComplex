# this script calculates interchain precision for a list of proteins
#Usage: python doAll_precision_inter.py <pdb_list> TODO: <intra_folder> <dncon2_rr_folder>

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

def getSystemOutput(command):
    out = subprocess.check_output(command,shell = True)#"ls "+intra_folder+protein_name+"*.rr"
    out = out.rstrip()
    out = str(out)
    out = out[1:].strip("'").strip()
    if ("filtered" in out):
        split=out.split("\\n")
        out = split[-1].strip()
        #if ("\\n" in out): print ("ADFADSF")

    print ("Processing: "+out)

    return out

protein_list_file=sys.argv[1]
#intra_folder=sys.argv[2]
#dncon2_folder=sys.argv[3]
#outfolder=sys.argv[4]
#inter_folder="/data/farhan/SoftwareTools/HomopolymerProject/data/homodimers/scripts/interchains/"
inter_folder="/data/farhan/SoftwareTools/HomopolymerProject/data/homodimers/scripts/interchains_heavy/"
intra_folder="/data/farhan/SoftwareTools/HomopolymerProject/data/homodimers/scripts/intrachains/"
dncon2_folder="/data/farhan/SoftwareTools/HomopolymerProject/data/homodimers/scripts/dncon2_rr/"
outfolder="/data/farhan/SoftwareTools/HomopolymerProject/data/homodimers/scripts/precisions/inter/"
if (not os.path.isdir(outfolder)): os.mkdir(outfolder)

intra_folder=refineFolderEnd(intra_folder)
inter_folder=refineFolderEnd(inter_folder)
dncon2_folder=refineFolderEnd(dncon2_folder)
outfolder=refineFolderEnd(outfolder)

protein_list=[]
with open (protein_list_file,"r") as f:
    for line in f:
        protein_list.append(line.strip())

protein_list=getPDBNames(protein_list)
for protein_name in protein_list:
#<interchain> <dncon2> <intrachain>
    print ("Processing protein: "+protein_name)
    if not(os.path.exists(dncon2_folder+protein_name+".dncon2.rr")): 
        print (dncon2_folder+protein_name+".dncon2.rr not found. Skipping!")
#        os.system("echo "+dncon2_folder+protein_name+".dncon2.rr >> no_dncon2_for_interchainprec.txt")
        os.system("echo "+dncon2_folder+protein_name+".dncon2.rr >> no_dncon2_for_interchainprec_fake.txt")
        continue
    exit_code=os.system("ls "+intra_folder+protein_name+"*.rr")
    if (exit_code!=0 or exit_code!="0"): 
        print ("Intracontact file for "+intra_folder+protein_name+"*.rr"+" not found. Skipping!")
#        os.system("echo "+dncon2_folder+protein_name+".dncon2.rr >> no_dncon2_for_interchainprec.txt")
        os.system("echo "+"Intracontact file for "+intra_folder+protein_name+"*.rr"+" not found. Skipping >> no_dncon2_for_interchainprec_fake.txt")
        continue
    exit_code=os.system("ls "+inter_folder+protein_name+"*.rr")
    if (exit_code!=0 or exit_code!="0"): 
        print ("Intercontact file for "+inter_folder+protein_name+"*.rr"+" not found. Skipping!")
#        os.system("echo "+dncon2_folder+protein_name+".dncon2.rr >> no_dncon2_for_interchainprec.txt")
        os.system("echo "+"Intercontact file for "+inter_folder+protein_name+"*.rr"+" not found. Skipping >> no_dncon2_for_interchainprec_fake.txt")
        continue

    #if not(os.path.exists(dncon2_folder+protein_name+".dncon2.rr")): continue
    #if not(os.path.exists(dncon2_folder+protein_name+".dncon2.rr")): continue
    dncon_rr_file=getSystemOutput("ls "+dncon2_folder+protein_name+".dncon2.rr")
    intra_rr_file=getSystemOutput("ls "+intra_folder+protein_name+"*.rr")
    inter_rr_file=getSystemOutput("ls "+inter_folder+protein_name+"*.rr")

    print ("system Command: python getPrecision_inter.py "+inter_rr_file+" "+dncon_rr_file+" "+intra_rr_file)
    os.system("python getPrecision_inter.py "+inter_rr_file+" "+dncon_rr_file+" "+intra_rr_file +" > "+outfolder+protein_name+"_inter_prec.txt")
    
