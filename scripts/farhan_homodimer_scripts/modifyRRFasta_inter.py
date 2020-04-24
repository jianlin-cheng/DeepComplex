#this script will read the interchain.rr file and replace the fasta at the beginning with the one in the final_combined_fasta_dictionary.txt file
#usage: python modifyRRFasta_inter.py 
import os,sys
from readRR import readRRFile, write2File
from loadFastaDictionary import loadFastaDictionary

def getFileName(file_path):
    os.system("ls "+file_path+"*.rr > temp_rr_test.txt")
    file_name=""
    #print ("Here")
    with open ("temp_rr_test.txt","r") as f:
        for line in f:
            if ("filtered" in line or "inter_all" in line): 
                #print(line)
                continue
            file_name=line.strip()
            #print ("Here"+file_name)
#    os.remove("temp_rr_test.txt")
    return file_name

fasta_dict_file="final_combined_fasta_dictionary.txt"
fasta_dict=loadFastaDictionary(fasta_dict_file)

pdb_list=list(fasta_dict.keys())
#pdb_list=fasta_dict.keys()
#print(type(pdb_list))
interchain_rr_folder="./interchains_heavy/"
outfolder="./interchains/"
for pdb in pdb_list:
    print ("Modifying fasta sequence of : "+pdb)
    file_name=getFileName(interchain_rr_folder+pdb)
    #print ("File_name: "+file_name)
    if (file_name=="" or not os.path.exists(file_name)): 
        print (file_name+" does not exist. Moving on!")
        os.system("echo "+pdb+": Not in list >> fasta_mod_failure.txt")
        continue
    fasta,contents=readRRFile(file_name)
    fasta=fasta_dict[pdb]
    print ("Writing to file: "+outfolder+file_name.split("/")[-1])
    write2File(outfolder+file_name.split("/")[-1],fasta,contents)
    print (len(contents)," contacts written!")
    #break
#print (len(pdb_list))
