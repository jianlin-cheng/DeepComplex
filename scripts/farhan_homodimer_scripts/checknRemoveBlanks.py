import os,sys

infile=os.path.abspath(sys.argv[1])
outfolder=os.path.abspath(sys.argv[2])

if not(outfolder.endswith("/")):outfolder+="/"
if not(os.path.isdir(outfolder)):os.makedirs(outfolder)
f=open(infile)
line_list=f.readlines()
f.close()

if (len(line_list)>5): os.system("cp "+infile+" "+outfolder)
