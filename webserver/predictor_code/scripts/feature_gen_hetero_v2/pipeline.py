#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  5 13:59:58 2020

@author: farhan
"""
#this script runs the heterodimer feature generation pipeline
#there are some hard paths below. Fix them first.
#Usage: python pipeline.py <fasta_A> <fasta_B> <outdir> <paths_file>
#1. 


import os, sys, shutil
from readFastaFile import readFastaFile

fasta_file_A=os.path.abspath(sys.argv[1])
fasta_file_B=os.path.abspath(sys.argv[2])
outdir=os.path.abspath(sys.argv[3])+"/"
alnfolder=os.path.abspath(sys.argv[4])+"/"
paths_file=os.path.abspath(sys.argv[5])
dir_A=outdir+"A/"
dir_B=outdir+"B/"
package_dir=os.path.dirname(os.path.abspath(sys.argv[0]))+"/"
print ("Current package directory: "+package_dir)
#sys.exit()
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

os.system("scp "+fasta_file_A+" "+dir_A+"A.fasta")
os.system("scp "+fasta_file_B+" "+dir_B+"B.fasta")

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

#################### Copy the already prepared alignments to the outdir/aligments/ folder. Later add the alignment generation code ######################33
if not os.path.isdir(outdir+"alignments/"): os.makedirs(outdir+"alignments/")
#shutil.copy2("/storage/htc/bdm/farhan/string_db/hetero30_aln_run/doe_aln_final/"+name_AB+".a3m",outdir+"alignments/")
shutil.copy2(alnfolder+name_AB+".a3m",outdir+"alignments/")
#shutil.copy2("/storage/htc/bdm/farhan/string_db/hetero30_aln_run/doe_aln_final/"+name_AB+".aln",outdir+"alignments/")
shutil.copy2(alnfolder+name_AB+".aln",outdir+"alignments/")

##################################################################################################################

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
os.system("scp "+dir_AB+name_AB+".fasta "+dir_AB+"AB.fasta")

#1. generate PSSM for combined fasta
print ("Generating PSSM for combined fasta...")
#exitcode=os.system("python generatePSSM.py paths.txt "+dir_AB+name_AB+".fasta "+dir_AB)

################### Change the following to directly generate pssm using generated alignments ######################
exitcode=os.system("python "+package_dir+"generatePSSM.py "+paths_file+" "+dir_AB+name_AB+".fasta "+outdir+"alignments/"+name_AB+".a3m "+dir_AB)
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
exitcode_A=os.system("python "+package_dir+"generatePSIPRED.py "+paths_file+" "+dir_A+name_A+".fasta "+dir_A)
exitcode_B=os.system("python "+package_dir+"generatePSIPRED.py "+paths_file+" "+dir_B+name_B+".fasta "+dir_B)
if (exitcode_A==0 and exitcode_B==0):
    print ("PSIPRED successfully created! ")
    os.system("scp "+dir_A+"psipred/"+name_A+".solv "+dir_A+"psipred/A.solv")
    os.system("scp "+dir_A+"psipred/"+name_A+".ss "+dir_A+"psipred/A.ss")
    os.system("scp "+dir_A+"psipred/"+name_A+".ss2 "+dir_A+"psipred/A.ss2")

    os.system("scp "+dir_B+"psipred/"+name_B+".solv "+dir_B+"psipred/B.solv")
    os.system("scp "+dir_B+"psipred/"+name_B+".ss "+dir_B+"psipred/B.ss")
    os.system("scp "+dir_B+"psipred/"+name_B+".ss2 "+dir_B+"psipred/B.ss2")

else:
    print ("Failure! Could not generate PSIPRED")
    sys.exit(2)
#combine psipred features
print ("Concatenating PSIPRED features into one file")
if not (os.path.isdir(dir_AB+"psipred")): os.makedirs(dir_AB+"psipred")
exitcode=os.system("python "+package_dir+"combineSolv.py "+dir_A+"psipred/"+name_A+".solv "+dir_B+"psipred/"+name_B+".solv "+dir_AB+"psipred/"+name_AB+".solv ")
exitcode=os.system("python "+package_dir+"combineSS1.py "+dir_A+"psipred/"+name_A+".ss "+dir_B+"psipred/"+name_B+".ss "+dir_AB+"psipred/"+name_AB+".ss ")
exitcode=os.system("python "+package_dir+"combineSS2.py "+dir_A+"psipred/"+name_A+".ss2 "+dir_B+"psipred/"+name_B+".ss2 "+dir_AB+"psipred/"+name_AB+".ss2 ")
if exitcode==0:
    print("PSIPRED features successfully concatenated into one file")
    os.system("scp "+dir_AB+"psipred/"+name_AB+".solv "+dir_AB+"psipred/AB.solv")
    os.system("scp "+dir_AB+"psipred/"+name_AB+".ss "+dir_AB+"psipred/AB.ss")
    os.system("scp "+dir_AB+"psipred/"+name_AB+".ss2 "+dir_AB+"psipred/AB.ss2")
else:
    print("Failure to concatenate PSIPRED features!")
    sys.exit(3)
print ("Generating SCRATCH features for both chains...")
#exitcode_A=os.system("python generateSS_SA.py paths.txt "+dir_A+name_A+".fasta "+dir_A)
#exitcode_B=os.system("python generateSS_SA.py paths.txt "+dir_B+name_B+".fasta "+dir_B)
exitcode_A=os.system("python "+package_dir+"generateSS_SA.py "+paths_file+" "+dir_A+name_A+".fasta "+dir_A)
exitcode_B=os.system("python "+package_dir+"generateSS_SA.py "+paths_file+" "+dir_B+name_B+".fasta "+dir_B)

if (exitcode_A==0 and exitcode_B==0):
    print ("SCRATCH successfully done! ")
    os.system("scp "+dir_A+"ss_sa/"+name_A+".ss_sa "+dir_A+"ss_sa/A.ss_sa")
    os.system("scp "+dir_B+"ss_sa/"+name_B+".ss_sa "+dir_B+"ss_sa/B.ss_sa")
#    os.system("scp "+dir_A+"ss_sa/"+name_A+".ss2 "+dir_A+"ss_sa/A.ss2")
else:
    print ("Failure! Could not generate SCRATCH")
    sys.exit(4)

print ("Concatenating SCRATCH features for both chains...")

if not (os.path.exists(dir_AB+"ss_sa")):os.makedirs(dir_AB+"ss_sa")

exitcode=os.system("python "+package_dir+"combineSS_SA.py "+dir_A+"ss_sa/"+name_A+".ss_sa "+dir_B+"ss_sa/"+name_B+".ss_sa "+dir_AB+"ss_sa/"+name_AB+".ss_sa ")
if exitcode==0:
    print("SCRATCH features successfully concatenated into one file")
    os.system("scp "+dir_AB+"ss_sa/"+name_AB+".ss_sa "+dir_AB+"ss_sa/AB.ss_sa")

else:
    print("Failure to concatenate SCRATCH features!")
    sys.exit(5)
print ("All features successfully generated...")
#os.system("mv "+dir_AB+" "+outdir[0:-1]+"_AB")
print ("Moving output to directory "+outdir)
print ("Running command...")
print("scp -r "+dir_AB+"* "+outdir)
os.system("scp -r "+dir_AB+"* "+outdir)

#print ("Output saved in "+outdir[0:-1]+"_AB")
print ("Output saved in "+outdir)
print ("All alignment independent feature creation completed.")
#3. Now run dncon2 feature generation code. 
print ("Generating alignment dependent (co-evolutionary) features for the concatenated fasta file...")
#os.system("perl feature_gen_hetero.pl "+outdir[0:-1]+"_AB/"+name_AB+".fasta "+outdir[0:-1]+"_AB")
#os.system("perl feature_gen_hetero.pl "+outdir+"/"+name_AB+".fasta "+outdir)
print ("Running command...")
print("perl "+package_dir+"feature_gen_hetero.pl "+outdir+"/"+name_AB+".fasta "+outdir)
os.system("perl "+package_dir+"feature_gen_hetero.pl "+outdir+"/"+name_AB+".fasta "+outdir)
print ("Removing any temporary files and folders...")
#os.remove(dir_A)
#os.remove(dir_B)
#Unremark the following if you don't want to keep the temporary files and directories
#if os.path.isdir(dir_A):shutil.rmtree(dir_A)
#if os.path.isdir(dir_B):shutil.rmtree(dir_B)
#if os.path.isdir(dir_AB):shutil.rmtree(dir_AB)
print ("All features successfully generated and save in "+outdir)
