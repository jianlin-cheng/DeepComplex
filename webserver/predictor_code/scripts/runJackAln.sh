#!/bin/bash -l
#SBATCH -J run_jack
#SBATCH -o result-%j.out
#SBATCH -p Lewis,hpc4,hpc5
#SBATCH -N 1
#SBATCH -n 8
#SBATCH -t 0-06:00:00
#SBATCH --mem 50G
#SBATCH --mem-per-cpu 20G
echo "Startingdate date"
start=$(date +%s.%N)

fasta=$(readlink -f $1)
db_path=$(readlink -f $3) #/storage/htc/bdm/farhan/string_db/combined_strings_db/filter_combo/all_sequences.txt
outfolder=$(readlink -f $2)
fn=$(basename $fasta)
fasta_name=${fn%.*}

if [ ! -d $outfolder ]; then
    mkdir -p $outfolder
fi

mkdir -p $outfolder/tmpdir$fasta_name

scp $fasta $outfolder/tmpdir$fasta_name/

echo $fasta
echo $fasta_name
echo $db_path
echo $outfolder

if [ ! -f $outfolder/tmpdir$fasta_name/prot-1e-4.ali ]; then
    /storage/htc/bdm/tools/hmmer-3.1b2-linux-intel-x86_64/binaries/jackhmmer --cpu 8 -N 5 -E 1e-4 -A $outfolder/tmpdir$fasta_name/prot-1e-4.ali $fasta $db_path
fi

if [ ! -f $outfolder/tmpdir$fasta_name/prot-1e-4.a3m ]; then
    perl /storage/htc/bdm/farhan/DeepComplex/feature_gen_dncon2/reformat.pl -l 1500 -d 1500 sto a3m $outfolder/tmpdir$fasta_name/prot-1e-4.ali $outfolder/tmpdir$fasta_name/prot-1e-4.a3m
fi
if [ ! -f $outfolder/tmpdir$fasta_name/prot-1e-4.aln ]; then
    grep -v "^>" $outfolder/tmpdir$fasta_name/prot-1e-4.a3m | sed 's/[a-z]//g' > $outfolder/tmpdir$fasta_name/prot-1e-4.aln
fi


if [ ! -f $outfolder/tmpdir$fasta_name/prot-1e-20.ali ]; then
    /storage/htc/bdm/tools/hmmer-3.1b2-linux-intel-x86_64/binaries/jackhmmer --cpu 8 -N 5 -E 1e-20 -A $outfolder/tmpdir$fasta_name/prot-1e-20.ali $fasta $db_path
fi
if [ ! -f $outfolder/tmpdir$fasta_name/prot-1e-20.a3m ]; then 
    perl /storage/htc/bdm/farhan/DeepComplex/feature_gen_dncon2/reformat.pl -l 1500 -d 1500 sto a3m $outfolder/tmpdir$fasta_name/prot-1e-20.ali $outfolder/tmpdir$fasta_name/prot-1e-20.a3m
fi
if [ ! -f $outfolder/tmpdir$fasta_name/prot-1e-20.aln ]; then
    grep -v "^>" $outfolder/tmpdir$fasta_name/prot-1e-20.a3m | sed 's/[a-z]//g' > $outfolder/tmpdir$fasta_name/prot-1e-20.aln
fi


if [ ! -f $outfolder/tmpdir$fasta_name/prot-1e-10.ali ]; then
    /storage/htc/bdm/tools/hmmer-3.1b2-linux-intel-x86_64/binaries/jackhmmer --cpu 8 -N 5 -E 1e-10 -A $outfolder/tmpdir$fasta_name/prot-1e-10.ali $fasta $db_path
fi
if [ ! -f $outfolder/tmpdir$fasta_name/prot-1e-10.a3m ]; then
    perl /storage/htc/bdm/farhan/DeepComplex/feature_gen_dncon2/reformat.pl -l 1500 -d 1500 sto a3m $outfolder/tmpdir$fasta_name/prot-1e-10.ali $outfolder/tmpdir$fasta_name/prot-1e-10.a3m
fi
if [ ! -f $outfolder/tmpdir$fasta_name/prot-1e-10.aln ]; then
    grep -v "^>" $outfolder/tmpdir$fasta_name/prot-1e-10.a3m | sed 's/[a-z]//g' > $outfolder/tmpdir$fasta_name/prot-1e-10.aln
fi


if [ ! -f $outfolder/tmpdir$fasta_name/prot-1.ali ]; then
    /storage/htc/bdm/tools/hmmer-3.1b2-linux-intel-x86_64/binaries/jackhmmer --cpu 8 -N 5 -E 1 -A $outfolder/tmpdir$fasta_name/prot-1.ali $fasta $db_path
fi
if [ ! -f $outfolder/tmpdir$fasta_name/prot-1.a3m ]; then
    perl /storage/htc/bdm/farhan/DeepComplex/feature_gen_dncon2/reformat.pl -l 1500 -d 1500 sto a3m $outfolder/tmpdir$fasta_name/prot-1.ali $outfolder/tmpdir$fasta_name/prot-1.a3m
fi
if [ ! -f $outfolder/tmpdir$fasta_name/prot-1.aln ]; then
    grep -v "^>" $outfolder/tmpdir$fasta_name/prot-1.a3m | sed 's/[a-z]//g' > $outfolder/tmpdir$fasta_name/prot-1.aln
fi 

echo "Now selecting the best alignment..."
python patchAlignment.py $fasta $outfolder/tmpdir$fasta_name $outfolder/tmpdir$fasta_name

if [ ! -f $outfolder/tmpdir$fasta_name/$fasta_name.aln ];then
    echo "First time failed...running again!"
    python patchAlignment.py $fasta $outfolder/tmpdir$fasta_name $outfolder/tmpdir$fasta_name
fi

#end=$(date +%s.%N)
#echo "starting time $start"
#echo "ending time $end"
#runtime=$($end-$start)
#echo "Running time ... $runtime"
scp $outfolder/tmpdir$fasta_name/$fasta_name.aln $outfolder
scp $outfolder/tmpdir$fasta_name/$fasta_name.a3m $outfolder
sed 's/[a-z]/g' $outfolder/tmpdir$fasta_name/$fasta_name.a3m > $outfolder/$fasta_name.a3m

#rm -rf $outfolder/tmpdir$fasta_name

#mv $outfolder/tmpdir$fasta_name/prot.aln $outfolder/$fasta_name.aln


