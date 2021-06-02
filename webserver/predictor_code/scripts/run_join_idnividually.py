import os, sys

#list_file=os.path.abspath(sys.argv[1])
list_file=os.path.abspath(sys.argv[1])
aln_folder=os.path.abspath(sys.argv[2])
ppi_file=os.path.abspath(sys.argv[3])
outdir=os.path.abspath(sys.argv[4])+"/"

#l=[]
#with open(list_file) as f:
#    for line in f:
#        if "__" in line.strip(): line=line.replace("__","_")
#        os.system("sh /storage/htc/bdm/farhan/string_db/hetero30_aln_run/joinAln_one.sh "+line.strip()+" "+aln_folder+" "+ppi_file+" "+outdir)
os.system("sh /var/www/cgi-bin/deepcomplex/deepcomplex/scripts/joinAln_one.sh "+line.strip()+" "+aln_folder+" "+ppi_file+" "+outdir)

