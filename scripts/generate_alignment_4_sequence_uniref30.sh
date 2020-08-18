#!/bin/bash -l
#SBATCH -J gen_aln
#SBATCH -o result-%j.out
#SBATCH -p Lewis,hpc5,Interactive
#SBATCH -N 1
#SBATCH -n 8
#SBATCH -t 00-04:00:00
#SBATCH --mem 50G
#SBATCH --mem-per-cpu 20G

fasta=$1
outdir=$2
hhbid=$(basename $1)
echo "Running hhsuite for $fasta"
/storage/htc/bdm/tools/hhsuite-3.0-beta.1/bin/hhblits -i $fasta -d /storage/htc/bdm/tools/databases/UniRef30_2020_03/UniRef30_2020_03 -oa3m $outdir/$hhbid.a3m -cpu 8 -n 3 -maxfilt 500000 -diff inf -e 0.001 -id 99 -cov 60 > $outdir/$hhbid-hhblits.log
echo "Output saved in $outdir"

