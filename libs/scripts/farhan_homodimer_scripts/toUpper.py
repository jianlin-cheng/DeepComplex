#this script reads a file and converts all strings to upper case.
#usage: python toUpper.py <input_file> > <outputfile>

import os,sys

infile=sys.argv[1]

if not(os.path.exists(infile)): sys.exit(infile+" not found. Quitting")
l=[]
with open (infile,"r") as f:
    for line in f:
        l.append(line.upper().strip())

for line in l:
    print (line)
