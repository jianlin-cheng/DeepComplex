#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  5 13:59:58 2020

@author: farhan
"""
#this script runs the heterodimer feature generation pipeline
#Usage: python pipeline.py <fasta_A> <fasta_B> <outdir> <paths_file>
#1. 


import os, sys, shutil
from readFastaFile import readFastaFile

fasta_file_A=os.path.abspath(sys.argv[1])
fasta_file_B=os.path.abspath(sys.argv[2])
outdir=os.path.abspath(sys.argv[3])+"/"
paths_file=os.path.abspath(sys.argv[4])
dir_A=outdir+"A/"
dir_B=outdir+"B/"
if not (os.path.exists(fasta_file_A)): sys.exit ("Fasta file "+fasta_file_A+" not found! Quitting!")
if not (os.path.exists(fasta_file_B)): sys.exit ("Fasta file "+fasta_file_B+" not found! Quitting!")
if not (os.path.exists(paths_file)): sys.exit ("Paths file "+paths_file+" not found! Quitting!")
if not (os.path.isdir(outdir)): os.makedirs(outdir)

if not os.path.isdir(dir_A):os.makedirs(dir_A)
if not os.path.isdir(dir_B):os.makedirs(dir_B)
name_A=os.path.basename(fasta_file_A).split(".")[0]
name_B=os.path.basename(fasta_file_B).split(".")[0]

#Copy the individual fasta files to respective directories
os.system("scp "+fasta_file_A+" "+dir_A)
os.system("scp "+fasta_file_B+" "+dir_B)

#print (dir_A)
#print (dir_B)
#print (name_A)
#print (name_B)

#create combined fasta file
print ("Creating folder "+outdir+"AB/ for combined features...")
dir_AB=outdir+"AB/"
if not os.path.isdir(dir_AB):os.makedirs(dir_AB)
print ("Done!")
print ("Creating combined fasta file... ")
header_A,fasta_A=readFastaFile(fasta_file_A)
header_B,fasta_B=readFastaFile(fasta_file_B)
fasta_AB=fasta_A.strip()+fasta_B.strip()
name_AB=name_A.split("_")[0]+"_"+name_B.split("_")[0]
#header_AB=header_A.split(",")[0].split()[0]+" , Chain AB;"
if header_A==header_B:
    header_AB=">"+name_AB+" , Chain AB;"
else:
    header_AB=header_A.split(",")[0].split()[0]+"_"+header_B.split(",")[0].split()[0].replace(">","")+" , Chain AB;"
#Resolve the name. Best to create name_A+"_"+name_B
#name_AB=name_A.split("_")[0]+"_AB"


#print (name_AB)
#print(dir_AB)
with open (dir_AB+name_AB+".fasta","w") as f:
    f.write(header_AB+"\n")
    f.write(fasta_AB)
print ("Done! Combined fasta file called "+dir_AB+name_AB+".fasta created...")
#1. generate PSSM for combined fasta
print ("Generating PSSM for combined fasta...")
#exitcode=os.system("python generatePSSM.py paths.txt "+dir_AB+name_AB+".fasta "+dir_AB)
exitcode=os.system("python generatePSSM.py "+paths_file+" "+dir_AB+name_AB+".fasta "+dir_AB)
if (exitcode==0):
    print ("PSSM successfully created! ")
else:
    print ("Failure! Could not generate PSSM")
    sys.exit(1)
#os.system("python generatePSSM.py paths.txt "+dir_B+name_B+".fasta "+dir_B)

#2. generate psipred
print ("Generating PSIPRED")
#exitcode=os.system("python generatePSIPRED.py paths.txt "+dir_A+name_A+".fasta "+dir_A+" & "+"python generatePSIPRED.py paths.txt "+dir_B+name_B+".fasta "+dir_B)
##### separate the above code into two commands:
#exitcode_A=os.system("python generatePSIPRED.py paths.txt "+dir_A+name_A+".fasta "+dir_A)
#exitcode_B=os.system("python generatePSIPRED.py paths.txt "+dir_B+name_B+".fasta "+dir_B)
exitcode_A=os.system("python generatePSIPRED.py "+paths_file+" "+dir_A+name_A+".fasta "+dir_A)
exitcode_B=os.system("python generatePSIPRED.py "+paths_file+" "+dir_B+name_B+".fasta "+dir_B)
if (exitcode_A==0 and exitcode_B==0):
    print ("PSIPRED successfully created! ")
else:
    print ("Failure! Could not generate PSIPRED")
    sys.exit(2)
#combine psipred features
print ("Concatenating PSIPRED features into one file")
if not (os.path.isdir(dir_AB+"psipred")): os.makedirs(dir_AB+"psipred")
exitcode=os.system("python combineSolv.py "+dir_A+"psipred/"+name_A+".solv "+dir_B+"psipred/"+name_B+".solv "+dir_AB+"psipred/"+name_AB+".solv ")
exitcode=os.system("python combineSS1.py "+dir_A+"psipred/"+name_A+".ss "+dir_B+"psipred/"+name_B+".ss "+dir_AB+"psipred/"+name_AB+".ss ")
exitcode=os.system("python combineSS2.py "+dir_A+"psipred/"+name_A+".ss2 "+dir_B+"psipred/"+name_B+".ss2 "+dir_AB+"psipred/"+name_AB+".ss2 ")
if exitcode==0:
    print("PSIPRED features successfully concatenated into one file")
else:
    print("Failure to concatenate PSIPRED features!")
    sys.exit(3)
print ("Generating SCRATCH features for both chains...")
#exitcode_A=os.system("python generateSS_SA.py paths.txt "+dir_A+name_A+".fasta "+dir_A)
#exitcode_B=os.system("python generateSS_SA.py paths.txt "+dir_B+name_B+".fasta "+dir_B)
exitcode_A=os.system("python generateSS_SA.py "+paths_file+" "+dir_A+name_A+".fasta "+dir_A)
exitcode_B=os.system("python generateSS_SA.py "+paths_file+" "+dir_B+name_B+".fasta "+dir_B)

if (exitcode_A==0 and exitcode_B==0):
    print ("SCRATCH successfully done! ")
else:
    print ("Failure! Could not generate SCRATCH")
    sys.exit(4)

print ("Concatenating SCRATCH features for both chains...")

if not (os.path.exists(dir_AB+"ss_sa")):os.makedirs(dir_AB+"ss_sa")

exitcode=os.system("python combineSS_SA.py "+dir_A+"ss_sa/"+name_A+".ss_sa "+dir_B+"ss_sa/"+name_B+".ss_sa "+dir_AB+"ss_sa/"+name_AB+".ss_sa ")
if exitcode==0:
    print("SCRATCH features successfully concatenated into one file")
else:
    print("Failure to concatenate SCRATCH features!")
    sys.exit(5)
print ("All features successfully generated...")
#os.system("mv "+dir_AB+" "+outdir[0:-1]+"_AB")
print ("Moving output to directory "+outdir)
print ("Running command...")
print("mv "+dir_AB+"* "+outdir)
os.system("mv "+dir_AB+"* "+outdir)

#print ("Output saved in "+outdir[0:-1]+"_AB")
print ("Output saved in "+outdir)
print ("All alignment independent feature creation completed.")
#3. Now run dncon2 feature generation code. 
print ("Generating alignment dependent (co-evolutionary) features for the concatenated fasta file...")
#os.system("perl feature_gen_hetero.pl "+outdir[0:-1]+"_AB/"+name_AB+".fasta "+outdir[0:-1]+"_AB")
#os.system("perl feature_gen_hetero.pl "+outdir+"/"+name_AB+".fasta "+outdir)
print ("Running command...")
print("perl feature_gen_hetero.pl "+outdir+"/"+name_AB+".fasta "+outdir)
os.system("perl feature_gen_hetero.pl "+outdir+"/"+name_AB+".fasta "+outdir)
print ("Removing any temporary files and folders...")
#os.remove(dir_A)
#os.remove(dir_B)

shutil.rmtree(dir_A)
shutil.rmtree(dir_B)
shutil.rmtree(dir_AB)

