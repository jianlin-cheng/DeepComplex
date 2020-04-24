#Removes the contacts that are less than a particular range

import sys,os

file=sys.argv[1]
rng=int(sys.argv[2])

if (not os.path.exists(file)):
    sys.exit(file+" not found")

if (rng<0):
    sys.exit("Invalid range")
contents=[]
fasta=""
with open (file,"r") as f:
        for line in f:
            if (line.strip().startswith("0") or line.strip().startswith("1") or line.strip().startswith("2") or line.strip().startswith("3") or line.strip().startswith("4") or line.strip().startswith("5") or line.strip().startswith("6") or line.strip().startswith("7") or line.strip().startswith("8") or line.strip().startswith("9")):
                split=line.strip().split()
                i=int(split[0])
                j=int(split[1])
                if (abs(i-j)>=rng):
                    contents.append(line.strip())
                    continue
                continue
            if (line.strip().startswith("PFRMAT") or line.strip().startswith("END") or line.strip().startswith("METHOD") or line.strip().startswith("MODEL") or line.strip().startswith("REMARK") or line.strip().startswith("TARGET") or line.strip().startswith("AUTHOR")):
                continue
            fasta+=line.strip()     

print(fasta)
for content in contents:
    print(content)
