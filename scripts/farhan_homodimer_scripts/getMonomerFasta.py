#this script reads the multimer fasta file and outputs the fasta sequence of the first chain.
#usage: python getMonomerFasta.py <multimer_fasta_file>
import os, sys

fasta_all=sys.argv[1]
monomer_fasta_name=fasta_all.replace(".fasta","")+"_monomer.fasta"
fasta=""
if (os.path.exists(monomer_fasta_name)): os.system("rm -f "+monomer_fasta_name)
#print(monomer_fasta_name)
with open (fasta_all,"r") as f:
    line1=f.readline().strip()
    for line in f:
        #print(line)        
        #break
        if (line.startswith(">")): break
        if (not line.startswith(">")): fasta+=line.strip()

os.system("echo '"+line1+"' > "+monomer_fasta_name)
os.system("echo "+fasta+" >> "+monomer_fasta_name)
